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
        self.positions = {}      # {'000001':[100, 15.34, 139, '2015-02-05', 15.99], '600000':[200,5.54,259,'2015-05-15',5.99]}
        self.enter_trades = {}           # {'000001':[100, 15.34], '600000':[200,5.54]}
        self.exit_trades = {}            # {'000001':[100, 15.34], '600000':[200,5.54]}
        self.statistics = simu_stat.statistics()

    #评估总价值
    def get_total_price(self, dataApiList):
        cash = self.cash
        for (code,position) in self.positions.items():
            dataApi = dataApiList[code]
            index = dataApi.get_index_of_date(position[3])
            if index < 0:
                price = position[4]
            else:
                price = dataApi.close(index)
            cash += position[0] * price
            position[4] = price
        return cash
    
    def is_code_in(self, code):
        return code in self.positions.keys()

    def get_percent(self):
        return 1

    def on_exit(self, trade):
        pass

    def do_statistics(self, trade):
        pass


        




        

