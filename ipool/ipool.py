'''
    池子接口类，其他的实现对应的接口
'''

class IStockPool:
    #num持有数目
    def __init__(self, num, N1):
        self.num = num
        self.N1 = N1
        pass

    def get_num(self):
        return self.num
    
    def min_start(self):
        return self.N1 + 1

    def is_skip(self, dataApi, index):
        if index >= dataApi.length() - self.min_start():
            return True  
        return False

    #返回日期date，满足条件的前N个
    def select(self, dataApiList, date):
        N = min(len(dataApiList), self.num)
        if N == 0:
            return []
        else:
            return dataApiList[:N]

    def select_out(self, dataApiList, enterInfoList, date):
        return self.select(dataApiList, date)

