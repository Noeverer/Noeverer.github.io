#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Git历史恢复HTML文件并深度转换为Markdown (最终修复版)
"""

import os
import re
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path('/workspaces/Noeverer.github.io')
OUTPUT_DIR = BASE_DIR / 'source' / '_posts'

HTML_FILES_TO_RESTORE = [
    'chocolate/2015y.html',
    'chocolate/2016spring.html',
    'chocolate/2016autumn.html',
    'chocolate/2017spring.html',
    'chocolate/2017autumn.html',
    'chocolate/2018spring.html',
    'chocolate/2018autumn.html',
    'chocolate/2019spring.html',
    'code/leetcode/121. Best Time to Buy and Sell Stock.html',
    'code/leetcode/1144_Decrease Elements To Make Array Zigzag.html',
    'code/leetcode/912_Sort an array.html',
    'code/leetcode/leetcode_summary.html',
    'code/leetcode/冒泡排序.html',
    'code/python/python数据操作的总结.html',
    'code/mindmap/数据结构.html',
    'code/mindmap/算法.html',
]

def restore_file_from_git(filepath):
    """从Git历史恢复文件"""
    try:
        result = subprocess.run(
            ['git', 'show', f'HEAD:{filepath}'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"恢复文件失败 {filepath}: {e}")
        return None

def extract_full_content(soup):
    """提取完整的内容"""
    content_selectors = [
        'div.article-inner',
        'article',
        'div.post-content',
        'div.article-entry',
        'div.entry-content',
        'main',
        'div.content',
        'div.article',
    ]

    content = None
    for selector in content_selectors:
        element = soup.select_one(selector)
        if element:
            content = element
            break

    if not content:
        body = soup.find('body')
        if body:
            content = body.__copy__()
            for unwanted in content.select(
                '.left-col, .overlay, .mid-col, .right-col, '
                'header, footer, nav, .header-menu, .article-meta, '
                '.page-reward, .ds-thread, .duoshuo, .overlay'
            ):
                unwanted.decompose()

    return content

def parse_code_block(figure_element):
    """解析代码块 - 从figure元素提取"""
    if not figure_element:
        return ''

    # 查找table中的代码
    table = figure_element.find('table')
    if table:
        code_td = table.select_one('td.code')
        if code_td:
            pre = code_td.find('pre')
            if pre:
                # 方法：获取所有span.line的文本
                lines = []
                for line_span in pre.find_all('span', class_='line'):
                    # 移除内部span标签但保留文本
                    for inner in line_span.find_all('span'):
                        inner.unwrap()
                    line_text = line_span.get_text().strip()
                    if line_text:
                        lines.append(line_text)
                return '\n'.join(lines)

    # 备用方案：直接提取pre
    pre = figure_element.find('pre')
    if pre:
        for br in pre.find_all('br'):
            br.replace_with('\n')
        for span in pre.find_all('span'):
            span.unwrap()
        return pre.get_text().strip()

    return ''

def convert_html_to_markdown(html_content, filepath):
    """深度转换HTML到Markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')

    title = extract_title(soup, filepath)
    date = extract_date(soup, filepath)
    category, tags = infer_category(filepath)

    content_element = extract_full_content(soup)
    if not content_element:
        print(f"无法提取内容: {filepath}")
        return None

    markdown_content = convert_element_to_markdown(content_element)

    if not markdown_content or len(markdown_content.strip()) < 20:
        print(f"内容为空或过短: {filepath}")
        return None

    return {
        'title': title,
        'date': date,
        'tags': tags,
        'category': category,
        'content': markdown_content,
        'source_file': str(filepath)
    }

def extract_title(soup, filepath):
    """提取标题"""
    h1 = soup.find('h1')
    if h1:
        title = h1.get_text().strip()
        if title and title not in ['Ante Liu', 'Thanks For Watching！']:
            return title

    title_meta = soup.find('meta', property='og:title')
    if title_meta:
        title = title_meta.get('content', '').replace(' | Ante Liu', '')
        if title and title not in ['Ante Liu', 'Thanks For Watching！']:
            return title

    filename = Path(filepath).stem
    filename = re.sub(r'^\d+[\.\-_]', '', filename)
    title = filename.replace('-', ' ').replace('_', ' ')
    title = ' '.join(word.capitalize() for word in title.split())
    return title

def extract_date(soup, filepath):
    """提取日期"""
    url_meta = soup.find('meta', property='og:url')
    if url_meta:
        url = url_meta.get('content', '')
        date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', url)
        if date_match:
            year, month, day = date_match.groups()
            return f"{year}-{month}-{day}"

    filename = Path(filepath).stem
    year_match = re.match(r'^(\d{4})y$', filename)
    if year_match:
        return f"{year_match.group(1)}-01-01"

    season_match = re.match(r'^(\d{4})(spring|autumn)$', filename, re.IGNORECASE)
    if season_match:
        year, season = season_match.groups()
        month = "03" if season.lower() == 'spring' else "09"
        return f"{year}-{month}-01"

    return '2019-08-01'

