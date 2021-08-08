#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini', encoding='utf-8')


def getServer(key):
    return cfg.get('server', key, fallback=None)


def getJMeter(key):
    return cfg.get('jmeter', key, fallback=None)


def getStd(key):
    if key == 'errorRate':
        return cfg.getfloat('std', key, fallback=0.01)
    else:
        return cfg.getint('std', key, fallback=3)


def getLogger(key):
    if key == 'backupCount':
        return cfg.getint('logger', key, fallback=7)
    else:
        return cfg.get('logger', key, fallback=None)
