#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by longqi on 4/6/15
"""
__author__ = 'longqi'

import time
from configuration import hosts_info
from configuration import interval


def info_loop():
    while True:
        for host in iter(hosts_info):
            hosts_info.get(host)[2] += 1
            print(hosts_info.get(host)[2])

        time.sleep(interval)