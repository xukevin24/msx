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
from strategy import percent_strategy
from strategy import mv_strategy 
from strategy import time_strategy

from trade import trade as Trade

import simu_stat
import account as Account
import config.config as config
import config.db_config as db_config

def simulate_all_once(codes, N):
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

        doncainSTG = donchain_strategy.Strategy(N, 20, True)
        percentSTG = percent_strategy.Strategy(0.8)
        timeSTG = time_strategy.Strategy(60)
        randomSTG = random_strategy.Strategy(0.8)
        randomSTG1 = random_strategy.Strategy(0)
        mvSTG = mv_strategy.Strategy(N, 0.05, 0.05)

        STG = test_strategy.Strategy([doncainSTG], [doncainSTG, percentSTG, timeSTG])
        
        account = simulate(datas, STG, Trade.Trade)

        accounts.append(account)
        sts.acc(account.statistics)

        print("%s,%0.2f,%0.2f,%0.2f" % (code, account.cash, account.statistics.mfeToMae, sts.mfeToMae))

    #统计
    print("%4d--> succ %0.2f,profit %0.2f,mfe/mae %0.2f" % (N, sts.succRatio, sts.profit * 100 / (sts.accountNum * config.config.cash), sts.mfeToMae))
    
if __name__ == "__main__":
    cc = Code()
    codes = cc.getAllCodes()

    for i in range(200, 300, 20):
        simulate_all_once(codes, i)
        break