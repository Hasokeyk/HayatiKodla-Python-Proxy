#  -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import abort
import urllib
import requests
import re
#from bs4 import BeautifulSoup

app = Flask(__name__)

def is_http_url(s):
    
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if re.match(regex,s):
        return True
    else:
        return False

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        domain = request.form['domain']
    else:
        domain = request.args.get('domain')
        
    if domain is not None:
        if is_http_url(domain):
            try:
                text = requests.get(domain)
                if text.status_code == 200:
                    return text.text
                else:
                    return "501 Sitede bağlantı sorunu var"
            except:
                return "500 Siteye Bağlanamadı. Linki kontrol edin"
        else:
            return '502 Domain Geçerli Değil ÖRN. https://www.hayatikodla.net olarak gönderin'
    else:
        return "503 Domain Parametresi Bulunamadı"

if __name__ == "__main__":
    app.run()