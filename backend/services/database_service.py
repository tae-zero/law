from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from datetime import datetime, timedelta
from models.database import LegislationDB, get_db
from models.legislation_models import LegislationItem
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.db = next(get_db())
    
    def save_legislation_data(self, items: List[LegislationItem]) -> int:
        """입법예고 데이터를 데이터베이스에 저장"""
        try:
            saved_count = 0
            
            for item in items:
                # 기존 데이터 확인 (의안번호와 출처로 중복 체크)
                existing = self.db.query(LegislationDB).filter(
                    and_(
                        LegislationDB.bill_no == item.bill_no,
                        LegislationDB.source == item.source
                    )
                ).first()
                
                if existing:
                    # 기존 데이터 업데이트
                    existing.title = item.title
                    existing.committee = item.committee
                    existing.proposer = item.proposer
                    existing.start_date = item.start_date
                    existing.end_date = item.end_date
                    existing.content = item.content
                    existing.link_url = item.link_url
                    existing.updated_at = datetime.utcnow()
                    existing.is_active = True
                else:
                    # 새 데이터 삽입
                    new_item = LegislationDB(
                        bill_no=item.bill_no,
                        title=item.title,
                        committee=item.committee,
                        proposer=item.proposer,
                        start_date=item.start_date,
                        end_date=item.end_date,
                        content=item.content,
                        link_url=item.link_url,
                        source=item.source,
                        created_at=item.created_at or datetime.utcnow()
                    )
                    self.db.add(new_item)
                
                saved_count += 1
            
            self.db.commit()
            logger.info(f"데이터베이스 저장 완료: {saved_count}건")
            return saved_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"데이터베이스 저장 오류: {e}")
            raise e
    
    def get_legislation_data(self, source: Optional[str] = None, limit: int = 100) -> List[LegislationItem]:
        """입법예고 데이터 조회"""
        try:
            query = self.db.query(LegislationDB).filter(LegislationDB.is_active == True)
            
            if source:
                query = query.filter(LegislationDB.source == source)
            
            # 최신 데이터부터 정렬
            db_items = query.order_by(desc(LegislationDB.created_at)).limit(limit).all()
            
            # LegislationItem으로 변환
            items = []
            for db_item in db_items:
                item = LegislationItem(
                    id=str(db_item.id),
                    bill_no=db_item.bill_no,
                    title=db_item.title,
                    committee=db_item.committee,
                    proposer=db_item.proposer,
                    start_date=db_item.start_date,
                    end_date=db_item.end_date,
                    content=db_item.content,
                    link_url=db_item.link_url,
                    source=db_item.source,
                    created_at=db_item.created_at
                )
                items.append(item)
            
            return items
            
        except Exception as e:
            logger.error(f"데이터 조회 오류: {e}")
            return []
    
    def get_recent_data(self, hours: int = 24) -> List[LegislationItem]:
        """최근 N시간 내 데이터 조회"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            db_items = self.db.query(LegislationDB).filter(
                and_(
                    LegislationDB.is_active == True,
                    LegislationDB.created_at >= cutoff_time
                )
            ).order_by(desc(LegislationDB.created_at)).all()
            
            items = []
            for db_item in db_items:
                item = LegislationItem(
                    id=str(db_item.id),
                    bill_no=db_item.bill_no,
                    title=db_item.title,
                    committee=db_item.committee,
                    proposer=db_item.proposer,
                    start_date=db_item.start_date,
                    end_date=db_item.end_date,
                    content=db_item.content,
                    link_url=db_item.link_url,
                    source=db_item.source,
                    created_at=db_item.created_at
                )
                items.append(item)
            
            return items
            
        except Exception as e:
            logger.error(f"최근 데이터 조회 오류: {e}")
            return []
    
    def search_legislation(self, keyword: str, source: Optional[str] = None) -> List[LegislationItem]:
        """입법예고 검색"""
        try:
            query = self.db.query(LegislationDB).filter(
                and_(
                    LegislationDB.is_active == True,
                    or_(
                        LegislationDB.title.contains(keyword),
                        LegislationDB.committee.contains(keyword),
                        LegislationDB.content.contains(keyword)
                    )
                )
            )
            
            if source:
                query = query.filter(LegislationDB.source == source)
            
            db_items = query.order_by(desc(LegislationDB.created_at)).all()
            
            items = []
            for db_item in db_items:
                item = LegislationItem(
                    id=str(db_item.id),
                    bill_no=db_item.bill_no,
                    title=db_item.title,
                    committee=db_item.committee,
                    proposer=db_item.proposer,
                    start_date=db_item.start_date,
                    end_date=db_item.end_date,
                    content=db_item.content,
                    link_url=db_item.link_url,
                    source=db_item.source,
                    created_at=db_item.created_at
                )
                items.append(item)
            
            return items
            
        except Exception as e:
            logger.error(f"검색 오류: {e}")
            return []
    
    def get_statistics(self) -> dict:
        """통계 정보 조회"""
        try:
            total_count = self.db.query(LegislationDB).filter(LegislationDB.is_active == True).count()
            national_count = self.db.query(LegislationDB).filter(
                and_(LegislationDB.is_active == True, LegislationDB.source == "national")
            ).count()
            admin_count = self.db.query(LegislationDB).filter(
                and_(LegislationDB.is_active == True, LegislationDB.source == "admin")
            ).count()
            
            return {
                "total": total_count,
                "national": national_count,
                "admin": admin_count
            }
            
        except Exception as e:
            logger.error(f"통계 조회 오류: {e}")
            return {"total": 0, "national": 0, "admin": 0}
    
    def delete_legislation_by_source(self, source: str) -> int:
        """특정 출처의 모든 데이터 삭제"""
        try:
            deleted_count = self.db.query(LegislationDB).filter(
                LegislationDB.source == source
            ).delete()
            
            self.db.commit()
            logger.info(f"{source} 데이터 {deleted_count}건 삭제 완료")
            return deleted_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"{source} 데이터 삭제 오류: {e}")
            return 0
    
    def cleanup_old_data(self, days: int = 30):
        """오래된 데이터 정리 (N일 이전 데이터 비활성화)"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=days)
            
            old_items = self.db.query(LegislationDB).filter(
                and_(
                    LegislationDB.is_active == True,
                    LegislationDB.created_at < cutoff_time
                )
            ).all()
            
            for item in old_items:
                item.is_active = False
                item.updated_at = datetime.utcnow()
            
            self.db.commit()
            logger.info(f"오래된 데이터 정리 완료: {len(old_items)}건")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"데이터 정리 오류: {e}")
    
    def close(self):
        """데이터베이스 연결 종료"""
        self.db.close()
