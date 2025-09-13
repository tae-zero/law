/** @type {import('next').NextConfig} */
const nextConfig = {
  // experimental.appDir은 Next.js 13.4+에서 기본값이므로 제거
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://your-railway-backend-url.railway.app',
  },
  // Vercel 배포를 위한 설정
  output: 'standalone',
  // 이미지 최적화 설정
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
