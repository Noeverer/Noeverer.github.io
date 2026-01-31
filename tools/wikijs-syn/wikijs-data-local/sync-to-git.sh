#!/bin/bash
# 将 Wiki.js 本地数据同步到 Git 仓库

set -e

WIKI_DATA="/home/ante/10-personal/wikijs-data-local"

echo "=== 同步 Wiki.js 内容到 Git ==="

cd "$WIKI_DATA"

# 检查是否已初始化 Git
if [ ! -d .git ]; then
    echo "初始化 Git 仓库..."
    git init

    # 配置用户信息
    git config user.name "Wiki.js Auto Sync"
    git config user.email "wikijs@local"

    # 关联远程仓库（如果提供了参数）
    if [ -n "$1" ]; then
        git remote add origin "$1"
        echo "已关联远程仓库: $1"
    fi
fi

# 检查是否有更改
if git diff --quiet && git diff --cached --quiet; then
    echo "没有更改需要提交"
    exit 0
fi

# 添加所有文件
git add .

# 检查是否需要提交
if git diff --cached --quiet; then
    echo "没有新的更改需要提交"
    exit 0
fi

# 提交更改
echo "提交更改..."
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Auto-sync: $TIMESTAMP"

# 推送到远程（如果配置了远程仓库）
if git remote get-url origin > /dev/null 2>&1; then
    echo "推送到远程仓库..."
    git push
else
    echo "提示: 未配置远程仓库，使用以下命令添加:"
    echo "  git remote add origin https://github.com/Noeverer/wikijs-content.git"
fi

echo "=== 同步完成 ==="
git log --oneline -1
