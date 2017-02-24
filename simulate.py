#coding=utf-8
'''
    simulate
'''

import data_api
import config.config as config
import account as Account

from trade import trade as Trade

from strategy import istrategy as istrategy
from strategy import random_strategy as random_strategy
from strategy import donchain_strategy as donchain_strategy

def simulate(dataApi, strategy, tradeClass):
    account = Account.Account()
    trade = None
    length = dataApi.length()
    account.k_num = length
    start_idx = strategy.min_start()

    for index in range(length - start_idx, -1, -1):
        if strategy.is_skip(dataApi, index, trade):
            continue

        isTodayStart = False
        if trade == None:
            if account.cash > 0 and strategy.is_entry(dataApi, index):
                trade = tradeClass()
                trade.on_enter(dataApi, account, index)

                if trade.volume < 100:
                    trade = None
                else:
                    isTodayStart = True

        if isTodayStart and index != 0:
            continue

        if trade != None:
            if strategy.is_exit(dataApi, index, trade) or index == 0:
                trade.on_exit(dataApi, account, index)
                trade = None
    return account


#test code
if __name__ == "__main__":
    datas = data_api.KData()
    datas.init_data('601558')

    s = donchain_strategy.DonchainStrategy(50, 20)
    #s = random_strategy.RandomStrategy()
    
    r = simulate(datas, s, Trade.Trade)

    print(r.cash)