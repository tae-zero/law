from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 데이터베이스 URL (Railway 환경변수에서 가져오기)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./legislation.db")

# SQLite는 Railway에서 테스트용, PostgreSQL은 프로덕션용
if DATABASE_URL.startswith("postgres"):
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LegislationDB(Base):
    """입법예고 데이터베이스 모델"""
    __tablename__ = "legislation"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_no = Column(String(50), index=True, nullable=True)  # 의안번호
    title = Column(String(500), nullable=False)  # 제목
    committee = Column(String(200), nullable=False)  # 소관위원회
    proposer = Column(String(200), nullable=True)  # 제안자
    start_date = Column(String(20), nullable=False)  # 게시시작일
    end_date = Column(String(20), nullable=False)  # 게시종료일
    content = Column(Text, nullable=True)  # 주요내용
    link_url = Column(String(500), nullable=False)  # 링크 URL
    source = Column(String(20), nullable=False, index=True)  # 출처 (national/admin)
    created_at = Column(DateTime, default=datetime.utcnow)  # 수집일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 수정일시
    is_active = Column(Boolean, default=True)  # 활성 상태
    
    # 인덱스 설정
    __table_args__ = (
        Index('idx_source_date', 'source', 'start_date'),
        Index('idx_end_date', 'end_date'),
        Index('idx_committee', 'committee'),
    )

def get_db():
    """데이터베이스 세션 생성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """테이블 생성"""
    Base.metadata.create_all(bind=engine)
