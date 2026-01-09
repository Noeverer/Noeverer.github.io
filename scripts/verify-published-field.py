#!/usr/bin/env python3
"""
验证所有文章的 published 字段设置
"""
import re
from pathlib import Path

def check_published_field(file_path):
    """检查 Markdown 文件的 published 字段"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找 published 字段
        published_match = re.search(r'^published:\s*(true|false)', content, re.MULTILINE)
        
        if published_match:
            published_value = published_match.group(1)
            return True, published_value
        else:
            return False, None
    
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    posts_dir = Path("source/_posts")
    
    if not posts_dir.exists():
        print(f"❌ 错误: 目录不存在 {posts_dir}")
        return
    
    # 递归查找所有 .md 文件
    md_files = sorted(list(posts_dir.rglob("*.md")))
    
    print(f"🔍 检查 {len(md_files)} 个 Markdown 文件的 published 字段")
    print("=" * 80)
    
    published_true = 0
    published_false = 0
    no_field = 0
    error_files = []
    
    for md_file in md_files:
        relative_path = md_file.relative_to(posts_dir.parent.parent)
        has_field, value = check_published_field(md_file)
        
        if has_field:
            if value == 'true':
                print(f"✅ {relative_path}: published: {value}")
                published_true += 1
            else:
                print(f"⏸️  {relative_path}: published: {value} (不发布)")
                published_false += 1
        elif isinstance(value, str) and value.startswith("错误"):
            print(f"❌ {relative_path}: {value}")
            error_files.append(relative_path)
            no_field += 1
        else:
            print(f"⚠️  {relative_path}: 缺少 published 字段 (默认发布)")
            no_field += 1
    
    print("=" * 80)
    print(f"📊 统计结果：")
    print(f"  ✅ published: true (发布): {published_true}")
    print(f"  ⏸️  published: false (不发布): {published_false}")
    print(f"  ⚠️  缺少字段 (默认发布): {no_field}")
    print(f"  ❌ 错误文件: {len(error_files)}")
    
    if error_files:
        print(f"\n❌ 错误文件列表：")
        for f in error_files:
            print(f"  - {f}")
    
    print("\n💡 提示：")
    print(f"  - 所有设置 published: true 的文章将会发布到 GitHub Pages")
    print(f"  - 所有设置 published: false 的文章将不会发布")
    print(f"  - 缺少 published 字段的文章默认会发布（取决于 Hexo 配置）")

if __name__ == "__main__":
    main()
