'''
    池子接口类，其他的实现对应的接口
'''

class IStockPool:
    #返回日期date，满足条件的前N个
    def select(self, dataApiList, date, N):
        return False
