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
import pickle
import pymysql

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
import config.db_config as db

import concurrent_account as Account
import concurrent_simulate

#多个同时测试
def get_account_from_db(current_date, table):
    conn = None
    try:
        conn = pymysql.connect(host=db.ip, port=db.port, user=db.user, passwd=db.passwd, db='strategies', charset='utf8')
        cur = conn.cursor()
        sql = "select data from %s where date='%s'" % (table, current_date)
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if conn != None:
            conn.close()
    if len(data) == 0:
        return None
    return data[0][0]

def save_account_to_db(account, date, table):
    data = json.dumps(account, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    #data = pickle.dumps(codes)
    conn = None
    try:
        conn = pymysql.connect(host=db.ip, port=db.port, user=db.user, passwd=db.passwd, db='strategies', charset='utf8')
        cur = conn.cursor()
        #table = 'random_300'
        sql = "insert into %s values('%s','%s')" % (table, date, data)
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn != None:
            conn.close()

#test code
if __name__ == "__main__":
    print(dir(Account.MarketDayStat))
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(today)
    today = '2017-01-06'
    table = 'random_300'
    yestoday = '2017-01-05'
    jsonData = get_account_from_db(yestoday, table)
    if jsonData == None:
        account = Account.MarketDayStat()
        account.cash = 10000000    
    else:
        account = json.loads(jsonData)

    cc = Code()
    codes = cc.getAllCodes()

    #获取数据
    dataApiList = {}
    for code in codes:
        if code[:1] == '3' or False:
            datas = data_api.KData()
            datas.fileDir = db_config.config_path
            fromDB = False
            datas.init_data(code, fromDB=fromDB)
            dataApiList[code] = datas
            #print(datetime.datetime.now())

    randStg = random_strategy.RandomStrategy()
    timeSTG = time_strategy.Strategy(60)
    percentSTG = percent_strategy.Strategy(0.8)

    testStg = test_strategy.Strategy([randStg], [randStg, percentSTG, timeSTG])

    #pool = lowprice_pool.StockPool(5)
    pool = movement_pool.StockPool(10, asc=True)
    poolOut = movement_pool.StockPool(1, asc=False)

    #account = get_account_from_db(yestoday)
    #account = get_account_from_db(today, table)

    #test
    dailyAccount = concurrent_simulate.concurrent_simulate(dataApiList, testStg, pool, poolOut, today, today, account)

    save_account_to_db(dailyAccount[-1], today, table)

