#!/bin/bash
# Wiki.js 快速启动脚本

echo "=== Wiki.js 快速启动 ==="

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose 未安装"
    exit 1
fi

# 进入部署目录
cd "$(dirname "$0")"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "未找到 .env 文件，从 .env.example 创建..."
    cp .env.example .env
    echo "请编辑 .env 文件设置数据库密码后重新运行"
    exit 1
fi

# 启动服务
echo "启动 Wiki.js..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 15

# 检查状态
docker-compose ps

echo ""
echo "=== 启动完成 ==="
echo "访问地址: http://localhost:3000"
echo ""
echo "首次访问请完成初始化配置："
echo "  1. 选择数据库: PostgreSQL"
echo "  2. 数据库主机: wiki-db"
echo "  3. 数据库端口: 5432"
echo "  4. 数据库用户名: wikijs"
echo "  5. 数据库密码: 见 .env 文件"
echo "  6. 数据库名称: wikijs"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
