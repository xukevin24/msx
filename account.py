#coding=utf-8
'''
    账号信息
'''

import config.config as config
import trade as Trade
import simu_stat

class Account():
    def __init__(self):
        self.init_cash = config.config.cash
        self.enter_fee = config.config.enter_fee
        self.exit_fee = config.config.exit_fee
        self.percent = config.config.percent
        self.trades = []

        self.cash = self.init_cash
        self.k_num = 0
        self.statistics = simu_stat.statistics()

    def on_exit(self, trade):
        self.cash -= trade.fee
        self.cash += trade.profit
        self.trades.append(trade)

        self.do_statistics(trade)

    def do_statistics(self, trade):
        s = self.statistics
        s.initCash = self.init_cash
        s.k_num = self.k_num
        s.cash = self.cash
        s.profit += trade.profit
        s.fee += trade.fee
        s.totalMFE += trade.MFE
        s.totalMAE += trade.MAE

        if trade.profit > 0:
            s.success += 1
            s.totalProfit += trade.profit
        else:
            s.fail += 1
            s.totalLoss += trade.profit
        s.num += 1

        s.calc_everage()

        




        

