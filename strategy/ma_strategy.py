#coding=utf-8
import sys
import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 

class Strategy(istrategy.IStrategy):
    def __init__(self, NArr, isReverse=False):
        self.NArr = NArr
        self.isReverse = isReverse #反过来用

    def min_start(self):
        return max(self.NArr) + 1

    def is_entry(self, dataApi, index):  
        if self.isReverse == False: 
            for i in range(len(self.NArr) - 1):
                if dataApi.ma(index, self.NArr[i]) < dataApi.ma(index, self.NArr[i + 1]):
                    return False
            return True
        else:
            for i in range(len(self.NArr) - 1):
                if dataApi.ma(index, self.NArr[i]) > dataApi.ma(index, self.NArr[i + 1]):
                    return False
        return False

    def is_exit(self, dataApi, index, enterInfo):
        return not self.is_entry(dataApi, index)