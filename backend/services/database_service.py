from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from datetime import datetime, timedelta
from models.database import NationalLegislationDB, AdminLegislationDB, get_db
from models.legislation_models import LegislationItem
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.db = next(get_db())
    
    def save_national_legislation_data(self, items: List[LegislationItem]) -> int:
        """입법부 입법예고 데이터를 데이터베이스에 저장"""
        try:
            saved_count = 0
            
            for item in items:
                # 기존 데이터 확인 (의안번호로 중복 체크)
                existing = self.db.query(NationalLegislationDB).filter(
                    NationalLegislationDB.bill_no == item.bill_no
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
                    new_item = NationalLegislationDB(
                        bill_no=item.bill_no,
                        title=item.title,
                        committee=item.committee,
                        proposer=item.proposer,
                        start_date=item.start_date,
                        end_date=item.end_date,
                        content=item.content,
                        link_url=item.link_url,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                        is_active=True
                    )
                    self.db.add(new_item)
                
                saved_count += 1
            
            self.db.commit()
            logger.info(f"입법부 데이터 {saved_count}건 저장 완료")
            return saved_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"입법부 데이터 저장 오류: {e}")
            return 0
    
    def save_admin_legislation_data(self, items: List[LegislationItem]) -> int:
        """행정부 입법예고 데이터를 데이터베이스에 저장"""
        try:
            saved_count = 0
            
            for item in items:
                # 기존 데이터 확인 (의안번호로 중복 체크)
                existing = self.db.query(AdminLegislationDB).filter(
                    AdminLegislationDB.bill_no == item.bill_no
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
                    new_item = AdminLegislationDB(
                        bill_no=item.bill_no,
                        title=item.title,
                        committee=item.committee,
                        proposer=item.proposer,
                        start_date=item.start_date,
                        end_date=item.end_date,
                        content=item.content,
                        link_url=item.link_url,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                        is_active=True
                    )
                    self.db.add(new_item)
                
                saved_count += 1
            
            self.db.commit()
            logger.info(f"행정부 데이터 {saved_count}건 저장 완료")
            return saved_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"행정부 데이터 저장 오류: {e}")
            return 0
    
    def get_national_legislation_data(self, limit: int = 100) -> List[LegislationItem]:
        """입법부 입법예고 데이터 조회"""
        try:
            items = self.db.query(NationalLegislationDB).filter(
                NationalLegislationDB.is_active == True
            ).order_by(desc(NationalLegislationDB.created_at)).limit(limit).all()
            
            result = []
            for item in items:
                result.append(LegislationItem(
                    id=str(item.id),
                    bill_no=item.bill_no,
                    title=item.title,
                    committee=item.committee,
                    proposer=item.proposer,
                    start_date=item.start_date,
                    end_date=item.end_date,
                    content=item.content,
                    link_url=item.link_url,
                    source='national',
                    created_at=item.created_at.isoformat() if item.created_at else None
                ))
            
            logger.info(f"입법부 데이터 {len(result)}건 조회 완료")
            return result
            
        except Exception as e:
            logger.error(f"입법부 데이터 조회 오류: {e}")
            return []
    
    def get_admin_legislation_data(self, limit: int = 100) -> List[LegislationItem]:
        """행정부 입법예고 데이터 조회"""
        try:
            items = self.db.query(AdminLegislationDB).filter(
                AdminLegislationDB.is_active == True
            ).order_by(desc(AdminLegislationDB.created_at)).limit(limit).all()
            
            result = []
            for item in items:
                result.append(LegislationItem(
                    id=str(item.id),
                    bill_no=item.bill_no,
                    title=item.title,
                    committee=item.committee,
                    proposer=item.proposer,
                    start_date=item.start_date,
                    end_date=item.end_date,
                    content=item.content,
                    link_url=item.link_url,
                    source='admin',
                    created_at=item.created_at.isoformat() if item.created_at else None
                ))
            
            logger.info(f"행정부 데이터 {len(result)}건 조회 완료")
            return result
            
        except Exception as e:
            logger.error(f"행정부 데이터 조회 오류: {e}")
            return []
    
    def get_all_legislation_data(self, limit: int = 200) -> List[LegislationItem]:
        """모든 입법예고 데이터 조회 (입법부 + 행정부)"""
        try:
            national_data = self.get_national_legislation_data(limit // 2)
            admin_data = self.get_admin_legislation_data(limit // 2)
            
            all_data = national_data + admin_data
            # 생성일시 기준으로 정렬
            all_data.sort(key=lambda x: x.created_at or '', reverse=True)
            
            logger.info(f"전체 데이터 {len(all_data)}건 조회 완료 (입법부: {len(national_data)}, 행정부: {len(admin_data)})")
            return all_data
            
        except Exception as e:
            logger.error(f"전체 데이터 조회 오류: {e}")
            return []
    
    def delete_national_legislation_data(self) -> int:
        """입법부 데이터 삭제"""
        try:
            deleted_count = self.db.query(NationalLegislationDB).delete()
            self.db.commit()
            logger.info(f"입법부 데이터 {deleted_count}건 삭제 완료")
            return deleted_count
        except Exception as e:
            self.db.rollback()
            logger.error(f"입법부 데이터 삭제 오류: {e}")
            return 0
    
    def delete_admin_legislation_data(self) -> int:
        """행정부 데이터 삭제"""
        try:
            deleted_count = self.db.query(AdminLegislationDB).delete()
            self.db.commit()
            logger.info(f"행정부 데이터 {deleted_count}건 삭제 완료")
            return deleted_count
        except Exception as e:
            self.db.rollback()
            logger.error(f"행정부 데이터 삭제 오류: {e}")
            return 0
    
    def search_legislation(self, keyword: str, source: Optional[str] = None) -> List[LegislationItem]:
        """입법예고 검색"""
        try:
            if source == 'national':
                return self._search_national_legislation(keyword)
            elif source == 'admin':
                return self._search_admin_legislation(keyword)
            else:
                # 전체 검색
                national_results = self._search_national_legislation(keyword)
                admin_results = self._search_admin_legislation(keyword)
                all_results = national_results + admin_results
                all_results.sort(key=lambda x: x.created_at or '', reverse=True)
                return all_results
                
        except Exception as e:
            logger.error(f"검색 오류: {e}")
            return []
    
    def _search_national_legislation(self, keyword: str) -> List[LegislationItem]:
        """입법부 데이터 검색"""
        try:
            items = self.db.query(NationalLegislationDB).filter(
                and_(
                    NationalLegislationDB.is_active == True,
                    or_(
                        NationalLegislationDB.title.contains(keyword),
                        NationalLegislationDB.committee.contains(keyword),
                        NationalLegislationDB.content.contains(keyword)
                    )
                )
            ).order_by(desc(NationalLegislationDB.created_at)).all()
            
            result = []
            for item in items:
                result.append(LegislationItem(
                    id=str(item.id),
                    bill_no=item.bill_no,
                    title=item.title,
                    committee=item.committee,
                    proposer=item.proposer,
                    start_date=item.start_date,
                    end_date=item.end_date,
                    content=item.content,
                    link_url=item.link_url,
                    source='national',
                    created_at=item.created_at.isoformat() if item.created_at else None
                ))
            
            return result
        except Exception as e:
            logger.error(f"입법부 검색 오류: {e}")
            return []
    
    def _search_admin_legislation(self, keyword: str) -> List[LegislationItem]:
        """행정부 데이터 검색"""
        try:
            items = self.db.query(AdminLegislationDB).filter(
                and_(
                    AdminLegislationDB.is_active == True,
                    or_(
                        AdminLegislationDB.title.contains(keyword),
                        AdminLegislationDB.committee.contains(keyword),
                        AdminLegislationDB.content.contains(keyword)
                    )
                )
            ).order_by(desc(AdminLegislationDB.created_at)).all()
            
            result = []
            for item in items:
                result.append(LegislationItem(
                    id=str(item.id),
                    bill_no=item.bill_no,
                    title=item.title,
                    committee=item.committee,
                    proposer=item.proposer,
                    start_date=item.start_date,
                    end_date=item.end_date,
                    content=item.content,
                    link_url=item.link_url,
                    source='admin',
                    created_at=item.created_at.isoformat() if item.created_at else None
                ))
            
            return result
        except Exception as e:
            logger.error(f"행정부 검색 오류: {e}")
            return []
    
    def cleanup_old_data(self, days: int = 30):
        """오래된 데이터 정리 (N일 이전 데이터 비활성화)"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=days)
            
            # 입법부 데이터 정리
            old_national = self.db.query(NationalLegislationDB).filter(
                and_(
                    NationalLegislationDB.is_active == True,
                    NationalLegislationDB.created_at < cutoff_time
                )
            ).all()
            
            for item in old_national:
                item.is_active = False
                item.updated_at = datetime.utcnow()
            
            # 행정부 데이터 정리
            old_admin = self.db.query(AdminLegislationDB).filter(
                and_(
                    AdminLegislationDB.is_active == True,
                    AdminLegislationDB.created_at < cutoff_time
                )
            ).all()
            
            for item in old_admin:
                item.is_active = False
                item.updated_at = datetime.utcnow()
            
            self.db.commit()
            logger.info(f"오래된 데이터 정리 완료 - 입법부: {len(old_national)}건, 행정부: {len(old_admin)}건")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"데이터 정리 오류: {e}")
    
    def close(self):
        """데이터베이스 연결 종료"""
        self.db.close()