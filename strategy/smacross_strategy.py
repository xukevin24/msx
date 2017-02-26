#coding=utf-8
'''
    boll
'''
import sys
import strategy.istrategy as istrategy

import os
cwd = os.getcwd()
sys.path.insert(0, os.getcwd())

import data_api 

class SMACrossStrategy(istrategy.IStrategy):
    # N1, N2是用于计算两条SMA曲线的天数, N1<N2
    def __init__(self, N1, N2):
        self.N1 = N1
        self.N2 = N2

    #返回最小开始索引
    def min_start(self):
        return self.N2+1

    #对某一天返回是否进场-SMA（N1）向上突破SMA（N2）： 如果某日SMA(N1)>SMA(N2)，而前一日SMA(N1)<=SMA(N2)，进场
    def is_entry(self, dataApi, index):
        if (dataApi.ma(index,self.N1) > dataApi.ma(index,self.N2)) and (dataApi.ma(index+1,self.N1) <= dataApi.ma(index+1,self.N2)):
            return True
        return False

    #对某一天返回是否出场--SMA（N1）向下跌破SMA（N2）： 如果某日SMA(N1)<SMA(N2)，而前一日SMA(N1)>=SMA(N2)，出场
    def is_exit(self, dataApi, index, tradeInfo):
        if (dataApi.ma(index,self.N1) < dataApi.ma(index,self.N2)) and (dataApi.ma(index+1,self.N1) >= dataApi.ma(index+1,self.N2)):
            return True
        return False

    #判断是不是该跳过当日
    def is_skip(self, dataApi, index, tradeInfo):
        return False

    #进场使用资金比率
    def get_percent(self):
        return 1