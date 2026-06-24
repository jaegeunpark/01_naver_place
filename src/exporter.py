import logging

import pandas as pd

from src import config


def save_to_excel(data, filename):
    """
    [기존 유지] 단일 리스트 데이터를 엑셀로 저장하는 함수
    """
    file_path = config.OUTPUT_DIR / filename
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    logging.info(f"📁 단일 엑셀 파일 저장 완료: {file_path}")

def save_to_excel_multi_sheets(data_dict, filename):
    """
    [⚡ Phase 2 - 2일차] 딕셔너리 형태의 데이터를 받아 하나의 엑셀 파일에 멀티 시트로 저장하는 함수
    :param data_dict: {"시트명1": [데이터리스트], "시트명2": [데이터리스트]} 구조
    """
    file_path = config.OUTPUT_DIR / filename

    # 💡 Pandas의 ExcelWriter를 오픈합니다. (자바의 try-with-resources 구문과 같은 with 사용)
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, data_list in data_dict.items():
            # 1. 데이터를 판다스 DataFrame으로 변환
            df = pd.DataFrame(data_list)
            # 2. 지정한 시트 이름으로 엑셀에 써내려갑니다.
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            logging.info(f"   ↳ [Excel] '{sheet_name}' 시트에 {len(data_list)}개 행 저장 완료")

    logging.info(f"📁 멀티 시트 엑셀 파일 저장 완료: {file_path}")