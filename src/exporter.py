import os
import pandas as pd
from datetime import datetime

def save_to_excel(data_list, keyword):
    """
    수집된 데이터를 지정된 output 폴더 안에 엑셀 파일로 저장하는 함수
    """
    if not data_list:
        print("⚠️ 저장할 데이터가 없어 엑셀 저장을 건너뜁니다.")
        return

    print("\n📊 수집된 데이터를 엑셀로 변환하는 중...")

    # 💥 [통일성 추가] output 폴더가 없으면 자동으로 생성하는 로직
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 [{output_dir}] 폴더가 존재하지 않아 새로 생성했습니다.")

    # 1. 딕셔너리 리스트를 Pandas 데이터프레임(표 구조)으로 변환
    df = pd.DataFrame(data_list)

    # 2. 저장할 파일명 생성
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_keyword = keyword.replace(" ", "_")
    filename = f"{safe_keyword}_{current_time}.xlsx"

    # 💥 [경로 결합] output/파일명.xlsx 형태로 경로를 묶어줍니다.
    filepath = os.path.join(output_dir, filename)

    # 3. 지정된 경로로 엑셀 파일 내보내기 (인덱스 제외)
    df.to_excel(filepath, index=False)

    # 4. 저장된 절대 경로 출력
    absolute_path = os.path.abspath(filepath)
    print(f"💾 [대성공] 엑셀 파일 저장 완료!")
    print(f"📂 파일 경로: {absolute_path}")