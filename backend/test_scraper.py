#!/usr/bin/env python3
"""
웹 스크래퍼 테스트 스크립트
requests + BeautifulSoup 방식으로 크롤링 테스트
"""

import asyncio
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.web_scraper import WebScraper
from services.legislation_service import LegislationService

async def test_web_scraper():
    """웹 스크래퍼 테스트"""
    print("🔍 웹 스크래퍼 테스트 시작...")
    
    scraper = WebScraper()
    
    try:
        # 입법부 데이터 테스트
        print("\n📊 입법부 데이터 수집 테스트...")
        national_data = scraper.get_national_legislation_data()
        print(f"✅ 입법부 데이터 수집 완료: {len(national_data)}건")
        
        if national_data:
            print("\n📋 입법부 데이터 샘플:")
            for i, item in enumerate(national_data[:3]):  # 처음 3개만 출력
                print(f"  {i+1}. {item['제목']}")
                print(f"     소관위: {item['소관위']}")
                print(f"     의안번호: {item['의안번호']}")
                print(f"     게시기간: {item['게시시작일']} ~ {item['게시종료일']}")
                print()
        
        # 행정부 데이터 테스트
        print("\n📊 행정부 데이터 수집 테스트...")
        admin_data = scraper.get_admin_legislation_data()
        print(f"✅ 행정부 데이터 수집 완료: {len(admin_data)}건")
        
        if admin_data:
            print("\n📋 행정부 데이터 샘플:")
            for i, item in enumerate(admin_data[:3]):  # 처음 3개만 출력
                print(f"  {i+1}. {item['title']}")
                print(f"     소관위: {item['committee']}")
                print(f"     게시기간: {item['start_date']} ~ {item['end_date']}")
                print()
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
    finally:
        scraper.close()

async def test_legislation_service():
    """LegislationService 통합 테스트"""
    print("\n🔧 LegislationService 통합 테스트...")
    
    service = LegislationService()
    
    try:
        # 입법부 데이터 테스트
        print("\n📊 입법부 서비스 테스트...")
        national_items = await service.get_national_legislation()
        print(f"✅ 입법부 서비스 완료: {len(national_items)}건")
        
        if national_items:
            print("\n📋 입법부 서비스 데이터 샘플:")
            for i, item in enumerate(national_items[:2]):
                print(f"  {i+1}. {item.title}")
                print(f"     소관위: {item.committee}")
                print(f"     출처: {item.source}")
                print()
        
        # 행정부 데이터 테스트
        print("\n📊 행정부 서비스 테스트...")
        admin_items = await service.get_admin_legislation()
        print(f"✅ 행정부 서비스 완료: {len(admin_items)}건")
        
        if admin_items:
            print("\n📋 행정부 서비스 데이터 샘플:")
            for i, item in enumerate(admin_items[:2]):
                print(f"  {i+1}. {item.title}")
                print(f"     소관위: {item.committee}")
                print(f"     출처: {item.source}")
                print()
        
    except Exception as e:
        print(f"❌ 서비스 테스트 중 오류 발생: {e}")

async def main():
    """메인 테스트 함수"""
    print("🚀 입법예고 수집기 테스트 시작")
    print("=" * 50)
    
    # 웹 스크래퍼 테스트
    await test_web_scraper()
    
    print("\n" + "=" * 50)
    
    # 서비스 통합 테스트
    await test_legislation_service()
    
    print("\n" + "=" * 50)
    print("✅ 모든 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(main())
