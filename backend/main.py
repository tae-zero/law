from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime, timedelta
import os
import logging
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from services.legislation_service import LegislationService
from services.database_service import DatabaseService
from models.legislation_models import LegislationResponse, LegislationItem
from models.database import create_tables

# 환경변수 로드
load_dotenv()

app = FastAPI(
    title="입법예고 수집 API",
    description="국회입법예고와 행정부 입법예고를 자동으로 수집하는 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # 모든 도메인 허용
        "https://*.vercel.app",  # 모든 Vercel 도메인
        "https://*.railway.app",  # 모든 Railway 도메인
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 서비스 인스턴스
legislation_service = LegislationService()

# 데이터베이스 테이블 생성
try:
    logger.info("🏗️ 데이터베이스 테이블 생성 중...")
    create_tables()
    logger.info("✅ 데이터베이스 테이블 생성 완료")
except Exception as e:
    logger.error(f"❌ 데이터베이스 테이블 생성 실패: {str(e)}")

# 데이터베이스 서비스 초기화 및 연결 테스트
try:
    database_service = DatabaseService()
    logger.info("✅ 데이터베이스 서비스 초기화 성공")
    
    # 데이터베이스 연결 테스트
    test_result = database_service.get_legislation_data(limit=1)
    logger.info(f"✅ 데이터베이스 연결 테스트 성공 - 기존 데이터: {len(test_result) if test_result else 0}건")
    
except Exception as e:
    logger.error(f"❌ 데이터베이스 연결 실패: {str(e)}")
    logger.error(f"❌ DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT_SET')[:50]}...")
    database_service = None

@app.get("/")
async def root():
    return {"message": "입법예고 수집 API 서버가 실행 중입니다."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/test-db")
async def test_database():
    """데이터베이스 연결 테스트"""
    logger.info("🔍 데이터베이스 연결 테스트 시작")
    
    if database_service is None:
        logger.error("❌ 데이터베이스 서비스가 초기화되지 않음")
        return {
            "status": "error", 
            "message": "데이터베이스 서비스가 초기화되지 않았습니다",
            "database_url": os.getenv('DATABASE_URL', 'NOT_SET')[:50] + "..."
        }
    
    try:
        # 데이터베이스 연결 테스트
        national_count = len(database_service.get_national_legislation_data(limit=1))
        admin_count = len(database_service.get_admin_legislation_data(limit=1))
        data_count = national_count + admin_count
        
        logger.info(f"✅ 데이터베이스 연결 테스트 성공 - 데이터: {data_count}건")
        
        return {
            "status": "success", 
            "message": "데이터베이스 연결 성공",
            "data_count": data_count,
            "national_count": national_count,
            "admin_count": admin_count,
            "database_url": os.getenv('DATABASE_URL', 'NOT_SET')[:50] + "..."
        }
    except Exception as e:
        logger.error(f"❌ 데이터베이스 연결 테스트 실패: {str(e)}")
        return {
            "status": "error", 
            "message": f"데이터베이스 연결 실패: {str(e)}",
            "database_url": os.getenv('DATABASE_URL', 'NOT_SET')[:50] + "..."
        }

@app.get("/api/legislation/national", response_model=LegislationResponse)
async def get_national_legislation():
    """입법부 입법예고 데이터를 가져옵니다."""
    logger.info("🏛️ 입법부 입법예고 데이터 요청 시작")
    
    try:
        if database_service is None:
            logger.error("❌ 데이터베이스 서비스가 초기화되지 않음")
            raise HTTPException(status_code=500, detail="데이터베이스 서비스가 사용 불가능합니다")
        
        # 데이터베이스에서 조회
        logger.info("📊 데이터베이스에서 입법부 데이터 조회 중...")
        data = database_service.get_national_legislation_data()
        
        if not data:
            logger.warning("⚠️ 데이터베이스에 입법부 데이터가 없음 - 실시간 크롤링 시작")
            try:
                # 데이터가 없으면 실시간 크롤링 (백업)
                data = await legislation_service.get_national_legislation()
                if data:
                    logger.info(f"💾 크롤링한 입법부 데이터 {len(data)}건을 데이터베이스에 저장 중...")
                    # 크롤링한 데이터를 데이터베이스에 저장
                    database_service.save_national_legislation_data(data)
                    logger.info("✅ 데이터베이스 저장 완료")
                else:
                    logger.error("❌ 입법부 데이터 크롤링 실패 - 데이터 없음")
                    data = []
            except Exception as crawl_error:
                logger.error(f"❌ 입법부 데이터 크롤링 오류: {str(crawl_error)}")
                data = []
        else:
            logger.info(f"✅ 데이터베이스에서 입법부 데이터 {len(data)}건 조회 성공")
        
        return LegislationResponse(
            success=True,
            message="입법부 입법예고 데이터를 성공적으로 가져왔습니다.",
            data=data,
            total_count=len(data)
        )
    except Exception as e:
        logger.error(f"❌ 입법부 데이터 수집 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"입법부 데이터 수집 중 오류가 발생했습니다: {str(e)}")

@app.get("/api/legislation/admin", response_model=LegislationResponse)
async def get_admin_legislation():
    """행정부 입법예고 데이터를 가져옵니다."""
    logger.info("🏢 행정부 입법예고 데이터 요청 시작")
    
    try:
        if database_service is None:
            logger.error("❌ 데이터베이스 서비스가 초기화되지 않음")
            raise HTTPException(status_code=500, detail="데이터베이스 서비스가 사용 불가능합니다")
        
        # 데이터베이스에서 조회
        logger.info("📊 데이터베이스에서 행정부 데이터 조회 중...")
        data = database_service.get_admin_legislation_data()
        
        if not data:
            logger.warning("⚠️ 데이터베이스에 행정부 데이터가 없음 - 실시간 크롤링 시작")
            # 데이터가 없으면 실시간 크롤링 (백업)
            data = await legislation_service.get_admin_legislation()
            if data:
                logger.info(f"💾 크롤링한 행정부 데이터 {len(data)}건을 데이터베이스에 저장 중...")
                # 크롤링한 데이터를 데이터베이스에 저장
                database_service.save_admin_legislation_data(data)
                logger.info("✅ 데이터베이스 저장 완료")
            else:
                logger.error("❌ 행정부 데이터 크롤링 실패")
        else:
            logger.info(f"✅ 데이터베이스에서 행정부 데이터 {len(data)}건 조회 성공")
        
        return LegislationResponse(
            success=True,
            message="행정부 입법예고 데이터를 성공적으로 가져왔습니다.",
            data=data,
            total_count=len(data)
        )
    except Exception as e:
        logger.error(f"❌ 행정부 데이터 수집 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"행정부 데이터 수집 중 오류가 발생했습니다: {str(e)}")

@app.get("/api/legislation/all", response_model=LegislationResponse)
async def get_all_legislation():
    """모든 입법예고 데이터를 가져옵니다."""
    logger.info("📋 모든 입법예고 데이터 요청 시작")
    
    try:
        if database_service is None:
            logger.error("❌ 데이터베이스 서비스가 초기화되지 않음")
            raise HTTPException(status_code=500, detail="데이터베이스 서비스가 사용 불가능합니다")
        
        # 데이터베이스에서 조회
        logger.info("📊 데이터베이스에서 모든 데이터 조회 중...")
        national_data = database_service.get_national_legislation_data()
        admin_data = database_service.get_admin_legislation_data()
        
        logger.info(f"📊 조회 결과 - 입법부: {len(national_data) if national_data else 0}건, 행정부: {len(admin_data) if admin_data else 0}건")
        
        # 데이터가 없으면 실시간 크롤링 (백업)
        if not national_data:
            logger.warning("⚠️ 입법부 데이터가 없음 - 실시간 크롤링 시작")
            national_data = await legislation_service.get_national_legislation()
            if national_data:
                logger.info(f"💾 크롤링한 입법부 데이터 {len(national_data)}건을 데이터베이스에 저장 중...")
                database_service.save_national_legislation_data(national_data)
                logger.info("✅ 입법부 데이터 저장 완료")
            else:
                logger.error("❌ 입법부 데이터 크롤링 실패")
                national_data = []
        
        if not admin_data:
            logger.warning("⚠️ 행정부 데이터가 없음 - 실시간 크롤링 시작")
            admin_data = await legislation_service.get_admin_legislation()
            if admin_data:
                logger.info(f"💾 크롤링한 행정부 데이터 {len(admin_data)}건을 데이터베이스에 저장 중...")
                database_service.save_admin_legislation_data(admin_data)
                logger.info("✅ 행정부 데이터 저장 완료")
            else:
                logger.error("❌ 행정부 데이터 크롤링 실패")
                admin_data = []
        
        all_data = national_data + admin_data
        logger.info(f"✅ 전체 데이터 조회 완료 - 총 {len(all_data)}건 (입법부: {len(national_data)}, 행정부: {len(admin_data)})")
        
        return LegislationResponse(
            success=True,
            message="모든 입법예고 데이터를 성공적으로 가져왔습니다.",
            data=all_data,
            total_count=len(all_data)
        )
    except Exception as e:
        logger.error(f"❌ 전체 데이터 수집 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"데이터 수집 중 오류가 발생했습니다: {str(e)}")

@app.post("/api/legislation/refresh")
async def refresh_legislation_data():
    """입법예고 데이터를 새로고침합니다."""
    logger.info("🔄 데이터 새로고침 요청 시작")
    
    try:
        if database_service is None:
            logger.error("❌ 데이터베이스 서비스가 초기화되지 않음")
            raise HTTPException(status_code=500, detail="데이터베이스 서비스가 사용 불가능합니다")
        
        # 기존 데이터 삭제 후 새로 수집
        logger.info("🗑️ 기존 데이터 삭제 중...")
        deleted_national = database_service.delete_national_legislation_data()
        deleted_admin = database_service.delete_admin_legislation_data()
        logger.info(f"🗑️ 삭제 완료 - 입법부: {deleted_national}건, 행정부: {deleted_admin}건")
        
        # 새로운 데이터 수집
        logger.info("🕷️ 새로운 데이터 수집 시작...")
        national_data = await legislation_service.get_national_legislation()
        admin_data = await legislation_service.get_admin_legislation()
        
        # 데이터베이스에 저장
        if national_data:
            logger.info(f"💾 입법부 데이터 {len(national_data)}건 저장 중...")
            database_service.save_national_legislation_data(national_data)
            logger.info("✅ 입법부 데이터 저장 완료")
        
        if admin_data:
            logger.info(f"💾 행정부 데이터 {len(admin_data)}건 저장 중...")
            database_service.save_admin_legislation_data(admin_data)
            logger.info("✅ 행정부 데이터 저장 완료")
        
        total_count = len(national_data) + len(admin_data)
        logger.info(f"✅ 데이터 새로고침 완료 - 총 {total_count}건 (입법부: {len(national_data)}, 행정부: {len(admin_data)})")
        
        return {
            "success": True,
            "message": "데이터가 성공적으로 새로고침되었습니다.",
            "national_count": len(national_data),
            "admin_count": len(admin_data),
            "total_count": total_count
        }
    except Exception as e:
        logger.error(f"❌ 데이터 새로고침 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"데이터 새로고침 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7050))
    uvicorn.run(app, host="0.0.0.0", port=port)
