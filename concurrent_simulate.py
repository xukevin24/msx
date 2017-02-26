#coding=utf-8
'''
    simulate
'''

import datetime
import time
import sys
import os

sys.dont_write_bytecode = True

import data_api
from code_api import Code
from simulate import simulate
from strategy import donchain_strategy
from strategy import random_strategy
from strategy import test_strategy
from trade import trade as Trade
from pool import ipool
import simu_stat
import config.config as config

import concurrent_account as Account

#多个同时测试
def concurrent_simulate(dataApiList, strategy, selectPool, startDate, endDate):
    dailyAccount = [] #放入每日最终情况

    last_account = Account.MarketDayStat()
    last_account.cash = 10000000

    #对每一个交易日遍历
    current_date = datetime.datetime.strptime(str(startDate), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(endDate), "%Y-%m-%d")
    while current_date <= end_date:
        weekday = current_date.strftime("%w")
        if weekday == '0' or weekday == '6':
            continue
        current_date += datetime.timedelta(days=1)

        #处理所有持有是否exit
        exit_dataApiList = []
        for position in last_account.positions:
            dataApi = dataApiList[position[0]]
            
            index = dataApi.get_index_of_date(str(current_date))
            if index < 0:
                continue

            if strategy.is_skip(dataApi, index, trade) == False and strategy.is_exit(dataApi, index, trade):
                #处理positon及Account
                pass

        #获取所有可入集合
        available_dataApiList = []
        for dataApi in dataApiList.values():
            index = dataApi.get_index_of_date(str(current_date))
            if index < 0:
                continue

            if strategy.is_skip(dataApi, index, trade) == False and .is_entry(dataApi, index):
                available_dataApiList.append(dataApi)

        #用selectPool选择目标范围
        enter_dataApiList = selectPool.select(available_dataApiList, current_date, 5)

        #处理所有enter
        for dataApi in enter_dataApiList:
            pass
        
        dailyAccount.append(last_account)
    
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
            datas.init_data(code, fromDB=False)
            dataApiList[code] = datas

    s = donchain_strategy.DonchainStrategy(5,20)
    pool = ipool.IStockPool()

    dailyAccount = concurrent_simulate(dataApiList, s, pool, '2015-01-01', '2017-01-01')
    account = dailyAccount[:-1]

    print('最终资金:10000000')
    print('最终资金:%0.2f' % (account.cash))