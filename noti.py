#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

key = 'sea100UMmw23Xycs33F1EQnumONR%2F9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw%3D%3D'
TOKEN = '7486427871:AAHANOAhNoBGZtvt7X0i9lWbemzpO997o8s'
MAX_MSG_LENGTH = 300
baseurl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade?ServiceKey='+key
bot = telepot.Bot(TOKEN)

def getData():
    res_list = []
    # url = baseurl+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
    url = "http://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2?searchWrd=%EA%B4%91%EA%B5%90%EC%82%B0&pageNo=1&numOfRows=5&ServiceKey=kqMzwvJlxICdXrO0eXEHyXirL%2FhuIAmVPWway9BnnQKyFdi4KSrxyyF71z60Cn5avZSEp7U3W5MBXfls1Z24BA%3D%3D"
    # print(url)
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('|')
        try:
            row = parsed[6] + ', ' + parsed[0] + ', ' + parsed[1] + '\t' + parsed[2] + ', ' + parsed[3] + ', ' + parsed[4].strip() + '\n'
            # row = parsed[6] + ', ' + parsed[14] + ' ' + parsed[9] + ' ' + parsed[10] + ' ' + parsed[5] + '동, ' + parsed[13] + 'm², ' + parsed[17] + 'F, ' + parsed[1].strip() + '만원\n'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        # print(user, date_param, param)
        res_list = getData()
        print(res_list)
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run()