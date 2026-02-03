#!/bin/bash

# 部署脚本 - 将生成的静态文件部署到 GitHub Pages

set -e  # 遇到错误时退出

echo "开始部署过程..."

# 1. 生成静态文件
echo "正在生成静态文件..."
cd blog
hexo clean
hexo generate
cd ..

# 2. 检查生成的文件是否存在
if [ ! -d "public" ] || [ -z "$(ls -A public)" ]; then
  echo "错误: public 目录不存在或为空，请检查生成过程"
  exit 1
fi

# 3. 复制生成的文件到临时目录
echo "正在准备部署文件..."
TEMP_DEPLOY_DIR="/tmp/noeverer-deploy"
rm -rf "$TEMP_DEPLOY_DIR"
mkdir -p "$TEMP_DEPLOY_DIR"
cp -r public/* "$TEMP_DEPLOY_DIR/"

# 4. 切换到 gh-pages 分支
echo "切换到 gh-pages 分支..."
git checkout gh-pages || git checkout -b gh-pages

# 5. 清空当前内容并复制新内容
echo "更新 gh-pages 分支内容..."
git rm -rf . 2>/dev/null || echo "没有文件需要删除"
cp -r "$TEMP_DEPLOY_DIR"/* .

# 6. 提交更改
echo "提交更改..."
git add .
git commit -m "自动部署: $(date '+%Y-%m-%d %H:%M:%S')" || echo "没有更改需要提交"

# 7. 推送到远程仓库
echo "推送到远程仓库..."
git push origin gh-pages

# 8. 返回主分支
echo "返回主分支..."
git checkout master || git checkout main

echo "部署完成！"