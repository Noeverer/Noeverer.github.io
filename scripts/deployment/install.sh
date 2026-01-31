#!/bin/bash
# 一键安装和设置脚本

set -e

echo "=========================================="
echo "HTML to Hexo 转换系统 - 安装脚本"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    echo "请先安装Python3: https://www.python.org/downloads/"
    exit 1
fi
echo "✓ Python3: $(python3 --version)"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到Node.js"
    echo "请先安装Node.js: https://nodejs.org/"
    exit 1
fi
echo "✓ Node.js: $(node --version)"

# 检查Git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未找到Git"
    echo "请先安装Git: https://git-scm.com/downloads"
    exit 1
fi
echo "✓ Git: $(git --version)"

echo ""
echo "=========================================="
echo "安装Python依赖"
echo "=========================================="

pip3 install beautifulsoup4 GitPython

if [ $? -eq 0 ]; then
    echo "✓ Python依赖安装成功"
else
    echo "❌ Python依赖安装失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "安装Hexo依赖"
echo "=========================================="

npm install -g hexo-cli

if [ $? -eq 0 ]; then
    echo "✓ Hexo CLI安装成功"
else
    echo "❌ Hexo CLI安装失败"
    exit 1
fi

if [ -f package.json ]; then
    npm install
    if [ $? -eq 0 ]; then
        echo "✓ npm依赖安装成功"
    else
        echo "⚠ npm依赖安装失败（可能已安装）"
    fi
else
    echo "⚠ 未找到package.json，跳过npm依赖安装"
fi

echo ""
echo "=========================================="
echo "设置脚本权限"
echo "=========================================="

chmod +x html2hexo.py
chmod +x deploy_helper.py
chmod +x install.sh

echo "✓ 脚本权限设置完成"

echo ""
echo "=========================================="
echo "创建必要目录"
echo "=========================================="

mkdir -p source/_posts
mkdir -p .github/workflows
mkdir -p themes

echo "✓ 目录结构创建完成"

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "快速开始："
echo "  1. 运行转换: python3 html2hexo.py"
echo "  2. 启动服务器: python3 deploy_helper.py serve"
echo "  3. 完整设置: python3 deploy_helper.py setup"
echo "  4. 查看状态: python3 deploy_helper.py status"
echo ""
echo "文档："
echo "  - HTML2HEXO_README.md - 使用说明"
echo "  - BRANCH_WORKFLOW.md - 分支管理"
echo ""
