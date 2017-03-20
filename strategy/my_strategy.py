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
        return self.N1 * 2 + self.N2 + 5

    def is_entry(self, dataApi, index):
        if (dataApi.open(index) - dataApi.low(index)) <= abs(dataApi.open(index) - dataApi.close(index)) * 3:
            return False
    
        for i in range(self.N2):
            #if dataApi.close(index + i) > dataApi.close(index + i + 1) * 1.07:
            #    break
            if self.is_exist(dataApi, index, i):
                return True
        return False

    #n,F+2日,              F.. ...  R
    def is_exist(self, dataApi, index, i):
        n = index + i# + 1
        #F = n + 2
        #if dataApi.close(F) >= dataApi.close(F + 1):
        #    return False
        if dataApi.close(n) >= dataApi.ma(n, self.N1) * 0.9:# or dataApi.close(n) >= dataApi.ma(n, self.N1 * 2) * 0.8:
            return False
        
        #return dataApi.close(index) > dataApi.close(n) * 1.3: #and rClose > dataApi.close(n) * 0.97
        #print('%s,%s,%s' %(dataApi.get_code(), dataApi.date(n), dataApi.date(index)))
        return True
        num = 0
        for i in range(F + 1, F + self.N1):
            ma35 = dataApi.ma(i, self.N1)
            if dataApi.low(i) < ma35 * 0.08:
                num += 1
        return num <= 3

    def is_exit(self, dataApi, index, enterInfo):
        if dataApi.close(index) < dataApi.close(index + 1) and dataApi.high(index) < dataApi.high(index + 1):
        #if dataApi.close(index) < dataApi.low(enterInfo.enter_index):
            return True
        return False


