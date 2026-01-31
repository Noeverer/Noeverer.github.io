#!/bin/bash

# Hexo部署脚本
# 用于自动化生成、检查和部署hexo博客到GitHub Pages

echo "开始部署Hexo博客..."

# 检查Node.js是否安装
if ! command -v node &> /dev/null
then
    echo "错误: 未检测到Node.js，请先安装Node.js"
    exit 1
fi

# 检查npm是否安装
if ! command -v npm &> /dev/null
then
    echo "错误: 未检测到npm，请先安装npm"
    exit 1
fi

# 检查hexo是否安装（全局或本地）
HEXO_CMD=""
if command -v hexo &> /dev/null
then
    HEXO_CMD="hexo"
elif [ -f "node_modules/.bin/hexo" ]
then
    HEXO_CMD="./node_modules/.bin/hexo"
else
    echo "尝试全局安装hexo-cli..."
    npm install -g hexo-cli
    if command -v hexo &> /dev/null
    then
        HEXO_CMD="hexo"
        echo "hexo-cli安装成功"
    else
        echo "错误: 安装hexo-cli失败，请手动安装"
        exit 1
    fi
fi

# 清理旧的生成文件
echo "清理旧文件..."
$HEXO_CMD clean

# 生成静态文件
echo "生成静态文件..."
$HEXO_CMD generate

# 检查生成是否成功
if [ $? -ne 0 ]; then
    echo "错误: 生成失败"
    exit 1
fi

# 处理克隆仓库中的HTML文件
echo "处理克隆仓库中的HTML文件..."
# 修改为相对于当前部署脚本位置的路径
CLONE_REPO_DIR="$(dirname "$0")/../clone-repo"
if [ -d "$CLONE_REPO_DIR" ]; then
    echo "发现克隆仓库，复制HTML文件..."
    # 创建目标目录（如果不存在）
    mkdir -p public/clone-content
    
    # 复制所有HTML文件到public目录下
    cp -r "$CLONE_REPO_DIR"/*.html public/clone-content/ 2>/dev/null || true
    # 使用find命令更可靠地复制所有子目录中的HTML文件
    find "$CLONE_REPO_DIR" -name "*.html" -exec cp --parents {} public/clone-content/ \; 2>/dev/null || true
    
    # 如果有CSS/JS等静态资源也需要复制
    if [ -d "$CLONE_REPO_DIR/css" ]; then
        cp -r "$CLONE_REPO_DIR/css" public/clone-content/ 2>/dev/null
    fi
    
    if [ -d "$CLONE_REPO_DIR/js" ]; then
        cp -r "$CLONE_REPO_DIR/js" public/clone-content/ 2>/dev/null
    fi
    
    if [ -d "$CLONE_REPO_DIR/images" ]; then
        cp -r "$CLONE_REPO_DIR/images" public/clone-content/ 2>/dev/null
    fi
    
    echo "HTML文件处理完成"
else
    echo "未找到克隆仓库目录，跳过HTML文件处理"
fi

# 启动服务器进行本地检查(可选，3秒后自动关闭)
echo "启动本地服务器进行检查(3秒)..."
$HEXO_CMD server &
SERVER_PID=$!
sleep 3
kill $SERVER_PID

# 部署到GitHub Pages
echo "部署到GitHub Pages..."
$HEXO_CMD deploy

# 检查部署是否成功
if [ $? -eq 0 ]; then
    echo "部署成功完成!"
else
    echo "部署过程中出现错误"
    exit 1
fi