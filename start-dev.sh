#!/bin/bash

echo "입법예고 수집기 개발 서버 시작 중..."

echo ""
echo "백엔드 서버 시작 중..."
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo ""
echo "프론트엔드 서버 시작 중..."
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "서버가 시작되었습니다!"
echo "백엔드: http://localhost:8000"
echo "프론트엔드: http://localhost:3000"
echo ""
echo "종료하려면 Ctrl+C를 누르세요"

# 프로세스 종료 시 자식 프로세스도 함께 종료
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
