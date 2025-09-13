export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-secondary-200 dark:border-secondary-700"></div>
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-500 border-t-transparent absolute top-0 left-0"></div>
      </div>
      <div className="mt-6 text-center">
        <p className="text-lg font-semibold text-secondary-900 dark:text-secondary-100 mb-2">
          데이터를 불러오는 중...
        </p>
        <p className="text-sm text-secondary-600 dark:text-secondary-400">
          입법예고 정보를 수집하고 있습니다
        </p>
      </div>
    </div>
  );
}
