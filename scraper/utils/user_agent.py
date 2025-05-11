"""
User-Agent 관리 및 요청 간격 제어를 위한 유틸리티 모듈

이 모듈은 웹 스크래핑 시 IP 차단을 방지하기 위한 기능을 제공합니다.
- 랜덤 User-Agent 생성
- 요청 간격 제어
"""

# 서드파티 모듈
from fake_useragent import UserAgent
# UserAgent: 랜덤 User-Agent 문자열 생성

# Python 기본 모듈
import random
# random: 랜덤 숫자 생성 및 선택

import time
# time: 시간 관련 기능 (현재 시간, 지연 등)

from typing import List

class UserAgentManager:
    """
    User-Agent 관리 및 요청 간격을 제어하는 클래스
    
    이 클래스는 웹 스크래핑 시 IP 차단을 방지하기 위해
    랜덤한 User-Agent를 생성하고 요청 간격을 제어합니다.
    
    Attributes:
        user_agents (List[str]): 사용할 User-Agent 문자열 리스트
        last_request_time (float): 마지막 요청 시간
        min_delay (int): 최소 요청 간격 (초)
    """
    
    def __init__(self):
        """UserAgentManager 초기화"""
        self.user_agents: List[str] = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.254'
        ]
        self.last_request_time = 0
        self.min_delay = 1  # 최소 요청 간격 (초)

    def get_random_user_agent(self) -> str:
        """랜덤 User-Agent 문자열을 반환"""
        return random.choice(self.user_agents)

    def add_random_delay(self):
        """요청 간 랜덤 딜레이 추가"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_delay:
            delay = self.min_delay - time_since_last_request + random.uniform(0, 1)
            time.sleep(delay)
        
        self.last_request_time = time.time()

def get_random_user_agent() -> str:
    """UserAgentManager의 get_random_user_agent 함수를 호출하는 편의 함수"""
    manager = UserAgentManager()
    return manager.get_random_user_agent() 