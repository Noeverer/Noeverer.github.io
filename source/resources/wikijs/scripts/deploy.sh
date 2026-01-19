#!/bin/bash
#
# Wiki.js 部署脚本
# 用法: ./deploy.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  Wiki.js 部署脚本"
echo "========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${RED}错误: .env 文件不存在${NC}"
    echo -e "${YELLOW}请先复制 .env.example 并配置密码:${NC}"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# 加载环境变量
export $(grep -v '^#' .env | xargs)

# 验证必要的环境变量
if [ "$DB_PASSWORD" = "your_secure_password_here" ]; then
    echo -e "${RED}错误: 请先在 .env 文件中设置数据库密码${NC}"
    exit 1
fi

# 创建必要的目录
echo -e "${GREEN}[1/5] 创建目录结构...${NC}"
mkdir -p backup logs

# 备份现有数据（如果存在）
if [ -f "docker-compose.yml" ] && docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}[2/5] 备份现有数据...${NC}"
    BACKUP_NAME="backup/wiki-data-$(date +%Y%m%d-%H%M%S).tar.gz"
    docker-compose exec wiki tar czf - /wiki/data 2>/dev/null | gzip > "$BACKUP_NAME" || echo "警告: 数据备份跳过（容器未运行）"
fi

# 拉取最新镜像
echo -e "${GREEN}[3/5] 拉取 Docker 镜像...${NC}"
docker-compose pull

# 启动服务
echo -e "${GREEN}[4/5] 启动 Docker 容器...${NC}"
docker-compose up -d

# 等待服务就绪
echo -e "${GREEN}[5/5] 等待服务启动...${NC}"
MAX_ATTEMPTS=30
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|302"; then
        echo -e "${GREEN}✓ Wiki.js 已成功启动！${NC}"
        break
    fi
    ATTEMPT=$((ATTEMPT + 1))
    echo "等待服务启动... ($ATTEMPT/$MAX_ATTEMPTS)"
    sleep 2
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo -e "${RED}警告: 服务启动超时，请检查日志${NC}"
fi

# 显示服务状态
echo ""
echo "========================================="
echo "  部署完成"
echo "========================================="
echo ""
echo -e "${GREEN}服务状态:${NC}"
docker-compose ps
echo ""
echo -e "${GREEN}访问地址:${NC}"
echo "  本地: http://localhost:3000"
echo "  远程: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo -e "${YELLOW}常用命令:${NC}"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo "  备份数据: ./backup/backup.sh"
echo ""
echo -e "${GREEN}下一步:${NC}"
echo "1. 访问 Wiki.js 完成初始化配置"
echo "2. 在 Wiki.js 中配置 Git 存储（参考 Git 存储配置文档）"
echo ""
