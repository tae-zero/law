import { CheckCircle, Clock, AlertTriangle, XCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: 'active' | 'expired' | 'urgent' | 'pending';
  size?: 'sm' | 'md' | 'lg';
}

export default function StatusBadge({ status, size = 'md' }: StatusBadgeProps) {
  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
    lg: 'px-4 py-2 text-base'
  };

  const iconSizes = {
    sm: 'h-3 w-3',
    md: 'h-4 w-4',
    lg: 'h-5 w-5'
  };

  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'active':
        return {
          label: '진행중',
          icon: CheckCircle,
          className: 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400 border-success-200 dark:border-success-800'
        };
      case 'expired':
        return {
          label: '마감',
          icon: XCircle,
          className: 'bg-error-100 dark:bg-error-900/20 text-error-700 dark:text-error-400 border-error-200 dark:border-error-800'
        };
      case 'urgent':
        return {
          label: '긴급',
          icon: AlertTriangle,
          className: 'bg-warning-100 dark:bg-warning-900/20 text-warning-700 dark:text-warning-400 border-warning-200 dark:border-warning-800 animate-pulse'
        };
      case 'pending':
        return {
          label: '대기중',
          icon: Clock,
          className: 'bg-secondary-100 dark:bg-secondary-800 text-secondary-700 dark:text-secondary-400 border-secondary-200 dark:border-secondary-700'
        };
      default:
        return {
          label: '알 수 없음',
          icon: Clock,
          className: 'bg-secondary-100 dark:bg-secondary-800 text-secondary-700 dark:text-secondary-400 border-secondary-200 dark:border-secondary-700'
        };
    }
  };

  const config = getStatusConfig(status);
  const Icon = config.icon;

  return (
    <span className={`inline-flex items-center space-x-1.5 rounded-full border font-medium ${sizeClasses[size]} ${config.className}`}>
      <Icon className={iconSizes[size]} />
      <span>{config.label}</span>
    </span>
  );
}
