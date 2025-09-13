from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LegislationItem(BaseModel):
    """입법예고 개별 항목 모델"""
    id: Optional[str] = None
    title: str = Field(..., description="입법예고 제목")
    committee: str = Field(..., description="소관위원회")
    proposer: Optional[str] = Field(None, description="제안자")
    start_date: str = Field(..., description="게시시작일")
    end_date: str = Field(..., description="게시종료일")
    content: str = Field(..., description="주요내용")
    link_url: str = Field(..., description="링크 URL")
    bill_no: Optional[str] = Field(None, description="의안번호")
    source: str = Field(..., description="데이터 출처 (national/admin)")
    created_at: Optional[datetime] = Field(None, description="수집일시")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class LegislationResponse(BaseModel):
    """입법예고 응답 모델"""
    success: bool = Field(..., description="성공 여부")
    message: str = Field(..., description="응답 메시지")
    data: List[LegislationItem] = Field(..., description="입법예고 데이터 목록")
    total_count: int = Field(..., description="총 데이터 개수")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="응답 시간")

class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    success: bool = Field(False, description="성공 여부")
    message: str = Field(..., description="에러 메시지")
    error_code: Optional[str] = Field(None, description="에러 코드")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="에러 발생 시간")
