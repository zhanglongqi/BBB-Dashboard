#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by longqi on 4/6/15
"""
__author__ = 'longqi'

import time

from configuration import hosts_info
from configuration import interval
from configuration import rows_in_one_time
from db.db_cassandra import get_hosts_list
from db.db_cassandra import init_db


def info_loop():
    init_db()
    while True:
        time.sleep(interval)

        # update the hosts_info from database

        for host_row in iter(get_hosts_list(rows_in_one_time)):
            # print(host_row)

            if host_row.hostname in hosts_info:
                hosts_info[host_row.hostname][1] = host_row.ip_info
                hosts_info[host_row.hostname][2] = host_row.date.now()
            else:
                hosts_info[host_row.hostname] = []
                hosts_info[host_row.hostname].append(host_row.hostname)
                hosts_info[host_row.hostname].append(host_row.ip_info)
                hosts_info[host_row.hostname].append(host_row.date.now())
                hosts_info[host_row.hostname].append(0)


