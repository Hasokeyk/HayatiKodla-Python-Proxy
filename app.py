﻿#  -*- coding: utf-8 -*-

#Kütüphanaler
from flask import Flask
from flask import request
from flask import abort
import urllib
import requests
import re
from fake_useragent import UserAgent
#from selenium import webdriver
import sys
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
#from bs4 import BeautifulSoup
#Kütüphanaler

#Değişkenler
domain = None
mobil  = None
ua = UserAgent(verify_ssl=False)
#Değişkenler

app = Flask(__name__)

def is_http_url(s):
    try:
        url = urlparse(s.strip())
        if url.scheme and url.netloc:
            return True
        else:
            return False
    except Exception as Hata:
        return False

@app.route('/debug', methods=['GET','POST'])
def debug():
    return 'V1.2.2'
    
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            if request.form['domain'] is not None:
                domain = request.form['domain']
            else:
                domain = None
        except:
            return '503 Domain Parametresi Bulunamadı'
        try:
            if request.form['mobil'] is not None:   
                type = request.form['mobil']
            else:
                type = None
        except:
            type = None 
    else:
        try:
            if request.args.get('domain') is not None:
                domain = request.args.get('domain')
            else:
                domain = None
        except:
            return '503 Domain Parametresi Bulunamadı'
        try:
            if request.args.get('mobil') is not None:   
                type = request.args.get('mobil')
            else:
                type = None
        except:
            type = None

    if type is not None and type == 'true':
        userAgent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
    else:
        #userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        userAgent = ua.random
    
    if domain is not None:
        if is_http_url(domain):
            try:
                r = requests.get(domain,headers={'User-agent':userAgent})
                if r.status_code == 200:
                    return str(r.text)
                else:
                    return "501 Sitede bağlantı sorunu var. Status Code : "+str(r.status_code)
            except ValueError as hata:
                print(hata)
                return "500 Siteye Bağlanamadı. Linki kontrol edin."
        else:
            return "502 Domain Geçerli Değil ÖRN. https://www.hayatikodla.net olarak gönderin."
    else:
        return "503 Domain Parametresi Bulunamadı"

if __name__ == "__main__":
    app.run()