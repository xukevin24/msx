import configparser

ip = "127.0.0.1"
port = 3306
user = 'root'
passwd = '123456'

cp = configparser.SafeConfigParser()
cp.read('c:/db.conf')

ip = cp.get('db', 'ip')
passwd = cp.get('db', 'passwd')

#print(ip)
#print(passwd)