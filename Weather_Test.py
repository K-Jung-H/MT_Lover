import time
from datetime import datetime, timedelta
import json
import pandas as pd
import requests


def get_weather_data(nx, ny):
    nx, ny = int(nx), int(ny)
    # 현재 시간 가져오기
    now = datetime.now()
    print(f"현재 시간: {now}")

    # 현재 시간을 정각으로 맞춤 (분과 초를 0으로 설정)
    now = now.replace(minute=0, second=0, microsecond=0)
    print(f"정각으로 맞춘 현재 시간: {now}")

    # now = "2024-06-03 22:00:00"

    start = time.time()
    # 엑셀 파일 로드
    data = pd.read_excel('location_grids.xlsx')
    print("read excel time :", time.time() - start)


    # 경도와 위도를 받아서 오차 범위 내에 있는 x, y 좌표를 반환하는 함수
    def find_grid(longitude, latitude, tolerance=1):
        matched_grids = []
        lon_min = longitude - tolerance
        lon_max = longitude + tolerance
        lat_min = latitude - tolerance
        lat_max = latitude + tolerance
        filtered_data = data[
            (data['경도(초/100)'] >= lon_min) & (data['경도(초/100)'] <= lon_max) &
            (data['위도(초/100)'] >= lat_min) & (data['위도(초/100)'] <= lat_max)
            ]
        for _, row in filtered_data.iterrows():
            matched_grids.append((row['x'], row['y']))
        return matched_grids


    # 현재 시간을 기준으로 base_date와 base_time 설정
    base_date = now.strftime("%Y%m%d")
    base_time = (now - timedelta(hours=1)).strftime("%H00")  # 현재 시간 기준으로 1시간 전

    # API 관련 코드
    api_key = 'kqMzwvJlxICdXrO0eXEHyXirL/huIAmVPWway9BnnQKyFdi4KSrxyyF71z60Cn5avZSEp7U3W5MBXfls1Z24BA=='
    serviceKey = api_key
    # nx = '37'  # 예보 지점 x좌표
    # ny = '126'  # 예보 지점 y좌표

    # url
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={serviceKey}&numOfRows=60&pageNo=1&dataType=json&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"


    # url로 API return값 요청
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"API 요청 실패, 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        exit()

    res = json.loads(response.text)
    if res['response']['header']['resultCode'] != '00':
        print(f"API 응답 오류, 결과 코드: {res['response']['header']['resultCode']}")
        print(f"결과 메시지: {res['response']['header']['resultMsg']}")
        exit()

    informations = dict()
    for items in res['response']['body']['items']['item']:
        cate = items['category']
        fcstTime = items['fcstTime']
        fcstValue = items['fcstValue']
        if fcstTime not in informations.keys():
            informations[fcstTime] = dict()
        informations[fcstTime][cate] = fcstValue

    # 현재 시각의 정각 + 1시간 정보만 출력
    next_hour_str = (now + timedelta(hours=1)).strftime("%H00")

    r_data = []

    if next_hour_str in informations:
        val = informations[next_hour_str]
        template = f"""{base_date[:4]}년 {base_date[4:6]}월 {base_date[-2:]}일 {next_hour_str[:2]}시 {next_hour_str[2:]}분 {(int(nx), int(ny))} 지역의 날씨는 """

        # 맑음(1), 구름많음(3), 흐림(4)
        if 'SKY' in val:
            sky_code = {1: '맑음', 3: '구름많음', 4: '흐림'}
            sky_temp = sky_code[int(val['SKY'])]
            template += sky_temp + " "
            r_data.append(str(sky_temp))
        # (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
        if 'PTY' in val:
            pty_code = {0: '강수 없음', 1: '비', 2: '비/눈', 3: '눈', 5: '빗방울', 6: '진눈깨비', 7: '눈날림'}
            pty_temp = pty_code[int(val['PTY'])]
            template += pty_temp
            r_data.append(str(pty_temp))
            # 강수 있는 경우
            if 'RN1' in val and val['RN1'] != '강수없음':
                # RN1 1시간 강수량
                rn1_temp = val['RN1']
                # template += f" 시간당 {rn1_temp}mm "

        # 기온
        if 'T1H' in val:
            t1h_temp = float(val['T1H'])
            template += f" 기온 {t1h_temp}℃ "
            r_data.append(str(t1h_temp))

        # 습도
        if 'REH' in val:
            reh_temp = float(val['REH'])
            template += f"습도 {reh_temp}% "
            r_data.append(str(reh_temp))

        # 풍향/풍속
        if 'VEC' in val and 'WSD' in val:
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


            vec_temp = deg_to_dir(float(val['VEC']))
            wsd_temp = val['WSD']
            template += f"풍속 {vec_temp} 방향 {wsd_temp}m/s"

        print(template)
    else:
        print(f"현재 시간의 정각 + 1시간({next_hour_str})에 대한 정보가 없습니다.")

    # 경도와 위도를 입력 받아서 오차 범위 내에 있는 격자 좌표 출력
    longitude = 126868  # 예시 경도 값 (초/100)
    latitude = 37475  # 예시 위도 값 (초/100)
    tolerance = 0.1  # 오차 범위

    matched_coordinates = find_grid(longitude, latitude, tolerance)
    print(f"오차 범위 {tolerance} 내에서 매칭된 좌표: {matched_coordinates}")

    r_data.append(str(now))

    return r_data