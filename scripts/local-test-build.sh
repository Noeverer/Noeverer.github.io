#!/bin/bash

# 本地构建测试脚本 - 模拟 GitHub Actions 构建过程

set -e

echo "=== 本地构建测试脚本 ==="
echo "此脚本模拟 GitHub Actions 的构建过程"
echo ""

# 检查是否在正确的目录
if [ ! -f "_config.yml" ]; then
    echo "❌ 错误: 请在 Hexo 博客根目录运行此脚本"
    exit 1
fi

# 1. 显示环境信息
echo "1. 环境信息..."
echo "Node version: $(node --version 2>/dev/null || echo 'Node.js 未安装')"
echo "NPM version: $(npm --version 2>/dev/null || echo 'NPM 未安装')"
echo "Working directory: $(pwd)"
echo ""

# 2. 检查依赖
echo "2. 检查依赖..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules 不存在，正在安装依赖..."
    npm install
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi
echo ""

# 3. 检查主题
echo "3. 检查主题..."
if [ -d "node_modules/hexo-theme-butterfly" ]; then
    echo "✅ butterfly 主题已安装"
else
    echo "❌ butterfly 主题未安装"
    exit 1
fi
echo ""

# 4. 清理缓存
echo "4. 清理 Hexo 缓存..."
npx hexo clean || hexo clean
echo "✅ 缓存清理完成"
echo ""

# 5. 生成静态文件
echo "5. 生成静态文件..."
npx hexo generate || hexo generate
echo "✅ 静态文件生成完成"
echo ""

# 6. 验证构建输出
echo "6. 验证构建输出..."
if [ ! -d "public" ]; then
    echo "❌ 错误: public 目录未生成"
    exit 1
fi

if [ ! -f "public/index.html" ]; then
    echo "❌ 错误: index.html 未生成"
    exit 1
fi

echo "✅ index.html 已生成"

# 显示 public 目录内容
echo ""
echo "📊 public 目录内容（前 20 行）:"
ls -la public/ | head -n 20
echo ""

# 统计文件
FILE_COUNT=$(find public -type f | wc -l)
echo "📊 生成的文件总数: $FILE_COUNT"
echo ""

# 检查文章页面
echo "7. 检查文章页面..."
POST_COUNT=$(find public/posts -name "index.html" 2>/dev/null | wc -l)
echo "📝 文章页面数量: $POST_COUNT"
echo ""

# 检查分类和标签页面
echo "8. 检查分类和标签页面..."
if [ -f "public/categories/index.html" ]; then
    echo "✅ 分类页面已生成"
else
    echo "⚠️  分类页面未生成"
fi

if [ -f "public/tags/index.html" ]; then
    echo "✅ 标签页面已生成"
else
    echo "⚠️  标签页面未生成"
fi
echo ""

# 9. 显示构建摘要
echo "=== 构建摘要 ==="
echo "✅ 构建成功完成！"
echo "📁 构建输出目录: $(pwd)/public"
echo "📊 文件总数: $FILE_COUNT"
echo "📝 文章页面: $POST_COUNT"
echo ""

# 10. 提供下一步建议
echo "下一步操作:"
echo "1. 运行 'hexo server' 启动本地服务器预览"
echo "2. 在浏览器中打开 http://localhost:4000"
echo "3. 如果一切正常，提交更改并推送到 GitHub"
echo "4. GitHub Actions 将自动部署到 gh-pages 分支"
echo ""

# 询问是否启动本地服务器
read -p "是否启动本地服务器？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "启动本地服务器..."
    echo "按 Ctrl+C 停止服务器"
    echo ""
    npx hexo server || hexo server
fi
