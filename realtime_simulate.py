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
        sql = "select `data` from %s where date='%s'" % (table, current_date)
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

def get_latest_trade_day_from_db(table):
    conn = None
    try:
        conn = pymysql.connect(host=db.ip, port=db.port, user=db.user, passwd=db.passwd, db='strategies', charset='utf8')
        cur = conn.cursor()
        sql = "select `date` from %s order by date DESC limit 1" % (table)
        cur.execute(sql)
        data = cur.fetchall()
        if len(data) == 0:
            return None
        return data[0][0]
    except Exception as e:
        print(e)
    finally:
        if conn != None:
            conn.close()
    return None

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

def real_main(table, startDate, endDate):
    current_date = datetime.datetime.strptime(str(startDate), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(endDate), "%Y-%m-%d")
    while current_date <= end_date:
        weekday = current_date.strftime("%w")
        if weekday == '0' or weekday == '6':
            print('weekday %s'% str(current_date))
            current_date += datetime.timedelta(days=1)
            continue

        yestoday = get_latest_trade_day_from_db(table)
        dateStr = current_date.strftime('%Y-%m-%d')

        jsonData = get_account_from_db(yestoday, table)
        if jsonData == None:
            account = Account.MarketDayStat()
            account.cash = 10000000    
        else:
            tmpAccount = json.loads(jsonData)
            account = Account.MarketDayStat()
            for name,value in vars(account).items(): 
                exec('account.%s = tmpAccount["%s"]'%(name, name))

        if True:#dateStr == startDate:
            cc = Code()
            codes = cc.getAllCodes()

            #获取数据
            dataApiList = {}
            for code in codes:
                if code[:1] == '6' or False:
                    datas = data_api.KData()
                    datas.fileDir = db_config.config_path
                    fromDB = True
                    datas.init_data(code, fromDB=fromDB, end=dateStr, Num=30)
                    dataApiList[code] = datas
                    #print(datetime.datetime.now())

        randStg = random_strategy.RandomStrategy()
        timeSTG = time_strategy.Strategy(60)
        percentSTG = percent_strategy.Strategy(0.8)

        testStg = test_strategy.Strategy([randStg], [randStg, percentSTG, timeSTG])

        pool = movement_pool.StockPool(5, asc=True)
        poolOut = movement_pool.StockPool(1, asc=False)

        #test
        dailyAccount = concurrent_simulate.concurrent_simulate(dataApiList, testStg, pool, poolOut, dateStr, dateStr, account)

        save_account_to_db(dailyAccount[-1], dateStr, table)
        print('finish')
        current_date += datetime.timedelta(days=1)

#test code
def test():
    table = 'random_6'
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    startDate = '2017-02-24'
    endDate = today
    real_main(table, startDate, endDate)

#real run
if __name__ == "__main__":
    table = 'random_6'
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    startDate = today
    endDate = today
    real_main(table, startDate, endDate)