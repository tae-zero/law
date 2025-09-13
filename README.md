# 📋 입법예고 통합 수집 및 관리 시스템

**자동화된 입법예고 데이터 수집, 저장, 시각화를 통한 민주적 참여 증진 플랫폼**

국회입법예고와 행정부 입법예고를 실시간으로 수집하고, 직관적인 웹 인터페이스를 통해 시민들이 쉽게 접근할 수 있는 통합 플랫폼입니다. GitHub Actions를 활용한 자동화된 데이터 수집과 PostgreSQL 기반의 안정적인 데이터 관리로 신뢰할 수 있는 입법정보 서비스를 제공합니다.

## 🎯 프로젝트 의의

### 📊 **민주적 참여 증진**
- 시민들이 입법과정에 쉽게 접근할 수 있는 통합 플랫폼 제공
- 복잡한 정부 웹사이트 대신 직관적인 인터페이스로 입법예고 정보 제공
- 실시간 데이터 업데이트로 최신 입법동향 파악 가능

### 🔄 **자동화된 데이터 관리**
- GitHub Actions를 통한 매일 자동 데이터 수집 (오전 9시: 행정부, 10시: 입법부)
- 기존 데이터 자동 삭제 후 신규 데이터 저장으로 데이터 신선도 보장
- PostgreSQL 기반 안정적인 데이터 저장 및 관리

### 🌐 **접근성 향상**
- 반응형 웹 디자인으로 모든 디바이스에서 최적화된 사용자 경험
- 다크/라이트 모드 지원으로 사용자 선호도 반영
- 검색, 필터링, 정렬 기능으로 원하는 정보 빠른 검색

## 🚀 기술 스택

### Frontend
- **Next.js 14** (App Router) - 최신 React 프레임워크
- **React 18** + **TypeScript** - 타입 안전성과 개발 생산성
- **Tailwind CSS** - Tech-Fin 스타일 디자인 시스템
- **Lucide React** - 일관된 아이콘 시스템
- **Axios** - HTTP 클라이언트
- **Context API** - 상태 관리 (다크모드)
- **Vercel** - 자동 배포 및 CDN

### Backend
- **FastAPI** - 고성능 Python 웹 프레임워크
- **PostgreSQL** (Railway) - 안정적인 관계형 데이터베이스
- **SQLAlchemy 2.0** - 현대적 ORM
- **Selenium** + **BeautifulSoup4** - 웹 스크래핑
- **Requests** - HTTP 라이브러리
- **Pydantic** - 데이터 검증 및 직렬화
- **Railway** - 클라우드 배포

### DevOps & Automation
- **GitHub Actions** - CI/CD 및 스케줄된 작업
- **Docker** - 컨테이너화
- **Railway** - 백엔드 호스팅
- **Vercel** - 프론트엔드 호스팅
- **PostgreSQL** - 데이터베이스 호스팅

## 📁 프로젝트 구조

```
law/
├── frontend/                    # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/                # App Router 페이지
│   │   │   ├── globals.css     # 글로벌 스타일
│   │   │   ├── layout.tsx      # 루트 레이아웃
│   │   │   └── page.tsx        # 메인 페이지
│   │   ├── components/         # React 컴포넌트
│   │   │   ├── LegislationCard.tsx
│   │   │   ├── ThemeToggle.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── contexts/           # React Context
│   │   │   └── ThemeContext.tsx
│   │   ├── lib/                # 유틸리티
│   │   │   └── api.ts          # API 클라이언트
│   │   └── types/              # TypeScript 타입
│   │       └── legislation.ts
│   ├── public/                 # 정적 파일
│   ├── package.json
│   ├── tailwind.config.js      # Tailwind 설정
│   └── vercel.json            # Vercel 배포 설정
├── backend/                    # FastAPI 백엔드
│   ├── models/                 # 데이터 모델
│   │   ├── database.py         # SQLAlchemy 모델
│   │   └── legislation_models.py # Pydantic 모델
│   ├── services/               # 비즈니스 로직
│   │   ├── legislation_service.py # 입법예고 수집 로직
│   │   ├── database_service.py    # 데이터베이스 서비스
│   │   └── web_scraper.py         # 웹 스크래핑
│   ├── main.py                 # FastAPI 애플리케이션
│   ├── requirements.txt        # Python 의존성
│   ├── Dockerfile             # Docker 설정
│   └── railway.json           # Railway 배포 설정
├── .github/                    # GitHub Actions
│   └── workflows/
│       ├── admin.yml          # 행정부 데이터 수집 (매일 9시)
│       └── national.yml       # 입법부 데이터 수집 (매일 10시)
├── law-scraper/               # 기존 스크래핑 코드
├── scheduled_crawler.py       # 스케줄된 크롤링 스크립트
└── README.md
```

