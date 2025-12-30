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
                title = filename.replace('-', ' ').replace('_', ' ')
                title = ' '.join(word.capitalize() for word in title.split())

            # 根据路径推断分类和标签
            path_parts = Path(filepath).parts
            if 'chocolate' in path_parts:
                category = 'chocolate'
                tags = ['chocolate', 'life']
            elif 'code' in path_parts:
                category = 'code'
                tags = ['code', 'tech']
            elif 'work' in path_parts:
                category = 'work'
                tags = ['work']
            elif 'life' in path_parts:
                category = 'life'
                tags = ['life']
            elif 'love' in path_parts:
                category = 'love'
                tags = ['love']
            else:
                category = 'uncategorized'
                if keywords:
                    tags = [tag.strip() for tag in keywords.split(',')]

            # 提取文章内容
            article_content = self.extract_content_from_html(soup, filepath)

            # 如果提取到了内容
            if title and (article_content or description):
                article_info = {
                    'title': title,
                    'date': date or '2019-01-01',
                    'tags': tags,
                    'category': category,
                    'description': description[:200] if description else '',
                    'content': article_content or description,
                    'source_file': filepath
                }
                self.articles.append(article_info)
                print(f"✓ 解析完成: {title}")
                return article_info

        except Exception as e:
            print(f"✗ 解析失败 {filepath}: {e}")
            return None

    def extract_date_from_url(self, url):
        """从URL提取日期"""
        date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', url)
        if date_match:
            year, month, day = date_match.groups()
            return f"{year}-{month}-{day}"

        # 尝试匹配年份，如 2015y, 2016autumn
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

        # 标准日期格式
        date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', path_str)
        if date_match:
            year, month, day = date_match.groups()
            return f"{year}-{month}-{day}"

        return None

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
            'div.content'
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
                desc = self.clean_description(desc)
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
            elif child.name in ['div', 'section', 'span']:
                # 递归处理容器元素
                child_lines = self.parse_element(child)
                lines.extend(child_lines)

        return lines

    def clean_description(self, desc):
        """清理和格式化description"""
        # 移除多余的空格和换行
        desc = ' '.join(desc.split())

        # 尝试识别日期格式，如 2016.08.19
        date_pattern = re.compile(r'(\d{4}\.\d{2}\.\d{2})')
        desc = date_pattern.sub(r'\n\n\1', desc)

        # 尝试识别句子
        sentences = re.split(r'(?<=[。！？.!?])\s+', desc)
        if len(sentences) > 1:
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

            print(f"✓ 保存: {filename}")


def main():
    base_dir = Path('/mnt/workspace/01-personal/01-note/Noeverer.github.io')

    print("开始解析HTML文件...")
    converter = MarkdownConverter()

    # 查找所有HTML文件
    html_files = []

    # 先查找标准格式的Hexo文章（包含日期路径）
    for filepath in base_dir.rglob('index.html'):
        path_str = str(filepath)
        # 跳过归档页面、首页等非文章页面
        if any(skip in path_str for skip in [
            'archives/', 'tags/', 'categories/', 'README.html',
            'TOC.html', 'fonts/', 'assets/', 'css/', 'js/'
        ]):
            continue

        # 只处理包含日期路径的文件（文章）
        if re.search(r'/(\d{4})/(\d{2})', path_str):
            html_files.append(filepath)

    # 查找chocolate目录下的HTML文件
    chocolate_dir = base_dir / 'chocolate'
    if chocolate_dir.exists():
        for filepath in chocolate_dir.glob('*.html'):
            # 跳过README和TOC
            if filepath.name not in ['README.html', 'TOC.html']:
                html_files.append(filepath)

    # 查找其他目录下的HTML文件
    for category in ['code', 'work', 'life', 'love', 'Fun_thing', 'Problem-Encounted-in-Blogging']:
        category_dir = base_dir / category
        if category_dir.exists():
            for filepath in category_dir.glob('*.html'):
                if filepath.name not in ['README.html', 'TOC.html', 'index.html']:
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
