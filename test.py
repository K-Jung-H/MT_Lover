import requests
import xml.etree.ElementTree as ET

# API 키
api_key = 'kqMzwvJlxICdXrO0eXEHyXirL%2FhuIAmVPWway9BnnQKyFdi4KSrxyyF71z60Cn5avZSEp7U3W5MBXfls1Z24BA%3D%3D'

# 요청 매개변수 설정
params = {
    'searchWrd': '북한산',
    'pageNo': '1',
    'numOfRows': '5',
    'ServiceKey': api_key
}

# API 요청 보내기 (보안 검사 비활성화)
response = requests.get("https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2", params=params, verify=False)

# 응답 받기
print(response.status_code)
if response.status_code == 200:
    root = ET.fromstring(response.content)  # XML 파싱 후 root 정의

    MT_NAME = root.find('.//mntiname').text
    MT_CODE = int(root.find('.//mntilistno').text)
    MT_LOCATION = root.find('.//mntiadd').text
    MT_HIGH = int(root.find('.//mntihigh').text)
    MT_ADMIN = root.find('.//mntiadmin').text
    MT_ADMIN_NUM = root.find('.//mntiadminnum').text
    MT_TOP_100_REASON = root.find('.//mntitop').text
    MT_INFO = root.find('.//mntisummary').text

    print("산 이름:", MT_NAME)
    print("산 코드:", MT_CODE)
    print("산 위치:", MT_LOCATION)
    print("산 높이:", MT_HIGH)
    print("산 관리주체:", MT_ADMIN)
    print("산 관리주체 연락처:", MT_ADMIN_NUM)
    print("산 100대 명산 선정 이유:", MT_TOP_100_REASON)
    print("산 정보:", MT_INFO)
else:
    print("OpenAPI 요청이 실패했습니다! 다시 시도해주세요.")