'''
    池子接口类，其他的实现对应的接口
'''

class IStockPool:
    def __init__(self):
        pass

    #返回日期date，满足条件的前N个
    def select(self, dataApiList, date, N):
        N = min(len(dataApiList), N)
        if N == 0:
            return []
        else:
            return dataApiList[:N]
