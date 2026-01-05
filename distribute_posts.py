#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import shutil
from pathlib import Path
from datetime import datetime

def load_config():
    """加载配置文件"""
    with open('publish_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def should_exclude(filename, title, config):
    """检查是否应该排除该文件"""
    exclude_patterns = config.get('exclude_patterns', [])
    
    for pattern in exclude_patterns:
        # 将通配符模式转换为正则表达式
        pattern = pattern.replace('*', '.*')
        if re.search(pattern, filename, re.IGNORECASE) or re.search(pattern, title, re.IGNORECASE):
            return True
    return False

def categorize_post(filepath, config):
    """根据配置文件对文章进行分类"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取front matter
    lines = content.split('\n')
    front_matter = {}
    in_front_matter = False
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_front_matter:
                in_front_matter = True
            else:
                break
        elif in_front_matter and ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip().strip('"\'')
                front_matter[key] = value
    
    # 获取文章信息
    title = front_matter.get('title', '')
    category = front_matter.get('categories', '')
    tags = front_matter.get('tags', '')
    
    # 检查是否应该排除
    if should_exclude(filepath.name, title, config):
        return 'excluded'
    
    # 根据配置判断应分配到哪个分支
    branches_config = config['branches']
    for branch_name, branch_config in branches_config.items():
        # 检查分类
        if category in branch_config['categories']:
            return branch_name
        
        # 检查标签
        # 将tags字符串转换为列表进行匹配
        if isinstance(tags, str) and tags.startswith('[') and tags.endswith(']'):
            try:
                tag_list = json.loads(tags)
                for tag in tag_list:
                    if tag in branch_config['tags']:
                        return branch_name
            except:
                # 如果解析失败，尝试简单的字符串匹配
                for tag in branch_config['tags']:
                    if tag in tags:
                        return branch_name
        elif tags in branch_config['tags']:
            return branch_name
    
    # 如果没有匹配到任何分支，返回默认分支
    return 'personal'  # 默认放到个人生活分支

def create_branch_directories(base_dir):
    """创建分支目录结构"""
    config = load_config()
    branches = config['branches']
    
    for branch_name in branches.keys():
        branch_dir = base_dir / branch_name
        branch_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建Hexo标准目录结构
        (branch_dir / 'source' / '_posts').mkdir(parents=True, exist_ok=True)
        (branch_dir / 'themes').mkdir(parents=True, exist_ok=True)
        (branch_dir / 'scaffolds').mkdir(parents=True, exist_ok=True)
        (branch_dir / 'source' / 'images').mkdir(parents=True, exist_ok=True)
        (branch_dir / 'source' / 'css').mkdir(parents=True, exist_ok=True)

def distribute_posts():
    """分发文章到不同分支目录"""
    config = load_config()
    
    # 源目录
    source_dir = Path('source/_posts')
    if not source_dir.exists():
        print("源目录 source/_posts 不存在")
        return
    
    # 创建分支目录
    base_dir = Path('distributed')
    create_branch_directories(base_dir)
    
    # 获取所有markdown文件
    markdown_files = list(source_dir.glob('*.md'))
    print(f"找到 {len(markdown_files)} 个Markdown文件")
    
    # 分类统计
    distribution = {}
    
    for file_path in markdown_files:
        branch = categorize_post(file_path, config)
        
        if branch == 'excluded':
            print(f"跳过排除文件: {file_path.name}")
            continue
        
        # 记录分布
        if branch not in distribution:
            distribution[branch] = []
        distribution[branch].append(file_path.name)
        
        # 复制文件到对应分支
        branch_posts_dir = base_dir / branch / 'source' / '_posts'
        dest_path = branch_posts_dir / file_path.name
        shutil.copy2(file_path, dest_path)
        print(f"✓ {file_path.name} -> {branch} 分支")
    
    # 为每个分支创建配置文件
    for branch_name in config['branches'].keys():
        branch_dir = base_dir / branch_name
        create_hexo_config(branch_dir, branch_name, config)
    
    print("\n分发完成！分布情况：")
    for branch, files in distribution.items():
        print(f"  {branch}: {len(files)} 篇")
        for file in files:
            print(f"    - {file}")
    
    return distribution

def create_hexo_config(branch_dir, branch_name, config):
    """为分支创建Hexo配置文件"""
    theme = config['theme']['branches'].get(branch_name, config['theme']['default'])
    
    # 创建 _config.yml
    config_content = f"""# {config['branches'][branch_name]['name']} 配置文件
# {config['branches'][branch_name]['description']}

# Site
title: {config['branches'][branch_name]['name']}
subtitle: {config['branches'][branch_name]['description']}
description: 个人博客 - {config['branches'][branch_name]['name']}
author: Ante Liu
language: zh-CN
timezone: Asia/Shanghai

# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: https://your-site-url.com
root: /
permalink: :year/:month/:day/:title/
permalink_defaults:

# Directory
source_dir: source
public_dir: public
tag_dir: tags
archive_dir: archives
category_dir: categories
code_dir: downloads/code
i18n_dir: :lang
skip_render:

# Writing
new_post_name: :title.md # File name of new posts
default_layout: post
titlecase: false # Transform title into titlecase
external_link: true # Open external links in new tab
filename_case: 0
render_drafts: false
post_asset_folder: false
relative_link: false
future: true
highlight:
  enable: true
  line_number: true
  auto_detect: false
  tab_replace:

# Category & Tag
default_category: uncategorized
category_map:
tag_map:

# Date / Time format
## Hexo uses Moment.js to parse and display date
## You can customize the date format as defined in
## http://momentjs.com/docs/#/displaying/format/
date_format: YYYY-MM-DD
time_format: HH:mm:ss

# Pagination
## Set per_page to 0 to disable pagination
per_page: 10
pagination_dir: page

# Extensions
## Plugins: https://hexo.io/plugins/
## Themes: https://hexo.io/themes/
theme: {theme}

# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
  type: git
  repo: <repository url>
  branch: {branch_name}
"""
    
    config_path = branch_dir / '_config.yml'
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    # 创建 package.json
    package_content = f"""{{
  "name": "{branch_name}-blog",
  "version": "1.0.0",
  "private": true,
  "hexo": {{
    "version": "3.8.0"
  }},
  "dependencies": {{
    "hexo": "^3.8.0",
    "hexo-generator-archive": "^0.1.5",
    "hexo-generator-category": "^0.1.3",
    "hexo-generator-index": "^0.2.1",
    "hexo-generator-tag": "^0.2.0",
    "hexo-renderer-ejs": "^0.3.1",
    "hexo-renderer-marked": "^0.3.2",
    "hexo-renderer-stylus": "^0.3.3",
    "hexo-server": "^0.3.3"
  }}
}}
"""
    
    package_path = branch_dir / 'package.json'
    with open(package_path, 'w', encoding='utf-8') as f:
        f.write(package_content)

def main():
    print("=" * 60)
    print("开始分发博客文章到不同分支...")
    print("=" * 60)
    
    distribution = distribute_posts()
    
    print("\n" + "=" * 60)
    print("分发完成！")
    print("生成的分支结构位于: /workspace/distributed/")
    print("每个分支都有独立的Hexo配置和主题设置")
    print("=" * 60)

if __name__ == '__main__':
    main()