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
from strategy import istrategy as istrategy
from strategy import test_strategy as test_strategy
from strategy import random_strategy as random_strategy
from strategy import donchain_strategy as donchain_strategy
from strategy import smacross_strategy as smacross_strategy
from strategy import time_strategy as time_strategy
from strategy import percent_strategy as percent_strategy
from trade import trade as Trade
from ipool import movement_pool
import simu_stat
import config.config as config
import util as util
import util_ftp as util_ftp
import config.db_config as db_config

import concurrent_account as Account

#多个同时测试
def concurrent_simulate(dataApiList, strategy, selectPool, selectOutPool, startDate, endDate, account=None):
    dailyAccount = [] #放入每日最终情况

    if account == None:
        account = Account.MarketDayStat()
        account.cash = 10000000
    else:
        account.enter_trades = {}
        account.exit_trades = {}

    num = selectPool.get_num()

    #对每一个交易日遍历
    current_date = datetime.datetime.strptime(str(startDate), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(endDate), "%Y-%m-%d")
    while current_date <= end_date:
        weekday = current_date.strftime("%w")
        if weekday == '0' or weekday == '6':
            current_date += datetime.timedelta(days=1)
            continue

        account.current_date = current_date.strftime('%Y-%m-%d')
        dateStr = account.current_date
        #获取所有可入集合，过程可改为多线程
        available_dataApiList = []
        for dataApi in dataApiList.values():
            if account.is_code_in(dataApi.get_code()):
                continue

            index = dataApi.get_index_of_date(dateStr)
            if index < 0:
                continue

            if strategy.is_skip(dataApi, index) == False and strategy.is_entry(dataApi, index):
                available_dataApiList.append(dataApi)

        #处理所有持有是否exit
        exit_sig_dataApiList = []
        clear_code = []
        for (code,position) in account.positions.items():
            dataApi = dataApiList[code]
            
            index = dataApi.get_index_of_date(dateStr)
            if index < 0:
                continue
            
            enterInfo = istrategy.IEnterInfo(position[1], position[0], position[2], position[3])
            if strategy.is_skip(dataApi, index) == False and strategy.is_exit(dataApi, index, enterInfo):
                exit_sig_dataApiList.append(dataApi)

        total_0 = account.get_total_price(dataApiList, dateStr)
        account_0 = copy.deepcopy(account)
        if len(exit_sig_dataApiList) > 0:
            exit_dataApiList = selectOutPool.select(exit_sig_dataApiList, dateStr)
            for (code,position) in account.positions.items():
                for dataApiItem in exit_dataApiList:
                    dataApi = dataApiItem['data']
                    if code == dataApi.get_code():
                        account.exit_trades[code] = position
                        index = dataApi.get_index_of_date(dateStr)
                        account.cash += position[0] * dataApi.close(index) * (1 - 0.002) 
                        clear_code.append(code)
                        break
            
            for code in clear_code:
                account.positions.pop(code)
        
        total_pre = account.get_total_price(dataApiList, dateStr)
        account_pre = copy.deepcopy(account)
        if (total_pre - total_0) / total_0 > 0.01:
            error = 'error'

        if len(available_dataApiList) > 0:
            #用selectPool选择目标范围
            enter_dataApiList = selectPool.select(available_dataApiList, dateStr)

            #处理所有enter
            total_price = account.get_total_price(dataApiList, dateStr)
            piece = total_price / num
            for dataApiItem in enter_dataApiList:
                dataApi = dataApiItem['data']
                index = dataApi.get_index_of_date(dateStr)
                use_cash = min(account.cash * account.get_percent(), piece)
                price = dataApi.close(index)
                if use_cash < piece/3: #小于三分之一份额中断
                    break
                
                volume = util.calc_voume(use_cash / (1 + 0.001), price)
                if volume < 100:
                    break
                
                account.positions[dataApi.get_code()] = [volume, price, index, dateStr, piece]
                account.enter_trades[dataApi.get_code()] = [volume, price]
                account.cash -= volume * price * (1 + 0.0005)

                #for error test
                if account.cash < 0:
                    error = 'error'
                    break
        
        total_cur = account.get_total_price(dataApiList, dateStr)
        if (total_pre - total_cur) / total_pre > 0.01:
            error = 'error'

        #print('%s total :%0.2f' % ( account.current_date, total_cur/10000000))
        dailyAccount.append(account)
        account = copy.deepcopy(account)
        account.enter_trades.clear()
        account.exit_trades.clear()

        current_date += datetime.timedelta(days=1)
    
    return dailyAccount

#test code
if __name__ == "__main__":
    #获取代码
    cc = Code()
    codes = cc.getAllCodes()

    print(datetime.datetime.now())

    #获取数据
    dataApiList = {}
    sts = simu_stat.statistics() 
    for code in codes:
        if code[:1] == '3' or False:
            datas = data_api.KData()
            datas.fileDir = db_config.config_path
            fromDB = False
            datas.init_data(code, fromDB=fromDB)
            dataApiList[code] = datas
            #print(datetime.datetime.now())

    randStg = random_strategy.RandomStrategy()
    donchainStg = donchain_strategy.DonchainStrategy(50,20)
    smaStg = smacross_strategy.SMACrossStrategy(7,20)
    timeSTG = time_strategy.Strategy(60)
    percentSTG = percent_strategy.Strategy(0.8)

    testStg = test_strategy.Strategy([randStg], [randStg, percentSTG, timeSTG])

    #pool = lowprice_pool.StockPool(5)
    pool = movement_pool.StockPool(5, asc=True)
    poolOut = movement_pool.StockPool(1, asc=False)
    
    #test
    #result =pool.select(dataApiList, '2017-01-01', 10)

    endCash = []
    minCash = 1000000
    maxCash = 0
    sumCash = 0
    for i in range(100):
        dailyAccount = concurrent_simulate(dataApiList, testStg, pool, poolOut, '2012-01-01', '2017-01-01')
        curCash = dailyAccount[-1].get_total_price(dataApiList, dailyAccount[-1].current_date) / 10000000
        minCash = min(minCash, curCash)
        maxCash = max(maxCash, curCash)
        endCash.append(curCash)
        sumCash += curCash
        print('%0.2f,%0.2f,%0.2f,%0.2f\n' %(curCash,minCash,maxCash,sumCash/(i+1)))
        open(db_config.config_path + 'result-time-percent.txt', 'a').write('%0.2f,%0.2f,%0.2f,%0.2f\n' %(curCash,minCash,maxCash,sumCash/(i+1)))

    print(datetime.datetime.now())

    filename = 'data'
    s = json.dumps(dailyAccount, default=lambda data: data.__dict__, sort_keys=True, indent=4)
    with open(db_config.config_path + filename + '.json', 'w') as json_file:
        json_file.write(s)
    #util_ftp.upload_file(db_config.config_path + filename + '.json', filename + '.json')
    #util.openInWeb(db_config.web_url + filename)

