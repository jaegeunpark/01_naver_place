import logging
import time
from datetime import datetime

from selenium.webdriver.common.by import By  # 💡 Next 버튼을 찾기 위해 임포트

from src import browser
from src import config
from src import exporter
from src import parser


def main():
    logging.info("==========================================")
    logging.info("🚀 [Phase 2] 멀티 페이지 크롤러를 시작합니다.")
    logging.info("==========================================")

    driver = browser.init_driver()
    # 💡 모든 시트의 데이터를 모아둘 거대한 딕셔너리 상자
    # 구조: {"명언_첫페이지": [...데이터...], "명언_두번째페이지": [...데이터...]}
    final_excel_data = {}

    try:
        # 💡 자바의 Map.entrySet() 돌리듯 딕셔너리의 key(시트이름)와 value(URL)를 가져옵니다.
        for sheet_name, target_url in config.TARGET_SITES.items():
            logging.info(f"▶️ [{sheet_name}] 크롤링을 시작합니다. URL: {target_url}")

            driver.get(target_url)
            browser.wait_for_element_visible(driver, ".quote")
            browser.scroll_down_to_end(driver)

            full_html = driver.page_source

            # 각 시트별로 번호는 다시 1번부터 이쁘게 나오도록 세팅합니다.
            current_sheet_data = parser.extract_quotes(full_html, start_num=1)

            # 수집된 데이터를 시트 이름을 Key로 해서 딕셔너리에 쏙 넣습니다.
            final_excel_data[sheet_name] = current_sheet_data
            logging.info(f"✅ [{sheet_name}] 수집 완료. (총 {len(current_sheet_data)}개)")
            logging.info("------------------------------------------")
            time.sleep(3)  # 사이트 전환 전 망가짐 방지용 딜레이

        # 모든 사이트 순회가 끝나면 멀티 시트 저장 함수 호출!
        today_str = datetime.now().strftime("%Y%m%d")
        file_name = f"명언_크롤링_멀티시트_{today_str}.xlsx"

        logging.info("💾 통합 멀티 시트 엑셀 파일 저장 프로세스 시작...")
        exporter.save_to_excel_multi_sheets(final_excel_data, file_name)
        logging.info("🎉 모든 카테고리 크롤링 및 통합 파일 저장 완료!")

    except Exception as e:
        logging.error(f"❌ 실행 중 치명적인 오류가 발생했습니다: {e}")
    finally:
        driver.quit()
        logging.info("🚪 브라우저를 닫고 프로그램을 안전하게 종료합니다.")

if __name__ == "__main__":
    main()