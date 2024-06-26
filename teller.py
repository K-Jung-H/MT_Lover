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

import noti
import xml_read


def replyAptData(date_param, user, loc_param='11710'):
    print(user, date_param, loc_param)
    res_list = noti.getData()
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    mountain_data = xml_read.MT_data_read(text)

    if mountain_data != -1:
        if mountain_data is not None:
            info_text = str()
            info_text += "=====" + text + "에 존재하는 산 목록=====\n"
            for mt_name in mountain_data["mntn_info"]:
                info_text += mt_name + " "
            info_text += "\n"
            noti.sendMessage(chat_id, info_text)
    else:
        data = xml_read.MT_deap_data(text)
        if data != -1:
            info_text = str()
            print(text,"의 data",data)
            if data == -2 or data is None:
                info_text += "산 정보 없음" + '\n'
            elif data and "MT_ADMIN_NUM" in data:
                info_text += "산 이름 : " + data["MT_NAME"] + '\n'
                info_text += "산 코드 : " + data["MT_CODE"] + '\n'
                info_text += "산 위치 : " + data["MT_LOCATION"] + '\n'
                info_text += "산 높이 : " + data["MT_HIGH"] + '\n'
                info_text += "산 관리 주체 : " + data["MT_ADMIN"] + '\n'
                info_text += "산 관리 주체 연락처 : " + data["MT_ADMIN_NUM"] + '\n'
            noti.sendMessage(chat_id, info_text)
        else:
            noti.sendMessage(chat_id, '모르는 명령어입니다.\n지역명을 입력하세요.')
    # if text.startswith('거래') and len(args)>1:
    #     print('try to 거래', args[1])
    #     replyAptData(args[1], chat_id, args[2])
    # elif text.startswith('지역') and len(args)>1:
    #     print('try to 지역', args[1])
    #     replyAptData( '201705', chat_id, args[1] )
    # elif text.startswith('저장')  and len(args)>1:
    #     print('try to 저장', args[1])
    #     save( chat_id, args[1] )
    # elif text.startswith('확인'):
    #     print('try to 확인')
    #     check( chat_id )
    # elif text.startswith('테스트'):
    #     replyAptData('201705', chat_id)
    # else:
    #     # noti.sendMessage(chat_id, '모르는 명령어입니다.\n지역 [지역번호], 저장 [지역번호], 확인 중 하나의 명령을 입력하세요.')
    #     noti.sendMessage(chat_id, 'ㅗㅗㅗㅗ')

def run():
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', noti.TOKEN )

    bot = telepot.Bot(noti.TOKEN)
    pprint( bot.getMe() )

    bot.message_loop(handle)

    print('Listening...')

    # while 1:
    #   time.sleep(10)