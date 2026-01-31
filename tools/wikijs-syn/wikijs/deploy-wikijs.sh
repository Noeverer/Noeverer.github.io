#!/bin/bash

# Wiki.js 部署脚本
set -e

echo "=== 开始部署 Wiki.js ==="

# 检查是否已存在 wikijs-deploy 目录
if [ ! -d "/home/ante/10-personal/Noeverer.github.io/wikijs-deploy" ]; then
    echo "错误: wikijs-deploy 目录不存在，请先创建该目录及相关配置文件"
    exit 1
fi

cd /home/ante/10-personal/Noeverer.github.io/wikijs-deploy

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "创建默认 .env 文件..."
    echo "DB_PASSWORD=changeme123!" > .env
    echo "注意: 请修改 .env 文件中的密码为安全密码！"
fi

# 启动服务
echo "启动 Wiki.js 服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 15

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 显示访问信息
echo ""
echo "==========================================="
echo "Wiki.js 部署成功！"
echo ""
echo "访问地址: http://localhost:3000"
echo "管理后台: http://localhost:3000/admin"
echo ""
echo "下一步操作:"
echo "1. 访问 http://localhost:3000 完成初始化配置"
echo "2. 配置 Git 存储以同步内容到 GitHub"
echo "3. 设置 GitHub Actions 自动部署到 GitHub Pages"
echo "==========================================="