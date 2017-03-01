import sys  
import os  
import json  
from ftplib import FTP
import config.db_config as db_config  

class Xfer:  
    _XFER_FILE = 0
    _XFER_DIR = 1
    
    def __init__(self):  
        self.ftp = None  
      
    def __del__(self):  
        pass  
      
    def init(self, ip, uname, pwd, port = 21, timeout = 60):          
        self.ip = ip  
        self.uname = uname  
        self.pwd = pwd  
        self.port = port  
        self.timeout = timeout  
      
        if self.ftp is None:  
            self.ftp = FTP()  
            print('### connect ftp server: %s ...'%self.ip)
            self.ftp.connect(self.ip, self.port, self.timeout)  
            self.ftp.login(self.uname, self.pwd)   
            print(self.ftp.getwelcome())
      
    def clear(self):  
        if self.ftp:  
            self.ftp.close()  
            print('### disconnect ftp server: %s!'%self.ip)
            self.ftp = None  
      
    def uploadDir(self, localdir='./', remotedir='./'):  
        if not os.path.isdir(localdir):    
            return  
        self.ftp.cwd(remotedir)   
        for file in os.listdir(localdir):  
            src = os.path.join(localdir, file)  
            if os.path.isfile(src):  
                self.uploadFile(src, file)  
            elif os.path.isdir(src):  
                try:    
                    self.ftp.mkd(file)    
                except:    
                    sys.stderr.write('the dir is exists %s'%file)  
                self.uploadDir(src, file)  
        self.ftp.cwd('..')  
      
    def uploadFile(self, localpath, remotepath):  
        if not os.path.isfile(localpath):    
            return  
        print('start upload %s to %s:%s'%(localpath, self.ip, remotepath))
        self.ftp.storbinary('STOR ' + '/home/uftp/res/' + remotepath, open(localpath, 'rb'))  
        print('upload finish..')
      
    def __filetype(self, src):  
        if os.path.isfile(src):  
            index = src.rfind('\\')  
            if index == -1:  
                index = src.rfind('/')                  
            return _XFER_FILE, src[index+1:]  
        elif os.path.isdir(src):  
            return _XFER_DIR, ''          
      
    def upload(self, src):  
        filetype, filename = self.__filetype(src)  
          
        self.initEnv()  
        if filetype == _XFER_DIR:  
            self.srcDir = src              
            self.uploadDir(self.srcDir)  
        elif filetype == _XFER_FILE:  
            self.uploadFile(src, filename)  
        self.clearEnv() 

def upload_file(loccalFile, remoteFile):
    xfer = Xfer()  
    xfer.init(db_config.ftp_ip, db_config.ftp_user, db_config.ftp_passwd)  
    xfer.uploadFile(loccalFile, remoteFile) 

if __name__ == "__main__":
    upload_file('util.py', 'test.txt')