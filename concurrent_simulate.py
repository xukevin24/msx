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

    last_account = Account.MarketDayStat()
    last_account.cash = 10000000
    num = selectPool.get_num()

    #对每一个交易日遍历
    current_date = datetime.datetime.strptime(str(startDate), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(endDate), "%Y-%m-%d")
    while current_date <= end_date:
        weekday = current_date.strftime("%w")
        if weekday == '0' or weekday == '6':
            current_date += datetime.timedelta(days=1)
            continue
        last_account.current_date = current_date
        current_date += datetime.timedelta(days=1)

        dateStr = last_account.current_date.strftime('%Y-%m-%d')
        #获取所有可入集合
        available_dataApiList = []
        for dataApi in dataApiList.values():
            if last_account.is_code_in(dataApi.get_code()):
                continue

            index = dataApi.get_index_of_date(dateStr)
            if index < 0:
                continue

            if strategy.is_skip(dataApi, index) == False and strategy.is_entry(dataApi, index):
                available_dataApiList.append(dataApi)

        #处理所有持有是否exit
        exit_dataApiList = []
        clear_code = []
        for (code,position) in last_account.positions.items():
            dataApi = dataApiList[code]
            
            index = dataApi.get_index_of_date(dateStr)
            if index < 0:
                continue
            
            enterInfo = istrategy.IEnterInfo(position[1], position[0], position[2], position[3])
            if strategy.is_skip(dataApi, index) == False and strategy.is_exit(dataApi, index, enterInfo):
                #处理positon及Account
                last_account.exit_trades[code] = position
                last_account.cash += position[0] * dataApi.close(index) * (1 - 0.002) 
                clear_code.append(code)
        
        for code in clear_code:
            last_account.positions.pop(code)

        #用selectPool选择目标范围
        enter_dataApiList = selectPool.select(available_dataApiList, dateStr, num)

        #处理所有enter
        total_price = last_account.get_total_price(dataApiList)
        piece = total_price / num
        for dataApiItem in enter_dataApiList:
            dataApi = dataApiItem['data']
            index = dataApi.get_index_of_date(dateStr)
            use_cash = min(last_account.cash, piece)
            price = dataApi.close(index)
            volume = util.calc_voume(use_cash / (1 + 0.001), last_account.get_percent(), price)

            if volume < 100:
                break
            
            last_account.positions[dataApi.get_code()] = [volume, price, index, dateStr, piece]
            last_account.enter_trades[dataApi.get_code()] = [volume, price]
            last_account.cash -= volume * price * (1 + 0.0005)

            #for error test
            if last_account.cash < 0:
                error = 'error'
        
        dailyAccount.append(last_account)
        last_account = copy.deepcopy(last_account)
        last_account.enter_trades.clear()
        last_account.exit_trades.clear()
    
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
        if code[:3] == '300':
            datas = data_api.KData()
            datas.fileDir = "C:/"
            datas.init_data(code, fromDB=False)
            dataApiList[code] = datas

    s = donchain_strategy.DonchainStrategy(5,20)
    #pool = lowprice_pool.StockPool(5)
    pool = movement_pool.StockPool(10)
    
    #test
    #result =pool.select(dataApiList, '2017-01-01', 10)

    dailyAccount = concurrent_simulate(dataApiList, s, pool, '2015-01-01', '2017-01-01')

    print(datetime.datetime.now())
    print('最终资金:10000000')
    for account in dailyAccount:
        print('%s资金:%0.2f' % (account.current_date, account.get_total_price(dataApiList)))