from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import uvicorn
from study_flow import (
    get_or_create_session, 
    get_session, 
    delete_session,
    StudyState
)
from knowledge_base import get_knowledge_base, init_knowledge_base
from typing import Dict, Optional, List, Any
from contextlib import asynccontextmanager
from coze_service import get_coze_service


# 加载环境变量
load_dotenv()

# 生命周期管理（新增）
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("🔄 应用启动中...")
    init_knowledge_base()
    yield
    # 关闭时执行
    print("🔄 应用关闭中...")

# 创建 FastAPI 应用实例

app = FastAPI(
    title="概率论与数理统计备考Agent API",
    description="大学生概率论与数理统计备考辅导Agent后端服务",
    version="0.1.0",
    lifespan=lifespan  # 使用新的生命周期管理
)

# 配置 CORS（跨域资源共享）
# 允许前端应用访问后端API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite 默认开发服务器
        "http://localhost:3000",  # React 默认开发服务器
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)
# 应用启动时初始化知识库
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化知识库"""
    init_knowledge_base()  

# 初始化 OpenAI 客户端
# 支持标准OpenAI API和兼容API（如智谱、DeepSeek等）
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
)

# 数据模型定义
class ChatRequest(BaseModel):
    """对话请求模型"""
    message: str
    model: str = os.getenv("DASHSCOPE_MODEL", "qwen-max")  # 默认模型
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "什么是随机事件？",
                "model": "qwen-max"
            }
        }

class ChatResponse(BaseModel):
    """对话响应模型"""
    reply: str
    model: str
    tokens_used: int = 0

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    timestamp: str

class StudyRequest(BaseModel):
    """学习请求模型"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "开始"
            }
        }

class StudyResponse(BaseModel):
    """学习响应模型"""
    type: str
    content: str
    progress: Optional[Dict] = None
    data: Optional[Dict] = None

class ProgressResponse(BaseModel):
    """进度响应模型"""
    session_id: str
    state: str
    progress: Dict
    elapsed_time: int


# 系统提示词（定义AI角色和行为）
SYSTEM_PROMPT = """你是一位专业的概率论与数理统计辅导老师，专门为大学生期末备考提供辅导。

你的教学风格：
1. 简洁明了：每个概念讲解控制在200字以内
2. 重点突出：强调定义、解题方法
3. 循序渐进：从基础概念到应用技巧
4. 鼓励互动：适时提问，检验理解程度

你可以帮助用户：
- 解释数学概念和定理
- 讲解例题的解题思路
- 提供备考建议和重点
- 回答概率论与数理统计相关问题

请用中文回答，使用清晰的格式（如分点、加粗等）提高可读性。"""

# API 路由定义

@app.get("/", response_model=HealthResponse)
async def root():
    """
    根路径 - 服务健康检查
    
    返回服务状态信息，用于确认服务是否正常运行
    """
    from datetime import datetime
    return HealthResponse(
        status="running",
        version="0.1.0",
        timestamp=datetime.now().isoformat()
    )

@app.get("/health")
async def health_check():
    """
    健康检查端点
    
    用于监控和负载均衡检查
    """
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    增强版对话接口，集成RAG检索
    
    接收用户消息，检索相关知识后调用AI生成回复
    """
    try:
        # 检索相关知识
        kb = get_knowledge_base()
        relevant_knowledge = kb.search(request.message, n_results=2)
        
        # 构建增强的提示词
        if relevant_knowledge:
            knowledge_text = "\n\n".join([
                f"[相关知识点 {i+1}] {k['content'][:300]}..."
                for i, k in enumerate(relevant_knowledge)
            ])
            
            enhanced_prompt = f"""基于以下相关知识回答用户问题：

{knowledge_text}

---

用户问题：{request.message}

