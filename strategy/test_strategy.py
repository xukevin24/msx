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
        self.enter_strategy = enterStrategy
        self.exit_strategy = exitStrategy

    #返回最小开始索引
    def min_start(self):
        return max(self.enter_strategy.min_start(), self.exit_strategy.min_start())
    
    def logic(a,func,b):
        mappings={
                '&': operator.and_,
                '|': operator.or_
                }
        return mappings[func](a,b)

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        if len(self.enterStrategy)==1:
            return self.enter_strategy[0].is_entry(dataApi, index)
        else:
            for s in self.enter_strategy:
                if type(s)==list:
                    s=self.logic(s[0].is_entry(dataApi, index),s[1],s[2].is_entry(dataApi, index))
                else:
                    continue
            
    #对某一天返回是否出场
    def is_exit(self, dataApi, index, enterInfo):
        return self.exit_strategy.is_exit(dataApi, index, enterInfo)

    #进场使用资金比率
    def get_percent(self):
        return self.enter_strategy.get_percent()