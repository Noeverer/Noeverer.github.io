#!/bin/bash
#
# Wiki.js 恢复脚本
# 用法: ./backup/restore.sh <backup_date>
# 示例: ./backup/restore.sh 20260114_120000
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$(dirname "$SCRIPT_DIR")"

# 检查参数
if [ -z "$1" ]; then
    echo "错误: 请指定备份日期"
    echo "用法: ./backup/restore.sh <backup_date>"
    echo "示例: ./backup/restore.sh 20260114_120000"
    echo ""
    echo "可用的备份:"
    ls -1 backup/ | grep -E "db_backup_|wiki_data_" | sed 's/db_backup_//g' | sed 's/wiki_data_//g' | sed 's/.sql//g' | sed 's/.tar.gz//g' | sort -u
    exit 1
fi

BACKUP_DATE=$1
BACKUP_DIR="$(pwd)/backup"
DB_CONTAINER="wikijs-db"
DB_USER="wikijs"
DB_NAME="wikijs"

echo "========================================="
echo "  Wiki.js 恢复脚本"
echo "========================================="
echo "备份日期: $BACKUP_DATE"
echo ""

# 检查备份文件是否存在
if [ ! -f "$BACKUP_DIR/db_backup_$BACKUP_DATE.sql" ] || [ ! -f "$BACKUP_DIR/wiki_data_$BACKUP_DATE.tar.gz" ]; then
    echo "错误: 备份文件不存在"
    echo "请检查以下文件:"
    echo "  - $BACKUP_DIR/db_backup_$BACKUP_DATE.sql"
    echo "  - $BACKUP_DIR/wiki_data_$BACKUP_DATE.tar.gz"
    exit 1
fi

# 确认恢复操作
read -p "恢复操作将覆盖当前数据，是否继续？(yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "操作已取消"
    exit 0
fi

# 停止服务
echo "停止 Wiki.js 服务..."
docker-compose stop wiki

# 恢复数据库
echo "恢复数据库..."
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" "$DB_NAME" < "$BACKUP_DIR/db_backup_$BACKUP_DATE.sql"

# 恢复 Wiki 数据
echo "恢复 Wiki 数据..."
# 删除现有数据
docker run --rm -v wikijs_wiki-data:/data alpine sh -c "rm -rf /data/*"
# 恢复备份
docker run --rm -v wikijs_wiki-data:/data -v "$BACKUP_DIR:/backup" alpine tar xzf "/backup/wiki_data_$BACKUP_DATE.tar.gz" -C /data

# 启动服务
echo "启动 Wiki.js 服务..."
docker-compose start wiki

echo ""
echo "========================================="
echo "  恢复完成"
echo "========================================="
echo ""
echo "服务正在启动，请稍后访问 http://localhost:3000"
