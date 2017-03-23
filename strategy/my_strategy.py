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
        if not self.is_R(dataApi, index):
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

    def is_R(self, dataApi, index):
        return (dataApi.open(index) - dataApi.low(index)) > abs(dataApi.open(index) - dataApi.close(index)) * 2
        
    def is_entry_first(self, dataApi, index):
        if not self.is_R(dataApi, index):
            return False
        j = -1
        for i in range(20):
            if self.is_exist(dataApi, index, i):
                j = i
                break
        if j < 0:
            return False
        if j <= 1:
            return True
        for i in range(2, j):
            if self.is_R(dataApi, index):
                return False
        return True

    def is_exit(self, dataApi, index, enterInfo):
        if dataApi.close(index) < dataApi.close(index + 1) and dataApi.high(index) < dataApi.high(index + 1):
            return True
        return False


