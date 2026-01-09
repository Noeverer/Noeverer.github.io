#!/usr/bin/env python3
"""
批量更新 Markdown 文章的 Front Matter，添加 published: true 字段
"""
import os
import re
from pathlib import Path

def add_published_field(file_path):
    """为 Markdown 文件添加 published: true 字段"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有 published 字段
        if re.search(r'^published:', content, re.MULTILINE):
            return False, "已有 published 字段"
        
        # 查找 Front Matter 结束标记
        front_matter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not front_matter_match:
            return False, "未找到 Front Matter"
        
        # 获取 Front Matter 内容（不包含 ---）
        front_matter_lines = front_matter_match.group(1).split('\n')
        
        # 构建新的 Front Matter
        new_front_matter = "---\n"
        for line in front_matter_lines:
            new_front_matter += line + "\n"
        
        # 添加 published: true
        new_front_matter += "published: true\n"
        new_front_matter += "---\n"
        
        # 替换原内容
        new_content = content[:front_matter_match.start()] + new_front_matter + content[front_matter_match.end():]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "成功添加 published 字段"
    
    except Exception as e:
        import traceback
        return False, f"错误: {str(e)}\n{traceback.format_exc()}"

def main():
    posts_dir = Path("source/_posts")
    
    if not posts_dir.exists():
        print(f"❌ 错误: 目录不存在 {posts_dir}")
        return
    
    # 递归查找所有 .md 文件
    md_files = list(posts_dir.rglob("*.md"))
    
    print(f"🔍 找到 {len(md_files)} 个 Markdown 文件")
    print("=" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for md_file in md_files:
        relative_path = md_file.relative_to(posts_dir.parent.parent)
        success, message = add_published_field(md_file)
        
        if success:
            print(f"✅ {relative_path}: {message}")
            success_count += 1
        elif "已有" in message:
            print(f"⏭️  {relative_path}: {message}")
            skip_count += 1
        else:
            print(f"❌ {relative_path}: {message}")
            error_count += 1
    
    print("=" * 60)
    print(f"📊 处理完成！")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ⏭️  跳过: {skip_count}")
    print(f"  ❌ 错误: {error_count}")
    print("")
    print("下一步：")
    print("  1. 检查修改的文件: git status")
    print("  2. 提交更改: git add . && git commit -m 'chore: 添加 published 字段到文章'")
    print("  3. 推送到 GitHub: git push origin master")
    print("  4. 监控 GitHub Actions: https://github.com/Noeverer/Noeverer.github.io/actions")

if __name__ == "__main__":
    main()
