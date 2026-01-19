#!/bin/bash

# Wiki.js 部署验证脚本
set -e

echo "=== 开始验证 Wiki.js 部署 ==="

# 检查 Docker 和 Docker Compose 是否已安装
echo "检查 Docker 和 Docker Compose..."
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose 未安装"
    exit 1
fi

echo "Docker 和 Docker Compose 已安装"

# 检查 Wiki.js 部署目录
DEPLOY_DIR="/home/ante/10-personal/Noeverer.github.io/wikijs-deploy"
if [ ! -d "$DEPLOY_DIR" ]; then
    echo "错误: 部署目录不存在: $DEPLOY_DIR"
    exit 1
fi

echo "部署目录存在: $DEPLOY_DIR"

# 检查必要的配置文件
CONFIG_FILES=(
    "$DEPLOY_DIR/docker-compose.yml"
    "$DEPLOY_DIR/.env"
    "$DEPLOY_DIR/deploy.sh"
    "$DEPLOY_DIR/nginx/wikijs.conf"
)

for file in "${CONFIG_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "错误: 配置文件不存在: $file"
        exit 1
    fi
done

echo "所有配置文件存在"

# 检查容器状态
echo "检查正在运行的容器..."
if [ -f "$DEPLOY_DIR/docker-compose.yml" ]; then
    cd "$DEPLOY_DIR"
    
    # 获取容器状态
    CONTAINER_STATUS=$(docker-compose ps --status running --format json 2>/dev/null || echo "")
    
    if [[ -z "$CONTAINER_STATUS" ]]; then
        echo "警告: 容器未运行，尝试启动..."
        ./deploy.sh
        sleep 10
    else
        echo "容器正在运行"
    fi
    
    # 检查特定容器
    WIKI_RUNNING=$(docker-compose ps | grep "wikijs.*Up")
    DB_RUNNING=$(docker-compose ps | grep "wikijs-db.*Up")
    
    if [[ -n "$WIKI_RUNNING" ]]; then
        echo "✓ Wiki.js 容器正在运行"
    else
        echo "✗ Wiki.js 容器未运行"
    fi
    
    if [[ -n "$DB_RUNNING" ]]; then
        echo "✓ 数据库容器正在运行"
    else
        echo "✗ 数据库容器未运行"
    fi
fi

# 检查端口是否开放
echo "检查端口连通性..."
if nc -z localhost 3000; then
    echo "✓ 端口 3000 (Wiki.js) 可访问"
else
    echo "? 端口 3000 (Wiki.js) 不可访问"
fi

# 检查 VitePress 配置
CONTENT_DIR="/home/ante/10-personal/wikijs-content"
if [ -d "$CONTENT_DIR" ]; then
    echo "✓ GitHub Pages 内容目录存在: $CONTENT_DIR"
    
    # 检查关键文件
    if [ -f "$CONTENT_DIR/package.json" ] && [ -f "$CONTENT_DIR/.vitepress/config.ts" ]; then
        echo "✓ VitePress 配置文件存在"
    else
        echo "? VitePress 配置文件缺失"
    fi
else
    echo "? GitHub Pages 内容目录不存在: $CONTENT_DIR"
fi

# 检查 GitHub Actions 配置
if [ -f "$CONTENT_DIR/.github/workflows/build-pages.yml" ]; then
    echo "✓ GitHub Actions 工作流配置存在"
else
    echo "? GitHub Actions 工作流配置缺失"
fi

echo ""
echo "==========================================="
echo "部署验证完成"
echo ""
echo "要完成 Wiki.js 与 GitHub Pages 的完整联动，还需要："
echo "1. 访问 http://localhost:3000 完成初始设置"
echo "2. 配置 Git 存储以同步内容到 GitHub"
echo "3. 设置 GitHub 仓库和访问令牌"
echo "4. 配置自定义域名 (可选)"
echo "==========================================="