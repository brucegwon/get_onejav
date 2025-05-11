import os
from dotenv import load_dotenv
from scraper.core.scraper import Scraper
from scraper.core.database import init_db

if __name__ == "__main__":
    load_dotenv()
    db = init_db()
    target_url = os.getenv('TARGET_URL')
    if not target_url:
        print("❌ Error: TARGET_URL 환경변수가 설정되어 있지 않습니다.")
        exit(1)
    scraper = Scraper(target_url)
    try:
        print("🚀 실제 스크래핑을 시작합니다...")
        scraper.scrape_new_posts()
        print("✨ 스크래핑이 완료되었습니다.")
    except Exception as e:
        print(f"❌ 스크래핑 중 오류 발생: {str(e)}")
    finally:
        scraper.close()
        db.close() 