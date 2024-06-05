import http.client
import urllib.parse
import xml.etree.ElementTree as ET
from tkinter import*
from io import BytesIO
import urllib.request
from PIL import Image,ImageTk

import Googlemap

class Food_Finder_API:
    def __init__(self):
        self.api_key = '9011fc15298c4ac68dee0da375463fa2'
        self.server = "openapi.gg.go.kr"

    def get_taste_places(self, sigun_nm):
        # 요청 매개변수 설정
        params = {
            'KEY': self.api_key,
            'Type': 'xml',
            'pIndex': 1,
            'pSize': 5,
            'SIGUN_NM': sigun_nm
        }

        # 매개변수를 URL에 맞게 인코딩
        query_string = urllib.parse.urlencode(params)

        # 전체 URL 생성
        url = f"/PlaceThatDoATasteyFoodSt?{query_string}"

        # 연결 설정 및 API 요청 보내기
        conn = http.client.HTTPSConnection(self.server)
        conn.request("GET", url)

        # 응답 받기
        response = conn.getresponse()

        if response.status == 200:
            response_data = response.read()
            root = ET.fromstring(response_data)  # XML 파싱 후 root 정의

            places = []

            for row in root.findall('.//row'):
                SIGUN_NM = row.find('SIGUN_NM').text
                RESTRT_NM = row.find('RESTRT_NM').text
                TASTFDPLC_TELNO = row.find('TASTFDPLC_TELNO').text
                REPRSNT_FOOD_NM = row.find('REPRSNT_FOOD_NM').text
                REFINE_ZIP_CD = row.find('REFINE_ZIP_CD').text
                REFINE_ROADNM_ADDR = row.find('REFINE_ROADNM_ADDR').text
                REFINE_LOTNO_ADDR = row.find('REFINE_LOTNO_ADDR').text
                REFINE_WGS84_LAT = row.find('REFINE_WGS84_LAT').text
                REFINE_WGS84_LOGT = row.find('REFINE_WGS84_LOGT').text

                data = {
                    "SIGUN_NM": SIGUN_NM,  # 시군명
                    "RESTRT_NM": RESTRT_NM,  # 음식점 명
                    "TASTFDPLC_TELNO": TASTFDPLC_TELNO,  # 맛집 전화번호
                    "REPRSNT_FOOD_NM": REPRSNT_FOOD_NM,  # 대표 음식명
                    "REFINE_ZIP_CD": REFINE_ZIP_CD,  # 소재지 우편번호
                    "REFINE_ROADNM_ADDR": REFINE_ROADNM_ADDR,  # 소재지 도로명 주소
                    "REFINE_LOTNO_ADDR": REFINE_LOTNO_ADDR,  # 소재지 지번 주소
                    "REFINE_WGS84_LAT": REFINE_WGS84_LAT,  # 위도
                    "REFINE_WGS84_LOGT": REFINE_WGS84_LOGT  # 경도
                }
                places.append(data)

            # 연결 닫기
            conn.close()
            #print(places)
            return places

        else:
            conn.close()
            raise None

#
# api = TastePlaceAPI()
# datas = api.get_taste_places('성남시')
#
#
# window=Tk()
# window.geometry("500x500+500+200")
#
# img=Gmap_Test.print_map_by_xy(datas[0]['REFINE_WGS84_LAT'], datas[0]['REFINE_WGS84_LOGT'])
# image=ImageTk.PhotoImage(img)
#
# Label(window, image=image, height=400,width=400).pack()
#
# window.mainloop()
