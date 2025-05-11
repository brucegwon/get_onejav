"""
웹 스크래핑을 수행하는 핵심 모듈

이 모듈은 지정된 웹사이트에서 게시물 정보를 수집하고
데이터베이스에 저장하는 기능을 제공합니다.

주요 기능:
- 웹 페이지 요청 및 응답 처리
- HTML 파싱
- 데이터 추출 및 저장
"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
from scraper.utils.user_agent import get_random_user_agent
from scraper.utils.logger import get_logger
from scraper.core.database import get_db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from scraper.utils.trans_desc import translate_to_korean
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# 상수 정의
BASE_URL = "https://onejav.com"
WAIT_TIME = 0.3  # 페이지 로드 대기 시간 (1초 → 0.3초)
PARSE_DELAY = 0.05  # 게시물별 파싱 간 대기 시간 (1초 → 0.05초)
MAX_RETRIES = 3  # 최대 재시도 횟수
MAX_WORKERS = 5  # 최대 병렬 작업 수

logger = get_logger(__name__)

class Scraper:
    """웹 스크래핑을 수행하는 클래스"""
    
    def __init__(self, target_url: str):
        """Scraper 초기화"""
        self.target_url = target_url
        self.db = get_db()
        
        # Selenium WebDriver 설정
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'user-agent={get_random_user_agent()}')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def get_page_with_selenium(self, url: str) -> BeautifulSoup:
        """Selenium을 사용하여 페이지를 가져옴"""
        for attempt in range(MAX_RETRIES):
            try:
                print(f"🌊 페이지 요청: {url}")
                self.driver.get(url)
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(WAIT_TIME)
                
                # 페이지 로드 완료 체크
                try:
                    self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                except Exception as e:
                    print(f"💥 페이지 로드 오류: {e}")
                    raise
                
                # 컨테이너 요소 체크
                try:
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
                except Exception as e:
                    print(f"💥 컨테이너 로드 오류: {e}")
                    raise
                
                return BeautifulSoup(self.driver.page_source, 'html.parser')
            except Exception as e:
                print(f"💥 페이지 요청 실패 (시도 {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(WAIT_TIME)

    def is_duplicate(self, post_data: dict) -> bool:
        """게시물이 이미 DB에 존재하는지 확인"""
        try:
            existing_post = self.db.get_post_by_url(post_data['url'])
            return existing_post is not None
        except Exception as e:
            print(f"💥 중복 체크 오류: {str(e)}")
            return False

    def process_card(self, card) -> Optional[dict]:
        """카드에서 게시물 데이터 추출"""
        try:
            date_elem = card.find('p', class_='subtitle').find('a')
            if not date_elem:
                return None
            post_date_str = date_elem.text.strip()
            try:
                post_date = datetime.strptime(post_date_str, '%B %d, %Y')
            except ValueError:
                post_date = datetime.now()

            title_elem = card.find('h5', class_='title').find('a')
            if not title_elem:
                return None
            title = title_elem.text.strip()
            
            # 제목 형식 변환
            m_fc2 = re.match(r'^(FC2)PPV(\d+)$', title, re.IGNORECASE)
            if m_fc2:
                title = f"{m_fc2.group(1).upper()}-PPV-{m_fc2.group(2)}"
            else:
                m_3prefix = re.match(r'^(\d{3})([A-Za-z]+)(\d+)$', title)
                if m_3prefix:
                    title = f"{m_3prefix.group(1)}{m_3prefix.group(2)}-{m_3prefix.group(3)}"
                elif len(title) <= 8:
                    m = re.match(r'^([A-Za-z]+)(\d+)$', title)
                    if m:
                        title = f"{m.group(1)}-{m.group(2)}"

            post_url = title_elem['href']
            if not post_url.startswith('http'):
                post_url = f"{BASE_URL}{post_url}"

            img_elem = card.find('img', class_='image')
            if not img_elem or 'src' not in img_elem.attrs:
                return None
            image_url = img_elem['src']

            size_elem = card.find('span', class_='is-size-6')
            if not size_elem:
                return None
            file_size = size_elem.text.strip()

            tag_elems = card.find_all('a', class_='tag')
            tags = [tag.text.strip() for tag in tag_elems]

            download_elem = card.find('a', class_='button is-primary is-fullwidth')
            if not download_elem or 'href' not in download_elem.attrs:
                return None
            download_url = download_elem['href']
            if not download_url.startswith('http'):
                download_url = f"{BASE_URL}{download_url}"

            # description 추출
            description = ""
            desc_elem = card.find('p', class_='level has-text-grey-dark')
            if desc_elem:
                description = desc_elem.text.strip()

            # actress 추출
            actress = []
            panel_elem = card.find('div', class_='panel')
            if panel_elem:
                actress = [a.text.strip() for a in panel_elem.find_all('a', class_='panel-block')]

            return {
                'url': post_url,
                'code': title,
                'title': title,
                'image_url': image_url,
                'file_size': file_size,
                'post_date': post_date,
                'tags': json.dumps(tags),
                'description': description,
                'translated_desc': "",  # 번역은 나중에 수행
                'actress': json.dumps(actress, ensure_ascii=False),
                'download_url': download_url,
                'scraped_at': datetime.now()
            }
        except Exception as e:
            print(f"💥 게시물 처리 오류: {str(e)}")
            return None

    def save_post(self, post_data: dict, skip_duplicate_check: bool = False):
        """게시물 데이터를 DB에 저장"""
        try:
            # 중복 체크 (skip_duplicate_check가 False일 때만)
            if not skip_duplicate_check and self.is_duplicate(post_data):
                return False

            # 번역 수행
            if post_data['description']:
                try:
                    post_data['translated_desc'] = translate_to_korean(post_data['description'])
                except Exception as e:
                    print(f"💥 번역 오류: {e}")
                    post_data['translated_desc'] = ""

            # 저장
            with self.lock:  # 스레드 안전성을 위한 락 사용
                if self.db.add_post(post_data):
                    print(f"💫 저장 완료: {post_data['title']}")
                    return True
                else:
                    print(f"💥 저장 실패: {post_data['title']}")
                    return False
        except Exception as e:
            print(f"💥 저장 오류: {str(e)}")
            raise

    def get_next_page_url(self, soup: BeautifulSoup) -> Optional[str]:
        """다음 페이지 URL을 추출"""
        try:
            pagination = soup.find('nav', class_='pagination')
            if not pagination:
                print("⚠️ 페이지네이션 없음")
                return None
            next_link = pagination.find('a', class_='pagination-next')
            if not next_link or 'href' not in next_link.attrs:
                print("⚠️ 다음 페이지 링크 없음")
                return None
            next_url = next_link['href']
            if not next_url.startswith('http'):
                if next_url.startswith('?'):
                    next_url = f"{BASE_URL}/new{next_url}"
                else:
                    next_url = f"{BASE_URL}{next_url}"
            print(f"➡️ 다음 페이지: {next_url}")
            return next_url
        except Exception as e:
            print(f"💥 URL 추출 오류: {str(e)}")
        return None

    def scrape_new_posts(self):
        """새로운 게시물을 스크래핑"""
        start_time = time.time()
        print("🚀 스크래핑 시작")
        current_url = f"{BASE_URL}/new"
        yesterday = datetime.now().date() - timedelta(days=1)
        should_continue = True
        last_page_posts = []
        all_posts = []
        duplicate_count = 0
        saved_count = 0
        
        while current_url and should_continue:
            print(f"📚 페이지 처리: {current_url}")
            soup = self.get_page_with_selenium(current_url)
            
            cards = soup.find_all('div', class_='card mb-3')
            print(f"🔮 발견된 게시물: {len(cards)}개")
            
            # 병렬 처리로 게시물 데이터 추출
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                future_to_card = {executor.submit(self.process_card, card): card for card in cards}
                page_posts = []
                
                for future in as_completed(future_to_card):
                    post_data = future.result()
                    if post_data:
                        if post_data['post_date'].date() < yesterday:
                            should_continue = False
                            print("⏳ 어제 이전 게시물 발견")
                            break
                        page_posts.append(post_data)
                        print(f"✨ 게시물 처리: {post_data['title']}")
            
            all_posts.extend(page_posts)
            if not should_continue:
                last_page_posts = page_posts
                break
                
            current_url = self.get_next_page_url(soup)
            if not current_url:
                print("🎯 마지막 페이지 도달")
                last_page_posts = page_posts
                break

        # 마지막 페이지 게시물 저장 (중복 체크 수행)
        for post_data in last_page_posts:
            if self.save_post(post_data, skip_duplicate_check=False):
                saved_count += 1
            else:
                duplicate_count += 1
        
        # 나머지 게시물 저장 (중복 체크 건너뛰기)
        for post_data in all_posts:
            if post_data['url'] not in set(post['url'] for post in last_page_posts):
                if self.save_post(post_data, skip_duplicate_check=True):
                    saved_count += 1
        
        end_time = time.time()
        print(f"🔄 중복 게시물: {duplicate_count}개")
        print(f"💫 저장된 게시물: {saved_count}개")
        print(f"🌟 스크래핑 완료 ({end_time - start_time:.1f}초)")

    def close(self):
        """세션 종료"""
        if hasattr(self, 'driver'):
            self.driver.quit() 