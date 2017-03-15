import math
import sys
import webbrowser
import json
from config import db_config as db_config

def calc_voume(cash, price):
    return math.floor(cash / (price * 100)) * 100

def store2json(data, filename):
    with open(filename, 'w') as json_file:
        s = json.dumps(data, default=lambda data: data.__dict__, sort_keys=True, indent=4)
        json_file.write(json.dumps(data))

def openInWeb(url):
    #url = 'http://www.baidu.com'
    webbrowser.open(url)

def send_email(email_address, content):
    import smtplib  
    import email.mime.multipart  
    import email.mime.text  
    import email.mime.text
  
    me = db_config.email_user + '@' + db_config.email_postfix
    msg = email.mime.text.MIMEText(content, 'plain', 'utf-8') 
    msg['From'] = me
    msg['To'] = email_address 
    msg['Subject'] = email.header.Header('github update', 'utf-8')
    
    smtp = smtplib.SMTP(db_config.email_smtp)
    #smtp.connect(db_config.email_stmp)  
    smtp.login(db_config.email_user, db_config.email_passwd)  
    smtp.sendmail(me, email_address, msg.as_string())  
    smtp.quit()  
    print('email send success.')

if __name__ == "__main__":
    #path = db_config.config_path 
    #filename = 'data'
    #store2json([1], path + filename + '.json')
    #openInWeb(db_config.web_url + filename)
    send_email('xxxxxx@qq.com', '''
    You can view, comment on, or merge this pull request online at:

     https://github.com/ax614/msx/pull/2

    Commit Summary
    ''')
