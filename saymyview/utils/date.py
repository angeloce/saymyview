#coding:utf-8

import time
import datetime


def now():
    return datetime.datetime.now()

def strnow():
    return time.strftime('%Y-%m-%d %H:%M:%S')
