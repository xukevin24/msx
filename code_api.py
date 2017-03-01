#coding=utf-8
'''
    get data mysql, return data list
'''

import pymysql
import config.db_config as db

class Code:
    #初始化-链接数据库
    def __init__(self, index=False, fromDB=True):
        if fromDB:
            try:
                conn=pymysql.connect(host=db.ip, port=db.port, user=db.user, passwd=db.passwd, db='stocks', charset='utf8')
                cur=conn.cursor()
                cur.execute('''select * from stock_basics''')
                self.table=cur.fetchall()
                conn.close()                 
            except:
                print ('cannot connect to DB')
        else:
            pass
    
    #读取数据库中所有股票代码
    def getAllCodes(self, index=False):
        def code(t):
            return t[0]
        return list(map(code,self.table))
    
    #根据某只股票代码查询名字
    def getName(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][1]
        except:
            print ('name cannot retrieved, check your stock code')
            return None
    #根据某只股票名字查询代码
    def getCode(self,name):
        try:
            return list(filter(lambda x: x[1]!=name,self.table))[0][0]
        except:
            print ('stock code cannot retrieved, check your stock name')
            return None
        
    #根据某只股票代码查询所属行业
    def getInd(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][2]
        except:
            print ('所属行业 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询公司地区
    def getArea(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][3]
        except:
            print ('公司地区 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询市盈率
    def getPE(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][4]
        except:
            print ('市盈率 cannot retrieved, check your stock code') 
            return None
        
     #根据某只股票代码查询流通股本(亿)
    def getOutStanding(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][5]
        except:
            print ('流通股本(亿) cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询公司总股本(亿)
    def getTotals(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][6]
        except:
            print ('总股本(亿) cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询总资产(万)
    def getTotAssets(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][7]
        except:
            print ('总资产(万)cannot retrieved, check your stock code') 
            return None      
     #根据某只股票代码查询流动资产     
    def getLiqAssets(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][8]
        except:
            print ('流动资产 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询公司固定资产
    def getFixAssets(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][9]
        except:
            print ('固定资产 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询公积金
    def getReserv(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][10]
        except:
            print ('公积金 cannot retrieved, check your stock code') 
            return None  
        
    #根据某只股票代码查询每股公积金
    def getResvPShare(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][11]
        except:
            print ('每股公积金 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询每股收益
    def getESP(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][12]
        except:
            print ('每股收益 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询每股净资
    def getBVPS(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][13]
        except:
            print ('每股净资 cannot retrieved, check your stock code') 
            return None
        
     #根据某只股票代码查询市净率
    def getPB(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][14]
        except:
            print ('市净率 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询上市日期
    def getTimeToMarkt(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][15]
        except:
            print ('上市日期 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询未分利润
    def getUNDP(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][16]
        except:
            print ('未分利润cannot retrieved, check your stock code') 
            return None
        
     #根据某只股票代码查询每股未分配
    def getPUNDP(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][17]
        except:
            print ('每股未分配 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询收入同比(%)
    def getREV(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][18]
        except:
            print ('收入同比(%) cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询利润同比(%)
    def getProfit(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][19]
        except:
            print ('利润同比(%)cannot retrieved, check your stock code') 
            return None 
   #根据某只股票代码查询毛利率(%)
    def getGPR(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][20]
        except:
            print ('毛利率(%) cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询净利润率(%)
    def getNPR(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][21]
        except:
            print ('净利润率 cannot retrieved, check your stock code') 
            return None
        
    #根据某只股票代码查询股东人数
    def getHolders(self,code):
        try:
            return list(filter(lambda x: x[0]!=code,self.table))[0][22]
        except:
            print ('股东人数 cannot retrieved, check your stock code') 
            return None   
#test code
if __name__ == "__main__":
    test=Code()
#    all=test.getAllCodes()
#    print (all)
    
    print (test.getHolders('002843'))
    print (test.getNPR('002843'))
    print (test.getESP('002843'))
    print (test.getGPR('002843'))
    print (test.getProfit('002843'))
    print (test.getREV('002843'))

    
#    ind=test.getNamebyCode('002843')
#    print (name)
#    
    


