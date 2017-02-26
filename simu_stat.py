import math

class statistics:
    def __init__(self):
        self.initCash = 0     #最初资金
        self.cash = 0         #最终资金
        self.profit = 0       #利润
        self.profitRatio = 0  #总收益率
        self.totalProfit = 0  #盈利总额
        self.totalLoss = 0    #亏损总额
        self.fee = 0          #总费用
        self.success = 0      #总成功次数
        self.fail = 0         #总失败此时
        self.maxContinusSucc = 0    #最大连续盈利次数
        self.maxContinusFail = 0    #最大连续失败次数
        self.num = 0          #总交易次数
        self.succRatio = 0    #胜率
        self.ev = 0           #平均每笔交易盈亏比率
        self.averageProfit = 0  #盈利平均每笔利润
        self.averageLoss = 0    #亏损平均每笔亏损
        #self.dynamic = []      #暂时不用
        self.accountNum = 1     #不用
        self.profitRatio_single = 0     #年化利润（单利）
        self.profitRatio_compound = 0   #年化利润（复利）
        self.k_num = 0                  #k线数量

        self.totalMFE = 0       #开仓70日平均最大有利偏移
        self.totalMAE = 0       #开仓70日平均最大不利偏移
        self.mfeToMae = 0       #开仓70日平均最大有利偏移 / 开仓70日平均最大不利偏移

    def calc_everage(self):
        if self.num > 0:
            self.succRatio = self.success / self.num
            self.ev = self.profit / self.num
            self.averageProfit = self.totalProfit / self.num
            self.averageLoss = self.totalLoss / self.num
            self.profitRatio = self.profit / self.initCash
            self.profitRatio_single = self.profitRatio / (self.k_num/250)
            self.profitRatio_compound = math.pow(1 + self.profitRatio, 250/self.k_num) - 1
            if self.totalMAE != 0:
                self.mfeToMae = self.totalMFE / self.totalMAE

    def acc(self, other):
        self.cash = other.cash
        self.initCash += other.initCash
        self.profit += other.profit
        self.fee += other.fee
        self.success += other.success
        self.totalProfit += other.totalProfit
        self.fail += other.fail
        self.num += other.num
        self.k_num += other.k_num
        self.totalMFE += other.totalMFE
        self.totalMAE += other.totalMAE

        self.calc_everage()
        self.accountNum += 1