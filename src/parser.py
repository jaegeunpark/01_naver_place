from bs4 import BeautifulSoup


def extract_quotes(html, start_num=1):  # 💡 start_num 파라미터 추가 (기본값 1)
    """
    HTML 소스코드를 분석하여 명언, 저자, 번호를 딕셔너리 리스트로 추출
    """
    soup = BeautifulSoup(html, 'html.parser')
    quote_elements = soup.select('.quote')

    data_list = []

    # 💡 start=1 대신 넘겨받은 start_num을 시작점으로 설정합니다!
    for idx, element in enumerate(quote_elements, start=start_num):
        text = element.select_one('.text').text.strip()
        author = element.select_one('.author').text.strip()

        data_list.append({
            "번호": idx,
            "명언": text,
            "저자": author
        })

    return data_list