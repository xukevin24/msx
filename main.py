#coding=utf-8

'''
测试
'''

#禁止生成pyc文件
import sys
import datetime
sys.dont_write_bytecode = True

import data_api
from code_api import Code
from simulate import simulate
from strategy import donchain_strategy
from strategy import random_strategy
from strategy import test_strategy
from trade import trade as Trade
from strategy import mv_strategy 

import simu_stat
import account as Account
import config.config as config
import config.db_config as db_config


def simulate_all_once(codes):
    #对每个进行仿真运算
    accounts = []
    sts = simu_stat.statistics() 
    for code in codes:
        datas = data_api.KData()
        datas.fileDir = db_config.config_path
        if datas.init_data(code, fromDB=False, start='2012-01-01', end='2017-01-01') == False:
            #print('init code error')
            continue
        #print(datetime.datetime.now())

        #s = donchain_strategy.DonchainStrategy(20, 20)
        randomSTG = random_strategy.RandomStrategy(100)
        randomSTG1 = random_strategy.RandomStrategy(0)
        mvSTG = mv_strategy.Strategy(20, 0.05, 0.05)

        s = test_strategy.Strategy([mvSTG], [mvSTG])
        
        account = simulate(datas, s, Trade.Trade)

        accounts.append(account)
        sts.acc(account.statistics)

        #print("%s,%0.2f,%0.2f,%0.2f" % (code, account.cash, account.statistics.mfeToMae, sts.mfeToMae))

    #统计
    print(sts.succRatio)
    print(sts.profit / (sts.accountNum * config.config.cash))
    print(sts.mfeToMae)
    
if __name__ == "__main__":
    cc = Code()
    codes = cc.getAllCodes()

    for i in range(1):
        simulate_all_once(codes)