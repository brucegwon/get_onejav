"""
데이터베이스 관련 모듈

이 모듈은 SQLite 데이터베이스 연결 및 모델을 정의합니다.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
import os
from scraper.utils.logger import get_logger

logger = get_logger(__name__)

class Database:
    def __init__(self, db_path: str = "database/scraper.db"):
        """데이터베이스 초기화"""
        try:
            # 데이터베이스 디렉토리 생성
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            self.db_path = db_path
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
            self.create_tables()
            logger.info(f"데이터베이스 초기화 완료: {db_path}")
        except Exception as e:
            logger.error(f"데이터베이스 초기화 중 오류 발생: {str(e)}")
            raise
    
    def create_tables(self):
        """테이블 생성"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    code TEXT NOT NULL,
                    title TEXT NOT NULL,
                    image_url TEXT NOT NULL,
                    file_size TEXT NOT NULL,
                    post_date TIMESTAMP NOT NULL,
                    tags TEXT NOT NULL,
                    description TEXT,
                    translated_desc TEXT,
                    actress TEXT,
                    download_url TEXT NOT NULL,
                    scraped_at TIMESTAMP NOT NULL
                )
            """)
            
            # 인덱스 추가
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_url ON posts(url)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_post_date ON posts(post_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_code ON posts(code)")
            
            self.conn.commit()
            logger.info("테이블 및 인덱스 생성 완료")
        except Exception as e:
            logger.error(f"테이블 생성 중 오류 발생: {str(e)}")
            raise
    
    def add_post(self, post_data: dict) -> bool:
        """게시물 추가"""
        try:
            with self.conn:  # 트랜잭션 컨텍스트 매니저 사용
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO posts (
                        url, code, title, image_url, file_size,
                        post_date, tags, description, translated_desc, actress,
                        download_url, scraped_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    post_data['url'],
                    post_data['code'],
                    post_data['title'],
                    post_data['image_url'],
                    post_data['file_size'],
                    post_data['post_date'],
                    post_data['tags'],
                    post_data['description'],
                    post_data.get('translated_desc', None),
                    post_data['actress'],
                    post_data['download_url'],
                    post_data['scraped_at']
                ))
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"게시물 추가 성공: {post_data['title']}")
                else:
                    logger.info(f"게시물 추가 실패 (중복): {post_data['title']}")
                return success
        except sqlite3.Error as e:
            logger.error(f"게시물 추가 중 오류 발생: {str(e)}")
            return False
    
    def get_post_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """URL로 게시물 조회"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE url = ?", (url,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except sqlite3.Error as e:
            logger.error(f"게시물 조회 중 오류 발생: {str(e)}")
            return None
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """모든 게시물 조회"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM posts ORDER BY post_date DESC")
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"전체 게시물 조회 중 오류 발생: {str(e)}")
            return []
    
    def close(self):
        """데이터베이스 연결 종료"""
        try:
            if self.conn:
                self.conn.close()
                logger.info("데이터베이스 연결 종료")
        except Exception as e:
            logger.error(f"데이터베이스 연결 종료 중 오류 발생: {str(e)}")

# 싱글톤 인스턴스
_db = None

def get_db() -> Database:
    """데이터베이스 인스턴스 반환"""
    global _db
    if _db is None:
        _db = Database()
    return _db 

def init_db():
    """데이터베이스 초기화"""
    try:
        db = get_db()
        db.create_tables()
        logger.info("데이터베이스 초기화 완료")
        return db
    except Exception as e:
        logger.error(f"데이터베이스 초기화 중 오류 발생: {str(e)}")
        raise