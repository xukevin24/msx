'''
    池子接口类，其他的实现对应的接口
'''

class IStockPool:
    #num持有数目
    def __init__(self, num):
        self.num = N
        pass

    def get_num(self):
        return self.num

    #返回日期date，满足条件的前N个
    def select(self, dataApiList, date, num):
        N = min(len(dataApiList), num)
        if N == 0:
            return []
        else:
            return dataApiList[:N]
