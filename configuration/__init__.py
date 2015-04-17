#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by longqi on 4/6/15
"""
__author__ = 'longqi'

import datetime

interval = 3
hosts_info = {'B1': ['B1', '10.0.25.1', datetime.datetime.now(), -1],
              'B2': ['B2', '10.0.25.2', datetime.datetime.now(), -1],
              'B3': ['B3', '10.0.25.3', datetime.datetime.now(), -1],
              }
threshold = 20
rows_in_one_time = 10