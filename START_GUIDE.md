# SkinMe AI 护肤助手 - 完整启动指南

## 📋 项目概述

基于 EWG 数据库的 AI 护肤产品推荐系统，集成了：
- ✅ RAG 语义搜索 (ChromaDB + OpenAI Embeddings)
- ✅ AI 对话助手 (Vertex AI)
- ✅ GPT-4 Vision 皮肤分析
- ✅ 实时天气显示 (Open-Meteo API)
- ✅ 中英文双语支持
- ✅ 皮肤状况历史记录

---

## 🚀 从头启动步骤

### 1. 停止并清理现有容器

```bash
cd /Users/apple/Downloads/25FALL-Courses/APCOMP\ 215/class16/app-building-template

# 停止所有容器
docker-compose down

# 可选：清理所有容器和卷（如果需要完全重置）
# docker-compose down -v
```

### 2. 确认必要文件存在

检查以下关键文件：

```bash
# GCP 凭证文件
ls -la secrets/ewg-data.json

# 数据集文件
ls -la input-datasets/outputs/ewg_index.npz
ls -la input-datasets/outputs/ewg_meta.jsonl
```

### 3. 启动所有服务

```bash
# 构建并启动所有容器
docker-compose up --build -d

# 查看启动日志
docker-compose logs -f
```

### 4. 等待服务就绪

**等待约 30-60 秒**，让所有服务完全启动。可以通过以下命令检查：

```bash
# 检查容器状态
docker-compose ps

# 应该看到 3 个容器都是 "Up" 状态：
# - skincare-backend    (port 8000)
# - skincare-frontend   (port 3001)
# - skincare-chromadb   (port 8001)
```

### 5. 验证服务

```bash
# 测试后端 API
curl http://localhost:8000/health

# 测试 ChromaDB
curl http://localhost:8001/api/v1/heartbeat

# 前端会在浏览器中打开：
# http://localhost:3001
```

---

## 🌐 访问应用

### 主应用
打开浏览器访问：**http://localhost:3001**

### API 文档
- **FastAPI Docs**: http://localhost:8000/docs
- **后端健康检查**: http://localhost:8000/health

---

## ✨ 功能说明

### 1. 产品检索 (🔍 Product Search)
- 使用自然语言搜索护肤品
- 基于 ChromaDB 向量相似度检索
- 显示产品详情、成分、EWG 评分

### 2. AI 对话 (💬 AI Chat)
- 与 AI 护肤顾问对话
- 获取个性化护肤建议
- 支持上传图片进行分析

### 3. 皮肤分析 (📷 Photo Analysis)
- 上传皮肤照片
- GPT-4 Vision 自动分析肤质和问题
- 推荐适合的护肤品

### 4. 天气日历 (右侧边栏)
- **实时天气显示**（使用 Open-Meteo API）
- 自动获取您的位置
- 根据天气提供护肤建议
- 记录每日皮肤状况

### 5. 语言切换
- 点击顶部的 🇨🇳/🇺🇸 按钮
- 支持中文/英文界面
- 天气描述自动切换语言

---

## 🔧 天气功能说明

### 使用的 API
**Open-Meteo** (https://open-meteo.com/)
- ✅ 完全免费，无需 API key
- ✅ 支持 CORS，可直接从浏览器调用
- ✅ 无调用限制
- ✅ 全球范围天气数据

### 如何使用
1. 首次打开应用时，浏览器会请求位置权限
2. **允许位置权限**，系统会显示您当前位置的实时天气
3. 如果拒绝权限，系统会使用默认城市（Boston）的天气
4. 点击天气卡片中的 🔄 按钮可刷新天气数据

### 如果天气无法显示
**可能原因**：
- 浏览器阻止了位置权限
- 网络连接问题
- API 临时不可用

**解决方法**：
1. 检查浏览器控制台（F12）查看错误信息
2. 确保浏览器允许了位置权限
3. 点击 🔄 按钮重新获取
4. 如果仍然失败，应用会显示 "--" 作为占位符

---

## 📝 环境变量

重要的环境变量（在 `.env` 或 `docker-compose.yml` 中）：

```bash
# Google Cloud 配置
GCP_PROJECT=301578946659
GCP_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/app/backend/credentials/gcp-key.json

# OpenAI 配置
OPENAI_API_KEY=your_openai_api_key_here

# ChromaDB 配置
CHROMA_HOST=chromadb
CHROMA_PORT=8000
```

---

## 🐛 常见问题

### 1. 前端无法连接后端
```bash
# 检查后端是否运行
docker logs skincare-backend --tail 50

# 重启后端
docker-compose restart backend
```

### 2. ChromaDB 数据未加载
```bash
# 确认数据文件存在
ls -la input-datasets/outputs/

# 重新构建并启动
docker-compose up --build -d
```

### 3. 天气功能不工作
- 打开浏览器开发者工具（F12）
- 查看 Console 标签页的错误信息
- 确认网络请求到 `api.open-meteo.com` 成功
- 允许浏览器的位置权限

### 4. 语言切换不生效
- 清除浏览器缓存和 localStorage
- 刷新页面（Ctrl+Shift+R 或 Cmd+Shift+R）

---

## 🔄 完全重启流程

如果遇到任何问题，可以执行完全重启：

```bash
# 1. 停止所有容器
docker-compose down

# 2. 可选：删除卷数据（会清除 ChromaDB 数据）
# docker-compose down -v

# 3. 清理 Docker 缓存（可选）
# docker system prune -a

# 4. 重新构建和启动
docker-compose up --build -d

# 5. 查看日志
docker-compose logs -f

# 6. 等待 30-60 秒后访问
# http://localhost:3001
```

---

## 📊 系统架构

```
┌─────────────────┐
│   Frontend      │  Next.js 15.5.6 (Port 3001)
│   (React)       │  - 产品检索界面
└────────┬────────┘  - AI 对话界面
         │           - 皮肤分析界面
         │           - 天气日历组件
         ▼
┌─────────────────┐
│   Backend       │  FastAPI (Port 8000)
│   (Python)      │  - RAG 检索
└────────┬────────┘  - AI 对话处理
         │           - 图片分析
         │           - 天气代理（可选）
         ▼
┌─────────────────┐
│   ChromaDB      │  向量数据库 (Port 8001)
│                 │  - 7,933 个产品向量
└─────────────────┘  - OpenAI Embeddings
         │
         ▼
┌─────────────────┐
│  External APIs  │
│                 │  - Vertex AI (Google Cloud)
│                 │  - OpenAI GPT-4 Vision
│                 │  - Open-Meteo Weather API
└─────────────────┘
```

---

## 📞 支持

如有问题，请检查：
1. Docker 容器日志：`docker-compose logs [service-name]`
2. 浏览器控制台（F12）
3. 后端 API 文档：http://localhost:8000/docs

---

**最后更新**: 2025-11-14
**版本**: 1.0.0
