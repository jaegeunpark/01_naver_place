import logging
import os
import sys  # 💡 실행 환경 감지를 위해 임포트
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# [⚡ 패키징 대응] 일반 실행(IDE)과 .exe 실행 시의 베이스 경로를 동적으로 구합니다.
if getattr(sys, 'frozen', False):
    # .exe 파일로 실행된 경우: 실행 파일이 있는 위치
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # 일반 파이썬 스크립트로 실행된 경우 (기존 유지)
    BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / 'output'
LOG_DIR = BASE_DIR / 'logs'

# output 폴더가 없으면 생성
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# 💡 [변경] 로그 로테이션 핸들러 세팅 (자바의 RollingFileAppender 역할)
# ----------------------------------------------------
log_file_path = LOG_DIR / 'crawler.log'

file_handler = TimedRotatingFileHandler(
    log_file_path,
    when='D',         # 로테이션 타이밍: 'D' (Day, 일 단위)
    interval=1,       # 주기: 1일마다 (즉, 매일 자정에 로테이션)
    backupCount=30,   # 백업 파일 개수: 30개 (즉, 한 달 치 로그 보관 후 자동 삭제)
    encoding='utf-8'
)

# ⚠️ 꿀팁: 자바처럼 로그 파일 뒤에 날짜 서픽스(.2026-06-11)가 깔끔하게 붙도록 설정
file_handler.suffix = "%Y-%m-%d"

stream_handler = logging.StreamHandler()  # 콘솔 출력용 핸들러
# ----------------------------------------------------

# 2. [⚡ Phase 1 - 2일차] 로깅 전역 설정 (자바의 logback.xml 역할)
# 콘솔창과 로그 파일에 동시에 기록이 남도록 세팅합니다.
logging.basicConfig(
    level=logging.INFO,  # INFO 등급 이상만 기록 (DEBUG는 제외)
    format='[%(asctime)s] [%(levelname)s] %(message)s',  # 로그 포맷 (날짜, 에러레벨, 메시지)
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[file_handler, stream_handler]
)

# 2. 크롤링 대상 사이트 설정
# (연습용으로 아주 좋은 자바스크립트 동적 로딩 명언 사이트입니다)
TARGET_SITES = {
    "명언_첫페이지": "https://quotes.toscrape.com/js/",
    "명언_두번째페이지": "https://quotes.toscrape.com/js/page/2/"
}
SELENIUM_WAIT_TIME = 10
SCROLL_COUNT = 2

# 3. 브라우저 차단 우회용 헤더 값
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"