from datetime import datetime, timedelta
import json
import pandas as pd

# 엑셀 파일 로드
data = pd.read_excel('location_grids.xlsx')


# 경도와 위도를 받아서 오차 범위 내에 있는 x, y 좌표를 반환하는 함수
def find_grid(longitude, latitude, tolerance=1):

    matched_grids = []

    # 오차 범위 내의 경도와 위도 범위 정의
    lon_min = longitude - tolerance
    lon_max = longitude + tolerance
    lat_min = latitude - tolerance
    lat_max = latitude + tolerance

    # 주어진 오차 범위 내에서 데이터를 필터링
    filtered_data = data[
        (data['경도(초/100)'] >= lon_min) & (data['경도(초/100)'] <= lon_max) &
        (data['위도(초/100)'] >= lat_min) & (data['위도(초/100)'] <= lat_max)
        ]

    # 매칭된 격자 좌표 추출
    for _, row in filtered_data.iterrows():
        matched_grids.append((row['x'], row['y']))

    return matched_grids


# API 관련 코드
api_key = 'kqMzwvJlxICdXrO0eXEHyXirL/huIAmVPWway9BnnQKyFdi4KSrxyyF71z60Cn5avZSEp7U3W5MBXfls1Z24BA=='
serviceKey = api_key  # 본인의 서비스 키 입력
base_date = '20240529'  # 발표 일자
base_time = '0700'  # 발표 시간
nx = '37'  # 예보 지점 x좌표
ny = '126'  # 예보 지점 y좌표

# 알고 싶은 시간
input_d = datetime.strptime(base_date + base_time, "%Y%m%d%H%M")
print(input_d)

# 실제 입력 시간
input_d = datetime.strptime(base_date + base_time, "%Y%m%d%H%M") - timedelta(hours=1)
print(input_d)

input_datetime = datetime.strftime(input_d, "%Y%m%d%H%M")
input_date = input_datetime[:-4]
input_time = input_datetime[-4:]

# url
url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={serviceKey}&numOfRows=60&pageNo=1&dataType=json&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"


# url로 API return값 요청
import requests

response = requests.get(url, verify=False)
res = json.loads(response.text)

informations = dict()
for items in res['response']['body']['items']['item']:
    cate = items['category']
    fcstTime = items['fcstTime']
    fcstValue = items['fcstValue']
    temp = dict()
    temp[cate] = fcstValue

    if fcstTime not in informations.keys():
        informations[fcstTime] = dict()
    informations[fcstTime][cate] = fcstValue

print(informations)

deg_code = {0: 'N', 360: 'N', 180: 'S', 270: 'W', 90: 'E', 22.5: 'NNE',
            45: 'NE', 67.5: 'ENE', 112.5: 'ESE', 135: 'SE', 157.5: 'SSE',
            202.5: 'SSW', 225: 'SW', 247.5: 'WSW', 292.5: 'WNW', 315: 'NW',
            337.5: 'NNW'}


def deg_to_dir(deg):
    close_dir = ''
    min_abs = 360
    if deg not in deg_code.keys():
        for key in deg_code.keys():
            if abs(key - deg) < min_abs:
                min_abs = abs(key - deg)
                close_dir = deg_code[key]
    else:
        close_dir = deg_code[deg]
    return close_dir


deg_to_dir(0)

pyt_code = {0: '강수 없음', 1: '비', 2: '비/눈', 3: '눈', 5: '빗방울', 6: '진눈깨비', 7: '눈날림'}
sky_code = {1: '맑음', 3: '구름많음', 4: '흐림'}

for key, val in zip(informations.keys(), informations.values()):

    template = f"""{base_date[:4]}년 {base_date[4:6]}월 {base_date[-2:]}일 {key[:2]}시 {key[2:]}분 {(int(nx), int(ny))} 지역의 날씨는 """

    # 맑음(1), 구름많음(3), 흐림(4)
    if val['SKY']:
        sky_temp = sky_code[int(val['SKY'])]
        template += sky_temp + " "

    # (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
    if val['PTY']:
        pty_temp = pyt_code[int(val['PTY'])]
        template += pty_temp
        # 강수 있는 경우
        if val['RN1'] != '강수없음':
            # RN1 1시간 강수량
            rn1_temp = val['RN1']
            template += f"시간당 {rn1_temp}mm "

    # 기온
    if val['T1H']:
        t1h_temp = float(val['T1H'])
        #         print(f"기온 : {t1h_temp}℃")
        template += f" 기온 {t1h_temp}℃ "

    # 습도
    if val['REH']:
        reh_temp = float(val['REH'])
        #         print(f"습도 : {reh_temp}%")
        template += f"습도 {reh_temp}% "

    # 풍향/ 풍속
    if val['VEC'] and val['WSD']:
        vec_temp = deg_to_dir(float(val['VEC']))
        wsd_temp = val['WSD']

    template += f"풍속 {vec_temp} 방향 {wsd_temp}m/s"
    print(template)

# 경도와 위도를 입력 받아서 오차 범위 내에 있는 격자 좌표 출력
longitude = 126868  # 예시 경도 값 (초/100)
latitude = 37475  # 예시 위도 값 (초/100)
tolerance = 1  # 오차 범위

matched_coordinates = find_grid(longitude, latitude, tolerance)
print(f"오차 범위 {tolerance} 내에서 매칭된 좌표: {matched_coordinates}")
