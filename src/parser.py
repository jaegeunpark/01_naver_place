import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_naver_place(driver):
    final_results = []

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchIframe")))
        driver.switch_to.frame("searchIframe")

        scroll_container = driver.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container")
        print("🔄 데이터 로딩을 위해 스크롤을 내리는 중...")
        for _ in range(2):
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_container)
            time.sleep(random.uniform(1.1, 1.9))

        # 직접 찾으신 신의 한 수 클래스명
        place_elements = driver.find_elements(By.CSS_SELECTOR, "span.O_Uah")
        total_count = min(len(place_elements), 5) # 테스트용으로 5개 고정
        print(f"🎉 총 {total_count}개의 업체를 상세 탐색합니다.\n")

        for i in range(total_count):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame("searchIframe")
                current_places = driver.find_elements(By.CSS_SELECTOR, "span.O_Uah")

                name = current_places[i].text.strip()
                print(f"========================================\n👉 [{i+1}/{total_count}] {name} 클릭!")

                # 💥 [핵심 수정] 오버레이 방어막을 무시하고 자바스크립트로 강제 클릭을 먹입니다.
                driver.execute_script("arguments[0].click();", current_places[i])

                time.sleep(random.uniform(2.5, 3.5))

                driver.switch_to.default_content()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "entryIframe")))
                driver.switch_to.frame("entryIframe")

                # 1. 업종(카테고리) 추출
                category = "추출 실패"
                category_selectors = ["span.DJJvD", "span.lnY3b", "span.placeholder", ".YXmsC", "span.dtDQt"]
                for sel in category_selectors:
                    try:
                        res = driver.find_element(By.CSS_SELECTOR, sel).text.strip()
                        if res:
                            category = res
                            break
                    except:
                        continue
                print(f"   🔹 업종 타겟팅 결과: {category}")

                # 2. 주소 추출
                address = "추출 실패"
                address_selectors = ["span.LD1gC", "span.v77gC", ".f_S7A", "span.Y3198", "span.pz7wy"]
                for sel in address_selectors:
                    try:
                        res = driver.find_element(By.CSS_SELECTOR, sel).text.strip()
                        if res:
                            address = res
                            break
                    except:
                        continue
                print(f"   🔹 주소 타겟팅 결과: {address}")

                # 3. 전화번호 추출
                phone = "추출 실패"
                phone_selectors = ["span.xl478", "span.O8qbU", "span.Z8ua1", ".NFu6X", "span.xlx7Q"]
                for sel in phone_selectors:
                    try:
                        res = driver.find_element(By.CSS_SELECTOR, sel).text.strip()
                        if res:
                            phone = res
                            break
                    except:
                        continue
                print(f"   🔹 전화번호 타겟팅 결과: {phone}")

                final_results.append({
                    "업체명": name,
                    "업종": category,
                    "주소": address,
                    "전화번호": phone
                })

                time.sleep(random.uniform(1.0, 2.0))

            except Exception as e:
                print(f"   ❌ {i+1}번째 업체 탐색 중 에러 발생: {e}")
                continue

        return final_results

    except Exception as e:
        print(f"❌ 파싱 중 치명적 에러 발생: {e}")
        return []