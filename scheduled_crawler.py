#!/usr/bin/env python3
"""
스케줄된 크롤링을 위한 스크립트
GitHub Actions에서 실행되어 데이터베이스에 저장
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.services.legislation_service import LegislationService
from backend.services.database_service import DatabaseService

class ScheduledCrawler:
    def __init__(self):
        self.legislation_service = LegislationService()
        self.database_service = DatabaseService()
        self.api_url = os.getenv("API_URL", "http://localhost:8000")
    
    async def crawl_and_save_national(self):
        """입법부 데이터 크롤링 및 저장"""
        print(f"[{datetime.now()}] 입법부 데이터 크롤링 시작...")
        
        try:
            # 기존 입법부 데이터 삭제
            self.database_service.delete_legislation_by_source("national")
            print("기존 입법부 데이터 삭제 완료")
            
            # 새로운 데이터 크롤링
            national_data = await self.legislation_service.get_national_legislation()
            
            if national_data:
                # 데이터베이스에 저장
                saved_count = self.database_service.save_legislation_data(national_data)
                print(f"입법부 데이터 {saved_count}건 저장 완료")
            else:
                print("입법부 데이터가 없습니다.")
                
        except Exception as e:
            print(f"입법부 데이터 크롤링 오류: {e}")
            raise
    
    async def crawl_and_save_admin(self):
        """행정부 데이터 크롤링 및 저장"""
        print(f"[{datetime.now()}] 행정부 데이터 크롤링 시작...")
        
        try:
            # 기존 행정부 데이터 삭제
            self.database_service.delete_legislation_by_source("admin")
            print("기존 행정부 데이터 삭제 완료")
            
            # 새로운 데이터 크롤링
            admin_data = await self.legislation_service.get_admin_legislation()
            
            if admin_data:
                # 데이터베이스에 저장
                saved_count = self.database_service.save_legislation_data(admin_data)
                print(f"행정부 데이터 {saved_count}건 저장 완료")
            else:
                print("행정부 데이터가 없습니다.")
                
        except Exception as e:
            print(f"행정부 데이터 크롤링 오류: {e}")
            raise
    
    def notify_api_refresh(self):
        """API 서버에 데이터 새로고침 알림"""
        try:
            response = requests.post(f"{self.api_url}/api/legislation/refresh")
            if response.status_code == 200:
                print("API 서버 새로고침 완료")
            else:
                print(f"API 서버 새로고침 실패: {response.status_code}")
        except Exception as e:
            print(f"API 서버 새로고침 오류: {e}")

async def main():
    """메인 실행 함수"""
    crawler = ScheduledCrawler()
    
    # 실행 모드 확인
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if mode == "national":
        await crawler.crawl_and_save_national()
    elif mode == "admin":
        await crawler.crawl_and_save_admin()
    elif mode == "all":
        await crawler.crawl_and_save_national()
        await crawler.crawl_and_save_admin()
    else:
        print(f"알 수 없는 모드: {mode}")
        sys.exit(1)
    
    # API 서버에 새로고침 알림
    crawler.notify_api_refresh()
    
    print(f"[{datetime.now()}] 크롤링 작업 완료")

if __name__ == "__main__":
    asyncio.run(main())
