'''
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

    #返回最小开始索引
    def min_start(self):
        return 60#self.N1 * 2 + 1

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        llv = dataApi.llv(index, self.N1 * 2 + 1, data_api.KDataType.Low)
        ma60 = dataApi.ma(index, 60)
        if dataApi.low(index + self.N1) == dataApi.llv(index, self.N1 * 2 + 1, data_api.KDataType.Low):
            if llv < ma60:
                return True
        return False

    #对某一天返回是否出场
    def is_exit(self, dataApi, index, enterInfo):
        if dataApi.length() > index + 20 and dataApi.low(index) == dataApi.llv(index, 20, data_api.KDataType.Low):
            return True
        return False

    #进场使用资金比率
    def get_percent(self):
        return 1