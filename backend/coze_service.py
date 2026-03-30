"""
Coze平台服务模块（URL版）
基于实际配置的5个插件：联网问答、必应谷歌搜索、文件读取（URL）、图片理解（URL）、文档生成
"""
import os
import json
import httpx
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class CozeResponse:
    """Coze响应结构"""
    content: str
    tool_calls: List[Dict[str, Any]]
    conversation_id: Optional[str] = None
    message_id: Optional[str] = None


class CozeService:
    """
    Coze服务类（URL版）
    
    基于配置的5个插件：
    1. 联网问答 - 搜索信息
    2. 必应谷歌搜索 - 搜索引擎
    3. 文件读取 - 通过URL读取文档
    4. 图片理解 - 通过URL分析图片
    5. 文档生成 - 生成PDF
    
    注意：图片和文件都通过URL方式处理，无需上传功能
    """
    
    BASE_URL = "https://api.coze.cn"
    
    def __init__(self):
        self.api_token = os.getenv("COZE_API_TOKEN")
        self.bot_id = os.getenv("COZE_BOT_ID")
        
        if not self.api_token:
            raise ValueError("未配置COZE_API_TOKEN环境变量")
        if not self.bot_id:
            raise ValueError("未配置COZE_BOT_ID环境变量")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def chat(
        self,
        message: str,
        user_id: str = "default_user",
        conversation_id: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> CozeResponse:
        """
        发起对话（支持工具调用）
        
        自动触发以下插件：
        - 联网问答/必应谷歌搜索：当用户需要搜索时
        - 文件读取：当用户提供了文件URL时
        - 图片理解：当用户提供了图片URL时
        - 文档生成：当用户需要生成文档时
        
        Args:
            message: 用户消息（可能包含URL）
            user_id: 用户标识
            conversation_id: 会话ID
            history: 历史消息
            
        Returns:
            CozeResponse: 响应结果
        """
        additional_messages = []
        
        # 添加历史消息
        if history:
            for msg in history:
                additional_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                    "content_type": "text",
                    "type": "question" if msg.get("role") == "user" else "answer"
                })
        
        # 检查消息中是否包含URL，构建相应的消息格式
        # Coze会自动识别URL并调用相应插件
        additional_messages.append({
            "role": "user",
            "content": message,
            "content_type": "text",
            "type": "question"
        })
        
        payload = {
            "bot_id": self.bot_id,
            "user_id": user_id,
            "additional_messages": additional_messages,
            "stream": False
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/v3/chat",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("code") != 0:
                    raise Exception(f"Coze API返回错误: {data.get('msg', '未知错误')}")
                
                return self._parse_response(data)
                    
        except httpx.HTTPStatusError as e:
            error_msg = f"Coze API错误: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg += f" - {error_data.get('msg', '')}"
            except:
                pass
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"调用Coze API失败: {str(e)}")
    
    def _parse_response(self, data: Dict[str, Any]) -> CozeResponse:
        """解析Coze响应"""
        response_data = data.get("data", {})
        
        messages = response_data.get("messages", [])
        content = ""
        tool_calls = []
        
        for msg in messages:
            msg_type = msg.get("type")
            
            if msg_type == "answer":
                content = msg.get("content", "")
            elif msg_type == "tool_response":
                tool_calls.append({
                    "tool": msg.get("tool_call_id", "unknown"),
                    "content": msg.get("content", "")
                })
        
        return CozeResponse(
            content=content,
            tool_calls=tool_calls,
            conversation_id=response_data.get("conversation_id"),
            message_id=response_data.get("id")
        )
    
    async def create_conversation(self, user_id: str = "default_user") -> str:
        """创建新会话"""
        payload = {"bot_id": self.bot_id}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/v1/conversation/create",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("code") != 0:
                    raise Exception(f"创建会话失败: {data.get('msg', '未知错误')}")
                
                return data["data"]["id"]
                
        except Exception as e:
            raise Exception(f"创建会话失败: {str(e)}")


# 全局服务实例
_coze_service: Optional[CozeService] = None


def get_coze_service() -> CozeService:
    """获取Coze服务实例（单例模式）"""
    global _coze_service
    if _coze_service is None:
        _coze_service = CozeService()
    return _coze_service
