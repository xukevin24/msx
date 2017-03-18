#coding=utf-8
'''
    唐奇安通道
'''
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 

class Strategy(istrategy.IStrategy):
    def __init__(self, N1, N2, isReverse=False):
        self.N1 = N1
        self.N2 = N2
        self.isReverse = isReverse

    #返回最小开始索引
    def min_start(self):
        return max(self.N1, self.N2)

    def is_entry(self, dataApi, index):
        if self.isReverse:
            return self.is_new_low(dataApi, index)
        else:
            return self.is_new_high(dataApi, index)

    def is_exit(self, dataApi, index, enterInfo):
        if self.isReverse:
            return self.is_new_high(dataApi, index)
        else:
            return self.is_new_low(dataApi, index)

    def is_new_high(self, dataApi, index):
        return dataApi.high(index) == dataApi.hhv(index, self.N1, data_api.KDataType.High)

    def is_new_low(self, dataApi, index):
        return dataApi.low(index) == dataApi.llv(index, self.N2, data_api.KDataType.Low)
    