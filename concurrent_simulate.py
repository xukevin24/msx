#coding=utf-8
'''
    simulate
'''

import datetime
import time
import sys
import os
import copy

sys.dont_write_bytecode = True

import data_api
from code_api import Code
from simulate import simulate
from strategy import *
from trade import trade as Trade
from ipool import movement_pool
import simu_stat
import config.config as config
import util as util

import concurrent_account as Account

#多个同时测试
def concurrent_simulate(dataApiList, strategy, selectPool, startDate, endDate):
    dailyAccount = [] #放入每日最终情况

    account = Account.MarketDayStat()
    account.cash = 10000000
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
        #获取所有可入集合
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
        exit_dataApiList = []
        clear_code = []
        for (code,position) in account.positions.items():
            dataApi = dataApiList[code]
            
            index = dataApi.get_index_of_date(dateStr)
            if index < 0:
                continue
            
            enterInfo = istrategy.IEnterInfo(position[1], position[0], position[2], position[3])
            if strategy.is_skip(dataApi, index) == False and strategy.is_exit(dataApi, index, enterInfo):
                #处理positon及Account
                account.exit_trades[code] = position
                account.cash += position[0] * dataApi.close(index) * (1 - 0.002) 
                clear_code.append(code)
        
        for code in clear_code:
            account.positions.pop(code)

        #用selectPool选择目标范围
        enter_dataApiList = selectPool.select(available_dataApiList, dateStr, num)

        #处理所有enter
        total_price = account.get_total_price(dataApiList)
        piece = total_price / num
        for dataApiItem in enter_dataApiList:
            dataApi = dataApiItem['data']
            index = dataApi.get_index_of_date(dateStr)
            use_cash = min(account.cash, piece)
            price = dataApi.close(index)
            volume = util.calc_voume(use_cash / (1 + 0.001), account.get_percent(), price)

            if volume < 100:
                break
            
            account.positions[dataApi.get_code()] = [volume, price, index, dateStr, piece]
            account.enter_trades[dataApi.get_code()] = [volume, price]
            account.cash -= volume * price * (1 + 0.0005)

            #for error test
            if account.cash < 0:
                error = 'error'
        
        print('%s资金:%0.2f' % (account.current_date, account.get_total_price(dataApiList)))
        dailyAccount.append(account)
        account = copy.deepcopy(account)
        account.enter_trades.clear()
        account.exit_trades.clear()

        current_date += datetime.timedelta(days=1)
    
    return dailyAccount

#test code
if __name__ == "__main__":
    #获取代码
    Code.init_data()
    codes = Code.get()

    print(datetime.datetime.now())

    #获取数据
    dataApiList = {}
    sts = simu_stat.statistics() 
    for code in codes:
        if code[:3] == '600' or True:
            datas = data_api.KData()
            datas.fileDir = "C:/"
            fromDB = False
            datas.init_data(code, fromDB=fromDB)
            dataApiList[code] = datas
            #print(datetime.datetime.now())

    s = donchain_strategy.DonchainStrategy(50,20)
    #pool = lowprice_pool.StockPool(5)
    pool = movement_pool.StockPool(10)
    
    #test
    #result =pool.select(dataApiList, '2017-01-01', 10)

    dailyAccount = concurrent_simulate(dataApiList, s, pool, '2015-01-01', '2017-01-01')

    print(datetime.datetime.now())
    print('起始:10000000')
    for account in dailyAccount:
        print('%s :%0.2f' % (account.current_date, account.get_total_price(dataApiList)))