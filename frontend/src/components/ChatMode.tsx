import { useState, useRef, useEffect } from 'react';
import { chatAPI, cozeAPI } from '../services/api';
import type { Message, CozeConfig } from '../types';
import '../App.css';

interface ChatModeProps {
  sessionId: string;
  onSwitchMode: () => void;
}

function ChatMode({ sessionId, onSwitchMode }: ChatModeProps) {
  // 状态管理
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState('qwen-max');
  
  // Coze相关状态
  const [useCoze, setUseCoze] = useState(true);
  const [cozeConversationId, setCozeConversationId] = useState<string | undefined>();
  const [cozeConfig, setCozeConfig] = useState<CozeConfig | null>(null);
  const [urlInput, setUrlInput] = useState('');
  const [showUrlInput, setShowUrlInput] = useState(false);
  const [urlType, setUrlType] = useState<'image' | 'file'>('image');
  
  // 滚动到底部
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // 组件挂载时获取Coze配置
  useEffect(() => {
    cozeAPI.getConfig().then(config => {
      setCozeConfig(config);
      if (config.status === 'not_configured') {
        setUseCoze(false);
      }
    }).catch(() => {
      setUseCoze(false);
    });
  }, []);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // 自动聚焦输入框
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // 生成唯一ID
  const generateId = () => {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  };

  // 发送消息
  const handleSendMessage = async () => {
    const trimmedInput = inputValue.trim();
    if (!trimmedInput || isLoading) return;
    
    // 清除错误
    setError(null);
    
    // 添加用户消息
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: trimmedInput,
      timestamp: Date.now()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    // 添加加载中的AI消息
    const loadingMessage: Message = {
      id: generateId(),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      isLoading: true
    };
    
    setMessages(prev => [...prev, loadingMessage]);
    
    try {
      let response;
      
      if (useCoze && cozeConfig?.status === 'configured') {
        // 使用Coze（自动调用插件）
        response = await cozeAPI.sendMessage(
          trimmedInput,
          sessionId,
          cozeConversationId,
          messages
        );
        
        if (response.conversation_id) {
          setCozeConversationId(response.conversation_id);
        }
        
        // 构建回复内容
        let content = response.reply;
        
        // 如果有工具调用，添加提示
        if (response.tool_calls && response.tool_calls.length > 0) {
          content += '\n\n---\n**使用的插件：**\n';
          response.tool_calls.forEach((call, index) => {
            content += `\n${index + 1}. ${call.tool} ✅`;
          });
        }
        
        // 更新AI消息
        setMessages(prev => 
          prev.map(msg => 
            msg.id === loadingMessage.id
              ? {
                  ...msg,
                  content: content,
                  isLoading: false
                }
              : msg
          )
        );
      } else {
        // 使用原有OpenAI方式
        response = await chatAPI.sendMessage(trimmedInput, selectedModel);
        
        // 更新AI消息
        setMessages(prev => 
          prev.map(msg => 
            msg.id === loadingMessage.id
              ? {
                  ...msg,
                  content: response.reply,
                  isLoading: false
                }
              : msg
          )
        );
      }
    } catch (err) {
      // 处理错误
      const errorMessage = err instanceof Error ? err.message : '发生未知错误';
      setError(errorMessage);
      
      // 移除加载消息，添加错误消息
      setMessages(prev => 
        prev.map(msg => 
          msg.id === loadingMessage.id
            ? {
                ...msg,
                content: `❌ ${errorMessage}`,
                isLoading: false
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  // 处理键盘事件
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // 清空对话
  const handleClearChat = () => {
    if (confirm('确定要清空所有对话吗？')) {
      setMessages([]);
      setError(null);
      setCozeConversationId(undefined);
    }
  };

  // 处理URL分析（图片或文件）
  const handleUrlAnalysis = async () => {
    if (!urlInput.trim()) {
      setError('请输入URL');
      return;
    }

    if (cozeConfig?.status !== 'configured') {
      setError('Coze未配置，无法使用URL分析功能');
      return;
    }

    setIsLoading(true);
    setError(null);

    const typeLabel = urlType === 'image' ? '图片' : '文件';
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: `[${typeLabel}URL] ${urlInput}`,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);

    const loadingMessage: Message = {
      id: generateId(),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      isLoading: true
    };

    setMessages(prev => [...prev, loadingMessage]);

    try {
      let response;

      if (urlType === 'image') {
        response = await cozeAPI.analyzeImageUrl(
          urlInput,
          '分析这张图片',
          sessionId,
          cozeConversationId
        );
      } else {
        response = await cozeAPI.analyzeFileUrl(
          urlInput,
          '分析这个文档',
          sessionId,
          cozeConversationId
        );
      }

      if (response.conversation_id) {
        setCozeConversationId(response.conversation_id);
      }

      // 构建回复内容
      let content = response.reply;

      // 如果有工具调用，添加提示
      if (response.tool_calls && response.tool_calls.length > 0) {
        content += '\n\n---\n**使用的插件：**\n';
        response.tool_calls.forEach((call, index) => {
          content += `\n${index + 1}. ${call.tool} ✅`;
        });
      }

      setMessages(prev =>
        prev.map(msg =>
          msg.id === loadingMessage.id
            ? { ...msg, content: content, isLoading: false }
            : msg
        )
      );

      // 清空URL输入
      setUrlInput('');
      setShowUrlInput(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'URL分析失败';
      setError(errorMessage);

      setMessages(prev =>
        prev.map(msg =>
          msg.id === loadingMessage.id
            ? { ...msg, content: `❌ ${errorMessage}`, isLoading: false }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  // 格式化时间
  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="app">
      {/* 头部 */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🎓</span>
            <h1>概率论与数理统计备考Agent</h1>
          </div>
          
          <div className="header-controls">
            {/* Coze开关 */}
            {cozeConfig?.status === 'configured' && (
              <label className="coze-toggle" title="使用Coze智能体（5个插件）">
                <input
                  type="checkbox"
                  checked={useCoze}
                  onChange={(e) => setUseCoze(e.target.checked)}
                />
                <span>🤖 Coze</span>
              </label>
            )}

            {/* 模型选择 */}
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="model-select"
              disabled={isLoading}
            >
              <option value="qwen-max">Qwen Max</option>
              <option value="qwen-turbo">Qwen Turbo</option>
              <option value="qwen-plus">Qwen Plus</option>
            </select>

            {/* 清空按钮 */}
            <button
              onClick={handleClearChat}
              className="clear-btn"
              disabled={messages.length === 0 || isLoading}
            >
              🗑️ 清空
            </button>

            {/* 切换到学习模式按钮 */}
            <button
              onClick={onSwitchMode}
              className="switch-btn"
              disabled={isLoading}
            >
              📚 系统学习
            </button>
          </div>
        </div>
      </header>

      {/* 错误提示 */}
      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* 消息列表 */}
      <main className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-icon">🎓</div>
            <h2>欢迎使用概率论与数理统计备考Agent</h2>
            <p>我是你的概率论与数理统计辅导老师，可以帮你：</p>
            <ul className="feature-list">
              <li>📚 解释数学概念和定理</li>
              <li>📝 讲解真题的解题思路</li>
              <li>🎯 推荐备考重点和建议</li>
              <li>❓ 回答概率论与数理统计相关问题</li>
            </ul>
            <p className="hint">在下方输入框开始提问吧！</p>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message) => (
              <div 
                key={message.id}
                className={`message ${message.role} ${message.isLoading ? 'loading' : ''}`}
              >
                <div className="message-avatar">
                  {message.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-role">
                      {message.role === 'user' ? '你' : 'AI老师'}
                    </span>
                    <span className="message-time">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                  <div className="message-body">
                    {message.isLoading ? (
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    ) : (
                      <div className="message-text">
                        {message.content.split('\n').map((line, i) => (
                          <p key={i}>{line}</p>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      {/* URL输入框（条件显示） */}
      {showUrlInput && (
        <div className="url-input-container">
          <select
            value={urlType}
            onChange={(e) => setUrlType(e.target.value as 'image' | 'file')}
            className="url-type-select"
          >
            <option value="image">📷 图片</option>
            <option value="file">📄 文件</option>
          </select>
          <input
            type="text"
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            placeholder={`请输入${urlType === 'image' ? '图片' : '文件'}URL...`}
            className="url-input"
            disabled={isLoading}
          />
          <button
            onClick={handleUrlAnalysis}
            disabled={isLoading || !urlInput.trim()}
            className="url-submit-btn"
          >
            分析
          </button>
        </div>
      )}

      {/* 输入区域 */}
      <footer className="input-area">
        <div className="input-container">
          {/* URL分析按钮 */}
          <button
            className="url-analysis-btn"
            onClick={() => setShowUrlInput(!showUrlInput)}
            disabled={!useCoze || isLoading}
            title="分析图片/文件URL"
          >
            🔗
          </button>

          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入你的概率论与数理统计问题，按 Enter 发送..."
            disabled={isLoading}
            className="message-input"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-btn"
          >
            {isLoading ? '发送中...' : '发送'}
          </button>
        </div>
        <div className="input-hint">
          按 Enter 发送，Shift + Enter 换行
        </div>
      </footer>
    </div>
  );
}

export default ChatMode;