# 概率论与数理统计备考Agent

## 📖 项目概述

**概率论与数理统计备考Agent**是一款面向国内本科大一/大二学生的智能学习辅导系统。系统基于概率论与数理统计教材与真题，主打"学练一体"的simple应试模式，核心解决大学生期末备考时间紧、传统自学效率低、学练分离、知识点割裂的痛点。

### 核心特色

- 🎯 **极简学习路径**：单知识点闭环≤5分钟，总时长控制在8小时内
- 🧠 **AI智能辅导**：基于大模型的引导式学习，理解而非死记
- 📚 **RAG知识检索**：基于教材内容的精准知识库问答
- 🤖 **Coze工具调用**：集成5大智能插件（联网搜索、图片理解、文件读取、文档生成）
- 🔗 **URL智能分析**：支持图片/文件URL直接分析，无需上传
- 🔄 **学练一体**：学完即测，即时反馈，错题智能复习

---

## ✨ 核心功能

### 1. 系统学习模式

按照教材逻辑顺序，依次学习：

```
学习路线展示 → 串联知识点 → 高频考点讲解 → 真题测试 → 智能评估
```

- **串联知识点**：极简铺陈（≤100字），建立知识框架
- **高频考点**：详细讲解+真题测试（≤200字），确保掌握
- **智能评估**：大模型语义理解，支持格式不同的正确答案
- **错题处理**：答错后显示正确答案+备用题目，确保真正掌握

### 2. 自由提问模式

随时切换，针对具体问题进行答疑：

- **RAG增强回答**：基于教材内容的精准回答，消除AI幻觉
- **Coze智能体**：一键切换Coze模式，自动调用工具插件
- **上下文保持**：同一session内保持学习上下文
- **一键切换**：不打断学习流程

### 3. Coze工具调用（5大插件）

集成Coze平台智能插件，扩展AI能力：

| 插件 | 功能 | 使用场景 |
|------|------|----------|
| 🔍 **联网问答** | 从多个网站搜索信息 | 查询最新概率论资料、概念解释 |
| 🌐 **必应谷歌搜索** | 搜索引擎查询 | 搜索题目解析、学习资源 |
| 🖼️ **图片理解** | 通过URL分析图片内容 | 分析题目截图、公式图片 |
| 📄 **文件读取** | 通过URL读取文档 | 分析PDF教材、Word文档 |
| 📑 **文档生成** | 生成PDF文档 | 导出学习笔记、错题总结 |

**使用方式**：
- 在聊天界面开启"Coze"开关
- 直接发送消息，AI自动判断是否需要调用工具
- 分析图片/文件时，点击🔗按钮输入URL即可

---

## 🛠️ 技术栈

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| FastAPI | 0.110+ | Web框架 |
| OpenAI API | - | AI对话与评估 |
| Coze API | v3 | 工具调用服务 |
| ChromaDB | 0.4.22 | 向量数据库 |
| Sentence-Transformers | 3.0.0 | 文本嵌入 |
| SQLite | - | 学习进度存储 |
| httpx | 0.27+ | 异步HTTP客户端 |

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| React | 19.2+ | UI框架 |
| TypeScript | 5.9+ | 类型系统 |
| Vite | 8.0+ | 构建工具 |
| Axios | 1.13+ | HTTP客户端 |

---

## 📋 环境配置

### 系统要求

- **操作系统**: Windows 10/11, macOS, Linux
- **Python**: 3.8 或更高版本
- **Node.js**: 18 或更高版本
- **内存**: 建议 8GB 以上（嵌入模型需要）

### API密钥配置

1. **阿里云百炼（DashScope）配置**：
   - 注册阿里云百炼账号
   - 获取 API Key
   - 在 `backend/.env` 文件中配置：

```env
OPENAI_API_KEY=your_dashscope_api_key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

2. **Coze平台配置**：
   - 注册Coze账号（https://www.coze.cn）
   - 创建智能体并发布
   - 配置5个插件：联网问答、必应谷歌搜索、图片理解、文件读取、文档生成
   - 获取 API Token 和 Bot ID
   - 在 `backend/.env` 文件中配置：

```env
COZE_API_TOKEN=your_coze_api_token
COZE_BOT_ID=your_coze_bot_id
```

---

## 🚀 安装与启动

### 方式一：一键启动（推荐）

```bash
# 进入项目目录
cd study-agent-demo

# 运行启动脚本
start.bat
```

脚本会自动：
- 启动后端服务（Python）
- 启动前端服务（Node.js）
- 打开浏览器访问界面

### 方式二：手动启动

#### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv study_venv

# 激活虚拟环境
study_venv\Scripts\activate  # Windows
# source study_venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端服务将运行在 `http://localhost:8000`

#### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将运行在 `http://localhost:5173`

#### 3. 访问应用

打开浏览器访问：`http://localhost:5173`

---

## 📖 使用指南

### 首次使用

1. **配置环境变量**：在 `backend/.env` 中填入API密钥
2. **添加教材内容**：将教材文本放入 `backend/documents/` 目录
3. **启动服务**：运行 `start.bat` 或手动启动前后端
4. **开始学习**：访问前端界面，输入"开始"进入学习流程

### 学习流程

```
1. 输入"开始" → 展示学习路线
2. 输入"继续" → 学习串联知识点
3. 输入"继续" → 学习高频考点
4. 输入答案 → 做题测试
5. 系统评估 → 正确进入下一题，错误显示答案+备用题目
```

### Coze工具调用使用指南

#### 开启Coze模式

