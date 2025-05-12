"""
스크래핑 작업을 주기적으로 실행하는 스케줄러 모듈

이 모듈은 APScheduler를 사용하여 스크래핑 작업을
정해진 간격으로 자동 실행합니다.

주요 기능:
- 주기적인 스크래핑 작업 실행
- 작업 상태 모니터링
- 에러 처리 및 로깅
"""

# 서드파티 모듈
from apscheduler.schedulers.background import BackgroundScheduler
# BackgroundScheduler: 백그라운드에서 작업을 실행하는 스케줄러
# - 작업 스케줄링
# - 작업 실행 관리

from apscheduler.triggers.interval import IntervalTrigger
# IntervalTrigger: 일정 간격으로 작업을 실행하는 트리거
# - 시간 간격 설정
# - 작업 반복 실행


from utils.logger import get_logger
# setup_logger: 로깅 시스템 설정
# - 로그 파일 생성
# - 로그 포맷 설정

# Python 기본 모듈
import os
# os: 운영체제 관련 기능
# - 환경 변수 접근
# - 파일 시스템 작업

from dotenv import load_dotenv
# load_dotenv: .env 파일에서 환경 변수 로드
# - 환경 변수 관리
# - 설정 값 로드

import subprocess

# 환경 변수 로드
load_dotenv()

class ScraperScheduler:
    """
    스크래핑 작업을 스케줄링하는 클래스
    
    Attributes:
        logger (logging.Logger): 로거 객체
        scheduler (BackgroundScheduler): APScheduler 인스턴스
        scraper (Scraper): 스크래퍼 인스턴스
        interval_minutes (int): 스크래핑 작업 실행 간격 (분)
    """
    
    def __init__(self):
        """ScraperScheduler 초기화"""
        self.logger = get_logger('scheduler')
        self.scheduler = BackgroundScheduler()
        self.interval_minutes = int(os.getenv('SCRAPE_INTERVAL_MINUTES', '60'))

    def start(self):
        """
        스케줄러를 시작하는 함수
        
        스케줄러를 초기화하고 스크래핑 작업을 등록한 후
        스케줄러를 시작합니다.
        """
        try:
            # 스케줄러에 작업 추가
            self.scheduler.add_job(
                self.scrape_job,
                trigger=IntervalTrigger(minutes=self.interval_minutes),
                id='scrape_job',
                replace_existing=True
            )
            
            # 스케줄러 시작
            self.scheduler.start()
            self.logger.info(f"Scheduler started with {self.interval_minutes} minutes interval")
            
            # 초기 실행
            self.scrape_job()
            
        except Exception as e:
            self.logger.error(f"Error starting scheduler: {str(e)}")

    def scrape_job(self):
        """
        run_scraper.py 파일을 실행하는 함수
        """
        try:
            self.logger.info("Starting scraping job (run run_scraper.py)")
            subprocess.run(["python", "run_scraper.py"], check=True)
            self.logger.info("Scraping job completed")
        except Exception as e:
            self.logger.error(f"Error in scraping job: {str(e)}")

    def stop(self):
        """
        스케줄러를 종료하는 함수
        
        스케줄러를 중지하고 스크래퍼의 리소스를 정리합니다.
        """
        try:
            self.scheduler.shutdown()
            self.logger.info("Scheduler stopped")
        except Exception as e:
            self.logger.error(f"Error stopping scheduler: {str(e)}")

if __name__ == "__main__":
    """
    스크래퍼 스케줄러 실행
    
    스케줄러를 시작하고 프로그램이 종료될 때까지
    실행을 유지합니다.
    """
    scheduler = ScraperScheduler()
    try:
        scheduler.start()
        # 스케줄러가 계속 실행되도록 유지
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop() 