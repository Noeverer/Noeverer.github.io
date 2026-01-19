#!/bin/bash
# Wiki.js 部署脚本

set -e

echo "=== 部署 Wiki.js ==="

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "错误: .env 文件不存在"
    echo "请先复制 .env.example 并配置密码"
    exit 1
fi

# 创建目录
mkdir -p backup logs

# 备份现有数据（如果存在）
if docker volume ls | grep -q wikijs_wiki-data; then
    echo "备份现有数据..."
    docker run --rm -v wikijs_wiki-data:/data -v "$(pwd)/backup:/backup" alpine tar czf "/backup/wiki-data-predeploy-$(date +%Y%m%d-%H%M%S).tar.gz" -C /data . 2>/dev/null || true
fi

# 启动服务
echo "启动 Docker 容器..."
docker-compose up -d

# 等待服务就绪
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

echo "=== 部署完成 ==="
echo "访问地址: http://localhost:3000"
echo "查看日志: docker-compose logs -f"
echo ""
echo "首次访问请完成初始化向导:"
echo "1. 访问 http://localhost:3000"
echo "2. 配置管理员账户"
echo "3. 配置站点信息"
