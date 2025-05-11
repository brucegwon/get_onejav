# 웹 스크래퍼 프로젝트 PRD

## 1. 프로젝트 개요

- Python 기반 웹 스크래퍼 개발
- SQLite를 활용한 로컬 데이터베이스 구축
- Next.js를 이용한 웹 인터페이스 개발
- 주기적인 데이터 수집 자동화

## 2. 기술 스택

### 백엔드 (스크래퍼)

- Python 3.11+
- 주요 라이브러리
  - requests/httpx (HTTP 요청)
  - beautifulsoup4 (HTML 파싱)
  - aiohttp (비동기 요청)
  - SQLAlchemy (ORM)
  - APScheduler (작업 스케줄링)
  - fake-useragent (User-Agent 랜덤화)
  - python-dotenv (환경 변수 관리)

### 데이터베이스

- SQLite3
- SQLAlchemy ORM

### 프론트엔드

- Next.js 14
- TypeScript
- Tailwind CSS
- shadcn/ui

## 3. 프로젝트 구조

```
├── scraper/
│   ├── core/
│   │   ├── scraper.py
│   │   ├── parser.py
│   │   └── database.py
│   ├── utils/
│   │   ├── proxy_manager.py
│   │   ├── user_agent.py
│   │   └── logger.py
│   ├── config/
│   │   └── settings.py
│   └── scheduler.py
├── web/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── api/
│   ├── components/
│   └── lib/
├── database/
│   └── scraper.db
├── logs/
├── .env
└── requirements.txt
```

## 4. 주요 기능

### 스크래퍼 기능

- 웹사이트 접근 및 데이터 수집
  - 타이틀 추출
  - 이미지 URL 수집
  - 파일 용량 정보
  - 날짜 정보
  - 태그 정보
  - 상세 설명
- IP 우회 메커니즘
  - 프록시 서버 활용
  - User-Agent 랜덤화
  - 요청 간격 조절
  - 세션 관리

### 데이터베이스 관리

- SQLite 스키마 설계
  ```sql
  CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    image_url TEXT,
    file_size TEXT,
    post_date DATETIME,
    tags TEXT,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  ```
- 데이터 중복 체크
- 데이터 업데이트 관리

### 스케줄러

- APScheduler를 이용한 주기적 실행
- 실패 시 재시도 메커니즘
- 로그 기록 및 모니터링

### 웹 인터페이스

- 데이터 조회 및 검색
- 필터링 기능
- 페이지네이션
- 정렬 기능

## 5. 보안 및 안정성

- IP 차단 방지
  - 프록시 서버 로테이션
  - 요청 간격 랜덤화
  - User-Agent 랜덤화
- 에러 처리
  - 네트워크 오류 대응
  - 파싱 오류 처리
  - 재시도 로직
- 로깅 시스템
  - 상세 로그 기록
  - 에러 추적
  - 성능 모니터링

## 6. 성능 요구사항

- 스크래핑 속도 최적화
- 데이터베이스 쿼리 최적화
- 메모리 사용량 관리
- 동시성 처리

## 7. 개발 환경 설정

### 필수 패키지

```txt
requests==2.31.0
beautifulsoup4==4.12.2
aiohttp==3.9.1
SQLAlchemy==2.0.23
APScheduler==3.10.4
fake-useragent==1.4.0
python-dotenv==1.0.0
httpx==0.25.2
```

## 8. 배포 전략

- 스크래퍼: Docker 컨테이너화
- 웹 애플리케이션: Vercel 배포
- 데이터베이스: 로컬 파일 시스템

## 9. 모니터링 및 유지보수

- 로그 모니터링
- 성능 모니터링
- 에러 알림 시스템
- 정기적인 코드 리뷰

## 10. 마일스톤

1. 스크래퍼 기본 기능 구현 (1주)
2. 데이터베이스 설계 및 구현 (3일)
3. 스케줄러 구현 (2일)
4. IP 우회 메커니즘 구현 (3일)
5. 웹 인터페이스 개발 (1주)
6. 테스트 및 최적화 (3일)
7. 배포 및 모니터링 설정 (2일)
