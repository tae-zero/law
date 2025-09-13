import axios from 'axios';
import { LegislationResponse, ErrorResponse } from '@/types/legislation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5분 타임아웃 (크롤링 시간 고려)
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API 요청: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API 요청 오류:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API 응답: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API 응답 오류:', error);
    return Promise.reject(error);
  }
);

export const legislationApi = {
  // 입법부 입법예고 데이터 가져오기
  getNational: async (): Promise<LegislationResponse> => {
    const response = await apiClient.get('/api/legislation/national');
    return response.data;
  },

  // 행정부 입법예고 데이터 가져오기
  getAdmin: async (): Promise<LegislationResponse> => {
    const response = await apiClient.get('/api/legislation/admin');
    return response.data;
  },

  // 모든 입법예고 데이터 가져오기
  getAll: async (): Promise<LegislationResponse> => {
    const response = await apiClient.get('/api/legislation/all');
    return response.data;
  },

  // 데이터 새로고침
  refresh: async (): Promise<{
    success: boolean;
    message: string;
    national_count: number;
    admin_count: number;
    total_count: number;
  }> => {
    const response = await apiClient.post('/api/legislation/refresh');
    return response.data;
  },

  // 헬스 체크
  healthCheck: async (): Promise<{ status: string; timestamp: string }> => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
