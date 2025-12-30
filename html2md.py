#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

class MarkdownConverter:
    def __init__(self):
        self.articles = []

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

            # 从URL提取日期
            url_meta = soup.find('meta', property='og:url')
            if url_meta:
                url = url_meta.get('content', '')
                # 提取日期部分，如 /2019/05/04/hello-world/index.html
                date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', url)
                if date_match:
                    year, month, day = date_match.groups()
                    date = f"{year}-{month}-{day}"

            # 提取标签
            if keywords:
                tags = [tag.strip() for tag in keywords.split(',')]

            # 提取文章内容
            # 查找主要内容区域
            article_section = soup.find('div', class_='article-inner') or \
                            soup.find('article') or \
                            soup.find('div', class_='post-content')

            if article_section:
                article_content = self.extract_content(article_section)

            # 如果是文章页（非首页、归档页等）
            if title and article_content:
                article_info = {
                    'title': title,
                    'date': date or datetime.now().strftime('%Y-%m-%d'),
                    'tags': tags,
                    'category': tags[0] if tags else 'uncategorized',
                    'description': description,
                    'content': article_content,
                    'source_file': filepath
                }
                self.articles.append(article_info)
                print(f"✓ 解析完成: {title}")
                return article_info

        except Exception as e:
            print(f"✗ 解析失败 {filepath}: {e}")
            return None

    def extract_content(self, element):
        """从HTML元素提取Markdown内容"""
        lines = []

        for child in element.descendants:
            if child.name is None:  # 文本节点
                text = str(child).strip()
                if text:
                    lines.append(text)
            elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(child.name[1])
                text = child.get_text().strip()
                if text:
                    lines.append('\n' + '#' * level + ' ' + text + '\n')
            elif child.name == 'p':
                text = child.get_text().strip()
                if text:
                    lines.append('\n' + text + '\n')
            elif child.name == 'strong' or child.name == 'b':
                text = child.get_text().strip()
                if text:
                    lines.append(f'**{text}**')
            elif child.name == 'em' or child.name == 'i':
                text = child.get_text().strip()
                if text:
                    lines.append(f'*{text}*')
            elif child.name == 'code':
                text = child.get_text()
                lines.append(f'`{text}`')
            elif child.name == 'pre':
                code_block = child.get_text()
                lines.append('\n```' + code_block + '```\n')
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
            elif child.name == 'a':
                text = child.get_text().strip()
                href = child.get('href', '')
                if text and href:
                    lines.append(f'[{text}]({href})')
            elif child.name == 'img':
                src = child.get('src', '')
                alt = child.get('alt', '')
                if src:
                    lines.append(f'![{alt}]({src})')
            elif child.name == 'blockquote':
                text = child.get_text().strip()
                if text:
                    lines.append(f'> {text}')

        # 清理空白行
        result = '\n'.join(lines)
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result.strip()

    def extract_date_from_path(self, filepath):
        """从文件路径提取日期"""
        path_str = str(filepath)
        date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', path_str)
        if date_match:
            year, month, day = date_match.groups()
            return f"{year}-{month}-{day}"
        return None

    def save_markdown_files(self, output_dir='source/_posts'):
        """保存为Markdown文件"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for article in self.articles:
            # 生成文件名
            date = article['date'][:10]  # YYYY-MM-DD
            title = re.sub(r'[^\w\s-]', '', article['title'])
            title = re.sub(r'[-\s]+', '-', title)
            filename = f"{date}-{title}.md"

            filepath = output_path / filename

            # 生成front matter
            front_matter = f"""---
title: {article['title']}
date: {article['date']} {datetime.now().strftime('%H:%M:%S')}
tags: {json.dumps(article['tags'], ensure_ascii=False)}
categories: {article['category']}
description: {article['description']}
---
"""

            full_content = front_matter + article['content']

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            print(f"✓ 保存: {filename}")


def main():
    base_dir = Path('/mnt/workspace/01-personal/01-note/Noeverer.github.io')

    print("开始解析HTML文件...")
    converter = MarkdownConverter()

    # 查找所有HTML文件
    html_files = []
    for pattern in ['**/index.html', '**/*.html']:
        for filepath in base_dir.rglob(pattern):
            # 跳过归档页面、首页等非文章页面
            path_str = str(filepath)
            if any(skip in path_str for skip in [
                'archives/', 'tags/', 'categories/', 'README.html',
                'TOC.html', 'fonts/', 'assets/', 'css/', 'js/'
            ]):
                continue

            # 只处理包含日期路径的文件（文章）
            date_match = re.search(r'/(\d{4})/(\d{2})', path_str)
            if date_match and 'index.html' in path_str:
                html_files.append(filepath)

    print(f"找到 {len(html_files)} 个HTML文件")

    # 解析所有HTML文件
    for html_file in html_files:
        converter.parse_html_file(html_file)

    print(f"\n共解析出 {len(converter.articles)} 篇文章")

    # 保存为Markdown
    print("\n保存Markdown文件...")
    output_dir = base_dir / 'source' / '_posts'
    converter.save_markdown_files(str(output_dir))

    print(f"\n完成！Markdown文件已保存到: {output_dir}")


if __name__ == '__main__':
    main()
