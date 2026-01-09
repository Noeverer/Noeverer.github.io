#!/bin/bash

# 批量更新文章 Front Matter，添加 published: true 字段
# 用于控制文章是否发布到 GitHub Pages

POSTS_DIR="source/_posts"
COUNT=0

echo "🔍 扫描文章目录: $POSTS_DIR"
echo "================================"

# 查找所有 .md 文件
find "$POSTS_DIR" -name "*.md" -type f | while read -r file; do
    # 检查文件是否已有 published 字段
    if grep -q "^published:" "$file"; then
        echo "✅ 已有 published 字段: $file"
    else
        # 在 Front Matter 中添加 published: true
        # 在 --- 之后的第一行插入
        sed -i '/^---$/{
            N
            /^---\n$/a\
published: true
            }' "$file"
        echo "✅ 添加 published 字段: $file"
        ((COUNT++))
    fi
done

echo "================================"
echo "📊 处理完成！共处理了 $COUNT 个文件"
echo ""
echo "下一步："
echo "  1. 运行: git add ."
echo "  2. 运行: git commit -m 'chore: 添加 published 字段到文章'"
echo "  3. 运行: git push origin master"
echo "  4. 检查 GitHub Actions 是否触发"