## 🎨 UI/UX 특징

### 🎯 **Tech-Fin 스타일 디자인 시스템**
- 금융/기술 분야의 전문적이고 신뢰할 수 있는 디자인
- 일관된 색상 팔레트와 타이포그래피
- 깔끔하고 직관적인 레이아웃

### 🌓 **다크/라이트 모드 지원**
- 사용자 선호도에 따른 테마 자동 전환
- 시스템 설정 기반 자동 감지
- 부드러운 전환 애니메이션

### 📱 **반응형 디자인**
- 모바일, 태블릿, 데스크톱 모든 기기 최적화
- 터치 친화적인 인터페이스
- 유연한 그리드 시스템

### ⚡ **실시간 데이터 업데이트**
- 자동 새로고침 기능
- 로딩 상태 표시
- 에러 처리 및 사용자 피드백

### 🔍 **고급 검색 및 필터링**
- 키워드 검색
- 소관위원회별 필터링
- 날짜 범위 검색
- 정렬 기능 (최신순, 제목순 등)

## 🔧 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/tae-zero/law-scraper.git
cd law-scraper
```

### 2. 백엔드 설정
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# .env 파일에 필요한 환경변수 설정
uvicorn main:app --reload
```

### 3. 프론트엔드 설정
```bash
cd frontend
npm install
npm run dev
```

## 🌐 배포

### Railway (백엔드)
1. Railway에 GitHub 저장소 연결
2. 환경변수 설정 (`DATABASE_URL`, `ASSEMBLY_API_KEY` 등)
3. 자동 배포 완료

### Vercel (프론트엔드)
1. Vercel에 GitHub 저장소 연결
2. 환경변수 설정 (`NEXT_PUBLIC_API_URL`)
3. 자동 배포 완료

## 📊 데이터 수집 시스템

### 🏛️ **국회입법예고**
- **API 수집**: 국회입법예고 공개 API 활용
- **웹 스크래핑**: 국회입법예고 웹사이트 (requests + BeautifulSoup)
- **수집 주기**: 매일 오전 10시 (KST)
- **데이터 처리**: API + 웹 스크래핑 데이터 통합

### 🏢 **행정부 입법예고**
- **웹 스크래핑**: 행정부 입법예고 웹사이트
- **수집 주기**: 매일 오전 9시 (KST)
- **데이터 처리**: BeautifulSoup 기반 HTML 파싱

### 🔄 **자동화 프로세스**
1. **GitHub Actions** 스케줄 실행
2. **기존 데이터 삭제** (소스별)
3. **새 데이터 수집** (API + 웹 스크래핑)
4. **데이터베이스 저장** (PostgreSQL)
5. **API 서버 알림** (새로고침)

## 🗄️ 데이터베이스 설계

### **PostgreSQL (Railway)**
- **테이블**: `legislations`
- **인덱스**: 소스별, 날짜별, 위원회별 최적화

