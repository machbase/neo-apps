# -*- coding: utf-8 -*-

import argparse
import logging
import os
import platform
import psutil
import requests
import socket
import sys
import time
import json

def get_ip_address(prefix):
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and addr.address.startswith(prefix):
                return addr.address
    return None

def get_total_disk_usage():
    total_size = 0
    total_used = 0
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_size += usage.total
            total_used += usage.used
        except PermissionError:
            continue

    return [total_used, total_size]

def collect_system_stats(ip_prefix):
    stats = {
        'cpu': psutil.cpu_percent(interval=1),
        'disk': get_total_disk_usage(),
        'network': psutil.net_io_counters()._asdict(),
        'os': platform.system(),
        'ip_address': get_ip_address(ip_prefix)
    }
    return stats

def get_system_stats_json(ip_address, servername):

    if servername != '':
        server_name = servername;
    else:
        if ip_address == "":
            ip_address = "192."  # Default IP prefix for filtering if none specified
        hostname = socket.gethostname()
        server_name = f"{collect_system_stats(ip_address)['ip_address']}-{platform.system()}-{hostname}"

    json_data = {
        "data": {
            "columns": ["name", "time", "value"],
            "rows": []
        }
    }
    stats = collect_system_stats(ip_address)
    current_epoch_time = int(time.time())

    # CPU usage data
    row = [f"CPU-{server_name}", current_epoch_time, stats['cpu']]
    json_data["data"]["rows"].append(row)

    # Disk usage data
    row = [f"DU-{server_name}", current_epoch_time, stats['disk'][0]]
    json_data["data"]["rows"].append(row)

    # Total disk space data
    row = [f"DT-{server_name}", current_epoch_time, stats['disk'][1]]
    json_data["data"]["rows"].append(row)

    # Free disk space data
    row = [f"DR-{server_name}", current_epoch_time, stats['disk'][1] - stats['disk'][0]]
    json_data["data"]["rows"].append(row)

    return json_data;
