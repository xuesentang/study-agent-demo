# 概率论与数理统计备考Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/React-18+-61DAFB.svg" alt="React 18+">
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
</p>

<p align="center">
  <b>基于RAG和OCR的智能学习辅导系统</b><br>
  专为大学生期末备考设计，提供学练一体的AI辅导体验
</p>

---

## 📖 项目概述

**概率论与数理统计备考Agent**是一款面向国内本科大一/大二学生的智能学习辅导系统。系统基于概率论与数理统计教材与真题，主打"学练一体"的simple应试模式，核心解决大学生期末备考时间紧、传统自学效率低、学练分离、知识点割裂的痛点。

### 核心特色

- 🎯 **极简学习路径**：单知识点闭环≤5分钟，总时长控制在8小时内
- 🧠 **AI智能辅导**：基于大模型的引导式学习，理解而非死记
- 📚 **RAG知识检索**：基于教材内容的精准知识库问答
- 📷 **OCR图像识别**：支持拍照上传题目，自动识别文字和公式
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
- **上下文保持**：同一session内保持学习上下文
- **一键切换**：不打断学习流程

### 3. OCR图像识别

降低输入成本，支持多种方式：

- **拍照上传**：手机拍照直接识别题目
- **公式识别**：专门优化数学公式识别
- **双模式支持**：文件上传 + Base64截图

---

## 🛠️ 技术栈

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| FastAPI | 0.110+ | Web框架 |
| OpenAI API | - | AI对话与评估 |
| ChromaDB | 0.4.22 | 向量数据库 |
| Sentence-Transformers | 3.0.0 | 文本嵌入 |
| PaddleOCR | 3.4.0 | 图像文字识别 |
| SQLite | - | 学习进度存储 |

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

1. 注册阿里云百炼（DashScope）账号
2. 获取 API Key
3. 在 `backend/.env` 文件中配置：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
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

### 常用命令

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
│   ├── ocr_service.py            # OCR图像识别服务
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
│   │   │   └── ChatMode.tsx      # 聊天模式组件
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

### OCR识别配置

OCR服务支持多种图片格式，包括PNG、JPG、JPEG、BMP等。识别后的文本可直接用于：
- 题目上传和识别
- 数学公式识别
- 截图文字提取

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

<p align="center">
  <sub>Built with ❤️ for students who want to master probability and statistics</sub>
</p>