#coding=utf-8
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
        return 200

    def is_entry(self, dataApi, index):
        if self.is_high(dataApi, index) and self.is_low(dataApi, index):
            return True
        return False

    def is_exit(self, dataApi, index, enterInfo):
        return False

    def is_low(self, dataApi, index):
        idx1 = dataApi.last_low_point(index, self.N1)
        if idx1 < 0:
            return False
        idx2 = dataApi.last_low_point(idx1, self.N1)
        if idx1 < 0:
            return False
        if dataApi.low(idx1) > dataApi.low(idx2) * 1.2:
            return True
        idx3 = dataApi.last_low_point(idx2, self.N1)
        if idx3 < 0:
            return False
        if dataApi.low(idx2) > dataApi.low(idx3) * 1.2:
            return True

    def is_high(self, dataApi, index):
        idx1 = dataApi.last_high_point(index, self.N1)
        if idx1 < 0:
            return False
        idx2 = dataApi.last_high_point(idx1, self.N1)
        if idx1 < 0:
            return False
        if dataApi.high(idx1) > dataApi.high(idx2) * 1.2:
            return True      
        idx3 = dataApi.last_high_point(idx2, self.N1)
        if idx3 < 0:
            return False
        if dataApi.high(idx2) > dataApi.high(idx3) * 1.2:
            return True              
