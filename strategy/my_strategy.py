#coding=utf-8
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 

class Strategy(istrategy.IStrategy):
    def __init__(self, N1, N2=20):
        self.N1 = N1
        self.N2 = N2

    def min_start(self):
        return self.N1 * 2 + 1

    def is_entry(self, dataApi, index):
        if (dataApi.open(index) - dataApi.low(index)) < abs(dataApi.open(index) - dataApi.close(index)) * 2:
            return False

        for i in range(20):
            if self.is_exist(dataApi, index, i):
                return True
        return False

    def is_exist(self, dataApi, index, i):
        F = index + i
        if dataApi.close(F) > dataApi.ma(F, self.N2) * 0.9:
            return False
        return True
        pass

    def is_exit(self, dataApi, index, enterInfo):
        if dataApi.close(index) < dataApi.close(index + 1) and dataApi.high(index) < dataApi.high(index + 1):
            return True
        return False


