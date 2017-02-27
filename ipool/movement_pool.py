import heapq
import ipool.ipool as ipool
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import data_api 

class StockPool(ipool.IStockPool):
    #num持有数目
    def __init__(self, num):
        self.num = num
        pass

    def get_num(self):
        return self.num

    #返回日期date，满足条件的前N个
    def select(self, dataApiList, date, num):
        sortList = []
        for dataApi in dataApiList:
            #dataApiList应该都是能取到index的
            index = dataApi.get_index_of_date(date)
            close = dataApi.close(index)
            tmp = {}
            if index + 20 >= dataApi.length():
                continue
            else:
                tmp['key'] = (dataApi.close(index) - dataApi.close(index + 20))/dataApi.close(index + 20)
            tmp['data'] = dataApi
            sortList.append(tmp)
        resultList = heapq.nlargest(num, sortList, key=lambda s: s['key'])
        return resultList

