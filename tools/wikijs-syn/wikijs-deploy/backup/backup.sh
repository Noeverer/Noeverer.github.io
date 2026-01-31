#!/bin/bash
# Wiki.js 备份脚本

set -e

BACKUP_DIR="$(dirname "$0")/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="wikijs-db"
DB_USER="wikijs"
DB_NAME="wikijs"

mkdir -p "$BACKUP_DIR"

echo "=== 开始备份 ($DATE) ==="

# 备份数据库
echo "备份数据库..."
if docker ps | grep -q "$DB_CONTAINER"; then
    docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/db_backup_$DATE.sql"
    echo "✓ 数据库备份完成"
else
    echo "✗ 数据库容器未运行"
    exit 1
fi

# 备份 Wiki 数据
echo "备份 Wiki 数据..."
if docker volume ls | grep -q wikijs_wiki-data; then
    docker run --rm -v wikijs_wiki-data:/data -v "$BACKUP_DIR:/backup" alpine tar czf "/backup/wiki_data_$DATE.tar.gz" -C /data . 2>/dev/null
    echo "✓ Wiki 数据备份完成"
else
    echo "✗ Wiki 数据卷不存在"
fi

# 删除 7 天前的备份
echo "清理旧备份..."
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "=== 备份完成 ==="
ls -lh "$BACKUP_DIR"/*$DATE.* 2>/dev/null || echo "备份文件列表为空"
