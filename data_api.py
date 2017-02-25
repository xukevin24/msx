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
        self.datas = ()

    #数据初始化
    def init_data(self, code, index=False):
        self.code = code
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
            self.datas = cur.fetchall()
            #print type(self.datas)
            #print self.datas[0][0]
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

#test code
if __name__ == "__main__":
    d = KData()
    d.init_data('000001', index=False)
    print(d.get_code())
    print(d.date(0))
    print(d.ma(0, 20))
