import heapq
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import ipool.ipool as ipool
import data_api 

class StockPool(ipool.IStockPool):
    #num持有数目
    def __init__(self, num, asc):
        self.num = num
        self.asc = asc
        pass

    def get_num(self):
        return self.num

    #返回日期date，满足条件的前N个
    def select(self, dataApiList, date):
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

        if self.asc:
            resultList = heapq.nsmallest(self.num, sortList, key=lambda s: s['key'])
        else:
            resultList = heapq.nlargest(self.num, sortList, key=lambda s: s['key'])
        return resultList

