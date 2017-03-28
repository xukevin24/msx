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
    
    #读取code那一行数据
    def getDataSet(self, code):
        return list(filter(lambda x: x[0]==code,self.table))[0]
    
    # 最后一个参数可以选择查询返回参数： 'code','name','industry','area','pe','outstanding','totals','totalAssets','liquidAssets','fixedAssets','reserved','reservedPerShare','esp','bvps','pb','timeToMarket','undp','perundp','rev','profit','gpr','npr','holders'
    def get(self, code, para):
        schema=['code','name','industry','area','pe','outstanding','totals','totalAssets','liquidAssets','fixedAssets','reserved','reservedPerShare','esp','bvps','pb','timeToMarket','undp','perundp','rev','profit','gpr','npr','holders']
        try:
            for i, item in enumerate(schema):
                if para==item:
                    dataset=self.getDataSet(code)
                    return dataset[i]
                else:
                    continue
        except:
            print ('cannot retrive ',para, 'for stock ', code, ', Check your Code!')
    
    #根据某只股票名字查询代码
    def getCode(self,name):
        try:
            return list(filter(lambda x: x[1]==name,self.table))[0][0]
        except:
            print ('stock code cannot retrieved, check your stock name')
            return None

#test code
if __name__ == "__main__":
    test=Code()
#    all=test.getAllCodes()
#    print (all)
    print (test.get('002843','name'))
    print (test.get('002843','area'))
    print (test.get('002843','pe'))
    print (test.get('002843','reserved'))
    


