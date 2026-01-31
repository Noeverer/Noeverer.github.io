#!/bin/bash
# 将 Wiki.js 本地数据同步到 VitePress 项目

set -e

WIKI_DATA="/home/ante/10-personal/wikijs-data-local"
VITEPRESS_DOCS="/home/ante/10-personal/wikijs-content/docs"

echo "=== 同步 Wiki.js 内容到 VitePress ==="

# 检查目录是否存在
if [ ! -d "$WIKI_DATA" ]; then
    echo "错误: Wiki.js 数据目录不存在: $WIKI_DATA"
    exit 1
fi

if [ ! -d "$VITEPRESS_DOCS" ]; then
    echo "错误: VitePress 文档目录不存在: $VITEPRESS_DOCS"
    exit 1
fi

# 备份 VitePress 文档
BACKUP_DIR="/home/ante/10-personal/wikijs-content/backup"
mkdir -p "$BACKUP_DIR"
echo "备份现有文档..."
cp -r "$VITEPRESS_DOCS" "$BACKUP_DIR/docs-backup-$(date +%Y%m%d-%H%M%S)"

# 清空 VitePress docs 目录（保留 README.md 和 index.md）
echo "清理 VitePress 文档目录..."
find "$VITEPRESS_DOCS" -mindepth 1 -name "README.md" -o -name "index.md" | while read file; do
    mv "$file" /tmp/
done
rm -rf "$VITEPRESS_DOCS"/*
# 恢复 README.md 和 index.md
if [ -f /tmp/README.md ]; then
    mv /tmp/README.md "$VITEPRESS_DOCS/"
fi
if [ -f /tmp/index.md ]; then
    mv /tmp/index.md "$VITEPRESS_DOCS/"
fi

# 复制 Wiki.js 内容
echo "复制 Wiki.js 内容..."
if [ -d "$WIKI_DATA/docs" ]; then
    cp -r "$WIKI_DATA/docs"/* "$VITEPRESS_DOCS/"
else
    echo "警告: Wiki.js docs 目录不存在，跳过"
fi

# 复制根目录的 Markdown 文件
find "$WIKI_DATA" -maxdepth 1 -name "*.md" -exec cp {} "$VITEPRESS_DOCS/" \;

# 复制图片资源（如果有）
if [ -d "$WIKI_DATA/images" ]; then
    mkdir -p "$VITEPRESS_DOCS/public"
    cp -r "$WIKI_DATA/images"/* "$VITEPRESS_DOCS/public/"
fi

# 创建 VitePress 首页（如果不存在）
if [ ! -f "$VITEPRESS_DOCS/index.md" ]; then
    cat > "$VITEPRESS_DOCS/index.md" << 'EOF'
---
layout: home

hero:
  name: "Ante's Wiki"
  text: "个人知识库"
  tagline: "记录、整理、分享"
  actions:
    - theme: brand
      text: 开始阅读
      link: /programming/
    - theme: alt
      text: GitHub
      link: https://github.com/Noeverer/wikijs-content
---
EOF
fi

echo "=== 同步完成 ==="
echo "文档已复制到: $VITEPRESS_DOCS"
echo ""
echo "下一步:"
echo "  1. cd /home/ante/10-personal/wikijs-content"
echo "  2. npm run dev  # 本地预览"
echo "  3. npm run build && git add . && git commit -m 'Update content' && git push  # 构建并推送"
