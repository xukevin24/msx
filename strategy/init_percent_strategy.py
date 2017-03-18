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
    def __init__(self, N1, isReverse=False):
        self.N1 = N1
        self.isReverse = isReverse #反过来用

    #返回最小开始索引
    def min_start(self):
        return 0

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        return False

    #对某一天返回是否出场
    def is_exit(self, dataApi, index, enterInfo):
        close = dataApi.close(index)
        if self.isReverse == False:
            return close / enterInfo.enter_price < self.N1
        else:
            return close / enterInfo.enter_price > self.N1
