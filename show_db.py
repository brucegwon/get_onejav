from scraper.core.database import get_db
import json
from datetime import datetime
import sys

def format_date(date_str):
    if isinstance(date_str, str):
        try:
            date = datetime.fromisoformat(date_str)
            return date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return date_str
    return date_str

def main():
    db = get_db()
    posts = db.get_all_posts()
    
    print(f"\n총 {len(posts)}개의 게시물이 있습니다.\n")
    print("=" * 100)
    
    for i, post in enumerate(posts, 1):
        print(f"\n[{i}번째 게시물]")
        print(f"제목: {post['title']}")
        print(f"코드: {post['code']}")
        print(f"URL: {post['url']}")
        print(f"이미지: {post['image_url']}")
        print(f"파일 크기: {post['file_size']}")
        print(f"게시일: {format_date(post['post_date'])}")
        print(f"배우: {post['actress']}")
        print(f"태그: {', '.join(json.loads(post['tags']))}")
        print(f"설명: {post['description']}")
        print(f"다운로드 URL: {post['download_url']}")
        print(f"스크래핑 시간: {format_date(post['scraped_at'])}")
        print("-" * 100)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1) 