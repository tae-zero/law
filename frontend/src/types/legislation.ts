export interface LegislationItem {
  id?: string;
  title: string;
  committee: string;
  proposer?: string;
  start_date: string;
  end_date: string;
  content: string;
  link_url: string;
  bill_no?: string;
  source: 'national' | 'admin';
  created_at?: string;
}

export interface LegislationResponse {
  success: boolean;
  message: string;
  data: LegislationItem[];
  total_count: number;
  timestamp?: string;
}

export interface ErrorResponse {
  success: false;
  message: string;
  error_code?: string;
  timestamp?: string;
}
