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
    PE = 6
    PB = 7
    PS = 8
    PCF = 9
    LCAP = 10
    LFLO = 11
    EPS = 12
    MAX = 13

class KData:
    def __init__(self):
        self.code = ''
        self.datas = []
        self.fileDir = ''

    #数据初始化,index是否指数
    def init_data(self, code, index=False, fromDB=True):
        self.code = code
        if fromDB:
            return self.init_data_from_db(code, index)
        else:
            return self.init_data_from_file(code, index)

    @classmethod
    def create_data_obj(cls):
        obj = []
        for i in range(KDataType.MAX):
            obj.append(0)
        return obj

    #从文件系统读取数据，目录为代码顶层目录并行
    def init_data_from_file(self, code, index=False):
        if len(self.fileDir) == 0:
            self.fileDir = '../'
        path = self.fileDir + '/stock_day_back/' + str(code) + '.csv'
        #print(path)
        for line in open(path): 
            data = KData.create_data_obj() 
            words = line.split(',')
            data[0] = words[0]
            for i in range(1, len(words) - 1):
                data[i] = float(words[i])
            self.datas.append(data)
        
        #print(type(self.datas))
        #print(self.datas[0])
        #print(self.datas[0][0])

    #从数据库读取数据
    def init_data_from_db(self, code, index=False):
        conn = None
        try:
            conn = pymysql.connect(host=db.ip, port=db.port, user=db.user, passwd=db.passwd, db='stocks', charset='utf8')
            cur = conn.cursor()
            table = 'stock_day_back'
            if index:
                table = 'index_day'

            sql = "SELECT date,open,close,high,low,volume FROM " + table + " WHERE code='" + code + "' ORDER BY date DESC;"# LIMIT 300;"
            #print(sql)
            cur.execute(sql)
            datas = list(cur.fetchall())
            for data in datas:
                newData = KData.create_data_obj() 
                newData[KDataType.Date] = data[KDataType.Date].strftime('%Y-%m-%d')
                for i in range(1, len(data)):
                    newData[i] = data[i]
                self.datas.append(newData)
            #print(type(self.datas))
            #print(self.datas[0][0])
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()
    
    #数据初始化,index是否指数
    def init_factor(self, code, index=False, fromDB=True):
        self.code = code
        if fromDB:
            return self.init_factor_from_db(code, index)
        else:
            return self.init_factor_from_file(code, index)

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

    #返回日期对应索引
    def get_index_of_date(self, date):
        left = 0
        right = len(self.datas) - 1

        while left <= right:
            mid = (left+right)//2
            cur = self.date(mid)
            if date == cur:      
                return mid     
            elif date > cur:
                right = mid - 1   
            else:
                left = mid + 1    
        return -1
    #
    def get_data(self, index, type):
        try:
            return self.datas[index][type]
        except:
            print(index)

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
    
    #会引用对于index来说是未来的数据，2N+1期的低点
    def low_point(self, index, N):
        cur = self.low(index)
        for j in range(N + 1):
            if cur > self.low(index + j) or cur > self.low(index - j):
                return False
        return True
    
    #会引用对于index来说是未来的数据，2N+1期的高点
    def high_point(self, index, N):
        cur = self.high(index)
        for j in range(N + 1):
            if cur < self.high(index + j) or cur < self.high(index - j):
                return False
        return True

            
    #返回最近的低点索引，从index开始往前寻找最近的N低点
    def last_low_point(self, index, N):
        for j in range(index + N, self.length() - N):
            if self.low_point(j, N):
                return j
        return -1
    
    #返回最近的高点索引，从index开始往前寻找最近的N高点
    def last_high_point(self, index, N):
        for j in range(index + N, self.length() - N):
            if self.high_point(j, N):
                return j
        return -1
    
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
    
    #计算 EMA = Exponential Moving Average, http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
    def ema(self,index,N):
        emaN = []
        for i in range(self.length() - 1, -1, -1):
            j = self.length() - 1 - i
            if j == 0:
                emaN.append(self.close(i))
            else:
                emaN.append(self.close(i) + 2/N * emaN[j - 1])
        return emaN[self.length() - 1 - index]

    def dif(self,index,N):
        value = self.ema(index,12)-self.ema(index,26)
        return value

    def dea(self,index,N):
        sum == 0
        for j in range (9):
            sum += self.dif(index+j)
        return sum/9

    def bar(self,index,N):
        return self.dif(index,N)-self.dea(index.N)
        
##    #计算 MACD = Moving average convergence divergence
##    def macd(self):


#test code
if __name__ == "__main__":
    d = KData()
    d.init_data('300082', index=False, fromDB=False)
    print(d.get_code())
    print(d.date(0))
    print(d.ma(0, 20))
    print(d.get_index_of_date('2017-02-03'))
    print(d.ema(0, 20))
    print(d.ema(d.length() - 1, 20))

    idx = 0
    while True:
        idx = d.last_low_point(idx, 10)
        if idx < 0:
            break
        print(d.date(idx))
        print(d.high(idx))
    
    index = d.get_index_of_date('2012-01-04')
    print(d.close(index))
    print(d.close(index + 20))
    print((d.close(index) - d.close(index + 20)) / d.close(index + 20))
