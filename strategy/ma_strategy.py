#coding=utf-8
'''
    boll
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

    def min_start(self):
        return self.N1+1

    def is_entry(self, dataApi, index):  
        if self.isReverse == False:   
            if dataApi.close(index) > dataApi.ma(index, self.N1):
                return True
        else:
            if dataApi.close(index) < dataApi.ma(index, self.N1):
                return True
        return False

    def is_exit(self, dataApi, index, enterInfo):
        if self.isReverse == False:   
            if dataApi.close(index) < dataApi.ma(index, self.N1):
                return True
        else:
            if dataApi.close(index) > dataApi.ma(index, self.N1):
                return True
        return False

    #进场使用资金比率
    def get_percent(self):
        return 1