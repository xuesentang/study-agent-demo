import { useState, useEffect, useRef } from 'react';
import { studyAPI } from '../services/api';
import type { Message, StudyProgress } from '../types';
import './StudyMode.css';

interface StudyModeProps {
  sessionId: string;
  onSwitchMode: () => void;
}

export function StudyMode({ sessionId, onSwitchMode }: StudyModeProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState<StudyProgress | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const initialized = useRef(false);
  
  // 初始化学习
  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      initStudy();
    }
  }, []);
  
  // 自动滚动
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // 自动聚焦
  useEffect(() => {
    if (!isLoading) {
      inputRef.current?.focus();
    }
  }, [isLoading]);
  
  const initStudy = async () => {
    setIsLoading(true);
    try {
      const response = await studyAPI.sendMessage(sessionId, '');
      addMessage('assistant', response.content);
      if (response.progress) {
        setProgress(response.progress);
      }
    } catch (err) {
      setError('初始化学习失败，请刷新页面重试');
    } finally {
      setIsLoading(false);
    }
  };
  
  // 在组件顶部添加计数器
let messageIdCounter = 0;

// 修改 addMessage 函数
const addMessage = (role: 'user' | 'assistant', content: string, isLoading = false) => {
    messageIdCounter += 1;
    const message: Message = {
      id: `${Date.now()}_${messageIdCounter}`,
      role,
      content,
      timestamp: Date.now(),
      isLoading
    };
    setMessages(prev => [...prev, message]);
    return message.id;
};
  
  const updateMessage = (id: string, content: string, isLoading = false) => {
    setMessages(prev => 
      prev.map(msg => 
        msg.id === id ? { ...msg, content, isLoading } : msg
      )
    );
  };
  
  const handleSend = async () => {
    const trimmedInput = inputValue.trim();
    if (!trimmedInput || isLoading) return;
    
    setError(null);
    addMessage('user', trimmedInput);
    setInputValue('');
    setIsLoading(true);
    
    const loadingId = addMessage('assistant', '', true);
    
    try {
      const response = await studyAPI.sendMessage(sessionId, trimmedInput);
      updateMessage(loadingId, response.content, false);
      
      if (response.progress) {
        setProgress(response.progress);
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '发送失败';
      updateMessage(loadingId, `❌ ${errorMsg}`, false);
      setError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  };
  
  const handleReset = async () => {
    if (!confirm('确定要重置学习进度吗？')) return;
    
    try {
      await studyAPI.resetProgress(sessionId);
      setMessages([]);
      setProgress(null);
      initialized.current = false;
      initStudy();
    } catch (err) {
      setError('重置失败');
    }
  };
  
  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  return (
    <div className="study-mode">
      {/* 头部 */}
      <header className="study-header">
        <div className="study-header-content">
          <div className="study-title">
            <span className="study-icon">📚</span>
            <h2>系统学习模式</h2>
          </div>
          
          <div className="study-controls">
            {progress && (
              <div className="progress-badge">
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${progress.percentage}%` }}
                  />
                </div>
                <span className="progress-text">
                  {progress.completed}/{progress.total}
                </span>
              </div>
            )}
            
            <button onClick={handleReset} className="reset-btn" title="重置进度">
              🔄
            </button>
            
            <button onClick={onSwitchMode} className="switch-btn">
              自由提问
            </button>
          </div>
        </div>
      </header>
      
      {/* 错误提示 */}
      {error && (
        <div className="study-error">
          {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}
      
      {/* 消息区域 */}
      <div className="study-messages">
        {messages.map((message) => (
          <div 
            key={message.id}
            className={`study-message ${message.role}`}
          >
            <div className="message-avatar">
              {message.role === 'user' ? '👤' : '🎓'}
            </div>
            <div className="message-bubble">
              <div className="message-header">
                <span>{message.role === 'user' ? '你' : 'AI老师'}</span>
                <span className="message-time">{formatTime(message.timestamp)}</span>
              </div>
              <div className="message-body">
                {message.isLoading ? (
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
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
      
      {/* 输入区域 */}
      <div className="study-input-area">
        <div className="study-input-container">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isLoading ? '等待回复...' : '输入回复...'}
            disabled={isLoading}
          />
          <button 
            onClick={handleSend}
            disabled={!inputValue.trim() || isLoading}
          >
            {isLoading ? '发送中...' : '发送'}
          </button>
        </div>
        <div className="study-hint">
          按 Enter 发送 • 回复"帮助"查看可用命令
        </div>
      </div>
    </div>
  );
}