def infer_category(filepath):
    """推断分类和标签"""
    path_str = str(filepath).lower()

    if 'chocolate' in path_str:
        return 'chocolate', ['chocolate', 'life', '感悟']
    elif 'code' in path_str:
        if 'leetcode' in path_str:
            return 'leetcode', ['leetcode', 'algorithm', 'code']
        elif 'python' in path_str:
            return 'python', ['python', 'code']
        elif 'mindmap' in path_str:
            return 'mindmap', ['mindmap', 'study']
        return 'code', ['code', 'tech']
    elif 'work' in path_str:
        return 'work', ['work']
    elif 'love' in path_str:
        return 'love', ['love']
    elif 'fun_thing' in path_str:
        return 'fun', ['fun', 'life']
    elif 'problem' in path_str:
        return 'problem', ['problem', 'tech']
    else:
        return 'uncategorized', ['blog']

def convert_element_to_markdown(element):
    """递归转换HTML元素为Markdown"""
    if element is None:
        return ''

    result = []

    for child in element.children:
        if child.name is None:
            text = str(child).strip()
            if text and text not in ['\n', '\r', ' ', '\t', '\xa0']:
                result.append(text)
        elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(child.name[1])
            text = child.get_text().strip()
            if text and text not in ['Ante Liu', 'Thanks For Watching！']:
                result.append(f"\n{'#' * level} {text}\n")
        elif child.name == 'p':
            text = child.get_text().strip()
            if text and len(text) > 1:
                result.append(f"\n{text}\n")
        elif child.name in ['strong', 'b']:
            text = child.get_text().strip()
            if text:
                result.append(f"**{text}**")
        elif child.name in ['em', 'i']:
            text = child.get_text().strip()
            if text:
                result.append(f"*{text}*")
        elif child.name == 'code':
            text = child.get_text()
            result.append(f"`{text}`")
        elif child.name == 'pre':
            code_block = parse_code_block(child)
            if code_block and len(code_block.strip()) > 5:
                result.append(f"\n```python\n{code_block}\n```\n")
        elif child.name == 'figure':
            if child.get('class') and 'highlight' in str(child.get('class', '')):
                code_block = parse_code_block(child)
                if code_block and len(code_block.strip()) > 5:
                    result.append(f"\n```python\n{code_block}\n```\n")
            elif child.find('figcaption'):
                continue
        elif child.name == 'ul':
            for li in child.find_all('li', recursive=False):
                text = li.get_text().strip()
                if text:
                    result.append(f"- {text}")
        elif child.name == 'ol':
            for i, li in enumerate(child.find_all('li', recursive=False), 1):
                text = li.get_text().strip()
                if text:
                    result.append(f"{i}. {text}")
        elif child.name == 'blockquote':
            text = child.get_text().strip()
            if text:
                result.append(f"\n> {text}\n")
        elif child.name == 'br':
            result.append('\n')
        elif child.name == 'a':
            text = child.get_text().strip()
            href = child.get('href', '')
            if text and 'javascript:' not in href and 'onenote:' not in href:
                result.append(f"[{text}]({href})")
        elif child.name == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            if src and 'javascript' not in src:
                result.append(f"![{alt}]({src})")
        elif child.name not in ['script', 'style', 'noscript', 'iframe', 'figcaption', 'div.page-reward']:
            child_result = convert_element_to_markdown(child)
            if child_result and len(child_result.strip()) > 0:
                result.append(child_result)

    markdown = ' '.join(str(r) for r in result)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = re.sub(r'[ \t]+', ' ', markdown)
    return markdown.strip()

def save_markdown(article):
    """保存Markdown文件"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    date = article['date'][:10]
    title = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', article['title'])
    title = re.sub(r'[-\s]+', '-', title).strip('-')

    filename = f"{date}-{title}.md"
    filepath = OUTPUT_DIR / filename

    counter = 1
    while filepath.exists():
        filename = f"{date}-{title}-{counter}.md"
        filepath = OUTPUT_DIR / filename
        counter += 1

    tags_str = '["' + '", "'.join(article['tags']) + '"]'

    desc = article['content'][:200] if article['content'] else ''
    desc = desc.replace('\n', ' ').replace('\r', '')
    desc = re.sub(r'[^\w\s\u4e00-\u9fff.,;:!?-]', '', desc).strip()

    front_matter = f"""---
title: {article['title']}
date: {article['date']} 12:00:00
tags: {tags_str}
categories: {article['category']}
description: {desc}
---
"""

    full_content = front_matter + article['content']

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return filepath

def main():
    """主函数"""
    print("=" * 70)
    print("从Git历史恢复并深度转换HTML文件 (最终修复版)")
    print("=" * 70)

    converted_files = []
    failed_files = []

    for html_file in HTML_FILES_TO_RESTORE:
        print(f"\n处理: {html_file}")

        html_content = restore_file_from_git(html_file)
        if not html_content:
            print(f"  ✗ 无法从Git恢复")
            failed_files.append(html_file)
            continue

        article = convert_html_to_markdown(html_content, html_file)
        if not article:
            print(f"  ✗ 转换失败")
            failed_files.append(html_file)
            continue

        filepath = save_markdown(article)
        print(f"  ✓ 保存: {filepath.name}")
        converted_files.append(filepath)

    print("\n" + "=" * 70)
    print("转换完成")
    print("=" * 70)
    print(f"成功转换: {len(converted_files)} 个文件")
    print(f"转换失败: {len(failed_files)} 个文件")

    if failed_files:
        print("\n失败的文件:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == '__main__':
    main()
