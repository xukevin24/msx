#coding=utf-8
'''
    随机开始
'''

import random

import strategy.istrategy as istrategy

class RandomStrategy(istrategy.IStrategy):
    #返回最小开始索引
    def min_start(self):
        return 20

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        if random.randint(0,9) == 0:
            return True
        return False

    #对某一天返回是否出场
    def is_exit(self, dataApi, index, tradeInfo):
        if random.randint(0,9) == 0:
            return True
        return False

    #进场使用资金比率
    def get_percent(self):
        return 1