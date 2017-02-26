#coding=utf-8
'''
    账号信息
'''

import config.config as config
import trade as Trade
import simu_stat

#当天结束时账号状况
class MarketDayStat():
    def __init__(self):
        self.cash = 0
        self.enter_fee = 0
        self.exit_fee = 0
        self.current_date = ''
        self.positions = {}      # {'000001':[100, 15.34], '600000':[200,5.54]}
        self.enter_trades = {}           # {'000001':[100, 15.34], '600000':[200,5.54]}
        self.exit_trades = {}            # {'000001':[100, 15.34], '600000':[200,5.54]}
        self.statistics = simu_stat.statistics()

    def on_exit(self, trade):
        pass

    def do_statistics(self, trade):
        pass

        




        

