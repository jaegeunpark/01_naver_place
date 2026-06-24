import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src import config


def init_driver():
    """
    크롬 브라우저를 초기화하고 최적의 옵션을 설정하는 함수
    """
    logging.info("🌐 크롬 브라우저를 실행하는 중...")
    chrome_options = Options()

    # 💡 팁: 개발 단계에서는 브라우저가 뜨는 걸 눈으로 봐야 하니까 주석 처리합니다.
    # 나중에 완전히 완성되면 아래 주석을 해제해서 백그라운드(Headless)로 돌릴 수 있습니다.
    chrome_options.add_argument("--headless=new")

    # 리소스 제한 및 크래시 방지를 위한 필수 옵션들
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 봇 차단 우회를 위해 '자동화 제어되고 있음' 문구 숨기기 및 유저 에이전트 설정
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={config.USER_AGENT}")

    # 브라우저 생성
    driver = webdriver.Chrome(options=chrome_options)

    # 창 크기 최대화 (창이 작으면 요소가 숨겨져서 크롤링이 안 될 수 있습니다)
    driver.maximize_window()

    # 웹페이지 요소가 로드될 때까지 최대 설정 시간(10초)만큼 기다려주는 안전장치
    driver.implicitly_wait(config.SELENIUM_WAIT_TIME)

    return driver

def wait_for_element_visible(driver, css_selector, timeout=None):
    """
    [⚡ Phase 1] 특정 CSS 선택자가 화면에 '눈으로 보일 때까지' 명시적으로 대기하는 함수
    """
    if timeout is None:
        timeout = config.SELENIUM_WAIT_TIME

    logging.info(f"⏳ 요소 [{css_selector}]가 나타날 때까지 대기 중... (최대 {timeout}초)")
    try:
        # WebDriverWait(드라이버, 최대대기시간).until(조건) 구조입니다.
        # 조건이 만족되면 해당 엘리먼트를 즉시 리턴하고 대기를 끝냅니다.
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return element
    except Exception as e:
        print(f"⚠️ 대기 시간 초과 또는 요소를 찾을 수 없음: {e}")
        return None

def scroll_down_to_end(driver, scroll_count=None):
    """
    동적 페이지의 데이터를 더 불러오기 위해 스크롤을 아래로 내리는 함수
    """
    if scroll_count is None:
        scroll_count = config.SCROLL_COUNT

    logging.info(f"🔄 동적 데이터 수집을 위해 스크롤을 {scroll_count}회 진행합니다.")

    for i in range(scroll_count):
        # 자바스크립트 명령어로 브라우저 스크롤을 가장 아래로 이동
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.info(f"   ↳ 스크롤 [{i+1}/{scroll_count}] 완료... 로딩 대기 중")

        # 스크롤 후 새로운 데이터가 로딩될 시간을 줍니다 (너무 빠르면 차단당함)
        time.sleep(2)