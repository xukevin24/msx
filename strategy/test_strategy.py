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
    def __init__(self, enterStrategy, exitStrategy):
        self.enter_strategy = enterStrategy
        self.exit_strategy = exitStrategy

    #返回最小开始索引
    def min_start(self):
        return max(self.enter_strategy.min_start(), self.exit_strategy.min_start())

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        return self.enter_strategy.is_entry(dataApi, index)

    #对某一天返回是否出场
    def is_exit(self, dataApi, index, enterInfo):
        return self.exit_strategy.is_exit(dataApi, index, enterInfo)

    #进场使用资金比率
    def get_percent(self):
        return self.enter_strategy.get_percent()