import requests
import xml.etree.ElementTree as ET
import urllib3

# Disable warnings related to SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API 키
api_key = 'kqMzwvJlxICdXrO0eXEHyXirL/huIAmVPWway9BnnQKyFdi4KSrxyyF71z60Cn5avZSEp7U3W5MBXfls1Z24BA=='

# 서버 정보 및 URL
url = "http://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2"

# 요청 매개변수 설정
params = {
    'searchWrd': '인룡산',
    'pageNo': '1',
    'numOfRows': '5',
    'ServiceKey': api_key
}

# API 요청 보내기 (verify=False는 SSL 인증서 검증을 비활성화합니다)
response = requests.get(url, params=params, verify=False)
print("HTTP Status:", response.status_code)

if response.status_code == 200:
    root = ET.fromstring(response.content)

    result_code = root.find('.//resultCode').text
    result_msg = root.find('.//resultMsg').text
    print("API Response Code:", result_code)
    print("API Response Message:", result_msg)

    if result_code == "00":  # NORMAL SERVICE
        items = root.findall('.//item')
        for item in items:
            MT_NAME = item.find('mntiname').text if item.find('mntiname') is not None else "N/A"
            MT_CODE = item.find('mntilistno').text if item.find('mntilistno') is not None else "N/A"
            MT_LOCATION = item.find('mntiadd').text if item.find('mntiadd') is not None else "N/A"
            MT_HIGH = item.find('mntihigh').text if item.find('mntihigh') is not None else "N/A"
            MT_ADMIN = item.find('mntiadmin').text if item.find('mntiadmin') is not None else "N/A"
            MT_ADMIN_NUM = item.find('mntiadminnum').text if item.find('mntiadminnum') is not None else "N/A"
            MT_TOP_100_REASON = item.find('mntitop').text if item.find('mntitop') is not None else "N/A"
            MT_INFO = item.find('mntisummary').text if item.find('mntisummary') is not None else "N/A"

            print("산 이름:", MT_NAME)
            print("산 코드:", MT_CODE)
            print("산 위치:", MT_LOCATION)
            print("산 높이:", MT_HIGH)
            print("산 관리주체:", MT_ADMIN)
            print("산 관리주체 연락처:", MT_ADMIN_NUM)
            print("산 100대 명산 선정 이유:", MT_TOP_100_REASON)
            print("산 정보:", MT_INFO)
    else:
        print(f"Error: {result_msg} (Code: {result_code})")
else:
    print("OpenAPI 요청이 실패했습니다! 다시 시도해주세요. Status code:", response.status_code)