1. 在聊天界面顶部，将"Coze"开关打开
2. 输入你的问题，AI会自动判断是否需要调用工具

#### 分析图片/文件

1. 点击输入框左侧的 🔗 按钮
2. 选择类型（图片/文件）
3. 输入URL地址
4. 点击"分析"按钮

**示例**：
- 图片分析：`https://example.com/problem.jpg`
- 文件分析：`https://example.com/textbook.pdf`

#### 常用命令

| 命令 | 说明 |
|------|------|
| `开始` | 开始学习流程 |
| `继续` | 进入下一步 |
| `帮助` | 查看可用命令 |
| `重置` | 重置学习进度 |

---

## 📁 目录结构

```
study-agent-demo/
├── backend/                      # 后端服务
│   ├── main.py                   # FastAPI主应用入口
│   ├── study_flow.py             # 学习流程状态机
│   ├── knowledge_base.py         # RAG知识库模块
│   ├── database.py               # SQLite数据库操作
│   ├── coze_service.py           # Coze工具调用服务
│   ├── requirements.txt          # Python依赖
│   ├── .env                      # 环境变量配置
│   ├── documents/                # 知识库文档目录
│   │   └── *.txt                 # 教材文本文件
│   └── chroma_db/                # 向量数据库（自动创建）
├── frontend/                     # 前端应用
│   ├── src/
│   │   ├── App.tsx               # 主应用组件
│   │   ├── components/
│   │   │   ├── StudyMode.tsx     # 学习模式组件
│   │   │   └── ChatMode.tsx      # 聊天模式组件（含Coze集成）
│   │   ├── services/
│   │   │   └── api.ts            # API服务封装
│   │   └── types.ts              # TypeScript类型定义
│   ├── package.json              # Node依赖
│   └── index.html
├── .gitignore                    # Git忽略文件
├── start.bat                     # 一键启动脚本
└── README.md                     # 项目说明文档
```

---

## 🔧 配置说明

### 知识库配置

将教材内容按章节保存为 `.txt` 文件，放入 `backend/documents/` 目录：

```
documents/
├── 第一章_随机试验与随机事件.txt
├── 第二章_概率的定义与性质.txt
└── ...
```

文件格式示例：
```
1.1 随机现象与确定性现象

确定性现象：在给定条件下，某一结果一定会出现的现象。
随机现象：在一定条件下，有多种可能的结果且无法预知哪一个结果将会出现的现象。

1.2 随机试验

为找出随机现象的内在规律而进行的大量、重复的试验。
...
```

### 备用题目配置

备用题目用于当用户首次答题错误时，提供额外的练习机会。在 `study_flow.py` 的 `KeyPoint` 数据类中配置：

```python
backup_questions=[
    {
        "question": "备用题目1",
        "answer": "备用答案1"
    },
    {
        "question": "备用题目2",
        "answer": "备用答案2"
    }
]
```

**学习流程说明**：
1. 用户首次答题错误 → 显示正确答案
2. 切换到备用题目模式
3. 用户回答备用题目：
   - 回答正确 → 进入下一考点
   - 回答错误 → 显示正确答案 + 进入下一考点

### Coze插件配置

在Coze平台（https://www.coze.cn）配置智能体：

1. **创建智能体**：新建一个智能体，设置基础信息
2. **添加插件**：
   - 联网问答（从多个网站或平台搜索信息）
   - 必应谷歌搜索
   - 图片理解（通过URL）
   - 文件读取（通过URL）
   - 文档生成
3. **发布智能体**：发布后获取 Bot ID
4. **获取API Token**：在设置中获取 Personal Access Token

---

## 🔌 API接口说明

### 基础接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/chat` | POST | 普通对话（RAG增强） |
| `/chat/coze` | POST | Coze智能体对话（支持工具调用） |
| `/coze/config` | GET | 获取Coze配置状态 |
| `/coze/conversation/create` | POST | 创建Coze会话 |

### Coze对话接口示例

**请求**：
```json
POST /chat/coze
{
  "message": "搜索概率论中心极限定理",
  "user_id": "user_123",
  "conversation_id": "conv_456"
}
```

**响应**：
```json
{
  "reply": "中心极限定理是指...",
  "conversation_id": "conv_456",
  "tool_calls": [
    {"tool": "web_search", "content": "..."}
  ],
  "model": "coze"
}
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- Python 代码遵循 PEP 8 规范
- TypeScript 代码遵循项目现有风格
- 提交前请确保代码通过 lint 检查

---

## 📄 许可证

本项目基于 MIT 许可证开源。详情请参阅 [LICENSE](LICENSE) 文件。

---

## 📧 联系方式

- **项目地址**: https://github.com/xuesentang/study-agent-demo
- **问题反馈**: https://github.com/xuesentang/study-agent-demo/issues

---

## 🔄 更新日志

### v2.0.0 (2025-03-30)
- ✨ 集成Coze平台工具调用功能
- 🔗 支持5大智能插件（联网搜索、图片理解、文件读取、文档生成）
- 🖼️ 新增URL方式分析图片和文件
- 🗑️ 移除原有OCR模块，改用Coze图片理解
- 🎨 优化前端界面，新增Coze开关和URL分析功能

### v1.0.0 (2025-03-20)
- 🎉 项目初始版本发布
- 📚 RAG知识检索功能
- 🧠 AI智能辅导对话
- 🔄 学练一体学习流程
- 📷 OCR图像识别功能

---

<p align="center">
  <sub>Built with ❤️ for students who want to master probability and statistics</sub>
</p>
