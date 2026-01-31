#!/bin/bash
# 清理大文件并防止它们被提交到 Git

set -e

echo "=== 清理大文件 ==="

# 创建外部存储目录用于存放大文件
EXTERNAL_DIR="../wikijs-backups"
mkdir -p "$EXTERNAL_DIR"

# 查找当前项目中的大文件 (>100MB)
echo "查找大于 100MB 的文件..."
find . -name "*.tar" -size +100M -type f
find . -name "*.tar.gz" -size +100M -type f

# 移动大文件到外部目录
echo "移动大文件到外部备份目录..."
for file in $(find . -name "*.tar" -size +100M -not -path "../wikijs-backups/*" -type f); do
    echo "移动 $file 到 $EXTERNAL_DIR"
    mv "$file" "$EXTERNAL_DIR/"
done

for file in $(find . -name "*.tar.gz" -size +100M -not -path "../wikijs-backups/*" -type f); do
    echo "移动 $file 到 $EXTERNAL_DIR"
    mv "$file" "$EXTERNAL_DIR/"
done

# 更新 .gitignore 文件以排除大文件
echo "更新 .gitignore 文件..."
IGNORE_FILE=".gitignore"

# 添加大文件类型到 .gitignore
if ! grep -q "# 大文件和导出文件" "$IGNORE_FILE"; then
    cat >> "$IGNORE_FILE" << 'EOF'

# 大文件和导出文件
*.tar
*.tar.gz
*.zip
*.rar
*.7z
*.iso
*.dmg
*.img

# Wiki.js 导出文件
tools/wikijs-syn/wikijs-deploy/export/*
tools/wikijs-syn/wikijs-deploy/wikijs-*.tar*
EOF
fi

echo "大文件已移至: $EXTERNAL_DIR"
echo ".gitignore 已更新以排除大文件"

# 从 Git 缓存中移除这些文件（保留本地副本）
echo "从 Git 缓存中移除大文件..."
git rm --cached tools/wikijs-syn/wikijs-deploy/wikijs-*.tar* 2>/dev/null || true

echo "清理完成！"
echo ""
echo "注意：大文件已被移至 $EXTERNAL_DIR 目录"
echo "这些文件不再受 Git 版本控制，但仍在本地可用"