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

if __name__ == "__main__":
    path = 'C:/' 
    filename = 'data'
    store2json([1], path + filename + '.json')
    openInWeb(db_config.web_url + filename)
