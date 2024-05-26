import http.client
import urllib.parse
import xml.etree.ElementTree as ET

# API 키
api_key = 'b109a81aed5742bab617df81af4feb9e'  # 여기에 발급받은 API 키를 넣으세요

# 서버 정보
server = "openapi.gg.go.kr"

# 요청 매개변수 설정
params = {
    'KEY': api_key,
    'Type': 'xml',   # XML 형식으로 데이터 요청
    'pIndex': 1,     # 페이지 번호
    'pSize': 100,    # 페이지 당 요청 숫자
    'SIGUN_NM': '안산시'  # 선택적으로 시군명 입력
}

# 매개변수를 URL에 맞게 인코딩
query_string = urllib.parse.urlencode(params)

# 전체 URL 생성
url = f"/FrtStret?{query_string}"

# 연결 설정 및 API 요청 보내기
conn = http.client.HTTPSConnection(server)
conn.request("GET", url)

# 응답 받기
response = conn.getresponse()
print(response.status)
if response.status == 200:
    response_data = response.read()
    root = ET.fromstring(response_data)  # XML 파싱 후 root 정의
    place_direction = root.find('.//REGION_DIV_NM').text
    mntn_info = root.find('.//MNTN_INFO').text.split(', ')  # MNTN_INFO 요소의 내용을 리스트로 분할하여 mntn_info에 저장
    local_MT_num = int(root.find('.//MNTN_CNT').text)  # MNTN_CNT 요소의 내용을 정수형으로 변환하여 저장
    print("지역의 위치: 경기도 " + place_direction)
    print("산의 개수:", local_MT_num)  # 결과 출력
    print("산의 종류:", mntn_info)  # 결과 출력

else:
    print("OpenAPI 요청이 실패했습니다! 다시 시도해주세요.")

# 연결 닫기
conn.close()
