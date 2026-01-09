#!/bin/bash

# Wiki.js 部署脚本
# 用于快速部署 Wiki.js 服务

set -e

echo "========================================="
echo "   Wiki.js Docker 部署脚本"
echo "========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: Docker Compose 未安装${NC}"
    echo "请先安装 Docker Compose"
    exit 1
fi

# 获取 GitHub 仓库信息
echo ""
echo -e "${YELLOW}请输入 GitHub 仓库信息:${NC}"
read -p "GitHub 用户名: " github_username
read -p "GitHub 仓库名: " github_repo

if [ -z "$github_username" ] || [ -z "$github_repo" ]; then
    echo -e "${RED}错误: 用户名和仓库名不能为空${NC}"
    exit 1
fi

# 更新配置文件
echo ""
echo -e "${GREEN}更新配置文件...${NC}"
sed -i "s/YOUR_USERNAME/$github_username/g" config.yml
sed -i "s/YOUR_USERNAME/$github_username/g" docker-compose.yml
sed -i "s/YOUR_REPO/$github_repo/g" config.yml
sed -i "s/YOUR_REPO/$github_repo/g" docker-compose.yml

# 创建必要的目录
echo -e "${GREEN}创建数据目录...${NC}"
mkdir -p ./data/git

# 设置 SSH 密钥
echo ""
echo -e "${YELLOW}配置 Git SSH 密钥${NC}"
read -p "是否配置 SSH 密钥用于 Git 仓库访问? (y/n): " configure_ssh

if [ "$configure_ssh" = "y" ] || [ "$configure_ssh" = "Y" ]; then
    if [ -f ~/.ssh/id_rsa ]; then
        cp ~/.ssh/id_rsa ./data/git/id_rsa
        chmod 600 ./data/git/id_rsa
        echo -e "${GREEN}SSH 私钥已复制${NC}"
    else
        echo -e "${YELLOW}未找到默认 SSH 私钥，跳过${NC}"
    fi
fi

# 构建和启动容器
echo ""
echo -e "${GREEN}构建和启动容器...${NC}"
docker-compose down 2>/dev/null || true
docker-compose up -d --build

# 等待服务启动
echo ""
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo ""
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Wiki.js 服务已成功启动!${NC}"
    echo ""
    echo "访问地址: http://localhost:3000"
    echo ""
    echo "首次访问时，您需要:"
    echo "1. 创建管理员账户"
    echo "2. 配置存储类型为 Git"
    echo "3. 设置 Git 仓库地址"
    echo ""
    echo "查看日志: docker-compose logs -f"
    echo "停止服务: docker-compose down"
    echo "重启服务: docker-compose restart"
else
    echo -e "${RED}✗ 服务启动失败${NC}"
    echo "请检查日志: docker-compose logs"
    exit 1
fi

echo ""
echo "========================================="
