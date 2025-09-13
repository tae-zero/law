import { LegislationItem } from '@/types/legislation';
import { Building2, Calendar, ExternalLink, Clock, User, ArrowUpRight, AlertTriangle } from 'lucide-react';

interface LegislationCardProps {
  item: LegislationItem;
}

export default function LegislationCard({ item }: LegislationCardProps) {
  const getSourceConfig = (source: string) => {
    switch (source) {
      case 'national':
        return {
          label: '입법부',
          bgColor: 'bg-accent-blue/10 dark:bg-accent-blue/20',
          textColor: 'text-accent-blue dark:text-accent-blue-300',
          borderColor: 'border-accent-blue/20 dark:border-accent-blue/30',
          icon: Building2
        };
      case 'admin':
        return {
          label: '행정부',
          bgColor: 'bg-accent-green/10 dark:bg-accent-green/20',
          textColor: 'text-accent-green dark:text-accent-green-300',
          borderColor: 'border-accent-green/20 dark:border-accent-green/30',
          icon: Calendar
        };
      default:
        return {
          label: '알 수 없음',
          bgColor: 'bg-secondary-100 dark:bg-secondary-800',
          textColor: 'text-secondary-600 dark:text-secondary-400',
          borderColor: 'border-secondary-200 dark:border-secondary-700',
          icon: Building2
        };
    }
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return '날짜 없음';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  const isExpired = (endDate: string) => {
    if (!endDate) return false;
    try {
      const end = new Date(endDate);
      const now = new Date();
      return end < now;
    } catch {
      return false;
    }
  };

  const isUrgent = (endDate: string) => {
    if (!endDate) return false;
    try {
      const end = new Date(endDate);
      const now = new Date();
      const diffDays = Math.ceil((end.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
      return diffDays <= 3 && diffDays > 0;
    } catch {
      return false;
    }
  };

  const sourceConfig = getSourceConfig(item.source);
  const SourceIcon = sourceConfig.icon;
  const expired = isExpired(item.end_date);
  const urgent = isUrgent(item.end_date);

  return (
    <div className="group relative bg-white dark:bg-secondary-800 rounded-2xl border border-secondary-200 dark:border-secondary-700 p-6 hover:shadow-medium dark:hover:shadow-hard transition-all duration-300 hover:-translate-y-1 hover:border-primary-300 dark:hover:border-primary-600">
      {/* 상태 표시 */}
      {expired && (
        <div className="absolute -top-2 -right-2 bg-error-500 text-white rounded-full p-1">
          <AlertTriangle className="h-4 w-4" />
        </div>
      )}
      {urgent && !expired && (
        <div className="absolute -top-2 -right-2 bg-warning-500 text-white rounded-full p-1 animate-pulse">
          <Clock className="h-4 w-4" />
        </div>
      )}

      {/* 헤더 */}
      <div className="flex items-start justify-between mb-6">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-3">
            <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-full text-xs font-semibold border ${sourceConfig.bgColor} ${sourceConfig.textColor} ${sourceConfig.borderColor}`}>
              <SourceIcon className="h-3 w-3" />
              <span>{sourceConfig.label}</span>
            </div>
            {item.bill_no && (
              <span className="text-xs text-secondary-500 dark:text-secondary-400 bg-secondary-100 dark:bg-secondary-700 px-2 py-1 rounded-md font-mono">
                {item.bill_no}
              </span>
            )}
          </div>
          <h3 className="text-lg font-bold text-secondary-900 dark:text-secondary-100 mb-2 line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
            {item.title}
          </h3>
        </div>
        <a
          href={item.link_url}
          target="_blank"
          rel="noopener noreferrer"
          className="ml-4 p-2 text-secondary-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20"
        >
          <ArrowUpRight className="h-5 w-5" />
        </a>
      </div>

      {/* 메타 정보 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="flex items-center space-x-3 text-sm">
          <div className="p-1.5 bg-secondary-100 dark:bg-secondary-700 rounded-lg">
            <Building2 className="h-4 w-4 text-secondary-600 dark:text-secondary-400" />
          </div>
          <span className="text-secondary-700 dark:text-secondary-300 font-medium">{item.committee}</span>
        </div>
        
        {item.proposer && (
          <div className="flex items-center space-x-3 text-sm">
            <div className="p-1.5 bg-secondary-100 dark:bg-secondary-700 rounded-lg">
              <User className="h-4 w-4 text-secondary-600 dark:text-secondary-400" />
            </div>
            <span className="text-secondary-700 dark:text-secondary-300 font-medium">{item.proposer}</span>
          </div>
        )}
        
        <div className="flex items-center space-x-3 text-sm">
          <div className="p-1.5 bg-secondary-100 dark:bg-secondary-700 rounded-lg">
            <Calendar className="h-4 w-4 text-secondary-600 dark:text-secondary-400" />
          </div>
          <span className="text-secondary-700 dark:text-secondary-300">
            <span className="text-secondary-500 dark:text-secondary-400">시작:</span> {formatDate(item.start_date)}
          </span>
        </div>
        
        <div className="flex items-center space-x-3 text-sm">
          <div className="p-1.5 bg-secondary-100 dark:bg-secondary-700 rounded-lg">
            <Clock className="h-4 w-4 text-secondary-600 dark:text-secondary-400" />
          </div>
          <span className={`font-medium ${expired ? 'text-error-600 dark:text-error-400' : urgent ? 'text-warning-600 dark:text-warning-400' : 'text-secondary-700 dark:text-secondary-300'}`}>
            <span className="text-secondary-500 dark:text-secondary-400">종료:</span> {formatDate(item.end_date)}
            {expired && ' (마감)'}
            {urgent && !expired && ' (긴급)'}
          </span>
        </div>
      </div>

      {/* 내용 */}
      {item.content && (
        <div className="mb-6">
          <p className="text-sm text-secondary-600 dark:text-secondary-400 line-clamp-3 leading-relaxed">
            {item.content}
          </p>
        </div>
      )}

      {/* 액션 버튼 */}
      <div className="flex items-center justify-between pt-4 border-t border-secondary-200 dark:border-secondary-700">
        <div className="flex items-center space-x-4">
          <a
            href={item.link_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-2 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm font-semibold transition-colors group/link"
          >
            <span>자세히 보기</span>
            <ExternalLink className="h-4 w-4 group-hover/link:translate-x-0.5 group-hover/link:-translate-y-0.5 transition-transform" />
          </a>
        </div>
        
        <div className="flex items-center space-x-2">
          {expired && (
            <span className="px-2 py-1 bg-error-100 dark:bg-error-900/20 text-error-700 dark:text-error-400 text-xs font-medium rounded-full">
              마감
            </span>
          )}
          {urgent && !expired && (
            <span className="px-2 py-1 bg-warning-100 dark:bg-warning-900/20 text-warning-700 dark:text-warning-400 text-xs font-medium rounded-full animate-pulse">
              긴급
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
