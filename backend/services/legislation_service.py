import asyncio
import os
from datetime import datetime, timedelta
from typing import List
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import requests
import time

from models.legislation_models import LegislationItem
from services.web_scraper import WebScraper

class LegislationService:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLY_API_KEY", "자신의 국회입법예고 API KEY")
        self.base_url = "https://open.assembly.go.kr/portal/openapi/nknalejkafmvgzmpt"
        self.web_scraper = WebScraper()
        
    async def get_national_legislation(self) -> List[LegislationItem]:
        """입법부 입법예고 데이터를 수집합니다."""
        try:
            # API 데이터 수집
            api_data = await self._collect_api_data()
            
            # requests + BeautifulSoup로 크롤링 (더 빠르고 안정적)
            web_data = self.web_scraper.get_national_legislation_data()
            
            # 데이터 통합
            combined_data = self._combine_data_new(api_data, web_data)
            
            return combined_data
        except Exception as e:
            print(f"입법부 데이터 수집 오류: {e}")
            return []
    
    async def get_admin_legislation(self) -> List[LegislationItem]:
        """행정부 입법예고 데이터를 수집합니다."""
        try:
            # requests + BeautifulSoup로 크롤링 (더 빠르고 안정적)
            web_data = self.web_scraper.get_admin_legislation_data()
            
            # 데이터를 LegislationItem으로 변환
            return self._convert_admin_data_to_items(web_data)
        except Exception as e:
            print(f"행정부 데이터 수집 오류: {e}")
            return []
    
    async def _collect_api_data(self) -> dict:
        """API를 통해 입법부 데이터를 수집합니다."""
        api_data = {}
        page = 1
        
        # 어제 날짜 계산
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        yesterday_dash = yesterday.strftime("%Y-%m-%d")
        
        while True:
            params = {
                "KEY": self.api_key,
                "Type": "json",
                "pIndex": page,
                "pSize": 100
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            rows = data.get("nknalejkafmvgzmpt", [None, {}])[1].get("row", [])
            
            if not rows:
                break
                
            for bill in rows:
                noti_st_dt = bill.get("NOTI_ST_DT", "")
                if noti_st_dt != yesterday_dash:
                    continue
                    
                bill_no = bill.get("BILL_NO")
                api_data[bill_no] = {
                    "의안번호": bill_no,
                    "제목": bill.get("BILL_NAME", ""),
                    "링크": bill.get("LINK_URL", ""),
                    "소관위": bill.get("CURR_COMMITTEE", ""),
                    "제안자": bill.get("PROPOSER", ""),
                    "게시종료일": bill.get("NOTI_ED_DT", ""),
                    "내용요약": "(내용 없음)"
                }
            
            page += 1
            
        return api_data
    
    async def _collect_selenium_data(self) -> List[dict]:
        """Selenium을 통해 상세 정보를 수집합니다."""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        wait = WebDriverWait(driver, 10)
        
        combined_rows = []
        
        try:
            list_url = "https://pal.assembly.go.kr/napal/lgsltpa/lgsltpaOngoing/list.do?searchConClosed=0&menuNo=1100026"
            driver.get(list_url)
            
            current_page = 1
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            yesterday_dash = yesterday.strftime("%Y-%m-%d")
            
            while True:
                wait.until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    "#frm > div > div.board01.pr.td_center.board-added > table > tbody > tr"
                )))
                
                links = driver.find_elements(By.CSS_SELECTOR,
                    "#frm > div > div.board01.pr.td_center.board-added > table > tbody > tr > td.align_left.td_block > a"
                )
                
                if not links:
                    break
                
                for i in range(len(links)):
                    links = driver.find_elements(By.CSS_SELECTOR,
                        "#frm > div > div.board01.pr.td_center.board-added > table > tbody > tr > td.align_left.td_block > a"
                    )
                    
                    try:
                        driver.execute_script("arguments[0].click();", links[i])
                        time.sleep(2)
                        
                        # 의안번호 추출
                        try:
                            elem = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((
                                    By.XPATH, 
                                    '/html/body/div[4]/div/div[4]/table/tbody/tr/td[1]'
                                ))
                            )
                            bill_no = elem.get_attribute("innerText").strip()
                        except:
                            bill_no = "(없음)"
                        
                        # 제목 추출
                        try:
                            raw_title = driver.find_element(
                                By.CSS_SELECTOR, 
                                "#content > div.legislation-heading > h3"
                            ).text.strip()
                            if "]" in raw_title and "(" in raw_title:
                                title = raw_title.split("]")[-1].split("(")[0].strip()
                            else:
                                title = raw_title
                        except:
                            title = "(제목 없음)"
                        
                        # 제안자 추출
                        try:
                            proposer = driver.find_element(
                                By.CSS_SELECTOR,
                                '#content > div.board01.pr.td_center.board-added > table > tbody > tr > td:nth-child(2)'
                            ).text.strip()
                        except:
                            proposer = "(제안자 없음)"
                        
                        # 소관위 추출
                        try:
                            committee = driver.find_element(
                                By.CSS_SELECTOR,
                                '#content > div.board01.pr.td_center.board-added > table > tbody > tr > td.td_block'
                            ).text.strip()
                        except:
                            committee = "(소관위 없음)"
                        
                        # 게시기간 추출
                        try:
                            period_element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((
                                    By.CSS_SELECTOR,
                                    '#content > div.board01.pr.td_center.board-added > table > tbody > tr > td:nth-child(6)'
                                ))
                            )
                            period_text = period_element.text.strip()
                            
                            noti_range = period_text.split("~")
                            noti_st_dt = noti_range[0].strip() if len(noti_range) >= 1 else ""
                            noti_ed_dt = noti_range[1].strip() if len(noti_range) >= 2 else ""
                            
                            if noti_st_dt != yesterday_dash:
                                driver.back()
                                time.sleep(1)
                                continue
                        except Exception as e:
                            noti_st_dt = ""
                            noti_ed_dt = ""
                        
                        # 내용 추출
                        try:
                            content = driver.find_element(
                                By.CSS_SELECTOR, 
                                "#content > div.card-wrap > div:nth-child(1) > div"
                            ).text.strip()
                            summary = content
                        except:
                            summary = "(내용 없음)"
                        
                        row = {
                            "의안번호": bill_no,
                            "제목": title,
                            "제안자": proposer,
                            "소관위": committee,
                            "링크": driver.current_url,
                            "게시종료일": noti_ed_dt,
                            "내용요약": summary,
                            "게시시작일": noti_st_dt
                        }
                        combined_rows.append(row)
                        
                    except Exception as e:
                        print(f"크롤링 에러: {e}")
                    
                    driver.back()
                    time.sleep(2)
                
                current_page += 1
                try:
                    driver.execute_script("fnSearch(arguments[0])", current_page)
                    time.sleep(2)
                except Exception as e:
                    break
                    
        finally:
            driver.quit()
        
        return combined_rows
    
    async def _collect_admin_data(self) -> List[LegislationItem]:
        """행정부 입법예고 데이터를 수집합니다."""
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        wait = WebDriverWait(driver, 10)
        
        results = []
        
        try:
            url = "https://opinion.lawmaking.go.kr/gcom/ogLmPp"
            driver.get(url)
            page_number = 1
            
            # 어제 날짜 계산
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            yesterday_dash = yesterday.strftime("%Y-%m-%d")
            today_date = today.date()
            
            while True:
                time.sleep(2)
                wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#listView > ul"))
                )
                link_elements = driver.find_elements(
                    By.CSS_SELECTOR, "#listView > ul > li.title.W40 > a"
                )
                
                for i in range(len(link_elements)):
                    wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "#listView > ul")
                        )
                    )
                    link_elements = driver.find_elements(
                        By.CSS_SELECTOR, "#listView > ul > li.title.W40 > a"
                    )
                    if i >= len(link_elements):
                        break
                    
                    link = link_elements[i]
                    try:
                        driver.execute_script("arguments[0].click();", link)
                    except:
                        time.sleep(2)
                        try:
                            driver.execute_script("arguments[0].click();", link)
                        except:
                            continue
                    
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ogLmPpVo")))
                    
                    # 제목 추출
                    try:
                        title = driver.find_element(
                            By.CSS_SELECTOR,
                            "#ogLmPpVo > div:nth-child(7) > div > p:nth-child(8) > span",
                        ).text.strip()
                    except:
                        title = "제목 없음"
                    
                    # 소관위 추출
                    try:
                        committee_raw = driver.find_element(
                            By.CSS_SELECTOR,
                            "#ogLmPpVo > ul.basic > li:nth-child(2) > table > tbody > tr > td",
                        ).text.strip()
                        committee = committee_raw.split("전화번호")[0].strip()
                    except:
                        committee = "소관위 없음"
                    
                    # 게시기간 추출
                    try:
                        period_raw = driver.find_element(
                            By.CSS_SELECTOR, "#ogLmPpVo > ul.basic > li:nth-child(1)"
                        ).text.strip()
                        match = re.search(
                            r"(\d{4})[.\- ]\s*(\d{1,2})[.\- ]\s*(\d{1,2})[.]?\s*~\s*(\d{4})[.\- ]\s*(\d{1,2})[.\- ]\s*(\d{1,2})",
                            period_raw,
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
                        else:
                            start_date, end_date = None, None
                    except Exception as e:
                        start_date, end_date = None, None
                    
                    if not start_date or start_date.strftime("%Y-%m-%d") != yesterday_dash:
                        driver.back()
                        time.sleep(2)
                        continue
                    
                    if end_date and end_date < today_date:
                        driver.back()
                        time.sleep(2)
                        continue
                    
                    # 내용 추출
                    try:
                        content_raw = driver.find_element(
                            By.CSS_SELECTOR, "#ogLmPpVo > div:nth-child(7) > div"
                        ).text.strip()
                        content = self._extract_until_opinion(content_raw)
                    except:
                        content = "내용 없음"
                    
                    # 링크 추출
                    try:
                        link_element = driver.find_element(
                            By.CSS_SELECTOR, "#ogLmPpVo > ul:nth-child(2) > a:nth-child(2)"
                        )
                        link_url = link_element.get_attribute("href").strip()
                    except:
                        link_url = "링크 없음"
                    
                    results.append(LegislationItem(
                        title=title,
                        committee=committee,
                        proposer="",
                        start_date=start_date.strftime("%Y-%m-%d") if start_date else "",
                        end_date=end_date.strftime("%Y-%m-%d") if end_date else "",
                        content=content,
                        link_url=link_url,
                        source="admin",
                        created_at=datetime.now()
                    ))
                    
                    driver.back()
                    time.sleep(2)
                
                # 페이지네이션
                try:
                    pagination = driver.find_elements(By.CSS_SELECTOR, "#nav > ol > li")
                    next_clicked = False
                    for li in pagination:
                        a_tags = li.find_elements(By.TAG_NAME, "a")
                        if a_tags and a_tags[0].text.strip() == str(page_number + 1):
                            driver.execute_script("arguments[0].click();", a_tags[0])
                            page_number += 1
                            next_clicked = True
                            break
                    if not next_clicked:
                        break
                except Exception as e:
                    break
                    
        finally:
            driver.quit()
        
        return results
    
    def _extract_until_opinion(self, text: str) -> str:
        """의견제출 이전까지 내용만 추출"""
        cut_keywords = ["3. 의견제출", "의견제출", "※ 제출의견", "의견 제출"]
        for key in cut_keywords:
            if key in text:
                return text.split(key)[0].strip()
        return text.strip()
    
    def _combine_data(self, api_data: dict, selenium_data: List[dict]) -> List[LegislationItem]:
        """API 데이터와 Selenium 데이터를 통합합니다."""
        combined_items = []
        
        # API 데이터 처리
        for bill_no, info in api_data.items():
            combined_items.append(LegislationItem(
                bill_no=bill_no,
                title=info["제목"],
                committee=info["소관위"],
                proposer=info["제안자"],
                start_date="",  # API에서 제공하지 않음
                end_date=info["게시종료일"],
                content=info["내용요약"],
                link_url=info["링크"],
                source="national",
                created_at=datetime.now()
            ))
        
        # Selenium 데이터 처리 (API에 없는 것만)
        for row in selenium_data:
            bill_no = row["의안번호"]
            if bill_no not in api_data:
                combined_items.append(LegislationItem(
                    bill_no=bill_no,
                    title=row["제목"],
                    committee=row["소관위"],
                    proposer=row["제안자"],
                    start_date=row["게시시작일"],
                    end_date=row["게시종료일"],
                    content=row["내용요약"],
                    link_url=row["링크"],
                    source="national",
                    created_at=datetime.now()
                ))
        
        return combined_items
    
    def _combine_data_new(self, api_data: dict, web_data: List[dict]) -> List[LegislationItem]:
        """API 데이터와 웹 스크래핑 데이터를 통합합니다 (새로운 방식)"""
        combined_items = []
        
        # API 데이터 처리
        for bill_no, info in api_data.items():
            combined_items.append(LegislationItem(
                bill_no=bill_no,
                title=info["제목"],
                committee=info["소관위"],
                proposer=info["제안자"],
                start_date="",  # API에서 제공하지 않음
                end_date=info["게시종료일"],
                content=info["내용요약"],
                link_url=info["링크"],
                source="national",
                created_at=datetime.now()
            ))
        
        # 웹 스크래핑 데이터 처리 (API에 없는 것만)
        for row in web_data:
            bill_no = row["의안번호"]
            if bill_no not in api_data:
                combined_items.append(LegislationItem(
                    bill_no=bill_no,
                    title=row["제목"],
                    committee=row["소관위"],
                    proposer=row["제안자"],
                    start_date=row["게시시작일"],
                    end_date=row["게시종료일"],
                    content=row["내용요약"],
                    link_url=row["링크"],
                    source="national",
                    created_at=datetime.now()
                ))
        
        return combined_items
    
    def _convert_admin_data_to_items(self, web_data: List[dict]) -> List[LegislationItem]:
        """행정부 웹 스크래핑 데이터를 LegislationItem으로 변환"""
        items = []
        
        for row in web_data:
            items.append(LegislationItem(
                title=row["title"],
                committee=row["committee"],
                proposer=row["proposer"],
                start_date=row["start_date"],
                end_date=row["end_date"],
                content=row["content"],
                link_url=row["link_url"],
                source=row["source"],
                created_at=datetime.now()
            ))
        
        return items
