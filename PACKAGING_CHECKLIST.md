# 📦 打包清单 - 给同学测试前的准备

## ✅ 必须检查的项目

### 1. 环境变量配置

- [ ] `.env` 文件已包含有效的 OpenAI API Key
- [ ] `.env.example` 文件已创建（作为模板）

```bash
# 检查 .env 文件
cat .env

# 应该看到：
# OPENAI_API_KEY=sk-proj-...
```

### 2. 数据文件完整性

- [ ] `backend/input-datasets/` 目录存在
- [ ] embedding 文件存在（`embeddings-char-split-*.jsonl`）
- [ ] 原始数据文件存在（`ewg_face_label_structured.jsonl`）

```bash
# 检查数据文件数量
ls backend/input-datasets/outputs/embeddings-char-split-*.jsonl | wc -l
# 应该显示多个文件

ls backend/input-datasets/structured/*.jsonl
# 应该显示 ewg_face_label_structured.jsonl
```

### 3. Docker 配置文件

- [ ] `docker-compose.yml` 存在
- [ ] `backend/Dockerfile.dev` 存在
- [ ] `frontend-template/Dockerfile.dev` 存在

```bash
# 验证文件存在
ls -la docker-compose.yml
ls -la backend/Dockerfile.dev
ls -la frontend-template/Dockerfile.dev
```

### 4. 文档完整性

- [ ] `README.md` 包含完整的项目介绍
- [ ] `QUICK_START.md` 包含快速启动指南
- [ ] `PACKAGING_CHECKLIST.md` 包含打包清单（本文件）

### 5. 清理不必要的文件

- [ ] 已删除所有 `.sh` 脚本文件
- [ ] 已删除 `frontend-example/` 目录
- [ ] 已删除 `secrets/` 目录
- [ ] 已删除 `backend/backend/` 空目录
- [ ] 已删除未使用的 Python 文件

```bash
# 检查是否还有 .sh 文件
ls *.sh 2>/dev/null || echo "✅ 所有 .sh 文件已删除"

# 检查是否还有不需要的目录
ls -d frontend-example 2>/dev/null && echo "❌ 需要删除 frontend-example" || echo "✅ frontend-example 已删除"
ls -d secrets 2>/dev/null && echo "❌ 需要删除 secrets" || echo "✅ secrets 已删除"
```

---

## 📋 打包步骤

### 方法 1: 压缩整个项目（推荐）

```bash
# 进入项目父目录
cd /Users/apple/Downloads/25FALL-Courses/APCOMP\ 215/class16/

# 创建压缩包（排除不需要的文件）
tar -czf SkinMe-Project.tar.gz \
  --exclude='app-building-template/node_modules' \
  --exclude='app-building-template/.next' \
  --exclude='app-building-template/__pycache__' \
  --exclude='app-building-template/.DS_Store' \
  --exclude='app-building-template/frontend-template/node_modules' \
  --exclude='app-building-template/frontend-template/.next' \
  app-building-template/

# 或者使用 zip（Windows 友好）
zip -r SkinMe-Project.zip app-building-template/ \
  -x "*/node_modules/*" \
  -x "*/.next/*" \
  -x "*/__pycache__/*" \
  -x "*/.DS_Store"
```

### 方法 2: 使用 Git（如果项目已初始化 Git）

```bash
# 确保所有更改已提交
git add .
git commit -m "准备打包给同学测试"

# 创建 Git 归档
git archive --format=zip -o SkinMe-Project.zip HEAD
```

---

## 🎯 给同学的交付物

### 必须包含的文件/目录：

