import configparser

config_path = 'c:/'
cp = configparser.SafeConfigParser()
cp.read(config_path + 'db.conf')

#mysqldb
ip = cp.get('db', 'ip')
port = int(cp.get('db', 'port'))
user = cp.get('db', 'user')
passwd = cp.get('db', 'passwd')

#mysqldb
stg_ip = cp.get('db_strategy', 'ip')
stg_port = int(cp.get('db_strategy', 'port'))
stg_user = cp.get('db_strategy', 'user')
stg_passwd = cp.get('db_strategy', 'passwd')

#ftp
ftp_ip = cp.get('ftp', 'ip')
ftp_user = cp.get('ftp', 'user')
ftp_passwd = cp.get('ftp', 'passwd')

#web
web_url = cp.get('web', 'url')
#print(ip)
#print(passwd)