#coding=utf-8
'''
    boll
'''
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 

class BBandStrategy(istrategy.IStrategy):
    # N1是用于计算布林格的天数
    def __init__(self, N1):
        self.N1 = N1
        #self.N2 = N2

    #返回最小开始索引
    def min_start(self):
        return self.N1+1

    #对某一天返回是否进场-收盘价向上突破布林格下限： 如果某日收盘价高于当日的布林格下限，而前一日收盘价低于当日布林格下限，进场
    def is_entry(self, dataApi, index):
        if (dataApi.close(index) > dataApi.bb_lower(index,self.N1)) and (dataApi.close(index+1) <= dataApi.bb_lower(index+1,self.N1)):
            return True
        return False

    #对某一天返回是否出场-收盘价向下跌破布林格上限： 如果某日收盘价低于当日布林格上限，而前一日收盘价高于当日布林格上限，出场
    def is_exit(self, dataApi, index, enterInfo):
        if (dataApi.close(index) < dataApi.bb_upper(index,self.N1)) and (dataApi.close(index+1) >= dataApi.bb_upper(index+1,self.N1)):
            return True
        return False

    #进场使用资金比率
    def get_percent(self):
        return 1