#!/usr/bin/env python3
# validate-published.py
# 检查并修复 markdown 文件的 published 字段

import os
import re
import argparse
from pathlib import Path


def add_published_field(file_path, dry_run=False):
    """为 markdown 文件添加 published: true 字段"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有 published 字段
    if re.search(r'^published:', content, re.MULTILINE):
        return False, "Already has published field"

    # 在第二个 --- 前插入 published: true
    pattern = r'^(---)$'
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    if len(matches) >= 2:
        insert_pos = matches[1].start()
        new_content = content[:insert_pos] + 'published: true\n' + content[insert_pos:]
        
        if dry_run:
            return True, "Would add published field (dry run)"
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Added published field"
    
    return False, "Could not find valid frontmatter"


def validate_posts(posts_dir, mode='check'):
    """验证并修复所有文章"""
    missing_files = []
    fixed_files = []

    # 递归查找所有 .md 文件
    for file_path in Path(posts_dir).rglob('*.md'):
        has_field, msg = add_published_field(file_path, dry_run=(mode == 'check'))
        
        if not has_field and "Could not find valid frontmatter" not in msg:
            missing_files.append(str(file_path))
            print(f"❌ Missing published: in {file_path}")
        elif has_field and mode == 'fix':
            fixed_files.append(str(file_path))
            print(f"✓ Fixed: {file_path}")
        else:
            print(f"✓ OK: {file_path.name}")

    return missing_files, fixed_files


def main():
    parser = argparse.ArgumentParser(description='Validate and fix published field in markdown files')
    parser.add_argument('mode', choices=['check', 'fix'], default='check', nargs='?',
                        help='Mode: check (default) or fix')
    parser.add_argument('--dir', default='blog/source/_posts',
                        help='Posts directory (default: blog/source/_posts)')
    
    args = parser.parse_args()
    
    print(f"Scanning markdown files in {args.dir}...")
    missing, fixed = validate_posts(args.dir, args.mode)
    
    if args.mode == 'check' and missing:
        print(f"\n❌ Found {len(missing)} files missing published field")
        print("Run with 'fix' mode to automatically fix them")
        exit(1)
    else:
        print(f"\n✅ All files validated")
        if fixed:
            print(f"✅ Fixed {len(fixed)} files")


if __name__ == '__main__':
    main()
