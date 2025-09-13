'use client';

import { useState } from 'react';
import { 
  X, 
  Info, 
  Code, 
  Database, 
  Zap, 
  Users, 
  Globe, 
  Shield,
  Target,
  Rocket,
  Lightbulb,
  CheckCircle,
  ArrowRight,
  ExternalLink
} from 'lucide-react';

interface ProjectInfoModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ProjectInfoModal({ isOpen, onClose }: ProjectInfoModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative min-h-screen flex items-center justify-center p-4">
        <div className="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                  <Info className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                    입법예고 통합 수집 및 관리 시스템
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    자동화된 입법예고 데이터 수집, 저장, 시각화를 통한 민주적 참여 증진 플랫폼
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
              >
                <X className="h-6 w-6 text-gray-500 dark:text-gray-400" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="overflow-y-auto max-h-[calc(90vh-120px)] px-6 py-6">
            <div className="space-y-8">
              {/* 프로젝트 의의 */}
              <section>
                <h3 className="flex items-center text-xl font-bold text-gray-900 dark:text-white mb-4">
                  <Target className="h-5 w-5 text-blue-600 dark:text-blue-400 mr-2" />
                  프로젝트 의의
                </h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">민주적 참여 증진</h4>
                    <p className="text-sm text-blue-700 dark:text-blue-300">
                      시민들이 입법과정에 쉽게 접근할 수 있는 통합 플랫폼 제공
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <h4 className="font-semibold text-green-900 dark:text-green-100 mb-2">자동화된 데이터 관리</h4>
                    <p className="text-sm text-green-700 dark:text-green-300">
                      GitHub Actions를 통한 매일 자동 데이터 수집 및 관리
                    </p>
                  </div>
                  <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                    <h4 className="font-semibold text-purple-900 dark:text-purple-100 mb-2">접근성 향상</h4>
                    <p className="text-sm text-purple-700 dark:text-purple-300">
                      반응형 웹 디자인으로 모든 디바이스에서 최적화된 사용자 경험
                    </p>
                  </div>
                </div>
              </section>

              {/* 기술 스택 */}
              <section>
                <h3 className="flex items-center text-xl font-bold text-gray-900 dark:text-white mb-4">
                  <Code className="h-5 w-5 text-green-600 dark:text-green-400 mr-2" />
                  기술 스택
                </h3>
                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Frontend</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        Next.js 14 (App Router)
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        React 18 + TypeScript
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        Tailwind CSS
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        Lucide React
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Backend</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        FastAPI
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        PostgreSQL
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        SQLAlchemy 2.0
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        BeautifulSoup4
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-3">DevOps</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        GitHub Actions
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        Docker
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        Railway + Vercel
                      </li>
                      <li className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                        PostgreSQL
                      </li>
                    </ul>
                  </div>
                </div>
              </section>

              {/* 주요 기능 */}
              <section>
                <h3 className="flex items-center text-xl font-bold text-gray-900 dark:text-white mb-4">
                  <Zap className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mr-2" />
                  주요 기능
                </h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <h4 className="font-semibold text-gray-900 dark:text-white">자동화된 데이터 수집</h4>
                    <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                      <li>• GitHub Actions 기반 스케줄된 크롤링</li>
                      <li>• 국회/행정부 데이터 통합 수집</li>
                      <li>• 실시간 데이터베이스 업데이트</li>
                    </ul>
                  </div>
                  <div className="space-y-3">
                    <h4 className="font-semibold text-gray-900 dark:text-white">사용자 인터페이스</h4>
                    <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                      <li>• Tech-Fin 스타일 디자인 시스템</li>
                      <li>• 다크/라이트 모드 지원</li>
                      <li>• 반응형 디자인</li>
                    </ul>
                  </div>
                  <div className="space-y-3">
                    <h4 className="font-semibold text-gray-900 dark:text-white">데이터 검색 및 필터링</h4>
                    <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                      <li>• 키워드 검색 기능</li>
                      <li>• 소관위원회별 필터링</li>
                      <li>• 날짜 범위 검색</li>
                    </ul>
                  </div>
                  <div className="space-y-3">
                    <h4 className="font-semibold text-gray-900 dark:text-white">데이터 시각화</h4>
                    <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                      <li>• 실시간 통계 대시보드</li>
                      <li>• 입법예고 현황 차트</li>
                      <li>• 위원회별 분포 표시</li>
                    </ul>
                  </div>
                </div>
              </section>

              {/* 기대효과 */}
              <section>
                <h3 className="flex items-center text-xl font-bold text-gray-900 dark:text-white mb-4">
                  <Lightbulb className="h-5 w-5 text-orange-600 dark:text-orange-400 mr-2" />
                  기대효과
                </h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                    <h4 className="font-semibold text-orange-900 dark:text-orange-100 mb-2">민주적 참여 증진</h4>
                    <p className="text-sm text-orange-700 dark:text-orange-300">
                      시민들이 입법과정에 쉽게 접근하고 의견 제시 가능
                    </p>
                  </div>
                  <div className="p-4 bg-cyan-50 dark:bg-cyan-900/20 rounded-lg">
                    <h4 className="font-semibold text-cyan-900 dark:text-cyan-100 mb-2">기술적 혁신</h4>
                    <p className="text-sm text-cyan-700 dark:text-cyan-300">
                      자동화된 데이터 수집으로 수동 작업 없이 최신 데이터 보장
                    </p>
                  </div>
                  <div className="p-4 bg-pink-50 dark:bg-pink-900/20 rounded-lg">
                    <h4 className="font-semibold text-pink-900 dark:text-pink-100 mb-2">사회적 가치</h4>
                    <p className="text-sm text-pink-700 dark:text-pink-300">
                      정보 격차 해소 및 민주주의 강화
                    </p>
                  </div>
                </div>
              </section>

              {/* 향후 계획 */}
              <section>
                <h3 className="flex items-center text-xl font-bold text-gray-900 dark:text-white mb-4">
                  <Rocket className="h-5 w-5 text-purple-600 dark:text-purple-400 mr-2" />
                  향후 계획
                </h3>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
                      <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Phase 1: 기본 기능 완성</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">자동 데이터 수집 시스템 구축, 기본 웹 인터페이스 개발</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                      <ArrowRight className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Phase 2: 고도화</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">AI 기반 분석, 알림 시스템, API 확장</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
                      <ArrowRight className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">Phase 3: 확장</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">다국어 지원, 모바일 앱, 데이터 분석</p>
                    </div>
                  </div>
                </div>
              </section>

              {/* 개발자 정보 */}
              <section className="pt-6 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                      <Users className="h-5 w-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">개발자</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">@tae-zero</p>
                    </div>
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    <p>💡 민주적 참여와 투명성을 증진하기 위해 개발되었습니다.</p>
                  </div>
                </div>
              </section>
            </div>
          </div>

          {/* Footer */}
          <div className="sticky bottom-0 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                <span className="flex items-center">
                  <Shield className="h-4 w-4 mr-1" />
                  MIT License
                </span>
                <span className="flex items-center">
                  <Globe className="h-4 w-4 mr-1" />
                  Open Source
                </span>
              </div>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