请根据上述知识点回答，如果知识点不足以回答问题，请使用你的知识补充。"""
        else:
            enhanced_prompt = request.message
        
        # 调用 OpenAI API
        response = await client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": enhanced_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # 提取回复内容
        reply = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else 0
        
        return ChatResponse(
            reply=reply,
            model=request.model,
            tokens_used=tokens_used
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI服务调用失败: {str(e)}"
        )

@app.get("/models")
async def list_models():
    """
    列出可用的AI模型
    
    返回支持的模型列表
    """
    return {
        "models": [

            {"id": "qwen-max", "name": "Qwen-max", "description": "参数多，擅长代码和推理的智能模型"},
            {"id": "qwen-turbo", "name": "Qwen Turbo", "description": "能力不错的智能模型"},
            {"id": "qwen-plus", "name": "Qwen Plus", "description": "多模态、能力全面的智能模型"}
            
        ]
    }
#学习流程API
@app.post("/study/{session_id}", response_model=StudyResponse)
async def study(session_id: str, request: StudyRequest):
    """
    学习流程主接口
    
    管理用户的学习会话和流程状态
    
    - **session_id**: 用户会话ID（可用任意字符串，如用户ID或随机生成）
    - **message**: 用户输入的消息
    
    根据当前学习状态返回相应的学习内容或提示
    """
    try:
        # 获取或创建会话
        session = get_or_create_session(session_id)
        
        # 处理用户输入
        result = session.handle_input(request.message)
        
        # 如果有下一步动作，直接使用 next_action 的内容
        if "next_action" in result:
            next_action = result["next_action"]  # 不使用 pop，避免修改 result
            return StudyResponse(
                type=next_action.get("type", result.get("type", "info")),
                content=next_action.get("content", result.get("content", "")),
                progress=next_action.get("progress"),
                data=next_action
            )
        
        return StudyResponse(
            type=result.get("type", "unknown"),
            content=result.get("content", ""),
            progress=result.get("progress"),
            data=result
        )
        
    except Exception as e:
        import traceback
        print("=" * 50)
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print("详细堆栈:")
        print(traceback.format_exc())
        print("=" * 50)
        raise HTTPException(
            status_code=500,
            detail=f"学习流程处理失败: {str(e)}"
        )

@app.get("/study/{session_id}/progress", response_model=ProgressResponse)
async def get_study_progress(session_id: str):
    """
    获取学习进度
    
    返回当前会话的学习状态和进度信息
    """
    session = get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="会话不存在"
        )
    
    return ProgressResponse(
        session_id=session_id,
        state=session.state.value,
        progress=session.get_progress(),
        elapsed_time=(datetime.now() - session.start_time).seconds // 60
    )

@app.delete("/study/{session_id}")
async def reset_study(session_id: str):
    """
    重置学习进度
    
    清除指定会话的学习数据，重新开始
    """
    success = delete_session(session_id)
    if success:
        return {"message": "学习进度已重置", "session_id": session_id}
    else:
        return {"message": "会话不存在或已过期", "session_id": session_id}

@app.get("/study/sessions")
async def list_sessions():
    """
    列出所有活跃会话（仅用于调试）
    """
    from study_flow import get_all_sessions
    return {
        "sessions": get_all_sessions(),
        "count": len(get_all_sessions())
    }
# 知识库搜索接口
@app.post("/knowledge/search")
async def search_knowledge(query: str, n_results: int = 3):
    """
    搜索知识库
    
    - **query**: 查询文本
    - **n_results**: 返回结果数量
    """
    try:
        kb = get_knowledge_base()
        results = kb.search(query, n_results)
        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"搜索失败: {str(e)}"
        )


# ============ Coze工具调用API（URL版，5个插件） ============

class CozeChatRequest(BaseModel):
    """Coze对话请求"""
    message: str = Field(..., description="用户消息（可包含图片/文件URL）")
    user_id: str = Field(default="default_user", description="用户标识")
    conversation_id: Optional[str] = Field(default=None, description="会话ID")
    history: List[Dict[str, str]] = Field(default=[], description="历史消息")


class CozeChatResponse(BaseModel):
    """Coze对话响应"""
    reply: str = Field(..., description="智能体回复")
    conversation_id: Optional[str] = Field(default=None, description="会话ID")
    tool_calls: List[Dict[str, Any]] = Field(default=[], description="工具调用记录")
    model: str = Field(default="coze", description="模型标识")


@app.post("/chat/coze", response_model=CozeChatResponse)
async def chat_with_coze(request: CozeChatRequest):
    """
    使用Coze智能体进行对话（支持工具调用，URL版）
    
    基于配置的5个插件：
    - 联网问答/必应谷歌搜索：搜索概率论资料
    - 文件读取（URL）：分析文档URL
    - 图片理解（URL）：分析图片URL
    - 文档生成：导出学习笔记
    
    使用方式：
    - 普通对话：直接发送文字
    - 分析图片：发送消息包含图片URL，如"分析这张图片：https://example.com/image.jpg"
    - 分析文件：发送消息包含文件URL，如"分析这个文档：https://example.com/doc.pdf"
    """
    try:
        coze_service = get_coze_service()
        
        result = await coze_service.chat(
            message=request.message,
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            history=request.history
        )
        
        return CozeChatResponse(
            reply=result.content,
            conversation_id=result.conversation_id,
            tool_calls=result.tool_calls,
            model="coze"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Coze调用失败: {str(e)}"
        )


@app.post("/coze/conversation/create")
async def create_coze_conversation(user_id: str = "default_user"):
    """创建Coze会话"""
    try:
        coze_service = get_coze_service()
        conversation_id = await coze_service.create_conversation(user_id)
        
        return {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message": "会话创建成功"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建会话失败: {str(e)}"
        )


@app.get("/coze/config")
async def get_coze_config():
    """获取Coze配置信息（调试用）"""
    bot_id = os.getenv("COZE_BOT_ID", "未配置")
    
    return {
        "bot_id": bot_id,
        "status": "configured" if bot_id != "未配置" else "not_configured",
        "message": "Coze服务已集成" if bot_id != "未配置" else "请在.env中配置COZE_BOT_ID",
        "features": [
            "chat",
            "image_understanding_url",
            "file_reading_url",
            "web_search",
            "document_generation"
        ],
        "plugins": [
            "联网问答",
            "必应谷歌搜索",
            "文件读取（URL）",
            "图片理解（URL）",
            "文档生成"
        ],
        "note": "图片和文件通过URL方式处理，无需上传功能"
    }


# 启动入口
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print("启动概率论与数理统计备考Agent后端服务...")
    print(f"服务地址: http://{host}:{port}")
    print(f"API文档: http://{host}:{port}/docs")
    print(f"调试模式: {debug}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,  # 调试模式下自动重载
        log_level="info"
    )

