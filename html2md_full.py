#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

class MarkdownConverter:
    def __init__(self):
        self.articles = []
        self.converted_files = set()

    def parse_html_file(self, filepath):
        """解析单个HTML文件，提取文章信息"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            # 提取基本信息
            title = ""
            description = ""
            keywords = ""
            date = ""
            article_content = ""
            tags = []
            category = ""

            # 从meta标签提取信息
            title_meta = soup.find('meta', property='og:title')
            if title_meta:
                title = title_meta.get('content', '').replace(' | Ante Liu', '')

            desc_meta = soup.find('meta', property='og:description')
            if desc_meta:
                description = desc_meta.get('content', '')

            keyword_meta = soup.find('meta', attrs={'name': 'keywords'})
            if keyword_meta:
                keywords = keyword_meta.get('content', '')

            # 从URL提取日期或从文件名推断
            url_meta = soup.find('meta', property='og:url')
            if url_meta:
                url = url_meta.get('content', '')
                date = self.extract_date_from_url(url)

            # 如果从URL没提取到日期，从文件名提取
            if not date:
                date = self.extract_date_from_path(filepath)

            # 从文件名提取标题（如果没有标题）
            if not title or title == 'Ante Liu':
                filename = Path(filepath).stem
                # 移除一些常见的后缀和前缀
                filename = re.sub(r'^\d+[\.\-_]', '', filename)
                title = filename.replace('-', ' ').replace('_', ' ')
                title = ' '.join(word.capitalize() for word in title.split())

            # 根据路径推断分类和标签
            category, tags = self.infer_category_and_tags(filepath)

            # 提取文章内容
            article_content = self.extract_content_from_html(soup, filepath)

            # 跳过空文件和导航页面
            skip_keywords = ['toc.html', 'readme.html', 'index.html', 'hello-world.html']
            if any(k in str(filepath).lower() for k in skip_keywords):
                return None

            # 跳过life目录下的重复文件
            if '/life/' in str(filepath):
                return None

            # 检查是否已转换过（使用文件路径作为唯一标识）
            file_hash = f"{Path(filepath).stem}-{category}"
            if file_hash in self.converted_files:
                return None
            self.converted_files.add(file_hash)

            # 如果提取到了内容
            if title:
                article_info = {
                    'title': title,
                    'date': date or '2019-08-01',
                    'tags': tags,
                    'category': category,
                    'description': description[:200] if description else '',
                    'content': article_content or description,
                    'source_file': filepath
                }
                self.articles.append(article_info)
                return article_info

        except Exception as e:
            return None

    def infer_category_and_tags(self, filepath):
        """根据文件路径推断分类和标签"""
        path_str = str(filepath).lower()

        # chocolate - 生活感悟类
        if 'chocolate' in path_str:
            return 'chocolate', ['chocolate', 'life', '感悟']

        # code - 技术文章
        elif 'code' in path_str:
            if 'leetcode' in path_str:
                return 'leetcode', ['leetcode', 'algorithm', 'code']
            elif 'python' in path_str:
                return 'python', ['python', 'code']
            elif 'mindmap' in path_str:
                return 'mindmap', ['mindmap', 'study']
            else:
                return 'code', ['code', 'tech']

        # work - 工作
        elif 'work' in path_str:
            return 'work', ['work']

        # life - 生活
        elif 'life' in path_str:
            return 'life', ['life']

        # love - 情感
        elif 'love' in path_str:
            return 'love', ['love']

        # fun_thing - 趣事
        elif 'fun_thing' in path_str:
            return 'fun', ['fun', 'life']

        # problem - 问题记录
        elif 'problem' in path_str:
            return 'problem', ['problem', 'tech']

        # 默认
        else:
            return 'uncategorized', ['blog']

    def extract_date_from_url(self, url):
        """从URL提取日期"""
        date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', url)
        if date_match:
            year, month, day = date_match.groups()
            return f"{year}-{month}-{day}"

        # 尝试匹配年份，如 2015y
        year_match = re.search(r'/(\d{4})y?\.html', url)
        if year_match:
            year = year_match.group(1)
            return f"{year}-01-01"

        return None

    def extract_date_from_path(self, filepath):
        """从文件路径提取日期"""
        path_str = str(filepath)
        filename = Path(filepath).stem

        # 匹配 2015y 格式
        year_match = re.match(r'^(\d{4})y$', filename)
        if year_match:
            year = year_match.group(1)
            return f"{year}-01-01"

        # 匹配 2016autumn, 2016spring 等格式
        season_match = re.match(r'^(\d{4})(spring|autumn)$', filename, re.IGNORECASE)
        if season_match:
            year, season = season_match.groups()
            month = "03" if season.lower() == 'spring' else "09"
            return f"{year}-{month}-01"

        # 匹配 LeetCode 题号
        leetcode_match = re.match(r'^(\d+)_', filename)
        if leetcode_match:
            return '2019-08-01'

        # 标准日期格式
        date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', path_str)
        if date_match:
            year, month, day = date_match.groups()
            return f"{year}-{month}-{day}"

        # 默认返回2019年8月
        return '2019-08-01'

    def extract_content_from_html(self, soup, filepath):
        """从HTML元素提取Markdown内容"""
        lines = []

        # 尝试多个可能的内容容器
        content_selectors = [
            'div.article-inner',
            'article',
            'div.post-content',
            'div.article-entry',
            'div.entry-content',
            'main',
            'div.content',
            'div.article'
        ]

        content_element = None
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content_element = element
                break

        # 如果没找到内容容器，尝试从body中提取
        if not content_element:
            body = soup.find('body')
            if body:
                # 移除侧边栏等非内容区域
                for unwanted in body.select('.left-col, .overlay, .mid-col, .right-col, header, footer, nav, .header-menu, .article-meta'):
                    unwanted.decompose()
                content_element = body

        if content_element:
            lines = self.parse_element(content_element)
        else:
            # 最后尝试：从description提取内容
            desc_meta = soup.find('meta', property='og:description')
            if desc_meta:
                desc = desc_meta.get('content', '')
                # 清理和格式化description
                desc = self.clean_description(desc, filepath)
                lines = [desc]

        # 清理空白行
        result = '\n'.join(lines)
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result.strip()

    def parse_element(self, element):
        """递归解析HTML元素"""
        lines = []

        for child in element.children:
            if child.name is None:
                # 文本节点
                text = str(child).strip()
                if text:
                    lines.append(text)
            elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(child.name[1])
                text = child.get_text().strip()
                if text and text != 'Ante Liu':
                    lines.append(f'\n{"#" * level} {text}\n')
            elif child.name == 'p':
                text = child.get_text().strip()
                if text and len(text) > 5:
                    lines.append(f'\n{text}\n')
            elif child.name in ['strong', 'b']:
                text = child.get_text().strip()
                if text:
                    lines.append(f'**{text}**')
            elif child.name in ['em', 'i']:
                text = child.get_text().strip()
                if text:
                    lines.append(f'*{text}*')
            elif child.name == 'code':
                text = child.get_text()
                lines.append(f'`{text}`')
            elif child.name == 'pre':
                code_block = child.get_text()
                lines.append(f'\n```\n{code_block}\n```\n')
            elif child.name == 'ul':
                for li in child.find_all('li', recursive=False):
                    text = li.get_text().strip()
                    if text:
                        lines.append(f'- {text}')
            elif child.name == 'ol':
                for i, li in enumerate(child.find_all('li', recursive=False), 1):
                    text = li.get_text().strip()
                    if text:
                        lines.append(f'{i}. {text}')
            elif child.name == 'blockquote':
                text = child.get_text().strip()
                if text:
                    lines.append(f'\n> {text}\n')
            elif child.name == 'br':
                lines.append('\n')
            elif child.name in ['div', 'section', 'span', 'td', 'tr']:
                # 递归处理容器元素
                child_lines = self.parse_element(child)
                lines.extend(child_lines)

        return lines

    def clean_description(self, desc, filepath):
        """清理和格式化description"""
        # 移除多余的空格和换行
        desc = ' '.join(desc.split())

        path_str = str(filepath).lower()

        # 对于技术类文章，尝试保持原有格式
        if 'code' in path_str or 'leetcode' in path_str:
            # 尝试识别LeetCode题目
            leetcode_pattern = re.compile(r'(\d+\.\s*[A-Z][^.]+)')
            desc = leetcode_pattern.sub(r'\n\n## \1\n', desc)

            return desc

        # 对于chocolate等生活记录，保持原有换行
        if 'chocolate' in path_str:
            # 尝试识别日期格式，如 2016.08.19
            date_pattern = re.compile(r'(\d{4}\.\d{2}\.\d{2})')
            desc = date_pattern.sub(r'\n\n### \1\n', desc)

            # 尝试识别句子
            sentences = re.split(r'(?<=[。！？.!?])\s+', desc)
            if len(sentences) > 3:
                return '\n\n'.join(sentences)

        return desc

    def save_markdown_files(self, output_dir='source/_posts'):
        """保存为Markdown文件"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for article in self.articles:
            # 生成文件名
            date = article['date'][:10]  # YYYY-MM-DD
            title = re.sub(r'[^\w\s-]', '', article['title'])
            title = re.sub(r'[-\s]+', '-', title)
            title = title.strip('-')

            filename = f"{date}-{title}.md"
            filepath = output_path / filename

            # 如果文件已存在，添加序号
            counter = 1
            while filepath.exists():
                filename = f"{date}-{title}-{counter}.md"
                filepath = output_path / filename
                counter += 1

            # 生成front matter
            tags_list = json.dumps(article['tags'], ensure_ascii=False)

            front_matter = f"""---
title: {article['title']}
date: {article['date']} 12:00:00
tags: {tags_list}
categories: {article['category']}
description: {article['description']}
---
"""

            full_content = front_matter + article['content']

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

        return len(self.articles)


