import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_national_legislation_data(self) -> List[Dict]:
        """입법부 입법예고 데이터를 requests + BeautifulSoup로 수집"""
        try:
            # 어제 날짜 계산
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            yesterday_dash = yesterday.strftime("%Y-%m-%d")
            
            logger.info(f"입법부 데이터 수집 시작 - 대상 날짜: {yesterday_dash}")
            
            # 1단계: 목록 페이지에서 링크 수집
            list_url = "https://pal.assembly.go.kr/napal/lgsltpa/lgsltpaOngoing/list.do?searchConClosed=0&menuNo=1100026"
            
            all_links = []
            page = 1
            
            while True:
                logger.info(f"목록 페이지 {page} 수집 중...")
                
                # 페이지별 데이터 요청
                params = {
                    'searchConClosed': '0',
                    'menuNo': '1100026',
                    'pIndex': page,
                    'pSize': '20'
                }
                
                response = self.session.get(list_url, params=params, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 테이블에서 링크 추출
                table_rows = soup.select('#frm > div > div.board01.pr.td_center.board-added > table > tbody > tr')
                
                if not table_rows:
                    logger.info(f"페이지 {page}에서 데이터 없음 - 수집 종료")
                    break
                
                page_links = []
                for row in table_rows:
                    link_elem = row.select_one('td.align_left.td_block > a')
                    if link_elem:
                        href = link_elem.get('href')
                        if href:
                            # 상대 URL을 절대 URL로 변환
                            if href.startswith('/'):
                                full_url = f"https://pal.assembly.go.kr{href}"
                            else:
                                full_url = href
                            page_links.append(full_url)
                
                if not page_links:
                    break
                    
                all_links.extend(page_links)
                logger.info(f"페이지 {page}에서 {len(page_links)}개 링크 수집")
                
                page += 1
                time.sleep(1)  # 요청 간격 조절
                
                # 최대 10페이지까지만 수집 (안전장치)
                if page > 10:
                    break
            
            logger.info(f"총 {len(all_links)}개 링크 수집 완료")
            
            # 2단계: 각 상세 페이지에서 데이터 추출
            results = []
            for i, detail_url in enumerate(all_links):
                try:
                    logger.info(f"상세 페이지 {i+1}/{len(all_links)} 처리 중: {detail_url}")
                    
                    detail_data = self._scrape_national_detail_page(detail_url, yesterday_dash)
                    if detail_data:
                        results.append(detail_data)
                        
                    time.sleep(0.5)  # 요청 간격 조절
                    
                except Exception as e:
                    logger.error(f"상세 페이지 처리 오류 ({detail_url}): {e}")
                    continue
            
            logger.info(f"입법부 데이터 수집 완료 - 총 {len(results)}건")
            return results
            
        except Exception as e:
            logger.error(f"입법부 데이터 수집 중 오류: {e}")
            return []
    
    def _scrape_national_detail_page(self, url: str, target_date: str) -> Optional[Dict]:
        """입법부 상세 페이지에서 데이터 추출"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 의안번호 추출 - CSS 선택자 사용
            bill_no_elem = soup.select_one('table tbody tr td:first-child')
            if not bill_no_elem:
                # 대안 선택자
                bill_no_elem = soup.select_one('.board01 table tbody tr td:first-child')
            bill_no = bill_no_elem.get_text(strip=True) if bill_no_elem else "(없음)"
            
            # 제목 추출 - 더 일반적인 선택자 사용
            title_elem = soup.select_one('h3, .legislation-heading h3, .board-title h3')
            if not title_elem:
                title_elem = soup.select_one('h1, h2, .title')
            if title_elem:
                raw_title = title_elem.get_text(strip=True)
                if "]" in raw_title and "(" in raw_title:
                    title = raw_title.split("]")[-1].split("(")[0].strip()
                else:
                    title = raw_title
            else:
                title = "(제목 없음)"
            
            # 제안자 추출 - 테이블에서 찾기
            proposer_elem = soup.select_one('table tbody tr td:nth-child(2), .board01 table tbody tr td:nth-child(2)')
            if not proposer_elem:
                proposer_elem = soup.select_one('table tr td:contains("제안자"), table tr td:contains("발의자")')
            proposer = proposer_elem.get_text(strip=True) if proposer_elem else "(제안자 없음)"
            
            # 소관위 추출
            committee_elem = soup.select_one('table tbody tr td.td_block, .board01 table tbody tr td.td_block')
            if not committee_elem:
                committee_elem = soup.select_one('table tr td:contains("소관위"), table tr td:contains("위원회")')
            committee = committee_elem.get_text(strip=True) if committee_elem else "(소관위 없음)"
            
            # 게시기간 추출
            period_elem = soup.select_one('table tbody tr td:nth-child(6), .board01 table tbody tr td:nth-child(6)')
            if not period_elem:
                period_elem = soup.select_one('table tr td:contains("~"), table tr td:contains("게시")')
            if period_elem:
                period_text = period_elem.get_text(strip=True)
                if "~" in period_text:
                    noti_range = period_text.split("~")
                    noti_st_dt = noti_range[0].strip() if len(noti_range) >= 1 else ""
                    noti_ed_dt = noti_range[1].strip() if len(noti_range) >= 2 else ""
                else:
                    noti_st_dt = period_text.strip()
                    noti_ed_dt = period_text.strip()
                
                # 대상 날짜와 일치하지 않으면 None 반환
                if noti_st_dt != target_date:
                    return None
            else:
                noti_st_dt = target_date
                noti_ed_dt = target_date
            
            # 내용 추출 - 더 일반적인 선택자
            content_elem = soup.select_one('.card-wrap div, .content div, .board-content div')
            if not content_elem:
                content_elem = soup.select_one('div:contains("내용"), div:contains("요약")')
            content = content_elem.get_text(strip=True) if content_elem else "(내용 없음)"
            
            return {
                "의안번호": bill_no,
                "제목": title,
                "제안자": proposer,
                "소관위": committee,
                "링크": url,
                "게시종료일": noti_ed_dt,
                "내용요약": content,
                "게시시작일": noti_st_dt
            }
            
        except Exception as e:
            logger.error(f"상세 페이지 파싱 오류 ({url}): {e}")
            return None
    
    def get_admin_legislation_data(self) -> List[Dict]:
        """행정부 입법예고 데이터를 requests + BeautifulSoup로 수집"""
        try:
            # 어제 날짜 계산
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            yesterday_dash = yesterday.strftime("%Y-%m-%d")
            today_date = today.date()
            
            logger.info(f"행정부 데이터 수집 시작 - 대상 날짜: {yesterday_dash}")
            
            results = []
            page = 1
            
            while True:
                logger.info(f"행정부 페이지 {page} 수집 중...")
                
                # 행정부 입법예고 목록 페이지
                url = "https://opinion.lawmaking.go.kr/gcom/ogLmPp"
                params = {
                    'pIndex': page,
                    'pSize': '20'
                }
                
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 목록에서 링크 추출
                list_items = soup.select('#listView > ul > li.title.W40 > a')
                
                if not list_items:
                    logger.info(f"페이지 {page}에서 데이터 없음 - 수집 종료")
                    break
                
                page_results = []
                for link_elem in list_items:
                    try:
                        href = link_elem.get('href')
                        if href:
                            # 상대 URL을 절대 URL로 변환
                            if href.startswith('/'):
                                detail_url = f"https://opinion.lawmaking.go.kr{href}"
                            else:
                                detail_url = href
                            
                            detail_data = self._scrape_admin_detail_page(detail_url, yesterday_dash, today_date)
                            if detail_data:
                                page_results.append(detail_data)
                                
                    except Exception as e:
                        logger.error(f"행정부 링크 처리 오류: {e}")
                        continue
                
                if not page_results:
                    break
                    
                results.extend(page_results)
                logger.info(f"페이지 {page}에서 {len(page_results)}건 수집")
                
                page += 1
                time.sleep(1)  # 요청 간격 조절
                
                # 최대 5페이지까지만 수집 (성능 최적화)
                if page > 5:
                    break
            
            logger.info(f"행정부 데이터 수집 완료 - 총 {len(results)}건")
            return results
            
        except Exception as e:
            logger.error(f"행정부 데이터 수집 중 오류: {e}")
            return []
    
    def _scrape_admin_detail_page(self, url: str, target_date: str, today_date) -> Optional[Dict]:
        """행정부 상세 페이지에서 데이터 추출"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 제목 추출 - 더 일반적인 선택자
            title_elem = soup.select_one('#ogLmPpVo span, .title span, h1, h2, h3')
            if not title_elem:
                title_elem = soup.select_one('p span, div span')
            title = title_elem.get_text(strip=True) if title_elem else "제목 없음"
            
            # 소관위 추출 - 더 일반적인 선택자
            committee_elem = soup.select_one('ul.basic li table tbody tr td, .basic li table td')
            if not committee_elem:
                committee_elem = soup.select_one('table td:contains("부서"), table td:contains("과")')
            if committee_elem:
                committee_raw = committee_elem.get_text(strip=True)
                committee = committee_raw.split("전화번호")[0].strip()
            else:
                committee = "소관위 없음"
            
            # 게시기간 추출 - 더 일반적인 선택자
            period_elem = soup.select_one('ul.basic li:first-child, .basic li:first-child')
            if not period_elem:
                period_elem = soup.select_one('li:contains("게시"), li:contains("기간")')
            if period_elem:
                period_text = period_elem.get_text(strip=True)
                match = re.search(
                    r"(\d{4})[.\- ]\s*(\d{1,2})[.\- ]\s*(\d{1,2})[.]?\s*~\s*(\d{4})[.\- ]\s*(\d{1,2})[.\- ]\s*(\d{1,2})",
                    period_text,
                )
                if match:
                    start_date = datetime.strptime(
                        f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}",
                        "%Y-%m-%d",
                    ).date()
                    end_date = datetime.strptime(
                        f"{match.group(4)}-{int(match.group(5)):02d}-{int(match.group(6)):02d}",
                        "%Y-%m-%d",
                    ).date()
                    
                    # 대상 날짜와 일치하지 않으면 None 반환
                    if start_date.strftime("%Y-%m-%d") != target_date:
                        return None
                    
                    # 마감된 건은 제외
                    if end_date < today_date:
                        return None
                else:
                    return None
            else:
                return None
            
            # 내용 추출
            content_elem = soup.select_one('#ogLmPpVo > div:nth-child(7) > div')
            if content_elem:
                content_raw = content_elem.get_text(strip=True)
                content = self._extract_until_opinion(content_raw)
            else:
                content = "내용 없음"
            
            # 링크 추출
            link_elem = soup.select_one('#ogLmPpVo > ul:nth-child(2) > a:nth-child(2)')
            link_url = link_elem.get('href', '').strip() if link_elem else "링크 없음"
            
            return {
                "title": title,
                "committee": committee,
                "proposer": "",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "content": content,
                "link_url": link_url,
                "source": "admin"
            }
            
        except Exception as e:
            logger.error(f"행정부 상세 페이지 파싱 오류 ({url}): {e}")
            return None
    
    def _extract_until_opinion(self, text: str) -> str:
        """의견제출 이전까지 내용만 추출"""
        cut_keywords = ["3. 의견제출", "의견제출", "※ 제출의견", "의견 제출"]
        for key in cut_keywords:
            if key in text:
                return text.split(key)[0].strip()
        return text.strip()
    
    def close(self):
        """세션 종료"""
        self.session.close()
