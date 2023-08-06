import yaml
import os

def main():
    """Return a JSON format for Zabbix discoveries
    https://www.zabbix.com/documentation/3.2/manual/discovery/low_level_discovery
    Input : cfg the configuration dictionary
    """
    cfg=[]
    root_path = os.path.dirname(os.path.abspath( __file__ )) + "/"
    with open(root_path + "config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    data = '{"data":['

    for lif in cfg['lifs']:
        for volume in lif['volumes']:
            data = data + '{"{#SUMMER_LIF}":"'+lif['name'] + '","{#SUMMER_JUNCTION}":"'+volume['mountpoint'] + '"},'
    # Virer la , de trop
    data = data[:-1]
    data = data+']}'
    print(data)

if __name__ == "__main__":
    main()
