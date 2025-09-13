'use client';

import { Moon, Sun, Monitor } from 'lucide-react';
import { useTheme } from '@/contexts/ThemeContext';

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const themes = [
    { value: 'light', label: '라이트', icon: Sun },
    { value: 'dark', label: '다크', icon: Moon },
    { value: 'system', label: '시스템', icon: Monitor },
  ] as const;

  return (
    <div className="relative">
      <div className="flex items-center space-x-1 bg-secondary-100 dark:bg-secondary-800 rounded-lg p-1">
        {themes.map(({ value, label, icon: Icon }) => (
          <button
            key={value}
            onClick={() => setTheme(value)}
            className={`
              flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200
              ${theme === value
                ? 'bg-white dark:bg-secondary-700 text-primary-600 dark:text-primary-400 shadow-sm'
                : 'text-secondary-600 dark:text-secondary-400 hover:text-secondary-900 dark:hover:text-secondary-100 hover:bg-secondary-200 dark:hover:bg-secondary-700'
              }
            `}
            title={`${label} 모드`}
          >
            <Icon className="h-4 w-4" />
            <span className="hidden sm:inline">{label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
