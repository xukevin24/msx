#coding=utf-8
'''
    百分比
'''
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 

class Strategy(istrategy.IStrategy):
    def __init__(self, N1):
        self.N1 = N1

    def min_start(self):
        return 0

    def is_entry(self, dataApi, index):
        return False

    def is_exit(self, dataApi, index, enterInfo):
        if enterInfo.enter_index == index:
            return False
        close = dataApi.close(index)
        h = dataApi.hhv(index, enterInfo.enter_index - index, data_api.KDataType.High)
        return close / h < self.N1
