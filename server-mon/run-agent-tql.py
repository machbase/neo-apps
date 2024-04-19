# -*- coding: utf-8 -*-
# python3 ./agent-csv2.py http://127.0.0.1:5654/db/tql/append.tql monitoring

import argparse
import logging
import requests
import time
import io
import csv
import agent_core

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main(url, tablename, ip_address, interval, servername, debug):
    final_url = f"{url}?table={tablename}"
    print(final_url)
    while True:
        headers = {'Content-Type': 'text/csv'}
        json_data = agent_core.get_system_stats_json(ip_address, servername);
        print(json_data)
        if debug != 'no':
            print(json_data)

        #############################################################################
        # Convert to CSV
        #############################################################################
        output = io.StringIO()  # 문자열 버퍼 생성
        csv_writer = csv.writer(output)
        csv_writer.writerows(json_data["data"]["rows"])
        # CSV 문자열 가져오기
        csv_content = output.getvalue()
        print("###\n" + csv_content);

        #############################################################################
        # Send data
        #############################################################################
        response = requests.post(final_url,  data=csv_content, headers=headers)
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
