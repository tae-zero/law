import { AlertCircle, RefreshCw, Wifi, WifiOff } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="text-center py-16">
      <div className="relative mb-6">
        <div className="p-4 bg-error-100 dark:bg-error-900/20 rounded-full w-20 h-20 mx-auto flex items-center justify-center">
          <AlertCircle className="h-10 w-10 text-error-500" />
        </div>
        <div className="absolute -top-2 -right-2 p-2 bg-error-500 rounded-full">
          <WifiOff className="h-4 w-4 text-white" />
        </div>
      </div>
      
      <div className="max-w-md mx-auto">
        <h3 className="text-xl font-bold text-secondary-900 dark:text-secondary-100 mb-3">
          오류가 발생했습니다
        </h3>
        <p className="text-secondary-600 dark:text-secondary-400 mb-6 leading-relaxed">
          {message}
        </p>
        
        {onRetry && (
          <div className="space-y-4">
            <button
              onClick={onRetry}
              className="btn-primary inline-flex items-center space-x-2"
            >
              <RefreshCw className="h-4 w-4" />
              <span>다시 시도</span>
            </button>
            
            <div className="text-xs text-secondary-500 dark:text-secondary-400">
              <p>문제가 지속되면 다음을 확인해주세요:</p>
              <ul className="mt-2 space-y-1 text-left">
                <li>• 인터넷 연결 상태</li>
                <li>• 서버 상태</li>
                <li>• 잠시 후 다시 시도</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
