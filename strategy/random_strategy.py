#coding=utf-8
'''
    随机开始
'''
import sys
import random
import os

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy

class RandomStrategy(istrategy.IStrategy):
    #返回最小开始索引
    def min_start(self):
        return 0

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        if random.randint(0,9) == 0:
            return True
        return False

    #对某一天返回是否出场
    def is_exit(self, dataApi, index, enterInfo):
        if random.randint(0,9) == 0:
            return True
        return False

    #进场使用资金比率
    def get_percent(self):
        return 1