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

class Code:
    codes = []

    #数据初始化
    @classmethod
    def init_data(cls, index=False, fromDB=True):
        if fromDB:
            return cls.init_data_from_db(index)
        else:
            return cls.init_data_from_file(index)
            
    @classmethod
    def init_data_from_file(cls, index=False):
        pass

    @classmethod
    def init_data_from_db(cls, index=False):
        cls.codes = []
        conn = None
        try:
            conn = pymysql.connect(host=db.ip, port=db.port, user=db.user, passwd=db.passwd, db='stocks', charset='utf8')
            cur = conn.cursor()

            cursor = conn.cursor()
            if index:
                sql = "SELECT code FROM index_basics;"
            else:
                sql = "SELECT code FROM stock_basics;"
            #print sql
            cur.execute(sql)
            result = cur.fetchall()
            for t in result:
                cls.codes.append(t[0])
        finally:
            conn.close()

    @classmethod
    def get(cls):
        return cls.codes
        
#test code
if __name__ == "__main__":
    Code.init_data()
    print(Code.get())


