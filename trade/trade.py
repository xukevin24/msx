#coding=utf-8
'''
    one trade
    似乎该考虑加减码
'''
import math
import sys
import os
cwd = os.getcwd()
sys.path.insert(0, os.getcwd())

import data_api 

class Trade():
    def __init__(self):
        self.enter_date = ''
        self.enter_price = 0
        self.enter_index = -1

        self.exit_date = ''
        self.exit_price = 0
        self.exit_index = -1

        self.volume = 0
        self.fee = 0
        self.profit = 0

        self.MFE = 0
        self.MAE = 0
    
    def on_enter(self, dataApi, account, index):
        self.enter_date = dataApi.date(index)
        self.enter_price = dataApi.close(index)
        self.enter_index = index
        self.volume = math.floor(account.cash * account.percent / (self.enter_price * 100)) * 100
        self.fee = self.enter_price * self.volume * account.enter_fee

        maxFNF_N = 70
        if index >= maxFNF_N:
            self.MFE = dataApi.hhv(index - maxFNF_N + 1, maxFNF_N, data_api.KDataType.High) / self.enter_price - 1
            self.MAE = 1 - dataApi.llv(index - maxFNF_N + 1, maxFNF_N, data_api.KDataType.Low) / self.enter_price

    def on_exit(self, dataApi, account, index):
        self.exit_date = dataApi.date(index)
        self.exit_price = dataApi.close(index)
        self.exit_index = index
        self.profit = (self.exit_price - self.enter_price) * self.volume
        self.fee += self.exit_price * self.volume * account.exit_fee

        account.on_exit(self)

