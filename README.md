# 护肤品 AI 助手 (Skincare AI Assistant)

基于 EWG 数据库的智能护肤品推荐系统，使用 **RAG (Retrieval-Augmented Generation)** 技术结合 **OpenAI GPT-4o-mini** 提供个性化护肤建议。

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Node](https://img.shields.io/badge/Node-20-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 📋 目录

- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [系统架构](#系统架构)
- [API 文档](#api-文档)
- [开发指南](#开发指南)
- [数据说明](#数据说明)
- [故障排除](#故障排除)

---

## ✨ 功能特性

### 🔍 产品检索 (Query)
- **语义搜索**: 基于 ChromaDB 向量数据库的语义相似度检索
- **7,933+ 产品**: 完整的 EWG 护肤品数据库
- **智能排序**: 按相关度自动排序搜索结果
- **产品链接**: 直接跳转亚马逊购买链接和 EWG 评级页面

### 💬 AI 对话 (Chat)
- **GPT-4o-mini**: 使用最新的 OpenAI 模型进行对话
- **RAG 技术**: 结合向量检索与 LLM 生成，确保回答准确性
- **个性化建议**: 根据肤质、问题提供定制化护肤方案
- **多轮对话**: 支持上下文理解的连续对话
- **成分分析**: 详细解释产品成分及其功效

### 🎯 核心优势
- ✅ **数据可靠**: 基于 EWG 权威数据库
- ✅ **实时响应**: 平均响应时间 < 3 秒
- ✅ **精准推荐**: 结合 RAG 技术，推荐有依据
- ✅ **易于部署**: Docker 一键启动
- ✅ **热重载**: 开发模式支持代码实时更新

---

## 🛠 技术架构

### 前端 (Frontend)
- **框架**: Next.js 15 + React 18
- **样式**: Tailwind CSS + shadcn/ui
- **状态管理**: React Hooks
- **端口**: 3001

### 后端 (Backend)
- **框架**: FastAPI (Python 3.10)
- **向量数据库**: ChromaDB
- **AI 模型**: OpenAI GPT-4o-mini + text-embedding-3-small
- **端口**: 8000

### 数据库 (Database)
- **ChromaDB**: 向量数据库存储 7,933 个产品 embeddings
- **维度**: 1536 (OpenAI text-embedding-3-small)
- **端口**: 8001 (映射到容器内 8000)

### DevOps
- **容器化**: Docker + Docker Compose
- **网络**: 自定义 Bridge 网络
- **持久化**: Docker Volumes

---

## 🚀 快速开始

### 前置要求

- Docker Desktop (最新版本)
- Docker Compose v2.0+
- 至少 4GB 可用内存
- OpenAI API Key

### 1. 克隆项目

\`\`\`bash
git clone <repository-url>
cd app-building-template
\`\`\`

### 2. 配置环境变量

项目已包含 \`.env\` 文件，其中配置了 OpenAI API Key。如需修改：

\`\`\`bash
# 编辑 .env 文件
nano .env

# 确保包含以下内容
OPENAI_API_KEY=your-api-key-here
\`\`\`

### 3. 启动所有服务

\`\`\`bash
# 停止旧容器（如果有）
docker-compose down

# 启动所有服务
docker-compose up -d
\`\`\`

### 4. 等待服务就绪

\`\`\`bash
# 查看所有容器状态
docker ps

# 查看日志
docker-compose logs -f
\`\`\`

预期输出：
\`\`\`
✓ Container skincare-chromadb   Running
✓ Container skincare-backend    Running
✓ Container skincare-frontend   Running
\`\`\`

### 5. 访问应用

打开浏览器访问：**http://localhost:3001**

---

## 🏗 系统架构

\`\`\`
┌─────────────────────────────────────────────────────────┐
│                      用户浏览器                          │
│                http://localhost:3001                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               Next.js Frontend (Port 3001)              │
│  - Query Tab: 产品检索                                   │
│  - Chat Tab: AI 对话                                     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────┐
│             FastAPI Backend (Port 8000)                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │  /api/search  - 产品检索 API                     │  │
│  │  /api/chat/   - AI 对话 API                       │  │
│  │  /health      - 健康检查                          │  │
│  └─────────┬──────────────────────┬──────────────────┘  │
│            │                      │                      │
└────────────┼──────────────────────┼──────────────────────┘
             │                      │
             ▼                      ▼
┌────────────────────┐    ┌────────────────────┐
│  ChromaDB          │    │  OpenAI API        │
│  (Port 8001)       │    │                    │
│                    │    │  - GPT-4o-mini     │
│  - 7,933 products  │    │  - text-embedding  │
│  - 1536 dims       │    │                    │
└────────────────────┘    └────────────────────┘
\`\`\`

---

## 📚 API 文档

### API Swagger 文档

访问: **http://localhost:8000/docs**

### 主要端点

| 端点 | 方法 | 描述 |
|------|------|------|
| \`/health\` | GET | 健康检查 |
| \`/api/search\` | GET | 产品检索 |
| \`/api/chat/\` | POST | AI 对话 |
| \`/api/products\` | GET | 产品列表 |

### 示例：搜索产品

\`\`\`bash
curl "http://localhost:8000/api/search?q=moisturizer&top_k=5"
\`\`\`

### 示例：AI 聊天

\`\`\`bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"推荐适合干性皮肤的保湿霜","history":[]}'
\`\`\`

---

## 💻 开发指南

### 项目结构

\`\`\`
app-building-template/
├── backend/                    # FastAPI 后端
│   ├── api/
│   │   ├── main.py            # 主应用
│   │   └── routes/
│   │       ├── chat.py        # 聊天路由 (GPT + RAG)
│   │       ├── search.py      # 搜索路由
│   │       └── products.py    # 产品路由
│   └── cli.py                 # 命令行工具
│
├── frontend-template/          # Next.js 前端
│   ├── src/
│   │   ├── app/
│   │   │   └── page.jsx       # 主页 (Query + Chat)
│   │   └── components/
│   │       ├── ui/            # UI 组件
│   │       └── layout/        # 布局组件
│   └── Dockerfile.dev
│
├── input-datasets/             # EWG 数据集
│   └── outputs/
│       └── embeddings-char-split-*.jsonl
│
├── docker-compose.yml
├── .env
└── README.md
\`\`\`

### 本地开发

#### 后端开发

\`\`\`bash
# 查看后端日志
docker-compose logs -f backend

# 重启后端
docker-compose restart backend

# 进入后端容器
docker exec -it skincare-backend bash
\`\`\`

#### 前端开发

\`\`\`bash
# 查看前端日志
docker-compose logs -f frontend

# 重启前端
docker-compose restart frontend

# 进入前端容器
docker exec -it skincare-frontend sh
\`\`\`

---

## 📊 数据说明

### EWG 数据库

- **来源**: Environmental Working Group (EWG) Skin Deep Database
- **产品数量**: 7,933 个护肤品
- **数据格式**: JSONL (JSON Lines)
- **Embedding 维度**: 1536 (OpenAI text-embedding-3-small)

### ChromaDB 集合

- **Collection 名称**: \`char-split-collection\`
- **存储路径**: Docker Volume \`skincare-chromadb-data\`
- **查询方式**: 向量相似度搜索

### 手动重新加载数据

\`\`\`bash
docker exec skincare-backend python3 -c "
from cli import load
load(method='char-split')
"
\`\`\`

---

## 🔧 故障排除

### 常见问题

#### 1. 容器无法启动

\`\`\`bash
# 查看日志
docker-compose logs

# 清理并重启
docker-compose down
docker-compose up -d
\`\`\`

#### 2. OpenAI API 错误

\`\`\`bash
# 检查 API Key
docker exec skincare-backend env | grep OPENAI_API_KEY

# 如果没有，编辑 .env 文件
nano .env
\`\`\`

#### 3. 前端依赖缺失

\`\`\`bash
# 安装依赖
docker exec skincare-frontend npm install

# 重启前端
docker-compose restart frontend
\`\`\`

#### 4. ChromaDB 数据丢失

\`\`\`bash
# 重新加载数据
docker exec skincare-backend python3 -c "
from cli import load
load(method='char-split')
"
\`\`\`

---

## 📝 命令速查表

### Docker 命令

\`\`\`bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看运行状态
docker ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart backend
docker-compose restart frontend
docker-compose restart chromadb

# 进入容器
docker exec -it skincare-backend bash
docker exec -it skincare-frontend sh
\`\`\`

### API 测试

\`\`\`bash
# 健康检查
curl http://localhost:8000/health

# 搜索产品
curl "http://localhost:8000/api/search?q=moisturizer&top_k=3"

# AI 聊天
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"推荐护肤品","history":[]}'
\`\`\`

---

## 🎯 性能指标

- **搜索响应时间**: ~500ms
- **Chat 响应时间**: ~8-12s (包含 GPT 调用)
- **数据加载时间**: ~5min (首次)
- **内存使用**: ~2GB (所有容器)

---

## 📄 许可证

本项目采用 MIT 许可证

---

## 🙏 致谢

- [EWG Skin Deep Database](https://www.ewg.org/skindeep/) - 护肤品数据
- [OpenAI](https://openai.com/) - GPT-4o-mini & Embeddings
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [FastAPI](https://fastapi.tiangolo.com/) - Python Web 框架
- [Next.js](https://nextjs.org/) - React 框架

---

<div align="center">
  <p>Made with ❤️ </p>
  <p>© 2025 Skincare AI Assistant</p>
</div>
