"""
환경 변수 설정을 테스트하는 스크립트

이 스크립트는 .env 파일에서 설정된 환경 변수들을 읽어와
정상적으로 로드되는지 확인합니다.
"""

import os
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_env_variables():
    """
    환경 변수 로드 및 테스트
    """
    try:
        # .env 파일 로드
        load_dotenv()
        logger.info("환경 변수 파일(.env) 로드 완료")

        # 데이터베이스 설정 테스트
        db_url = os.getenv('DATABASE_URL')
        logger.info(f"DATABASE_URL: {db_url}")

        # 스크래퍼 설정 테스트
        target_url = os.getenv('TARGET_URL')
        logger.info(f"TARGET_URL: {target_url}")

        scrape_interval = os.getenv('SCRAPE_INTERVAL_MINUTES')
        logger.info(f"SCRAPE_INTERVAL_MINUTES: {scrape_interval}")

        # 로깅 설정 테스트
        log_level = os.getenv('LOG_LEVEL')
        logger.info(f"LOG_LEVEL: {log_level}")

        # 필수 환경 변수 확인
        required_vars = ['DATABASE_URL', 'TARGET_URL', 'SCRAPE_INTERVAL_MINUTES']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"누락된 필수 환경 변수: {', '.join(missing_vars)}")
            return False
        
        logger.info("모든 환경 변수가 정상적으로 로드되었습니다.")
        return True

    except Exception as e:
        logger.error(f"환경 변수 테스트 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    test_env_variables() 