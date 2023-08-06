#!/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import logging
import re
from time import gmtime, strftime

import yaml
import paramiko
from influxdb import InfluxDBClient
from pyzabbix import ZabbixMetric, ZabbixSender # Only works on python2

def to_bytes(size):
    """
    Convert a string formated as size and unit (for instance 43.4GB) in bytes.
    Returns an integer.
    """
    # initialize power factor
    power = 1
    # List of valid units
    valid_units = ["B", "KB", "MB", "GB", "TB"]
    # Extract unit from string
    try:
        unit = re.split('[0-9]', size)[-1]
        # Check if we have a valid unit
        if not unit in valid_units:
            raise ValueError
        # Compute the power of 1024 from the position in the valid_units list
        for position, item in enumerate(valid_units):
            if item == unit:
                power = 1024**position
        # Get the numeric part of size
        num = re.split('[A-Z]+', size)[0]
        # Compute as bytes and return
        return int(float(num)*power)
    except ValueError:
        logging.error("%s does not match pattern.", size)
        raise

def main():
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Starting")
    configfile = os.getenv('MOSUSNAP_CONFIG_FILE', 'config.yaml')
    zabbix_packet = []
    now = gmtime()
    # Incluxdb initialize
    influxdb_json_data = []
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except FileNotFoundError as err:
        logging.error("Configuration file not foundd")
        logging.error(err)
        sys.exit(1)
    except yaml.YAMLError as err:
        logging.error(err)
        sys.exit(1)

    for lif in cfg['lifs']:
        logging.info("Handling LIF %s", lif['name'])
        password = os.getenv(f"LIF_{lif['name']}_PASSWORD".upper(), lif['password'])
        # Préparation des commandes à passer
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
            client.connect(lif['sshserver'], port=lif['port'], username=lif['login'], password=password, allow_agent=False, look_for_keys=False)
            for volume in lif['volumes']:
                snapshot_size = -1
                logging.debug("Getting data from volume %s", volume['mountpoint'])
                ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("volume show -volume %s" % volume['name'])
                for eline in ssh_stdout.readlines():
                    if re.search('^\s+Volume Size Used by Snapshot Copies:', eline):
                        logging.debug(eline)
                        size_with_unit = re.split(r":\s+", eline.rstrip())[-1]
                        logging.debug(size_with_unit)
                        snapshot_size = to_bytes(size_with_unit)
                        logging.debug(snapshot_size)
                        continue
                    if re.search('^\s+Available Size:', eline):
                        logging.debug(eline)
                        size_with_unit = re.split(r":\s+", eline.rstrip())[-1]
                        availabile_size = to_bytes(size_with_unit)
                        logging.debug("Available size: %s", availabile_size)
                        continue
                    if re.search('^\s+Used Size:', eline):
                        logging.debug(eline)
                        size_with_unit = re.split(r":\s+", eline.rstrip())[-1]
                        used_size = to_bytes(size_with_unit)
                        logging.debug("Used size: %s", used_size)
                        continue
                    if re.search('^\s+Filesystem Size:', eline):
                        logging.debug(eline)
                        size_with_unit = re.split(r":\s+", eline.rstrip())[-1]
                        total_size = to_bytes(size_with_unit)
                        logging.debug("Total size: %s", total_size)
                        continue
                    if re.search('^\s+Space Reserved for Snapshot Copies', eline):
                        logging.debug(eline)
                        reserved_snapshot_percent = float(re.split(r':\s+', eline.rstrip().strip('%'))[-1])
                        continue
                    if re.search('^\s+Snapshot Reserve Used:', eline):
                        logging.debug(eline)
                        snapshot_reserve_used_with_unit = re.split(r":\s+", eline.rstrip())[-1]
                        snapshot_reserve_used = snapshot_reserve_used_with_unit[:-1]
                        logging.debug(snapshot_reserve_used)
                    if re.search('^\s+Used Percentage:', eline):
                        logging.debug(eline)
                        volume_used_with_unit = re.split(r":\s+", eline.rstrip())[-1]
                        volume_used = volume_used_with_unit[:-1]
                        logging.debug("Volume used: %s", volume_used)
                #
                # Cleanup
                ssh_stdin.close()
                ssh_stdout.close()
                ssh_stderr.close()
                # Metric for Zabbix
                if cfg['zabbix']['active']:
                    zabbix_packet.append(ZabbixMetric(cfg['zabbix']['host'],
                                                    "%s[%s,%s]" % (cfg['zabbix']['usage_key'], lif['name'], volume['mountpoint']),
                                                    snapshot_size))
                    zabbix_packet.append(ZabbixMetric(cfg['zabbix']['host'],
                                                        "%s[%s,%s]" % (cfg['zabbix']['volume_used_key'], lif['name'], volume['mountpoint']),
                                                        volume_used))
                    zabbix_packet.append(ZabbixMetric(cfg['zabbix']['host'],
                                                        "%s[%s,%s]" % (cfg['zabbix']['reserve_key'], lif['name'], volume['mountpoint']),
                                                        snapshot_reserve_used))
                # Metric for influxdb
                if cfg['influxdb']['active']:
                    influxdb_json_data.append(
                        {"measurement": cfg['influxdb']['measurement'],
                            "tags": {
                                "lif": lif['name'],
                                "volume": volume['mountpoint'],
                                "qtree": None
                            },
                            "time": strftime("%Y-%m-%dT%H:%M:%SZ", now),
                            "fields": {
                                "available": availabile_size,
                                "used": used_size,
                                "total": total_size,
                                "snapshot_used": snapshot_size,
                                "snapshot_reserve": int(total_size * reserved_snapshot_percent /100.)
                            }
                        }
                    )

                # Now get the qota if needed
                ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(f"quota report -volume {volume['name']} -fields tree,disk-used,disk-limit")
                for eline in ssh_stdout.readlines():
                    # vserver    volume                     index               disk-used disk-limit
                    # ---------- -------------------------- ------------------- --------- ----------
                    # SVMp_RESIF vol_SVMp_RESIF_nfs_scratch 2305843013508661248 1.86GB    400GB
                    # SVMp_RESIF vol_SVMp_RESIF_nfs_scratch 2305843017803628544 243.0GB   1.50TB
                    # SVMp_RESIF vol_SVMp_RESIF_nfs_scratch 2305843022098595840 1.15MB    600GB
                    # SVMp_RESIF vol_SVMp_RESIF_nfs_scratch 2305843026393563136 155.2GB   250GB
                    #
                    if re.search(volume['name'], eline):
                        logging.debug(eline)
                        line_split = re.split(r"\s+", eline.rstrip())
                        try:
                            disk_used = to_bytes(line_split[-2])
                            disk_limit = to_bytes(line_split[-1])
                            disk_percent = int(disk_used / disk_limit * 100)
                        except ValueError as err:
                            logging.error(err)
                            continue
                        tree = line_split[-3]
                        logging.info("Quota on %s %s: %d/%d", volume['name'], tree, disk_used, disk_limit)
                        if cfg['zabbix']['active']:
                            zabbix_packet.append(ZabbixMetric(cfg['zabbix']['host'],
                                                                "%s[%s,%s,%s]" % (cfg['zabbix']['quota_used_key'], tree, lif['name'], volume['mountpoint']),
                                                                disk_used))
                            zabbix_packet.append(ZabbixMetric(cfg['zabbix']['host'],
                                                                "%s[%s,%s,%s]" % (cfg['zabbix']['quota_limit_key'], tree, lif['name'], volume['mountpoint']),
                                                                disk_limit))
                            zabbix_packet.append(ZabbixMetric(cfg['zabbix']['host'],
                                                                "%s[%s,%s,%s]" % (cfg['zabbix']['quota_percent_key'], tree, lif['name'], volume['mountpoint']),
                                                                disk_percent))
                        # Metric for influxdb
                        if cfg['influxdb']['active']:
                            influxdb_json_data.append(
                                {"measurement": cfg['influxdb']['measurement'],
                                    "tags": {
                                        "lif": lif['name'],
                                        "volume": volume['mountpoint'],
                                        "qtree": tree,
                                    },
                                    "time": strftime("%Y-%m-%dT%H:%M:%SZ", now),
                                    "fields": {
                                        "qtree_used": disk_used,
                                        "qtree_limit": disk_limit,
                                    }
                                }
                            )

        finally:
            client.close()
    if cfg['zabbix']['active']:
        logging.info("Sending data to zabbix")
        logging.info(zabbix_packet)
        try:
            ZabbixSender(zabbix_server=cfg['zabbix']['server']).send(zabbix_packet)
        except Exception as err:
            logging.error("Unexpected error writing data to Zabbix")
            logging.error(err)

    if cfg['influxdb']['active']:
        try:
            logging.info("Sending data to influxdb")
            logging.info("%s", influxdb_json_data)

            logging.debug("host     = %s", cfg['influxdb']['server'])
            logging.debug("port     = %s", str(cfg['influxdb']['port']))
            logging.debug("database = %s", cfg['influxdb']['database'])
            logging.debug("username = %s", cfg['influxdb']['user'])
            password = os.getenv('INFLUXDB_PASSWORD', cfg['influxdb']['password'])

            client = InfluxDBClient(host     = cfg['influxdb']['server'],
                                    port     = cfg['influxdb']['port'],
                                    database = cfg['influxdb']['database'],
                                    username = cfg['influxdb']['user'],
                                    password = password,
                                    ssl      = cfg['influxdb']['ssl'],
                                    verify_ssl = cfg['influxdb']['verify_ssl'])
            client.write_points(influxdb_json_data, retention_policy=cfg['influxdb']['retention_policy'])
        except Exception as err:
            logging.error("Unexpected error writing data to influxdb")
            logging.error(err)
        logging.info("Done")

if __name__ == "__main__":
    main()
