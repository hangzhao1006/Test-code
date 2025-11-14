# 🚀 SkinMe - 快速启动指南

> 给测试同学的零基础启动教程

---

## 📋 准备工作

### 1. 安装 Docker Desktop

**必须先安装 Docker！这是唯一需要安装的软件。**

- **Mac**: 下载 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- **Windows**: 下载 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

安装完成后，确保 Docker Desktop 正在运行（系统托盘会显示 Docker 图标）。

### 2. 验证 Docker 安装

打开终端（Mac）或命令提示符（Windows），输入：

```bash
docker --version
docker-compose --version
```

应该看到版本号输出，例如：
```
Docker version 24.0.0
Docker Compose version v2.20.0
```

---

## 🎯 一键启动（3步）

### 步骤 1: 解压项目

将项目文件解压到任意目录，例如：
- Mac: `/Users/你的用户名/Desktop/app-building-template`
- Windows: `C:\Users\你的用户名\Desktop\app-building-template`

### 步骤 2: 进入项目目录

打开终端，进入项目目录：

```bash
# Mac/Linux
cd /path/to/app-building-template

# Windows (命令提示符)
cd C:\path\to\app-building-template
```

### 步骤 3: 启动所有服务

```bash
docker-compose up -d
```

等待 3-5 分钟让所有容器启动完成。

---

## ✅ 验证启动成功

### 检查容器状态

```bash
docker ps
```

应该看到 3 个容器在运行：
```
CONTAINER ID   IMAGE                     STATUS          PORTS                    NAMES
xxxxx          skincare-frontend         Up 2 minutes    0.0.0.0:3001->3000/tcp   skincare-frontend
xxxxx          skincare-backend          Up 2 minutes    0.0.0.0:8000->8000/tcp   skincare-backend
xxxxx          chromadb/chroma:latest    Up 2 minutes    0.0.0.0:8001->8000/tcp   skincare-chromadb
```

### 访问应用

打开浏览器，访问：

**http://localhost:3001**

你应该看到 SkinMe 的主页面！

---

## 🎮 使用指南

### 功能 1: 产品检索 (Query)

1. 点击 **🔍 产品检索 (Query)** 标签
2. 在搜索框输入，例如：`moisturizer for dry skin`
3. 点击 **🔍 搜索产品** 按钮
4. 查看推荐的护肤品列表

### 功能 2: AI 对话 (Chat)

1. 点击 **💬 AI对话 (Chat)** 标签
2. 在输入框输入问题，例如：`我的皮肤很干燥，推荐什么保湿霜？`
3. 点击 **💬 发送消息** 按钮
4. AI 会基于 7,933 个护肤品数据库给出专业建议

### 功能 3: 皮肤分析 (照片上传)

1. 在 **💬 AI对话** 标签下
2. 点击 **📷 上传照片** 按钮
3. 选择一张皮肤照片
4. （可选）添加补充信息，例如：`最近皮肤有点干燥`
5. 点击 **🔍 分析皮肤** 按钮
6. 等待 AI 分析并推荐产品

### 功能 4: 天气 & 日历

右侧边栏显示：
- 当前日期和时间
- 基于定位的天气信息
- 根据天气的护肤建议
- 皮肤状况记录

---

## 🔧 常见问题

### Q1: 端口被占用

**错误信息**: `port is already allocated`

**解决方法**:
```bash
# 停止其他占用端口的服务，或修改 docker-compose.yml 中的端口
# 例如将 3001 改为 3002
```

### Q2: Docker 内存不足

**错误信息**: `container killed: OOMKilled`

**解决方法**:
1. 打开 Docker Desktop
2. 进入 Settings → Resources
3. 增加内存到至少 4GB

### Q3: 容器启动失败

```bash
# 查看日志
docker-compose logs -f

# 重启所有服务
docker-compose down
docker-compose up -d
```

### Q4: 前端无法连接后端

**检查后端是否正常运行**:
```bash
curl http://localhost:8000/health
```

应该返回：
```json
{
  "status": "healthy",
  "service": "skincare-ai-backend",
  "version": "1.0.0"
}
```

---

## 🛑 停止服务

```bash
# 停止所有容器
docker-compose down

# 停止并删除所有数据（谨慎使用！）
docker-compose down -v
```

---

## 📊 系统要求

- **操作系统**: macOS 10.15+, Windows 10+, Linux
- **Docker**: 24.0.0+
- **内存**: 至少 4GB 可用
- **磁盘**: 至少 5GB 可用空间
- **网络**: 需要互联网连接（首次下载镜像）

---

## 🆘 获取帮助

如果遇到问题：

1. 查看日志：`docker-compose logs -f`
2. 检查容器状态：`docker ps -a`
3. 重启服务：`docker-compose restart`
4. 完全重置：`docker-compose down && docker-compose up -d`

---

## 📝 技术栈

- **前端**: Next.js 14 + React + TailwindCSS
- **后端**: FastAPI + Python 3.11
- **数据库**: ChromaDB (向量数据库)
- **AI**: OpenAI GPT-4o-mini + text-embedding-3-small
- **数据**: EWG 护肤品数据库 (7,933 产品)

---

## ✨ 特性亮点

- ✅ 7,933+ 护肤品数据
- ✅ RAG (检索增强生成) 技术
- ✅ GPT-4 Vision 皮肤分析
- ✅ 语义搜索（不是简单的关键词匹配）
- ✅ 实时天气 + 护肤建议
- ✅ 购买链接（Amazon + EWG）

---

**祝测试顺利！** 🎉
