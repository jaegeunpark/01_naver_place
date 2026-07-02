import os
import time
import random
import logging  # 👈 파이썬 표준 로깅 라이브러리
from datetime import datetime
from src.browser import init_browser
from src.parser import parse_naver_place
from src.exporter import save_to_excel

# 💥 [템플릿 구조 살리기] log 폴더 설정 및 로거 초기화
LOG_DIR = "log"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 로그 파일명 생성 (예: log/crawler_20260629.log)
log_filename = f"crawler_{datetime.now().strftime('%Y%m%d')}.log"
log_filepath = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filepath, encoding='utf-8'), # log 폴더 내 파일로 저장
        logging.StreamHandler() # 콘솔 터미널창에도 동시에 출력
    ]
)

def main():
    # 이제 print() 대신 logging.info() 또는 logging.error()를 사용합니다.
    keyword = input("🔍 검색할 키워드를 입력하세요 (예: 강남구 미용실): ")
    if not keyword:
        logging.error("❌ 키워드가 입력되지 않아 프로그램을 종료합니다.")
        return

    logging.info(f"🚀 [{keyword}] 크롤링 및 DB 구축을 시작합니다...")

    driver = init_browser(headless=False)

    try:
        driver.get("https://map.naver.com/")
        time.sleep(random.uniform(2.0, 3.5))

        url = f"https://map.naver.com/p/search/{keyword}"
        driver.get(url)
        time.sleep(random.uniform(4.0, 5.5))

        results = parse_naver_place(driver)
        save_to_excel(results, keyword)

        logging.info("🎉 모든 프로세스가 성공적으로 종료되었습니다.")
        input("\n창을 닫으려면 엔터를 누르세요...")

    except Exception as e:
        logging.error(f"❌ 치명적 에러 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()