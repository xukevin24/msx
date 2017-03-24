#coding=utf-8
'''
    simulate
'''

import datetime
import time
import sys
import os
import copy
import json

sys.dont_write_bytecode = True

import data_api
from code_api import Code
from simulate import simulate
from strategy import istrategy
from strategy import test_strategy
from strategy import random_strategy
from strategy import donchain_strategy
from strategy import smacross_strategy as smacross_strategy
from strategy import time_strategy as time_strategy
from strategy import init_percent_strategy as init_percent_strategy
from strategy import percent_strategy as percent_strategy
from strategy import bolang_strategy as bolang_strategy
from strategy import ma_strategy as ma_strategy
from strategy import my_strategy as my_strategy
from strategy import mv_strategy as mv_strategy
from strategy import sidewaysbreak_strategy as sidewaysbreak_strategy
from trade import trade as Trade
from ipool import movement_pool
from ipool import random_pool
import simu_stat
import config.config as config
import util as util
import util_ftp as util_ftp
import config.db_config as db_config

import concurrent_account as Account
from concurrent_simulate import concurrent_simulate
from concurrent_simulate import insert_index_value

#test code
if __name__ == "__main__":
    #获取代码
    cc = Code()
    codes = cc.getAllCodes()

    print(datetime.datetime.now())

    #获取数据
    TEST_TYPE = 2
    dataApiList = {}
    year = 2012
    startDate = str(year) + '-01-01'
    endDate =  '2017-01-01'
    dataStartDate = str(year - 5) + '-01-01'

    for code in codes:
        if code[:1] == db_config._type[TEST_TYPE] or db_config._type[TEST_TYPE] == 'A':
            datas = data_api.KData()
            datas.fileDir = db_config.config_path
            fromDB = False
            if datas.init_data(code, fromDB=fromDB) == False:
                #print('init code error')
                continue
            dataApiList[code] = datas
            #print(datetime.datetime.now())

    for N in range(20, 400, 20):
        print(N)
        randStg = random_strategy.Strategy(75)
        randStg1 = random_strategy.Strategy(10)
        donchainStg = donchain_strategy.Strategy(50,20, False)
        smaStg = smacross_strategy.SMACrossStrategy(7,20)
        timeSTG = time_strategy.Strategy(60)
        percentSTG = init_percent_strategy.Strategy(2, True)
        percentSTG1 = percent_strategy.Strategy(0.8)
        bolangSTG = bolang_strategy.Strategy(50)
        maSTG = ma_strategy.Strategy([10, 20, 30, 60])
        maSTG1 = ma_strategy.Strategy([1, 5, 10], True)

        mySTG = my_strategy.Strategy(35)
        #mvSTG = mv_strategy.Strategy(20, 0.01 * N, 0.01 * N)
        mvSTG = mv_strategy.Strategy(20, 0.051, 0.051)
        sidSTG = sidewaysbreak_strategy.Strategy(20, 15, 3)

        testStg = test_strategy.Strategy([mySTG], [mySTG])

        #pool = lowprice_pool.StockPool(5)
        pool = movement_pool.StockPool(10, N, asc=True)
        poolOut = movement_pool.StockPool(1, 20, asc=False)
    
        endCash = []
        minCash = 1000000
        maxCash = 0
        sumCash = 0
        for i in range(5):
            dailyAccount = concurrent_simulate(dataApiList, testStg, pool, poolOut, '2012-01-01', '2017-01-01')
            insert_index_value(TEST_TYPE, startDate, endDate, dailyAccount)
            curCash = dailyAccount[-1].get_total_price(dataApiList, dailyAccount[-1].current_date) / 10000000
            minCash = min(minCash, curCash)
            maxCash = max(maxCash, curCash)
            endCash.append(curCash)
            sumCash += curCash
            print('%0.2f,%0.2f,%0.2f,%0.2f\n' %(curCash,minCash,maxCash,sumCash/(i+1)))
            open(db_config.config_path + 'result-time-percent.txt', 'a').write('%0.2f,%0.2f,%0.2f,%0.2f\n' %(curCash,minCash,maxCash,sumCash/(i+1)))
            break
        break
    print(datetime.datetime.now())

    filename = 'data'
    s = json.dumps(dailyAccount, default=lambda data: data.__dict__, sort_keys=True, indent=4)
    with open(db_config.config_path + filename + '.json', 'w') as json_file:
        json_file.write(s)
    #util_ftp.upload_file(db_config.config_path + filename + '.json', filename + '.json')
    #util.openInWeb(db_config.web_url + filename)
    print('finish ...')
