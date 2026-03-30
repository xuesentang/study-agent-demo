// 消息类型
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
  isLoading?: boolean;
}

// API 请求类型
export interface ChatRequest {
  message: string;
  model?: string;
}

// API 响应类型
export interface ChatResponse {
  reply: string;
  model: string;
  tokens_used: number;
}

// 应用状态
export interface AppState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

// 学习流程类型
export interface StudyProgress {
  completed: number;
  total: number;
  percentage: number;
  current_state: string;
  elapsed_time: number;
}

export interface KeyPoint {
  id: string;
  name: string;
  content: string;
  question: string;
  answer: string;
  hint: string;
  difficulty: string;
}

export interface ChainPoint {
  id: string;
  name: string;
  content: string;
  next_connection: string;
}

export interface Chapter {
  id: string;
  title: string;
  description: string;
  estimated_time: number;
  chain_points: ChainPoint[];
  keypoints: KeyPoint[];
}

export interface StudyResponse {
  type: string;
  content: string;
  progress?: StudyProgress;
  data?: {
    chapter?: Chapter;
    keypoint?: KeyPoint;
    chain_point?: ChainPoint;
    report?: {
      chapter: string;
      completed: number;
      total: number;
      accuracy: number;
      elapsed_time: number;
      wrong_attempts: Record<string, number>;
    };
  };
}

export interface StudyRequest {
  message: string;
}

export interface ProgressResponse {
  session_id: string;
  state: string;
  progress: StudyProgress;
  elapsed_time: number;
}

// 应用模式
export type AppMode = 'chat' | 'study';

// ========== Coze工具调用类型（URL版，5个插件） ==========

/** Coze对话请求 */
export interface CozeChatRequest {
  message: string;
  user_id?: string;
  conversation_id?: string;
  history?: Message[];
}

/** Coze对话响应 */
export interface CozeChatResponse {
  reply: string;
  conversation_id?: string;
  tool_calls: Array<{
    tool: string;
    content: string;
  }>;
  model: string;
}

/** Coze配置信息 */
export interface CozeConfig {
  bot_id: string;
  status: 'configured' | 'not_configured';
  message: string;
  features: string[];
  plugins: string[];
  note?: string;
}