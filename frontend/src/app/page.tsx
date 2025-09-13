'use client';

import { useState, useEffect } from 'react';
import { 
  RefreshCw, 
  Building2, 
  FileText, 
  Calendar, 
  ExternalLink, 
  AlertCircle,
  TrendingUp,
  Clock,
  Users,
  BarChart3,
  Filter,
  Search,
  Download,
  Settings
} from 'lucide-react';
import { legislationApi } from '@/lib/api';
import { LegislationItem, LegislationResponse } from '@/types/legislation';
import LegislationCard from '@/components/LegislationCard';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorMessage from '@/components/ErrorMessage';
import ThemeToggle from '@/components/ThemeToggle';

export default function Home() {
  const [legislationData, setLegislationData] = useState<LegislationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [activeTab, setActiveTab] = useState<'all' | 'national' | 'admin'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const fetchData = async (type: 'all' | 'national' | 'admin' = 'all') => {
    try {
      setError(null);
      let response: LegislationResponse;
      
      switch (type) {
        case 'national':
          response = await legislationApi.getNational();
          break;
        case 'admin':
          response = await legislationApi.getAdmin();
          break;
        default:
          response = await legislationApi.getAll();
      }
      
      if (response.success) {
        setLegislationData(response.data);
      } else {
        setError(response.message);
      }
    } catch (err) {
      setError('데이터를 가져오는 중 오류가 발생했습니다.');
      console.error('데이터 가져오기 오류:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await legislationApi.refresh();
      await fetchData(activeTab);
    } catch (err) {
      setError('데이터 새로고침 중 오류가 발생했습니다.');
      console.error('새로고침 오류:', err);
    } finally {
      setRefreshing(false);
    }
  };

  const handleTabChange = (tab: 'all' | 'national' | 'admin') => {
    setActiveTab(tab);
    setLoading(true);
    fetchData(tab);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getTabCounts = () => {
    const national = legislationData.filter(item => item.source === 'national').length;
    const admin = legislationData.filter(item => item.source === 'admin').length;
    return { national, admin, total: legislationData.length };
  };

  const filteredData = legislationData.filter(item => 
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.committee.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const counts = getTabCounts();

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 via-white to-primary-50 dark:from-secondary-900 dark:via-secondary-800 dark:to-secondary-900">
      {/* 헤더 */}
      <header className="glass sticky top-0 z-50 border-b border-secondary-200/50 dark:border-secondary-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-primary rounded-xl shadow-glow">
                  <FileText className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-secondary-900 dark:text-secondary-100">
                    입법예고 수집기
                  </h1>
                  <p className="text-xs text-secondary-600 dark:text-secondary-400">
                    Law Scraper System
                  </p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* 검색 바 */}
              <div className="hidden md:block relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-secondary-400" />
                <input
                  type="text"
                  placeholder="입법예고 검색..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="input pl-10 pr-4 py-2 w-64"
                />
              </div>
              
              {/* 테마 토글 */}
              <ThemeToggle />
              
              {/* 새로고침 버튼 */}
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50"
              >
                <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                <span className="hidden sm:inline">새로고침</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 히어로 섹션 */}
        <div className="text-center mb-12 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold text-secondary-900 dark:text-secondary-100 mb-4">
            실시간 입법예고 모니터링
          </h2>
          <p className="text-lg text-secondary-600 dark:text-secondary-400 max-w-2xl mx-auto">
            국회입법예고와 행정부 입법예고를 자동으로 수집하고 분석하여 
            <span className="text-primary-600 dark:text-primary-400 font-semibold"> 정책 변화를 한눈에</span> 파악하세요
          </p>
        </div>

        {/* 통계 카드 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 animate-slide-up">
          <div className="card hover-lift group">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl shadow-glow group-hover:shadow-glow-lg transition-all duration-300">
                  <FileText className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-sm font-medium text-secondary-600 dark:text-secondary-400">전체 입법예고</p>
                  <p className="text-3xl font-bold text-secondary-900 dark:text-secondary-100">{counts.total}</p>
                </div>
              </div>
              <TrendingUp className="h-5 w-5 text-success-500" />
            </div>
          </div>
          
          <div className="card hover-lift group">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-gradient-to-r from-accent-blue to-blue-600 rounded-xl shadow-glow group-hover:shadow-glow-lg transition-all duration-300">
                  <Building2 className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-sm font-medium text-secondary-600 dark:text-secondary-400">입법부</p>
                  <p className="text-3xl font-bold text-secondary-900 dark:text-secondary-100">{counts.national}</p>
                </div>
              </div>
              <BarChart3 className="h-5 w-5 text-accent-blue" />
            </div>
          </div>
          
          <div className="card hover-lift group">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-gradient-to-r from-accent-green to-green-600 rounded-xl shadow-glow group-hover:shadow-glow-lg transition-all duration-300">
                  <Calendar className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-sm font-medium text-secondary-600 dark:text-secondary-400">행정부</p>
                  <p className="text-3xl font-bold text-secondary-900 dark:text-secondary-100">{counts.admin}</p>
                </div>
              </div>
              <Clock className="h-5 w-5 text-accent-green" />
            </div>
          </div>
        </div>

        {/* 탭 네비게이션 */}
        <div className="card mb-6 animate-slide-up">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex space-x-1 bg-secondary-100 dark:bg-secondary-800 p-1 rounded-lg flex-1">
              <button
                onClick={() => handleTabChange('all')}
                className={`flex-1 py-3 px-4 rounded-lg text-sm font-medium transition-all duration-200 ${
                  activeTab === 'all' ? 'tab-active' : 'tab-inactive'
                }`}
              >
                <div className="flex items-center justify-center space-x-2">
                  <FileText className="h-4 w-4" />
                  <span>전체</span>
                  <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-xs">
                    {counts.total}
                  </span>
                </div>
              </button>
              <button
                onClick={() => handleTabChange('national')}
                className={`flex-1 py-3 px-4 rounded-lg text-sm font-medium transition-all duration-200 ${
                  activeTab === 'national' ? 'tab-active' : 'tab-inactive'
                }`}
              >
                <div className="flex items-center justify-center space-x-2">
                  <Building2 className="h-4 w-4" />
                  <span>입법부</span>
                  <span className="px-2 py-1 bg-accent-blue/10 text-accent-blue rounded-full text-xs">
                    {counts.national}
                  </span>
                </div>
              </button>
              <button
                onClick={() => handleTabChange('admin')}
                className={`flex-1 py-3 px-4 rounded-lg text-sm font-medium transition-all duration-200 ${
                  activeTab === 'admin' ? 'tab-active' : 'tab-inactive'
                }`}
              >
                <div className="flex items-center justify-center space-x-2">
                  <Calendar className="h-4 w-4" />
                  <span>행정부</span>
                  <span className="px-2 py-1 bg-accent-green/10 text-accent-green rounded-full text-xs">
                    {counts.admin}
                  </span>
                </div>
              </button>
            </div>
            
            {/* 모바일 검색 */}
            <div className="md:hidden relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-secondary-400" />
              <input
                type="text"
                placeholder="검색..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input pl-10 pr-4 py-3 w-full"
              />
            </div>
          </div>
        </div>

        {/* 데이터 표시 영역 */}
        <div className="card animate-fade-in">
          {loading ? (
            <LoadingSpinner />
          ) : error ? (
            <ErrorMessage message={error} onRetry={() => fetchData(activeTab)} />
          ) : filteredData.length === 0 ? (
            <div className="text-center py-16">
              <div className="p-4 bg-secondary-100 dark:bg-secondary-800 rounded-full w-20 h-20 mx-auto mb-6 flex items-center justify-center">
                <AlertCircle className="h-10 w-10 text-secondary-400" />
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 dark:text-secondary-100 mb-2">
                {searchQuery ? '검색 결과가 없습니다' : '데이터가 없습니다'}
              </h3>
              <p className="text-secondary-600 dark:text-secondary-400 mb-6">
                {searchQuery 
                  ? '다른 검색어를 시도해보세요.' 
                  : '현재 수집된 입법예고 데이터가 없습니다.'
                }
              </p>
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="btn-outline"
                >
                  검색어 지우기
                </button>
              )}
            </div>
          ) : (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-secondary-900 dark:text-secondary-100">
                  입법예고 목록 ({filteredData.length}건)
                </h3>
                <div className="flex items-center space-x-2">
                  <button className="btn-ghost flex items-center space-x-2">
                    <Filter className="h-4 w-4" />
                    <span>필터</span>
                  </button>
                  <button className="btn-ghost flex items-center space-x-2">
                    <Download className="h-4 w-4" />
                    <span>내보내기</span>
                  </button>
                </div>
              </div>
              
              <div className="grid gap-4">
                {filteredData.map((item, index) => (
                  <div key={`${item.source}-${index}`} className="animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
                    <LegislationCard item={item} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
