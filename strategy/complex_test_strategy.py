'''
'''
import sys
import json
import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

from simulate import simulate

import data_api
import account as Account

from trade import trade as Trade

from strategy import istrategy 
from strategy import donchain_strategy 
from strategy import random_strategy 
from strategy import ma_strategy 
from strategy import time_strategy 
import simu_stat
import config.config as config

#example
_test_json= '\
    {\
        "op" : "or",\
        "data" :\
             [\
                 {\
                     "op" : "null",\
                     "data" : ["donchain", 50, 20]\
                 },\
                 {\
                     "op" : "and",\
                     "data" : \
                        [\
                            {\
                                "op" : "null",\
                                "data" : ["random", 10]\
                             },\
                            {\
                                "op" : "null",\
                                "data" : ["donchain", 50, 20]\
                             }\
                        ]\
                 }\
            ]\
     }'

class Strategy(istrategy.IStrategy):
    def __init__(self, enterStrategy, exitStrategy):
        self.enter_strategy = enterStrategy #[]或，（）与
        self.exit_strategy = exitStrategy   #[]或，（）与
        self.min_start_val = -1

    def min_start(self):
        if self.min_start_val < 0:
            self.min_start_val = 0
            self.min_start_val = max(self.min_start_val, self.min_start_impl(self.enter_strategy))
            self.min_start_val = max(self.min_start_val, self.min_start_impl(self.exit_strategy))
        return self.min_start_val
    
    def min_start_impl(self, stgList):
        if isinstance(stgList, (tuple,list)):
            value = 0
            for STG in stgList:
                value = max(value, self.min_start_impl(STG))
            return value
        else:
             return max(self.min_start_val, stgList.min_start())

    def is_entry(self, dataApi, index):
        if isinstance(self.enter_strategy, list):
            return self.is_entry_list(dataApi, index, self.enter_strategy)
        elif isinstance(self.enter_strategy, tuple):
            return self.is_entry_tuple(dataApi, index, self.enter_strategy)
        else:
            return self.enter_strategy.is_entry(dataApi, index)

    def is_entry_list(self, dataApi, index, stgList):
        for STG in stgList:
            if isinstance(STG, list):
                ret = self.is_entry_list(dataApi, index, STG)
            elif isinstance(STG, tuple):
                ret = self.is_entry_tuple(dataApi, index, STG)
            else:
                ret = STG.is_entry(dataApi, index)
            if ret: return True
        return False

    def is_entry_tuple(self, dataApi, index, stgList):
        for STG in stgList:
            if isinstance(STG, list):
                ret = self.is_entry_list(dataApi, index, STG)
            elif isinstance(STG, tuple):
                ret = self.is_entry_tuple(dataApi, index, STG)
            else:
                ret = STG.is_entry(dataApi, index)
            if not ret: return False
        return True

    def is_exit(self, dataApi, index, enterInfo):
        if isinstance(self.exit_strategy, list):
            return self.is_exit_list(dataApi, index, enterInfo, self.exit_strategy)
        elif isinstance(self.exit_strategy, tuple):
            return self.is_exit_tuple(dataApi, index, enterInfo, self.exit_strategy)
        else:
            return self.exit_strategy.is_exit(dataApi, index, enterInfo)

    def is_exit_list(self, dataApi, index, enterInfo, stgList):
        for STG in stgList:
            if isinstance(STG, list):
                ret = self.is_exit_list(dataApi, index, enterInfo, STG)
            elif isinstance(STG, tuple):
                ret = self.is_exit_tuple(dataApi, index, enterInfo, STG)
            else:
                ret = STG.is_exit(dataApi, index, enterInfo)
            if ret: return True
        return False

    def is_exit_tuple(self, dataApi, index, enterInfo, stgList):
        for STG in stgList:
            if isinstance(STG, list):
                ret = self.is_exit_list(dataApi, index, enterInfo, STG)
            elif isinstance(STG, tuple):
                ret = self.is_exit_tuple(dataApi, index, enterInfo, STG)
            else:
                ret = STG.is_exit(dataApi, index, enterInfo)
            if not ret: return False
        return True

    @staticmethod
    def init_from_ast(ast):
        op = ast['op']
        data = ast['data']
        if op == 'or':
            stgs = []
            for stgData in data:
                stg = Strategy.init_from_ast(stgData)
                stgs.append(stg)
            return stgs
        elif op == 'and':
            stgs = []
            for stgData in data:
                stg = Strategy.init_from_ast(stgData)
                stgs.append(stg)
            return tuple(stgs)
        else:
            return Strategy.create_strategy(data)

    @staticmethod
    def init_from_json(jsonString):
        obj = json.loads(jsonString)
        return Strategy.init_from_ast(obj)

    @staticmethod
    def create_strategy(params):
        stgName = params[0]
        if stgName == 'random':
            return random_strategy.Strategy(params[1])
        elif stgName == 'donchain':
            return donchain_strategy.Strategy(params[1], params[2])
        else:
            raise(Exception('not surportted strategy'))

#real run
if __name__ == "__main__":
    exitSTG = Strategy.init_from_json(_test_json)

    datas = data_api.KData()
    datas.init_data('300017')

    s = Strategy(exitSTG, donchain_strategy.Strategy(50, 20))

    account = simulate(datas, s, Trade.Trade)

    sts = simu_stat.statistics() 
    sts.acc(account.statistics)
    print("%4d--> succ %0.2f,profit %0.2f,mfe/mae %0.2f" % (0, sts.succRatio, sts.profit * 100 / (sts.accountNum * config.config.cash), sts.mfeToMae))