```
SkinMe-Project/
├── .env                           # ✅ OpenAI API Key
├── .env.example                   # ✅ 环境变量模板
├── .gitignore                     # ✅ Git 忽略规则
├── docker-compose.yml             # ✅ Docker 编排配置
├── README.md                      # ✅ 完整文档
├── QUICK_START.md                 # ✅ 快速启动指南
├── backend/
│   ├── Dockerfile.dev             # ✅ 后端 Docker 配置
│   ├── requirements.txt           # ✅ Python 依赖
│   ├── cli.py                     # ✅ 核心工具
│   ├── reload_with_links.py       # ✅ 数据加载脚本
│   ├── api/
│   │   ├── main.py               # ✅ FastAPI 主应用
│   │   └── routes/               # ✅ API 路由
│   ├── credentials/              # ✅ GCP 凭证（如果有）
│   └── input-datasets/           # ✅ 数据集
│       ├── structured/
│       │   └── ewg_face_label_structured.jsonl
│       └── outputs/
│           └── embeddings-char-split-*.jsonl (多个文件)
└── frontend-template/
    ├── Dockerfile.dev            # ✅ 前端 Docker 配置
    ├── package.json              # ✅ Node.js 依赖
    ├── next.config.js            # ✅ Next.js 配置
    └── src/
        ├── app/
        │   └── page.jsx          # ✅ 主页面
        └── components/
            ├── ui/               # ✅ UI 组件
            └── WeatherCalendar.jsx  # ✅ 天气日历组件
```

---

## 🚀 测试清单（打包前）

### 1. 本地测试

```bash
# 停止所有容器
docker-compose down

# 重新启动
docker-compose up -d

# 等待服务启动（约 2-3 分钟）
sleep 120

# 检查容器状态
docker ps

# 测试后端健康检查
curl http://localhost:8000/health

# 测试前端
curl http://localhost:3001
```

### 2. 功能测试

- [ ] 访问 http://localhost:3001 显示主页
- [ ] 产品检索功能正常
- [ ] AI 对话功能正常
- [ ] 图片分析功能正常
- [ ] 天气显示正常（基于定位）
- [ ] 购买链接可以点击

### 3. 性能测试

```bash
# 测试搜索性能
time curl "http://localhost:8000/api/search?q=moisturizer&top_k=5"
# 应该 < 2 秒

# 检查容器资源使用
docker stats --no-stream
# 内存使用应该 < 4GB
```

---

## 📝 给同学的说明文档

打包时附带以下文档：

1. **QUICK_START.md** - 快速启动指南（零基础）
2. **README.md** - 完整项目文档
3. **一封简短的邮件/消息**：

```
嗨！

这是我开发的 SkinMe 护肤品推荐系统，请帮我测试一下。

只需要三步：
1. 安装 Docker Desktop
2. 解压项目文件
3. 运行 `docker-compose up -d`

详细步骤请看 QUICK_START.md 文件。

如果遇到问题，请：
- 查看 QUICK_START.md 的"常见问题"部分
- 或直接联系我

测试重点：
✅ 产品检索是否准确
✅ AI 对话是否流畅
✅ 图片分析是否有效
✅ 整体用户体验

谢谢！
```

---

## ⚠️ 注意事项

1. **API Key**: .env 文件包含真实的 OpenAI API Key
   - 提醒同学不要分享这个文件
   - 测试完成后可以考虑撤销这个 Key

2. **数据大小**: 完整项目约 500MB-1GB（包含所有 embeddings）
   - 确保同学有足够的硬盘空间
   - 建议使用云盘分享或压缩包

3. **网络要求**:
   - 首次启动需要下载 Docker 镜像（约 1-2GB）
   - 需要访问 OpenAI API（需要稳定网络）
   - 天气功能需要访问 wttr.in API

4. **系统要求**:
   - Docker Desktop 最新版
   - 至少 4GB 可用内存
   - 至少 5GB 可用硬盘空间

---

## ✅ 最终检查

打包前最后检查：

```bash
# 1. 检查 .env 文件
cat .env | grep OPENAI_API_KEY

# 2. 检查数据文件数量
ls backend/input-datasets/outputs/*.jsonl | wc -l

# 3. 检查文档完整性
ls -la README.md QUICK_START.md

# 4. 测试一次完整流程
docker-compose down
docker-compose up -d
sleep 120
curl http://localhost:8000/health
curl http://localhost:3001

# 5. 如果一切正常，执行打包
cd ..
tar -czf SkinMe-Project.tar.gz app-building-template/
```

完成！🎉
