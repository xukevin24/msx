import configparser

ip = "120.0.0.0"
port = 3306
user = 'root'
passwd = 'xyz'

cp = configparser.SafeConfigParser()
cp.read('c:/db.conf')

ip = cp.get('db', 'ip')
passwd = cp.get('db', 'passwd')

#print(ip)
#print(passwd)