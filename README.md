# OneJAV 스크래퍼

OneJAV 웹사이트의 게시물을 자동으로 수집하고 데이터베이스에 저장하는 스크래핑 도구입니다.

## 프로젝트 구조

```
get_onejav_db_py/
├── database/
│   └── scraper.db
├── scraper/
│   ├── core/
│   │   ├── database.py
│   │   └── scraper.py
│   └── utils/
│       ├── logger.py
│       ├── trans_desc.py
│       └── user_agent.py
├── run_scraper.py
├── show_db.py
└── requirements.txt
```

## 주요 기능

1. **웹 스크래핑**

   - Selenium을 사용한 동적 페이지 처리
   - 병렬 처리를 통한 성능 최적화
   - 자동 페이지네이션 처리

2. **데이터 처리**

   - 게시물 정보 추출 (제목, 날짜, 태그 등)
   - 일본어 설명 자동 번역
   - 중복 게시물 체크

3. **데이터베이스 관리**
   - SQLite 데이터베이스 사용
   - 게시물 정보 저장 및 조회
   - 중복 데이터 방지

## 최적화 사항

1. **성능 개선**

   - 페이지 로드 대기 시간 최적화 (1초 → 0.3초)
   - 파싱 대기 시간 최적화 (1초 → 0.05초)
   - 병렬 처리 도입 (최대 5개 스레드)

2. **중복 체크 로직 개선**

   - 마지막 페이지 게시물만 중복 체크
   - 나머지 페이지는 중복 체크 없이 저장
   - 번역 API 호출 최적화

3. **로깅 개선**
   - 이모지를 사용한 직관적인 로그 표시
   - 중복 게시물 수 표시
   - 저장된 게시물 수 표시

## 사용 방법

1. **환경 설정**

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

2. **스크래퍼 실행**

```bash
python run_scraper.py
```

3. **데이터베이스 조회**

```bash
python show_db.py
```

## 주요 수정 이력

1. **성능 최적화**

   - 대기 시간 조정
   - 병렬 처리 도입
   - 메모리 사용 최적화

2. **중복 체크 로직 개선**

   - 마지막 페이지 중심 중복 체크
   - 번역 API 호출 최적화
   - 저장 로직 개선

3. **UI/UX 개선**
   - 이모지 기반 로그 표시
   - 진행 상황 표시 개선
   - 에러 메시지 명확화

## 의존성

- Python 3.8+
- Selenium
- BeautifulSoup4
- SQLite3
- 기타 requirements.txt 참조

## 주의사항

1. 웹사이트 구조 변경 시 스크래퍼 수정 필요
2. 번역 API 사용량 제한 확인 필요
3. 데이터베이스 백업 권장

## 라이선스

MIT License
