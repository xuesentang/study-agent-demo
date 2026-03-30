import axios, { AxiosError } from 'axios';
import type { ChatRequest, ChatResponse, StudyRequest, StudyResponse, ProgressResponse, Message, CozeChatRequest, CozeChatResponse, CozeConfig } from '../types';

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://localhost:8000',  // 后端API地址
  timeout: 30000,                     // 30秒超时
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API请求: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ 请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API响应: ${response.status}`, response.data);
    return response;
  },
  (error: AxiosError) => {
    console.error('❌ 响应错误:', error.message);
    
    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response;
      console.error(`状态码: ${status}`, data);
      
      if (status === 401) {
        return Promise.reject(new Error('API认证失败，请检查API Key'));
      } else if (status === 429) {
        return Promise.reject(new Error('请求过于频繁，请稍后再试'));
      } else if (status >= 500) {
        return Promise.reject(new Error('服务器错误，请稍后再试'));
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      return Promise.reject(new Error('无法连接到服务器，请检查后端是否启动'));
    }
    
    return Promise.reject(error);
  }
);

// API 方法
export const chatAPI = {
  // 发送对话消息
  async sendMessage(message: string, model: string = 'gpt-3.5-turbo'): Promise<ChatResponse> {
    const request: ChatRequest = { message, model };
    const response = await api.post<ChatResponse>('/chat', request);
    return response.data;
  },
  
  // 健康检查
  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get('/health');
    return response.data;
  },
  
  // 获取可用模型列表
  async getModels(): Promise<{ models: Array<{id: string, name: string, description: string}> }> {
    const response = await api.get('/models');
    return response.data;
  }
};

// 学习流程 API
export const studyAPI = {
  // 发送学习消息
  async sendMessage(sessionId: string, message: string): Promise<StudyResponse> {
    const request: StudyRequest = { message };
    const response = await api.post<StudyResponse>(`/study/${sessionId}`, request);
    return response.data;
  },
  
  // 获取学习进度
  async getProgress(sessionId: string): Promise<ProgressResponse> {
    const response = await api.get<ProgressResponse>(`/study/${sessionId}/progress`);
    return response.data;
  },
  
  // 重置学习进度
  async resetProgress(sessionId: string): Promise<{ message: string; session_id: string }> {
    const response = await api.delete(`/study/${sessionId}`);
    return response.data;
  }
};

// ========== Coze API（URL版，5个插件） ==========

export const cozeAPI = {
  /**
   * 使用Coze进行对话（支持工具调用，URL版）
   * 自动触发插件：联网问答、必应谷歌搜索、文档生成
   * 当消息包含URL时，自动触发：文件读取、图片理解
   */
  async sendMessage(
    message: string,
    userId: string = 'default_user',
    conversationId?: string,
    history: Message[] = []
  ): Promise<CozeChatResponse> {
    const request: CozeChatRequest = {
      message,
      user_id: userId,
      conversation_id: conversationId,
      history
    };
    const response = await api.post<CozeChatResponse>('/chat/coze', request);
    return response.data;
  },

  /**
   * 分析图片URL（使用「图片理解」插件）
   * 将图片URL包含在消息中发送
   */
  async analyzeImageUrl(
    imageUrl: string,
    question: string = '分析这张图片',
    userId: string = 'default_user',
    conversationId?: string
  ): Promise<CozeChatResponse> {
    const message = `${question}：${imageUrl}`;
    return this.sendMessage(message, userId, conversationId);
  },

  /**
   * 分析文件URL（使用「文件读取」插件）
   * 将文件URL包含在消息中发送
   */
  async analyzeFileUrl(
    fileUrl: string,
    question: string = '分析这个文档',
    userId: string = 'default_user',
    conversationId?: string
  ): Promise<CozeChatResponse> {
    const message = `${question}：${fileUrl}`;
    return this.sendMessage(message, userId, conversationId);
  },

  /**
   * 创建新会话
   */
  async createConversation(userId: string = 'default_user'): Promise<{ conversation_id: string }> {
    const response = await api.post('/coze/conversation/create', null, {
      params: { user_id: userId }
    });
    return response.data;
  },

  /**
   * 获取Coze配置
   */
  async getConfig(): Promise<CozeConfig> {
    const response = await api.get('/coze/config');
    return response.data;
  }
};

export { api };