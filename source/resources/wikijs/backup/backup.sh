#!/bin/bash
#
# Wiki.js 备份脚本
# 用法: ./backup/backup.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$(dirname "$SCRIPT_DIR")"

# 配置
BACKUP_DIR="${BACKUP_DIR:-$(pwd)/backup}"
DATE=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="wikijs-db"
DB_USER="wikijs"
DB_NAME="wikijs"
KEEP_DAYS=${BACKUP_KEEP_DAYS:-7}

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 创建备份目录
mkdir -p "$BACKUP_DIR"

echo "========================================="
echo "  Wiki.js 备份脚本"
echo "========================================="
echo -e "${GREEN}备份时间: $DATE${NC}"
echo ""

# 检查容器是否运行
if ! docker ps | grep -q "$DB_CONTAINER"; then
    echo -e "${YELLOW}警告: 数据库容器未运行，跳过数据库备份${NC}"
else
    # 备份数据库
    echo -e "${GREEN}[1/3] 备份数据库...${NC}"
    docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/db_backup_$DATE.sql"
    echo -e "${GREEN}✓ 数据库备份完成: db_backup_$DATE.sql${NC}"
fi

# 备份 Wiki 数据
echo -e "${GREEN}[2/3] 备份 Wiki 数据...${NC}"
docker run --rm -v wikijs_wiki-data:/data -v "$BACKUP_DIR:/backup" alpine sh -c "cd /data && tar czf /backup/wiki_data_$DATE.tar.gz ."
echo -e "${GREEN}✓ Wiki 数据备份完成: wiki_data_$DATE.tar.gz${NC}"

# 清理旧备份
echo -e "${GREEN}[3/3] 清理 $KEEP_DAYS 天前的备份...${NC}"
DELETED=$(find "$BACKUP_DIR" -name "db_backup_*.sql" -mtime +$KEEP_DAYS -delete -print | wc -l)
DELETED=$((DELETED + $(find "$BACKUP_DIR" -name "wiki_data_*.tar.gz" -mtime +$KEEP_DAYS -delete -print | wc -l)))
echo -e "${GREEN}✓ 清理了 $DELETED 个旧备份文件${NC}"

# 显示备份信息
echo ""
echo "========================================="
echo "  备份完成"
echo "========================================="
echo ""
echo -e "${GREEN}当前备份文件:${NC}"
ls -lh "$BACKUP_DIR"/*$DATE.* 2>/dev/null || echo "无备份文件"
echo ""
echo -e "${GREEN}磁盘使用情况:${NC}"
du -sh "$BACKUP_DIR"
echo ""

# 验证备份
if [ -f "$BACKUP_DIR/db_backup_$DATE.sql" ]; then
    DB_SIZE=$(stat -f%z "$BACKUP_DIR/db_backup_$DATE.sql" 2>/dev/null || stat -c%s "$BACKUP_DIR/db_backup_$DATE.sql" 2>/dev/null)
    if [ "$DB_SIZE" -gt 100 ]; then
        echo -e "${GREEN}✓ 数据库备份验证通过${NC}"
    else
        echo -e "${YELLOW}警告: 数据库备份文件过小，可能备份失败${NC}"
    fi
fi
