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
        return self.N1 * 2 + 1

    def is_entry(self, dataApi, index):
        if ((dataApi.open(index) - dataApi.low(index)) / abs(dataApi.open(index) - dataApi.close(index)) <= 2:
            return False
        if dataApi.close(index) >= dataApi.close(index + 1):
            return False

        for i in range(20):
            if self.is_exist(i + 1):
                return True
        return False

    def is_exist(n):
        pass

    def is_exit(self, dataApi, index, enterInfo):
        if dataApi.close(index) < dataApi.close(index + 1) and dataApi.high(index) < dataApi.high(index + 1):
            return True
        return False


