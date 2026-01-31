#!/bin/bash

# validate-published.sh
# 检查并修复 markdown 文件的 published 字段

set -e

POSTS_DIR="blog/source/_posts"
MODE="${1:-check}"  # check 或 fix

echo "Scanning markdown files in $POSTS_DIR..."
files=$(find "$POSTS_DIR" -name "*.md")
total=$(echo "$files" | wc -l)
missing=0

echo "$files" | while read file; do
    if ! grep -q "^published:" "$file"; then
        echo "❌ Missing published: in $file"
        ((missing++))

        if [ "$MODE" = "fix" ]; then
            # 在 frontmatter 结束后添加
            awk '/^---$/{count++; if(count==2){print "published: true"; next}}1' "$file" > "${file}.tmp"
            mv "${file}.tmp" "$file"
            echo "✓ Fixed: $file"
        fi
    else
        echo "✓ OK: $(basename "$file")"
    fi
done

if [ "$MODE" = "check" ] && [ $missing -gt 0 ]; then
    echo "❌ Found $missing files missing published field"
    echo "Run '$0 fix' to automatically fix them"
    exit 1
fi

echo "✅ All $total files validated"
