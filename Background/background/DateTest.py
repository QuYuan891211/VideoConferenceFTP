#!/usr/bin/env python

# encoding: utf-8

# @Time    : 2021/7/16 12:16
# @Author  : yq
# @Site    : 
# @File    : DateTest.py
# @Software: PyCharm
import datetime
def test():
    now = datetime.date.today()
    time_str3 = datetime.datetime.strftime(now, '%Y%m%d')
    print(time_str3)

if __name__ == "__main__":
    test()