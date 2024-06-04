import requests
from bs4 import BeautifulSoup

class Image_Search:
    def get_image_link(query):
        # 구글 검색 결과 페이지 URL을 생성합니다.
        url = f"https://www.google.com/search?q={query}&tbm=isch"

        # HTTP GET 요청을 보냅니다.
        response = requests.get(url)

        # 응답의 HTML 내용을 파싱합니다.
        soup = BeautifulSoup(response.text, 'html.parser')

        # 이미지 링크를 담을 리스트를 초기화합니다.
        image_links = []

        # 이미지 태그들을 찾습니다.
        for img in soup.find_all('img'):
            # 이미지 태그의 'src' 속성에 이미지 링크가 있습니다.
            image_link = img.get('src')
            if image_link:
                # 이미지 링크를 리스트에 추가합니다.
                image_links.append(image_link)
            if len(image_links) == 3:
                break

        return image_links


image_links = Image_Search.get_image_link('한국공학대학교')

print(image_links)