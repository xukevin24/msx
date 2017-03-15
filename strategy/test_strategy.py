'''
'''
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 
import operator
class Strategy(istrategy.IStrategy):
    def __init__(self, enterStrategy, exitStrategy):
        self.enter_strategy = enterStrategy #[]与
        self.exit_strategy = exitStrategy   #[]或
        self.min_start_val = -1

    #返回最小开始索引
    def min_start(self):
        if self.min_start_val < 0:
            self.min_start_val = 0
            for STG in self.enter_strategy:
                self.min_start_val = max(STG.min_start(), self.min_start_val)
            for STG in self.exit_strategy:
                self.min_start_val = max(STG.min_start(), self.min_start_val)
        return self.min_start_val

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        for STG in self.enter_strategy:
            if STG.is_entry(dataApi, index) == False:
                return False
        return True

    #对某一天返回是否出场
    def is_exit(self, dataApi, index, enterInfo):
        for STG in self.exit_strategy:
            if STG.is_exit(dataApi, index, enterInfo):
                return True
        return False

    #进场使用资金比率
    def get_percent(self):
        return self.enter_strategy.get_percent()