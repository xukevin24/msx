#coding=utf-8
'''
    get data mysql, return data list
'''

import pymysql
import time
import datetime
import sys
import os
import config.db_config as db
import statistics as stat

class KDataType:
    Date = 0
    Open = 1
    Close = 2
    High = 3
    Low = 4
    Volume = 5

class KData:
    def __init__(self):
        self.code = ''
        self.datas = []

    #数据初始化,index是否指数
    def init_data(self, code, index=False, fromDB=True):
        self.code = code
        if fromDB:
            return self.init_data_from_db(code, index)
        else:
            return self.init_data_from_file(code, index)

    #从文件系统读取数据，目录为代码顶层目录并行
    def init_data_from_file(self, code, index=False):
        path = '../stock_day_back/' + str(code) + '.csv'
        #print(path)
        for line in open(path):  
            words = line.split(',')
            for i in range(1, len(words) - 1):
                words[i] = float(words[i])
            self.datas.append(words)
        
        #print(type(self.datas))
        #print(self.datas[0])
        #print(self.datas[0][0])

    #从数据库读取数据
    def init_data_from_db(self, code, index=False):
        conn = None
        try:
            conn = pymysql.connect(host=db.ip, port=db.port, user=db.user, passwd=db.passwd, db='stocks', charset='utf8')
            cur = conn.cursor()

            cursor = conn.cursor()
            table = 'stock_day_back'
            if index:
                table = 'index_day'

            sql = "SELECT date,open,close,high,low,volume FROM " + table + " WHERE code='" + code + "' ORDER BY date DESC;"# LIMIT 300;"
            #print(sql)
            cur.execute(sql)
            datas = list(cur.fetchall())
            for data in datas:
                newData = list(data)
                newData[KDataType.Date] = newData[KDataType.Date].strftime('%Y-%m-%d')
                self.datas.append(newData)
            #print(type(self.datas))
            #print(self.datas[0][0])
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    #
    def get_code(self):
        return self.code
    #
    def length(self):
        return len(self.datas)
    #
    def date(self, index):
        return self.get_data(index, KDataType.Date)
    #
    def open(self, index):
        return self.get_data(index, KDataType.Open)
    #
    def close(self, index):
        return self.get_data(index, KDataType.Close)
    #
    def high(self, index):
        return self.get_data(index, KDataType.High)
    #
    def low(self, index):
        return self.get_data(index, KDataType.Low)
    #
    def volume(self, index):
        return self.get_data(index, KDataType.Volume)

    #需要优化成二分查找
    def get_index_of_date(self, date):
        for i in range(len(self.datas)):
            #print(self.datas[i][KDataType.Date])
            if self.datas[i][KDataType.Date] == date:
                return i
        return -1
    #
    def get_data(self, index, type):
        return self.datas[index][type]

    #计算MA
    def ma_impl(self, index, N, type):
        sum = 0
        for j in range(N):
            sum += self.get_data(index + j, type)
        return sum/N

    #计算MA
    def ma(self, index, N):
        return self.ma_impl(index, N, KDataType.Close)

    #
    def hhv(self, index, N, type):
        value = 0
        for j in range(N):
            value = max(value, self.get_data(index + j, type))
        return value
    
    #
    def llv(self, index, N, type):
        value = 100000000
        for j in range(N):
            value = min(value, self.get_data(index + j, type))
        return value
    
    #计算某日收盘价较上一日收盘价相对变化（）
    def dReturn(self, index):
        return (self.close(index)-self.close(index+1))/self.close(index+1)
    
    #基于N天的收盘价计算index日的Volatility
    def vola(self,index,N):
        dataset=[]
        for i in range(N):
            dataset.append(self.close(index+i))
        return stat.stdev(dataset)
            
    #计算布林格band下限
    def bb_lower(self,index,N):
        return self.ma(index,N)-2*self.vola(index,N)
    
    #计算布林格band上限
    def bb_upper(self,index,N):
        return self.ma(index,N)+2*self.vola(index,N)
    
#    #计算 EMA = Exponential Moving Average, http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
#    def ema(self,index,N):
#        
##    #计算 MACD = Moving average convergence divergence
##    def macd(self):


#test code
if __name__ == "__main__":
    d = KData()
    d.init_data('300017', index=False, fromDB=True)
    print(d.get_code())
    print(d.date(0))
    print(d.ma(0, 20))
    print(d.get_index_of_date('2017-02-03'))
    
