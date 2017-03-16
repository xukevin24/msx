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
    def __init__(self, N1, N2=0, N3=0, isReverse=False):
        self.N1 = N1
        self.N2 = N2    #入场幅度
        self.N3 = N3    #出场幅度
        self.isReverse = isReverse

    #返回最小开始索引
    def min_start(self):
        return self.N1 + 1

    def is_entry(self, dataApi, index):
        if self.isReverse == False:
            if dataApi.close(index) > dataApi.close(index + self.N1) * (1 + self.N2):
                return True
        else:
            if dataApi.close(index) < dataApi.close(index + self.N1) * (1 - self.N2):
                return True
        return False

    def is_exit(self, dataApi, index, enterInfo):
        if self.isReverse == False:
            if dataApi.close(index) < dataApi.close(index + self.N1) * (1 - self.N3):
                return True
        else:
            if dataApi.close(index) > dataApi.close(index + self.N1) * (1 + self.N3):
                return False
        return False
