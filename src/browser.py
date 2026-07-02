import undetected_chromedriver as uc

def init_browser(headless=False):
    """
    네이버/구글 봇 탐지를 우회하는 undetected-chromedriver 초기화 함수
    """
    options = uc.ChromeOptions()

    # 일반 유저처럼 보이기 위한 필수 옵션
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-popup-blocking")

    if headless:
        options.add_argument("--headless")

    # 💥 [수정] version_main=149를 넣어 현재 내 크롬 버전과 강제로 싱크를 맞춥니다.
    driver = uc.Chrome(options=options, version_main=149)

    return driver