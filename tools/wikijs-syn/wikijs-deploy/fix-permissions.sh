#!/bin/bash
# 修复 Wiki.js Git 存储权限问题

set -e

echo "=== 修复 Wiki.js Git 权限 ==="

# 检查容器是否运行
if ! docker ps | grep -q wikijs; then
    echo "错误: Wiki.js 容器未运行"
    echo "请先运行: docker-compose up -d"
    exit 1
fi

# 获取当前用户的 UID 和 GID
CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)

echo "当前用户 UID: $CURRENT_UID"
echo "当前用户 GID: $CURRENT_GID"

# 方法 1: 使用临时容器修复权限
echo "修复 wiki-data 卷的权限..."
docker run --rm -v wikijs-deploy_wiki-data:/data alpine chown -R $CURRENT_UID:$CURRENT_GID /data

# 方法 2: 如果方法 1 不生效，直接修改 .env
echo "更新 .env 文件中的 UID/GID..."
sed -i "s/^UID=.*/UID=$CURRENT_UID/" /home/ante/10-personal/wikijs-deploy/.env
sed -i "s/^GID=.*/GID=$CURRENT_GID/" /home/ante/10-personal/wikijs-deploy/.env

echo ""
echo "权限修复完成"
echo ""
echo "请执行以下命令重启容器:"
echo "  cd /home/ante/10-personal/wikijs-deploy"
echo "  docker-compose down"
echo "  docker-compose up -d"
echo ""
echo "然后在 Wiki.js 管理界面重新配置 Git 存储"