### **데이터 스키마**
```sql
CREATE TABLE legislations (
    id SERIAL PRIMARY KEY,
    bill_no VARCHAR(50),           -- 법안번호
    title VARCHAR(500) NOT NULL,   -- 제목
    committee VARCHAR(200) NOT NULL, -- 소관위원회
    proposer VARCHAR(200),         -- 제안자
    start_date VARCHAR(20) NOT NULL, -- 게시일
    end_date VARCHAR(20) NOT NULL,   -- 마감일
    content TEXT,                  -- 내용
    link_url VARCHAR(500) NOT NULL, -- 원문 링크
    source VARCHAR(20) NOT NULL,   -- 출처 (national/admin)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### **데이터 관리**
- **일일 갱신**: 기존 데이터 삭제 후 신규 데이터 저장
- **데이터 검증**: Pydantic 모델을 통한 타입 검증
- **백업**: Railway 자동 백업 시스템 활용

## 🔑 환경변수

### Backend (.env)
```
ASSEMBLY_API_KEY=your_assembly_api_key
DATABASE_URL=postgresql://username:password@host:port/database
ENVIRONMENT=production
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

## 📱 주요 기능

### 🔄 **자동화된 데이터 수집**
- ✅ **GitHub Actions** 기반 스케줄된 크롤링
- ✅ **국회/행정부 데이터 통합** 수집
- ✅ **실시간 데이터베이스** 업데이트
- ✅ **에러 처리 및 로깅** 시스템

### 🎨 **사용자 인터페이스**
- ✅ **Tech-Fin 스타일** 디자인 시스템
- ✅ **다크/라이트 모드** 지원
- ✅ **반응형 디자인** (모바일/태블릿/데스크톱)
- ✅ **직관적인 네비게이션**

### 🔍 **데이터 검색 및 필터링**
- ✅ **키워드 검색** 기능
- ✅ **소관위원회별** 필터링
- ✅ **날짜 범위** 검색
- ✅ **정렬 기능** (최신순, 제목순 등)

### 📊 **데이터 시각화**
- ✅ **실시간 통계** 대시보드
- ✅ **입법예고 현황** 차트
- ✅ **위원회별 분포** 표시
- ✅ **트렌드 분석** 기능

### 🛡️ **안정성 및 성능**
- ✅ **PostgreSQL** 기반 안정적 데이터 저장
- ✅ **FastAPI** 고성능 API 서버
- ✅ **Docker** 컨테이너화
- ✅ **자동 배포** (Railway + Vercel)

## 🎯 기대효과

### 📈 **민주적 참여 증진**
- **시민 접근성 향상**: 복잡한 정부 웹사이트 대신 직관적인 인터페이스 제공
- **투명성 증대**: 입법과정에 대한 실시간 정보 제공
- **참여 활성화**: 시민들이 입법예고에 쉽게 접근하고 의견 제시 가능

### 🔧 **기술적 혁신**
- **자동화된 데이터 수집**: 수동 작업 없이 매일 최신 데이터 보장
- **확장 가능한 아키텍처**: 모듈화된 구조로 기능 확장 용이
- **클라우드 네이티브**: 현대적인 클라우드 기술 스택 활용

### 🌐 **사회적 가치**
- **정보 격차 해소**: 모든 시민이 동등하게 입법정보에 접근
- **정책 이해도 향상**: 시각화된 데이터로 정책 이해 용이
- **민주주의 강화**: 투명하고 접근 가능한 입법정보 제공

## 🚀 배포 URL

- **Frontend**: [Vercel 배포 URL]
- **Backend**: [Railway 배포 URL]  
- **도메인**: [가비아 도메인]

## 🔮 향후 계획

### Phase 1: 기본 기능 완성 ✅
- 자동 데이터 수집 시스템 구축
- 기본 웹 인터페이스 개발
- 데이터베이스 설계 및 구축

### Phase 2: 고도화 (예정)
- **AI 기반 분석**: 입법예고 내용 자동 분석 및 요약
- **알림 시스템**: 관심 키워드 기반 실시간 알림
- **API 확장**: 외부 서비스 연동을 위한 공개 API

### Phase 3: 확장 (예정)
- **다국어 지원**: 영어, 중국어 등 다국어 인터페이스
- **모바일 앱**: React Native 기반 모바일 애플리케이션
- **데이터 분석**: 입법 트렌드 분석 및 예측 서비스

## 📄 라이선스

MIT License

## 👨‍💻 개발자

[@tae-zero](https://github.com/tae-zero)

---

**💡 이 프로젝트는 민주적 참여와 투명성을 증진하기 위해 개발되었습니다.**