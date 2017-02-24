import math

class statistics:
    def __init__(self):
        self.initCash = 0
        self.cash = 0
        self.profit = 0
        self.profitRatio = 0
        self.totalProfit = 0
        self.totalLoss = 0
        self.fee = 0
        self.success = 0
        self.fail = 0
        self.maxContinusSucc = 0
        self.maxContinusFail = 0
        self.num = 0
        self.succRatio = 0
        self.ev = 0
        self.averageProfit = 0
        self.averageLoss = 0
        #self.dynamic = []
        self.accountNum = 1
        self.profitRatio_single = 0
        self.profitRatio_compound = 0
        self.k_num = 0

        self.totalMFE = 0
        self.totalMAE = 0
        self.mfeToMae = 0

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