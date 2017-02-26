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
from strategy import bband_strategy as bband_strategy
from strategy import smacross_strategy as smacross_strategy

#
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
    datas.init_data('300017')

#    s = donchain_strategy.DonchainStrategy(50, 20)
    #s = random_strategy.RandomStrategy()
#    s=bband_strategy.BBandStrategy(20)
    s=smacross_strategy.SMACrossStrategy(5,20)

    account = simulate(datas, s, Trade.Trade)

    print('初始资金:%0.2f' % (account.init_cash))
    print('最终资金:%0.2f' % (account.cash))
    print('胜率:%0.2f' % (account.statistics.succRatio))
    print('盈利比率:%0.2f' % (account.statistics.profitRatio))
    print('年单利:%0.2f' % (account.statistics.profitRatio_single))
    print('年复利:%0.2f' % (account.statistics.profitRatio_compound))