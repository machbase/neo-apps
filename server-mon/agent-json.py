# -*- coding: utf-8 -*-
# python3 ./agent-json.py http://127.0.0.1:5654 monitoring

import argparse
import logging
import requests
import time
import agent_core

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main(url, tablename, ip_address, interval, servername, debug):
    while True:
        headers = {'Content-Type': 'application/json'}
        json_data = agent_core.get_system_stats_json(ip_address, servername);
        print(json_data)
        if debug != 'no':
            print(json_data)
        # Send data to server
        response = requests.post(f"{url}/db/write/{tablename}?timeformat=s&method=append", json=json_data, headers=headers)
        result = response.json()
        print(result)
        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='System Statistics Collector')
    parser.add_argument('url', type=str, help='NEO-URL (e.g., http://host:port)')
    parser.add_argument('tablename', type=str, help='Table name for data storage')
    parser.add_argument('--ip_address', type=str, default='', help='IP Address prefix to filter (default: "")')
    parser.add_argument('--interval', type=int, default=3, help='Interval between posts in seconds (default: 3)')
    parser.add_argument('--servername', type=str, default='', help='servername')
    parser.add_argument('--debug', type=str, default='no', help='debugging')
    args = parser.parse_args()

    main(args.url, args.tablename, args.ip_address, args.interval, args.servername, args.debug)
