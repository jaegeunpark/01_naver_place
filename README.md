# 🕸️ 파이썬 크롤러 기본 템플릿

새로운 웹 크롤링 프로젝트를 시작할 때 복사해서 사용하는 기본 베이스 코드입니다.
셀레늄 설정, 엑셀 저장, 로깅, `.exe` 빌드 경로 최적화가 미리 세팅되어 있습니다.

## 📁 폴더 구조
- `main.py`: 프로그램 실행 진입점
- `src/config.py`: 환경 설정 및 경로 관리
- `src/browser.py`: 크롬 브라우저 초기화 (Headless 포함)
- `src/parser.py`: 웹 데이터 파싱 로직
- `src/exporter.py`: 엑셀 내보내기 (Pandas)

## 🚀 사용 방법

### 1. 라이브러리 설치 (최초 1회만)
```bash
pip install selenium pandas openpyxl pyinstaller
```

### 2. 프로그램 실행 (로컬 테스트)
```bash
python main.py
```

### 3. 단일 실행 파일(.exe) 빌드
```bash
pyinstaller --clean --onefile main.py
```