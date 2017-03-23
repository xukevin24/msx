#coding=utf-8
'''
    横盘突破
'''
import sys
import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 

class Strategy(istrategy.IStrategy):
    def __init__(self, N, M, L):
        self.N = N
        self.M = M
        self.L = L

    #返回最小开始索引，程序需要的最少K线数
    def min_start(self):
        return self.N+100
   
    def is_entry(self, dataApi, index):
        o_max = dataApi.hhv(index+1,self.N, data_api.KDataType.Open)
        c_max = dataApi.hhv(index+1,self.N, data_api.KDataType.Close)
        oc_max = max(o_max, c_max)
        percent_N = (oc_max /  min(o_max, c_max) - 1)*100
        percent_R = (dataApi.close(index) / dataApi.close(index+1) - 1)*100

        term_R_O = dataApi.open(index) < oc_max
        term_R_C = dataApi.close(index) >= oc_max
        term_R_M = dataApi.close(index+1) <= dataApi.ma((index+1),5) and dataApi.close(index)>dataApi.ma((index),5)
        if percent_N<=self.M and percent_R>=self.L and term_R_O and term_R_C and term_R_M and dataApi.ma((index),5)>dataApi.ma((index),60) :
            return True 
        else:
            return False

    def is_exit(self, dataApi, index, enterInfo):
        if dataApi.ma((index+1),60) < dataApi.ma((index+1),5) and dataApi.ma((index+1),60) < dataApi.ma((index+1),5):
            return True     
        else:
            return False
    
    