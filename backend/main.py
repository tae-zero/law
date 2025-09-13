from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from services.legislation_service import LegislationService
from services.database_service import DatabaseService
from models.legislation_models import LegislationResponse, LegislationItem

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
database_service = DatabaseService()

@app.get("/")
async def root():
    return {"message": "입법예고 수집 API 서버가 실행 중입니다."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/legislation/national", response_model=LegislationResponse)
async def get_national_legislation():
    """입법부 입법예고 데이터를 가져옵니다."""
    try:
        # 데이터베이스에서 조회
        data = database_service.get_legislation_by_source("national")
        
        if not data:
            # 데이터가 없으면 실시간 크롤링 (백업)
            data = await legislation_service.get_national_legislation()
            if data:
                # 크롤링한 데이터를 데이터베이스에 저장
                database_service.save_legislation_data(data)
        
        return LegislationResponse(
            success=True,
            message="입법부 입법예고 데이터를 성공적으로 가져왔습니다.",
            data=data,
            total_count=len(data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"입법부 데이터 수집 중 오류가 발생했습니다: {str(e)}")

@app.get("/api/legislation/admin", response_model=LegislationResponse)
async def get_admin_legislation():
    """행정부 입법예고 데이터를 가져옵니다."""
    try:
        # 데이터베이스에서 조회
        data = database_service.get_legislation_by_source("admin")
        
        if not data:
            # 데이터가 없으면 실시간 크롤링 (백업)
            data = await legislation_service.get_admin_legislation()
            if data:
                # 크롤링한 데이터를 데이터베이스에 저장
                database_service.save_legislation_data(data)
        
        return LegislationResponse(
            success=True,
            message="행정부 입법예고 데이터를 성공적으로 가져왔습니다.",
            data=data,
            total_count=len(data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"행정부 데이터 수집 중 오류가 발생했습니다: {str(e)}")

@app.get("/api/legislation/all", response_model=LegislationResponse)
async def get_all_legislation():
    """모든 입법예고 데이터를 가져옵니다."""
    try:
        # 데이터베이스에서 조회
        national_data = database_service.get_legislation_by_source("national")
        admin_data = database_service.get_legislation_by_source("admin")
        
        # 데이터가 없으면 실시간 크롤링 (백업)
        if not national_data:
            national_data = await legislation_service.get_national_legislation()
            if national_data:
                database_service.save_legislation_data(national_data)
        
        if not admin_data:
            admin_data = await legislation_service.get_admin_legislation()
            if admin_data:
                database_service.save_legislation_data(admin_data)
        
        all_data = national_data + admin_data
        
        return LegislationResponse(
            success=True,
            message="모든 입법예고 데이터를 성공적으로 가져왔습니다.",
            data=all_data,
            total_count=len(all_data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 수집 중 오류가 발생했습니다: {str(e)}")

@app.post("/api/legislation/refresh")
async def refresh_legislation_data():
    """입법예고 데이터를 새로고침합니다."""
    try:
        # 데이터 새로고침 로직 실행
        national_data = await legislation_service.get_national_legislation()
        admin_data = await legislation_service.get_admin_legislation()
        
        return {
            "success": True,
            "message": "데이터가 성공적으로 새로고침되었습니다.",
            "national_count": len(national_data),
            "admin_count": len(admin_data),
            "total_count": len(national_data) + len(admin_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 새로고침 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7050))
    uvicorn.run(app, host="0.0.0.0", port=port)
