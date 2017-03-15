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
        self.positions = {}      # 持仓情况{'000001':[100, 15.34, 139, '2015-02-05', 15.99], '600000':[200,5.54,259,'2015-05-15',5.99]}
        self.enter_trades = {}   # 当日入场{'000001':[100, 15.34], '600000':[200, 5.54]}
        self.exit_trades = {}    # 当日出场{'000001':[100, 15.34,  0.145, -30000, '2015-02-05', 13.4], '600000':[200, 5.54, 盈亏比例，盈亏额, '2015-05-15', 5.30]}
        self.total_price = 0
        self.index_price = 0     # 对应指数价值

    #评估总价值
    def get_total_price(self, dataApiList, dataStr):
        self.total_price = self.cash
        for (code,position) in self.positions.items():
            dataApi = dataApiList[code]
            index = dataApi.get_index_of_date(dataStr)
            if index < 0:
                price = position[4]
            else:
                price = dataApi.close(index)
            position[4] = price
            self.total_price += position[0] * price
        return self.total_price
    
    def is_code_in(self, code):
        return code in self.positions.keys()

    def get_percent(self):
        return 1

    def on_exit(self, trade):
        pass

    def do_statistics(self, trade):
        pass

    def __repr__(self): 
        return repr((self.cash, self.enter_fee, self.exit_fee, self.current_date, self.positions, self.enter_trades, self.exit_trades)) 

    def from_json(self, jsonObj):
        pass

    def dump_emal(self):
        txt = 'buy:\n'
        for (code, info) in self.enter_trades.items():
            txt += '%s \t%d \t%0.2f\n' % (code, info[0], info[1])
        txt += 'sell:\n'
        for (code, info) in self.exit_trades.items():
            txt += '%s \t%d \t%0.2f\t%0.2f%0.0f\n' % (code, info[0], info[1], info[2], info[3])
        txt += 'position:\n'
        for (code, info) in self.positions.items():
            txt += '%s \t%d \t%0.2f\n' % (code, info[0], info[1])
        return txt

'''
def dict_to_object(d):
    class_name = d.pop('__class__')
    module_name = d.pop('__module__')
    module = __import__(module_name)

    #print("MODULE:%s"%module)

    class_ = getattr(module,class_name)

    #print("CLASS%s"%class)

    args = dict((key.encode('ascii'),value) for key,value in d.items())

    #print('INSTANCE ARGS:%s'%args)

    inst = class_(**args)
    return inst
'''     




        

