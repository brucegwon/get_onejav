"""
로깅 관련 모듈

이 모듈은 애플리케이션 전체에서 사용할 로깅 기능을 제공합니다.
"""

import logging
import os
from datetime import datetime
from typing import Optional

def get_logger(name: str) -> logging.Logger:
    """
    로거 인스턴스를 반환합니다.
    
    Args:
        name: 로거 이름 (보통 __name__ 사용)
        
    Returns:
        logging.Logger: 로거 인스턴스
    """
    # 로그 디렉토리 생성
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # 로거 생성
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 있다면 추가하지 않음
    if logger.handlers:
        return logger
    
    # 로그 레벨 설정
    logger.setLevel(logging.INFO)
    
    # 파일 핸들러 설정
    log_file = os.path.join(log_dir, f"scraper_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 포맷터 설정
    class EmojiFormatter(logging.Formatter):
        LEVEL_EMOJI = {
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'DEBUG': '🐞',
            'CRITICAL': '🔥',
        }
        def format(self, record):
            emoji = self.LEVEL_EMOJI.get(record.levelname, '')
            return f"{emoji} {record.getMessage()}"

    formatter = EmojiFormatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 