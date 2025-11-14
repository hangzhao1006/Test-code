#!/bin/bash

echo "================================================"
echo "  SkinMe AI 护肤助手 - 完整重启脚本"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 步骤1: 停止所有容器
echo -e "${BLUE}[步骤 1/6]${NC} 停止所有运行中的容器..."
docker-compose down
echo -e "${GREEN}✓${NC} 容器已停止"
echo ""

# 步骤2: 检查必要文件
echo -e "${BLUE}[步骤 2/6]${NC} 检查必要文件..."

if [ -f "secrets/ewg-data.json" ]; then
    echo -e "${GREEN}✓${NC} GCP 凭证文件存在"
else
    echo -e "${RED}✗${NC} GCP 凭证文件不存在: secrets/ewg-data.json"
    exit 1
fi

if [ -f "input-datasets/outputs/ewg_index.npz" ]; then
    echo -e "${GREEN}✓${NC} 向量索引文件存在"
else
    echo -e "${RED}✗${NC} 向量索引文件不存在: input-datasets/outputs/ewg_index.npz"
    exit 1
fi

if [ -f "input-datasets/outputs/ewg_meta.jsonl" ]; then
    echo -e "${GREEN}✓${NC} 元数据文件存在"
else
    echo -e "${RED}✗${NC} 元数据文件不存在: input-datasets/outputs/ewg_meta.jsonl"
    exit 1
fi

echo ""

# 步骤3: 清理旧的镜像（可选）
echo -e "${BLUE}[步骤 3/6]${NC} 清理 Docker 缓存（可选）..."
read -p "是否清理 Docker 缓存？这会删除未使用的镜像和容器。(y/N): " clean_cache
if [ "$clean_cache" = "y" ] || [ "$clean_cache" = "Y" ]; then
    docker system prune -f
    echo -e "${GREEN}✓${NC} Docker 缓存已清理"
else
    echo -e "${YELLOW}⊘${NC} 跳过清理"
fi
echo ""

# 步骤4: 构建并启动容器
echo -e "${BLUE}[步骤 4/6]${NC} 构建并启动所有服务..."
echo -e "${YELLOW}这可能需要几分钟时间，请耐心等待...${NC}"
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 容器启动成功"
else
    echo -e "${RED}✗${NC} 容器启动失败"
    exit 1
fi
echo ""

# 步骤5: 等待服务就绪
echo -e "${BLUE}[步骤 5/6]${NC} 等待服务就绪..."
echo -e "${YELLOW}等待 40 秒让所有服务完全启动...${NC}"

for i in {40..1}; do
    echo -ne "\r倒计时: ${i} 秒... "
    sleep 1
done
echo -e "\n${GREEN}✓${NC} 等待完成"
echo ""

# 步骤6: 检查服务状态
echo -e "${BLUE}[步骤 6/6]${NC} 检查服务状态..."
echo ""

# 检查容器状态
echo -e "${YELLOW}容器状态:${NC}"
docker-compose ps
echo ""

# 测试后端健康检查
echo -e "${YELLOW}测试后端 API:${NC}"
BACKEND_HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} 后端 API 正常"
    echo "  响应: $BACKEND_HEALTH"
else
    echo -e "${RED}✗${NC} 后端 API 无响应"
fi
echo ""

# 测试 ChromaDB
echo -e "${YELLOW}测试 ChromaDB:${NC}"
CHROMA_HEALTH=$(curl -s http://localhost:8001/api/v1/heartbeat)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} ChromaDB 正常"
else
    echo -e "${RED}✗${NC} ChromaDB 无响应"
fi
echo ""

# 完成
echo "================================================"
echo -e "${GREEN}✓ 所有服务已启动！${NC}"
echo "================================================"
echo ""
echo "📱 访问方式:"
echo "   主应用:      http://localhost:3001"
echo "   API 文档:    http://localhost:8000/docs"
echo "   健康检查:    http://localhost:8000/health"
echo ""
echo "📝 测试天气功能:"
echo "   1. 在浏览器中打开: http://localhost:3001"
echo "   2. 允许位置权限"
echo "   3. 查看右侧天气卡片"
echo ""
echo "   或者使用测试页面:"
echo "   file://$(pwd)/test-weather-browser.html"
echo ""
echo "🔍 查看日志:"
echo "   所有服务: docker-compose logs -f"
echo "   前端:     docker-compose logs -f frontend"
echo "   后端:     docker-compose logs -f backend"
echo ""
echo "🛑 停止服务: docker-compose down"
echo ""
