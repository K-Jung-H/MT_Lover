import http.client
import urllib.parse
import xml.etree.ElementTree as ET
import requests
import urllib3

def MT_data_read(SIGUN_NM):
    # API 키
    api_key = 'b109a81aed5742bab617df81af4feb9e'  # 여기에 발급받은 API 키를 넣으세요

    # 서버 정보
    server = "openapi.gg.go.kr"

    # 요청 매개변수 설정
    params = {
        'KEY': api_key,
        'Type': 'xml',  # XML 형식으로 데이터 요청
        'pIndex': 1,  # 페이지 번호
        'pSize': 100,  # 페이지 당 요청 숫자
        'SIGUN_NM': SIGUN_NM  # 선택적으로 시군명 입력
    }

    # 매개변수를 URL에 맞게 인코딩
    query_string = urllib.parse.urlencode(params)

    # 전체 URL 생성
    url = f"/FrtStret?{query_string}"

    # 연결 설정 및 API 요청 보내기
    conn = http.client.HTTPSConnection(server)
    conn.request("GET", url)
    print(url)
    # 응답 받기
    response = conn.getresponse()
    print(response.status)
    print(type(response.status))
    if response.status == 200:
        response_data = response.read()
        root = ET.fromstring(response_data)  # XML 파싱 후 root 정의
        print(type(root))
        print(root)
        print(type(root))
        print(ET.tostring(root, encoding='utf8').decode('utf8'))  # XML 구조 출력

        # XML 구조를 확인한 후 정확한 태그를 사용하여 데이터 추출
        if root.find('.//MESSAGE') is not None and root.find('.//MESSAGE').text == "해당하는 데이터가 없습니다.":
            return -1
        place_direction = root.find('.//REGION_DIV_NM').text
        mntn_info = root.find('.//MNTN_INFO').text.split(', ')  # MNTN_INFO 요소의 내용을 리스트로 분할하여 mntn_info에 저장
        local_MT_num = int(root.find('.//MNTN_CNT').text)  # MNTN_CNT 요소의 내용을 정수형으로 변환하여 저장
        print("지역의 위치: 경기도 " + place_direction)
        print("산의 개수:", local_MT_num)  # 결과 출력
        print("산의 종류:", mntn_info)  # 결과 출력
        data = {
            "place_direction": place_direction,
            "local_MT_num": local_MT_num,
            "mntn_info": mntn_info,
        }
        return data
    else:
        print("OpenAPI 요청이 실패했습니다! 다시 시도해주세요.")
        return -1

    # 연결 닫기
    conn.close()

def MT_deap_data(MT_name):
    # Disable warnings related to SSL
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # API 키
    api_key = 'kqMzwvJlxICdXrO0eXEHyXirL/huIAmVPWway9BnnQKyFdi4KSrxyyF71z60Cn5avZSEp7U3W5MBXfls1Z24BA=='

    # 서버 정보 및 URL
    url = "http://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2"

    # 요청 매개변수 설정
    params = {
        'searchWrd': MT_name,
        'pageNo': '1',
        'numOfRows': '5',
        'ServiceKey': api_key
    }

    # API 요청 보내기 (verify=False는 SSL 인증서 검증을 비활성화합니다)
    response = requests.get(url, params=params, verify=False)
    print(response.url)
    print("HTTP Status:", response.status_code)



    if response.status_code == 200:
        root = ET.fromstring(response.content)

        result_code = root.find('.//resultCode').text
        result_msg = root.find('.//resultMsg').text
        print("API Response Code:", result_code)
        print("API Response Message:", result_msg)

        print(ET.tostring(root, encoding='utf8').decode('utf8'))  # XML 구조 출력
        # totalCount 요소를 확인하여 데이터 존재 여부를 판단
        total_count = int(root.find('.//totalCount').text)
        if total_count == 0:
            return -2

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

                if MT_LOCATION.find("경기도") != -1:
                    print("산 이름:", MT_NAME)
                    print("산 코드:", MT_CODE)
                    print("산 위치:", MT_LOCATION)
                    print("산 높이:", MT_HIGH)
                    print("산 관리주체:", MT_ADMIN)
                    print("산 관리주체 연락처:", MT_ADMIN_NUM)
                    print("산 100대 명산 선정 이유:", MT_TOP_100_REASON)
                    print("산 정보:", MT_INFO)

                    data = {
                        "MT_NAME" : MT_NAME,
                        "MT_CODE" : MT_CODE,
                        "MT_LOCATION" : MT_LOCATION,
                        "MT_HIGH" : MT_HIGH,
                        "MT_ADMIN" : MT_ADMIN,
                        "MT_ADMIN_NUM" : MT_ADMIN_NUM,
                        "MT_TOP_100_REASON" : MT_TOP_100_REASON,
                        "MT_INFO" : MT_INFO
                    }
                    return data
        else:
            print(f"Error: {result_msg} (Code: {result_code})")
            return -1
    else:
        print("OpenAPI 요청이 실패했습니다! 다시 시도해주세요. Status code:", response.status_code)
        return -1