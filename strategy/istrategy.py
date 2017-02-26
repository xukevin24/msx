#coding=utf-8
'''
    strategy 接口类，其他的实现对应的接口
'''

class IStrategy:
    def __init__(self):
        pass

    #返回最小开始索引
    def min_start(self):
        return 0

    #对某一天返回是否进场点
    def is_entry(self, dataApi, index):
        return False

    #对某一天返回是否出场
    def is_exit(self, dataApi, index, tradeInfo):
        return False

    #判断是不是该跳过当日
    def is_skip(self, dataApi, index, tradeInfo):
        if dataApi.volume(index) <= 0 or (dataApi.high(index) == dataApi.low(index))
            return True
        return False

    #进场使用资金比率
    def get_percent(self):
        return 1