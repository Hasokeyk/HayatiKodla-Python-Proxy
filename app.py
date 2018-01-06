#  -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import abort
import urllib
import requests
import re
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
#from bs4 import BeautifulSoup

app = Flask(__name__)

def is_http_url(s):
    try:
        url = urlparse(s.strip())
        if url.scheme and url.path:
            return True
        else:
            return False
    except Exception as Hata:
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
                    return "501 Sitede bağlantı sorunu var. Status Code : "+text.status_code
            except Exception as hata:
                return "500 Siteye Bağlanamadı. Linki kontrol edin."
        else:
            return "502 Domain Geçerli Değil ÖRN. https://www.hayatikodla.net olarak gönderin."
    else:
        return "503 Domain Parametresi Bulunamadı"

if __name__ == "__main__":
    app.run()