#!/bin/bash
# VitePress 初始化脚本

set -e

echo "=== VitePress 初始化 ==="

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "错误: Node.js 未安装"
    echo "请先安装 Node.js: https://nodejs.org/"
    exit 1
fi

echo "Node.js 版本: $(node --version)"
echo "npm 版本: $(npm --version)"

# 安装依赖
echo ""
echo "安装依赖..."
npm install

# 创建必要的目录（如果不存在）
mkdir -p docs/programming
mkdir -p docs/study
mkdir -p docs/life
mkdir -p backup

echo ""
echo "=== 初始化完成 ==="
echo ""
echo "下一步操作:"
echo "  1. 本地开发: npm run dev"
echo "  2. 构建站点: npm run build"
echo "  3. 预览构建: npm run preview"
echo ""
echo "文档已创建在 docs/ 目录"
