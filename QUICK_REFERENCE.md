# 🚀 快速参考卡片

## 一键启动（推荐）

```bash
# 1. 首次使用
./docker-shell-enhanced.sh setup    # 初始化 + 下载数据

# 2. 启动所有服务
./docker-shell-enhanced.sh start    # 后台运行
# 或
./docker-shell-enhanced.sh start-dev # 交互式（可看日志）

# 3. 访问
# 前端:     http://localhost:3001
# 后端 API: http://localhost:8000/docs
# ChromaDB: http://localhost:8001
```

---

## 📋 常用命令速查表

### 容器管理
```bash
./docker-shell-enhanced.sh start      # 启动所有容器
./docker-shell-enhanced.sh stop       # 停止所有容器
./docker-shell-enhanced.sh restart    # 重启
./docker-shell-enhanced.sh status     # 查看状态
./docker-shell-enhanced.sh health     # 健康检查
```

### 日志查看
```bash
./docker-shell-enhanced.sh logs              # 所有日志
./docker-shell-enhanced.sh logs-backend      # 后端日志
./docker-shell-enhanced.sh logs-frontend     # 前端日志
```

### 容器访问
```bash
./docker-shell-enhanced.sh shell             # 进入后端
./docker-shell-enhanced.sh shell-frontend    # 进入前端
```

### 数据同步
```bash
./docker-shell-enhanced.sh sync-data      # 从 GCS 下载
./docker-shell-enhanced.sh upload-data    # 上传到 GCS
```

---

## 🐛 快速调试

```bash
# 1. 查看容器状态
./docker-shell-enhanced.sh status

# 2. 健康检查
./docker-shell-enhanced.sh health

# 3. 查看后端日志
./docker-shell-enhanced.sh logs-backend

# 4. 进入后端容器测试
./docker-shell-enhanced.sh shell
python -c "from cli import ewg_query; print(ewg_query('test', 1))"
```

---

## 📁 三个脚本选择

| 脚本 | 使用场景 |
|------|---------|
| **docker-shell-enhanced.sh** ⭐ | **完整开发（推荐）** |
| docker-shell.sh | 标准三容器应用 |
| infra/docker-shell.sh | 原始脚本（备份） |

---

## 🔧 配置文件位置

```bash
.env.example              # 环境变量模板
docker-compose.yml        # 开发环境配置
docker-compose.prod.yml   # 生产环境配置
backend/api/main.py       # 后端入口
frontend/src/lib/SkincareService.js  # 前端 API 层
```

---

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| **YOUR_PROJECT_SUMMARY.md** | 📖 从这里开始 |
| **DOCKER_SCRIPT_COMPARISON.md** | 🐳 脚本对比 |
| **DOCKER_DEPLOYMENT_GUIDE.md** | 🚀 部署指南 |
| **EWG_RAG_INTEGRATION_GUIDE.md** | 🔧 集成指南 |

---

## ⚡ 核心架构

```
                    docker-shell-enhanced.sh
                            ↓
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
┌───▼────┐           ┌──────▼──────┐        ┌──────▼──────┐
│ChromaDB│◄──────────┤   Backend   │◄───────┤  Frontend   │
│:8001   │           │   (FastAPI) │        │  (Next.js)  │
│        │           │   :8000     │        │   :3001     │
└────────┘           └─────────────┘        └─────────────┘
  向量DB              ewg_query()              查询界面
```

---

## 💡 Tips

1. **开发时**: 使用 `start-dev` 查看实时日志
2. **调试时**: 用 `shell` 进入容器测试函数
3. **部署前**: 运行 `health` 确保所有服务正常
4. **数据更新**: 用 `sync-data` 同步最新数据

---

## 🆘 遇到问题？

```bash
# 查看完整帮助
./docker-shell-enhanced.sh help

# 查看容器状态
docker ps -a

# 查看网络
docker network ls | grep llm-rag

# 重启所有服务
./docker-shell-enhanced.sh restart

# 完全清理重来（谨慎！）
./docker-shell-enhanced.sh clean
./docker-shell-enhanced.sh start
```
