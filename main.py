#coding=utf-8

'''
测试
'''

#禁止生成pyc文件
import sys
sys.dont_write_bytecode = True

import data_api
from code_api import Code
from simulate import simulate
from strategy import donchain_strategy
from strategy import random_strategy
from strategy import test_strategy
from trade import trade as Trade
import statistics
import account as Account
import config.config as config

#获取代码
Code.init_data()
codes = Code.get()

#对每个进行仿真运算
accounts = []
sts = statistics.statistics() 
for code in codes:
    datas = data_api.KData()
    datas.init_data(code)

    #s = donchain_strategy.DonchainStrategy(20, 20)
    #s = random_strategy.RandomStrategy()
    s = test_strategy.Strategy(5)
    
    account = simulate(datas, s, Trade.Trade)

    accounts.append(account)
    sts.acc(account.statistics)

    print("%s,%0.2f,%0.2f,%0.2f" % (code, account.cash, account.statistics.mfeToMae, sts.mfeToMae))

#统计
print(sts.succRatio)
print(sts.profit / (sts.accountNum * config.cash))
print(sts.mfeToMae)
    