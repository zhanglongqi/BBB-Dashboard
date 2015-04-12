#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by lq on 12/4/15
"""
__author__ = 'lq'


def enum(**enums):
    return type('Enum', (), enums)


'''
>>> Numbers = enum(ONE=1, TWO=2, THREE='three')
>>> Numbers.ONE
1
>>> Numbers.TWO
2
>>> Numbers.THREE
'three'
'''


def enum_auto(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


'''
>>> Numbers = enum('ZERO', 'ONE', 'TWO')
>>> Numbers.ZERO
0
>>> Numbers.ONE
1
'''
