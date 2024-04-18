# -*- coding: utf-8 -*-

# create tag table if not exists monitoring (
#     name varchar(32) primary key,
#     time datetime basetime,
#     value double summarized
# ) with rollup;

import psutil
import requests
import time
import platform
import json
import logging
import socket
import requests
import sys
import os
import io
import csv

csv_data = """Metric,Timestamp,Value
CPU-127.0.0.1-Linux-sjkim-Precision-T1700,1712020816,15.0
DISK_USAGE-127.0.0.1-Linux-sjkim-Precision-T1700,1712020816,1502523846656
DISK_TOTAL-127.0.0.1-Linux-sjkim-Precision-T1700,1712020816,4442976378880
DISK_ROOM-127.0.0.1-Linux-sjkim-Precision-T1700,1712020816,2940452532224
"""

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def get_ip_address(prefix):
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and addr.address.startswith(prefix):
                return addr.address
    return None

def get_total_disk_usage():
    total_size = 0
    total_used = 0

    # 모든 디스크 파티션 정보를 가져옵니다.
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            # 각 파티션의 사용량 정보를 가져옵니다.
            usage = psutil.disk_usage(partition.mountpoint)
            total_size += usage.total
            total_used += usage.used
        except PermissionError:
            # 접근 권한이 없는 파티션은 건너뜁니다.
            continue

    return [total_used, total_size];

def collect_system_stats():

    stats = {
        'cpu': psutil.cpu_percent(interval=1),
        'disk' : get_total_disk_usage(),
        'network': psutil.net_io_counters()._asdict(),
        'os': platform.system(),
        'ip_address': get_ip_address('1')
    }
    return stats

if __name__ == '__main__':


    if len(sys.argv) != 3:
        print("agent.py neo-URL(http://host:port) tablename")
        os._exit(0)

    user_url   = sys.argv[1];
    table_name = sys.argv[2];

    hostname    = socket.gethostname()
    stats       = collect_system_stats()
    server_info = f"{stats['ip_address']}-{stats['os']}-{hostname}";

    while True:
        headers = {'Content-Type': 'text/csv'}
        try:
            json_data = {
                "data": {
                    "columns": ["name", "time", "value"],
                    "rows": []
                }
            }
            stats              = collect_system_stats()
            current_epoch_time = int(time.time());

            #############################################################################
            # Info add
            #############################################################################
            # CPU
            CPU_TAG = f"CPU-{server_info}";
            row = [CPU_TAG, current_epoch_time, stats['cpu']];
            json_data["data"]["rows"].append(row);

            # DISK TOTAL
            DISK_USAGE_TAG = f"DISK_USAGE-{server_info}";
            row = [DISK_USAGE_TAG, current_epoch_time, stats['disk'][0]];
            json_data["data"]["rows"].append(row);

            # DISK TOTAL
            DISK_TOTAL_TAG = f"DISK_TOTAL-{server_info}";
            row = [DISK_TOTAL_TAG, current_epoch_time, stats['disk'][1]];
            json_data["data"]["rows"].append(row);

            # DISK ROOM
            DISK_ROOM_TAG = f"DISK_ROOM-{server_info}";
            row = [DISK_ROOM_TAG, current_epoch_time, int(stats['disk'][1] - stats['disk'][0])];
            json_data["data"]["rows"].append(row);

            #############################################################################
            # Convert to CSV
            #############################################################################
            output = io.StringIO()  # 문자열 버퍼 생성
            csv_writer = csv.writer(output)

            csv_writer.writerows(json_data["data"]["rows"])

            # CSV 문자열 가져오기
            csv_content = output.getvalue()
            print("###\n" + csv_content);
            # 사용한 자원 해제
            #############################################################################
            # Send data
            #############################################################################
            url     = f"{user_url}"
            response = requests.post(url,  data=csv_content, headers=headers)
            print(response.text)
            #result = json.loads(response.text)
            #print("###\n" + result);
            time.sleep(3)
            output.close()
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")  # 예상치 못한 예외 처리
