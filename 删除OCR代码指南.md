# 删除OCR代码完整指南

## 一、概述

本指南将帮助你彻底删除项目中的OCR相关代码，并替换为Coze图片理解功能。

## 二、涉及文件清单

| 文件路径 | 操作类型 | 说明 |
|---------|---------|------|
| `backend/ocr_service.py` | 删除 | OCR服务完整文件 |
| `backend/main.py` | 修改 | 删除OCR导入和API端点 |
| `backend/requirements.txt` | 修改 | 删除PaddleOCR依赖 |

## 三、详细操作步骤

### 步骤1：删除OCR服务文件

**操作**：直接删除文件

```bash
# 删除文件
backend/ocr_service.py
```

**说明**：此文件包含136行OCR相关代码，直接删除即可。

---

### 步骤2：修改 backend/main.py

**需要修改的位置**：

#### 2.1 删除导入语句（第16行）

**查找代码**：
```python
from ocr_service import get_ocr_service
```

**操作**：删除这一行

#### 2.2 删除图片上传API（第222-276行）

**查找代码块**：
```python
@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片并识别文字
    
    支持图片中的文字和公式识别
    """
    try:
        # 读取图片数据
        contents = await file.read()
        
        # 检查文件大小（限制10MB）
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="图片大小超过10MB限制"
            )
        
        # 执行OCR识别
        ocr = get_ocr_service()
        result = ocr.recognize_formula(contents)
        
        return {
            "success": True,
            "filename": file.filename,
            "recognition": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"图片识别失败: {str(e)}"
        )

@app.post("/upload/base64")
async def upload_base64(image_base64: str):
    """
    上传Base64编码的图片
    
    适用于前端直接发送截图等场景
    """
    try:
        ocr = get_ocr_service()
        result = ocr.recognize_base64(image_base64)
        
        return {
            "success": True,
            "recognition": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"图片识别失败: {str(e)}"
        )
```

**操作**：删除上述两个完整的API端点函数

#### 2.3 可选：删除File和UploadFile导入（如果不再使用）

**查找代码**（第15行）：
```python
from fastapi import File, UploadFile
```

**操作**：如果这两个导入只在OCR中使用，则删除；如果其他地方还在使用，保留。

**检查方法**：搜索main.py中是否还有其他地方使用File或UploadFile

---

### 步骤3：修改 backend/requirements.txt

**查找代码**（第10行）：
```
paddleocr==3.4.0
```

**操作**：删除这一行

**注意**：Pillow（PIL）可能还有其他用途，暂时保留

---

## 四、修改后的文件参考

### 4.1 backend/main.py 修改后关键部分

```python
# 导入部分（删除第16行）
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import uvicorn
from study_flow import (
    get_or_create_session, 
    get_session, 
    delete_session,
    StudyState
)
from knowledge_base import get_knowledge_base, init_knowledge_base
# 删除: from ocr_service import get_ocr_service
from typing import Dict, Optional
from contextlib import asynccontextmanager

# ... 中间代码保持不变 ...

# 删除: @app.post("/upload/image") 和 @app.post("/upload/base64") 两个端点

# ... 其余代码保持不变 ...
```

### 4.2 backend/requirements.txt 修改后

```
fastapi==0.110.0
uvicorn[standard]==0.27.0
openai>=1.30.0
python-dotenv==1.0.1
pydantic==2.9.2
python-multipart==0.0.7
httpx==0.27.2
chromadb==0.4.22
sentence-transformers==3.0.0
# 删除: paddleocr==3.4.0
Pillow==12.1.1
```

---

## 五、验证清单

修改完成后，请检查：

- [ ] `backend/ocr_service.py` 文件已删除
- [ ] `backend/main.py` 中不再导入 `ocr_service`
- [ ] `backend/main.py` 中 `/upload/image` 端点已删除
- [ ] `backend/main.py` 中 `/upload/base64` 端点已删除
- [ ] `backend/requirements.txt` 中 `paddleocr` 已删除
- [ ] 后端服务能正常启动
- [ ] API文档中不再显示OCR相关端点

---

## 六、后续建议

删除OCR后，建议：

1. **在Coze平台添加「图片理解」插件**
2. **修改前端图片上传逻辑**，改为直接调用Coze的图片理解功能
3. **更新API文档**，移除OCR相关说明

---

**注意**：本指南只涉及代码删除，不涉及Coze图片理解的接入。如需接入Coze图片理解，请参考《Coze工具集成指南》。
