# 입법예고 수집 시스템

자동으로 국회입법예고와 행정부 입법예고를 수집하고 관리하는 풀스택 웹 애플리케이션입니다.

## 🚀 기술 스택

### Frontend
- **Next.js 14** (App Router)
- **React 18** + **TypeScript**
- **Tailwind CSS** (Tech-Fin 스타일 디자인 시스템)
- **다크 모드** 지원
- **Vercel** 배포

### Backend
- **FastAPI** (Python)
- **PostgreSQL** (Railway)
- **Selenium** + **BeautifulSoup4** (웹 스크래핑)
- **SQLAlchemy** (ORM)
- **Railway** 배포

## 📁 프로젝트 구조

```
law/
├── frontend/                 # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/             # App Router 페이지
│   │   ├── components/      # React 컴포넌트
│   │   └── contexts/        # React Context
│   ├── public/              # 정적 파일
│   └── package.json
├── backend/                 # FastAPI 백엔드
│   ├── models/              # Pydantic & SQLAlchemy 모델
│   ├── services/            # 비즈니스 로직
│   ├── main.py             # FastAPI 앱
│   └── requirements.txt
├── law-scraper/            # 기존 스크래핑 코드
└── README.md
```

## 🎨 UI/UX 특징

- **Tech-Fin 스타일 디자인 시스템**
- **다크/라이트 모드** 자동 전환
- **반응형 디자인**
- **실시간 데이터 업데이트**
- **직관적인 검색 및 필터링**

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

## 📊 데이터 수집

### 국회입법예고
- **API**: 국회입법예고 공개 API
- **웹 스크래핑**: 국회입법예고 웹사이트
- **수집 주기**: 실시간

### 행정부 입법예고
- **웹 스크래핑**: 행정부 입법예고 웹사이트
- **수집 주기**: 실시간

## 🗄️ 데이터베이스

- **PostgreSQL** (Railway)
- **테이블**: `legislations`
- **필드**: 제목, 소관위원회, 제안자, 게시일, 내용, 링크 등

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

- ✅ **실시간 입법예고 수집**
- ✅ **국회/행정부 데이터 통합**
- ✅ **검색 및 필터링**
- ✅ **다크 모드 지원**
- ✅ **반응형 디자인**
- ✅ **자동 데이터 새로고침**

## 🚀 배포 URL

- **Frontend**: [Vercel 배포 URL]
- **Backend**: [Railway 배포 URL]
- **도메인**: [가비아 도메인]

## 📄 라이선스

MIT License

## 👨‍💻 개발자

[@tae-zero](https://github.com/tae-zero)