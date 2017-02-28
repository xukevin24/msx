import configparser

cp = configparser.SafeConfigParser()
cp.read('c:/db.conf')

#mysqldb
ip = cp.get('db', 'ip')
port = int(cp.get('db', 'port'))
user = cp.get('db', 'user')
passwd = cp.get('db', 'passwd')

#ftp
ftp_ip = cp.get('ftp', 'ip')
ftp_user = cp.get('ftp', 'user')
ftp_passwd = cp.get('ftp', 'passwd')

#web
web_url = cp.get('web', 'url')
#print(ip)
#print(passwd)