def main():
    base_dir = Path('/mnt/workspace/01-personal/01-note/Noeverer.github.io')

    print("=" * 60)
    print("开始解析HTML文件...")
    print("=" * 60)

    converter = MarkdownConverter()

    # 查找所有HTML文件
    html_files = []

    # 1. chocolate目录下的HTML文件
    print("\n[1/6] 查找chocolate目录...")
    chocolate_dir = base_dir / 'chocolate'
    if chocolate_dir.exists():
        for filepath in chocolate_dir.glob('*.html'):
            # 跳过README和TOC
            if filepath.name not in ['README.html', 'TOC.html', '使用gitpress总结.html']:
                html_files.append(filepath)

    # 2. code目录下的HTML文件（跳过life下的重复）
    print("[2/6] 查找code目录...")
    code_dir = base_dir / 'code'
    if code_dir.exists():
        for filepath in code_dir.rglob('*.html'):
            if 'node_modules' not in str(filepath):
                html_files.append(filepath)

    # 3. Fun_thing目录
    print("[3/6] 查找Fun_thing目录...")
    fun_dir = base_dir / 'Fun_thing'
    if fun_dir.exists():
        for filepath in fun_dir.glob('*.html'):
            if filepath.name not in ['README.html', 'TOC.html']:
                html_files.append(filepath)

    # 4. work目录
    print("[4/6] 查找work目录...")
    work_dir = base_dir / 'work'
    if work_dir.exists():
        for filepath in work_dir.rglob('*.html'):
            if filepath.name not in ['README.html', 'TOC.html', 'index.html']:
                html_files.append(filepath)

    # 5. life和love目录
    print("[5/6] 查找life/love目录...")
    for category in ['life', 'love', 'Problem-Encounted-in-Blogging']:
        category_dir = base_dir / category
        if category_dir.exists() and 'life/chocolate' not in str(category_dir):
            for filepath in category_dir.rglob('*.html'):
                if filepath.name not in ['README.html', 'TOC.html', 'index.html']:
                    html_files.append(filepath)

    # 6. 根目录的独立HTML文件
    print("[6/6] 查找根目录独立文件...")
    for filepath in base_dir.glob('*.html'):
        if filepath.name not in ['index.html', 'README.html', 'TOC.html', 'hello-world.html']:
            html_files.append(filepath)

    # 去重
    html_files = list(set(html_files))
    print(f"\n找到 {len(html_files)} 个HTML文件")

    # 解析所有HTML文件
    print("\n开始解析...")
    for html_file in html_files:
        converter.parse_html_file(html_file)

    print("\n" + "=" * 60)
    print(f"共解析出 {len(converter.articles)} 篇新文章")
    print("=" * 60)

    # 统计分类
    category_count = {}
    for article in converter.articles:
        cat = article['category']
        category_count[cat] = category_count.get(cat, 0) + 1

    print("\n分类统计:")
    for cat, count in sorted(category_count.items()):
        print(f"  - {cat}: {count} 篇")

    # 保存为Markdown
    print("\n保存Markdown文件...")
    output_dir = base_dir / 'source' / '_posts'
    count = converter.save_markdown_files(str(output_dir))

    print(f"\n完成！Markdown文件已保存到: {output_dir}")


if __name__ == '__main__':
    main()
