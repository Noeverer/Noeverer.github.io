#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML to Markdown Converter with Hexo Integration
支持HTML转Markdown、Git分支管理、GitHub Actions自动化部署
"""

import os
import re
import json
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import git
import subprocess
import traceback


# ==================== 配置日志 ====================
def setup_logging(log_file: str = 'html2hexo.log') -> logging.Logger:
    """配置日志记录"""
    logger = logging.getLogger('html2hexo')
    logger.setLevel(logging.DEBUG)

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()


# ==================== 数据结构 ====================
@dataclass
class Article:
    title: str
    date: str
    tags: List[str]
    category: str
    description: str
    content: str
    source_file: str


@dataclass
class ConversionResult:
    total_files: int
    converted_files: int
    skipped_files: int
    failed_files: int
    articles: List[Article]
    errors: List[str]


# ==================== 主题推荐系统 ====================
class ThemeRecommender:
    """Hexo主题智能推荐系统"""

    THEMES = {
        'next': {
            'name': 'NexT',
            'description': '最受欢迎的Hexo主题，功能完善',
            'features': {
                'code_highlight': True,
                'responsive': True,
                'seo': True,
                'dark_mode': True,
                'mathjax': True,
                'gallery': True,
                'search': True,
                'comment': True
            },
            'suitability_score': 95,
            'official_url': 'https://theme-next.js.org/'
        },
        'butterfly': {
            'name': 'Butterfly',
            'description': '美观且功能强大的主题',
            'features': {
                'code_highlight': True,
                'responsive': True,
                'seo': True,
                'dark_mode': True,
                'mathjax': True,
                'gallery': True,
                'search': True,
                'comment': True
            },
            'suitability_score': 92,
            'official_url': 'https://butterfly.js.org/'
        },
        'fluid': {
            'name': 'Fluid',
            'description': '简洁优雅的主题，适合技术博客',
            'features': {
                'code_highlight': True,
                'responsive': True,
                'seo': True,
                'dark_mode': True,
                'mathjax': True,
                'gallery': False,
                'search': True,
                'comment': True
            },
            'suitability_score': 90,
            'official_url': 'https://hexo.fluid-dev.com/'
        },
        'stun': {
            'name': 'Stun',
            'description': '极简主义主题',
            'features': {
                'code_highlight': True,
                'responsive': True,
                'seo': True,
                'dark_mode': False,
                'mathjax': True,
                'gallery': False,
                'search': True,
                'comment': True
            },
            'suitability_score': 85,
            'official_url': 'https://github.com/liuyib/hexo-theme-stun'
        },
        'cactus': {
            'name': 'Cactus',
            'description': '轻量级极简主题',
            'features': {
                'code_highlight': True,
                'responsive': True,
                'seo': True,
                'dark_mode': False,
                'mathjax': False,
                'gallery': False,
                'search': False,
                'comment': False
            },
            'suitability_score': 80,
            'official_url': 'https://github.com/probberechts/hexo-theme-cactus'
        }
    }

    @classmethod
    def analyze_content(cls, articles: List[Article]) -> Dict[str, int]:
        """分析文章内容特征"""
        features = {
            'has_code': 0,
            'has_images': 0,
            'has_math': 0,
            'long_articles': 0,
            'tech_content': 0
        }

        for article in articles:
            content = article.content.lower()

            # 代码检测
            if re.search(r'```|<code>|\bfunction\b|\bdef\b|\bclass\b', content):
                features['has_code'] += 1

            # 图片检测
            if re.search(r'!\[.*?\]\(|<img|\.png|\.jpg|\.gif', content):
                features['has_images'] += 1

            # 数学公式检测
            if re.search(r'\$\$|\\frac|\\sum|\\int', content):
                features['has_math'] += 1

            # 长文章检测（超过1000字）
            if len(content) > 1000:
                features['long_articles'] += 1

            # 技术内容检测
            if article.category in ['code', 'leetcode', 'python', 'problem']:
                features['tech_content'] += 1

        return features

    @classmethod
    def recommend_theme(cls, articles: List[Article]) -> List[Dict]:
        """根据内容推荐主题"""
        content_features = cls.analyze_content(articles)
        total = len(articles) if articles else 1

        # 计算需求权重
        needs = {
            'code_highlight': content_features['has_code'] / total > 0.3,
            'responsive': content_features['long_articles'] / total > 0.5,
            'seo': True,  # SEO是基本需求
            'dark_mode': content_features['tech_content'] / total > 0.3,
            'mathjax': content_features['has_math'] / total > 0.1,
            'gallery': content_features['has_images'] / total > 0.3,
            'search': total > 10,
            'comment': total > 5
        }

        # 计算每个主题的适配分数
        recommendations = []
        for theme_id, theme_info in cls.THEMES.items():
            match_score = 0
            max_score = 0

            for feature, required in needs.items():
                max_score += 1
                if theme_info['features'].get(feature, False):
                    match_score += 1

            # 综合评分：特征匹配分数 * 0.7 + 基础适配分数 * 0.3
            final_score = (match_score / max_score * 70) if max_score > 0 else 0
            final_score += theme_info['suitability_score'] * 0.3

            recommendations.append({
                'theme_id': theme_id,
                'name': theme_info['name'],
                'description': theme_info['description'],
                'score': round(final_score, 1),
                'match_features': [f for f, r in needs.items()
                                   if theme_info['features'].get(f, False) and r],
                'missing_features': [f for f, r in needs.items()
                                     if not theme_info['features'].get(f, False) and r],
                'official_url': theme_info['official_url']
            })

        # 按分数排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)

        return recommendations

    @classmethod
    def print_recommendations(cls, articles: List[Article]):
        """打印推荐结果"""
        content_features = cls.analyze_content(articles)
        recommendations = cls.recommend_theme(articles)

        logger.info("\n" + "=" * 70)
        logger.info("内容特征分析")
        logger.info("=" * 70)
        logger.info(f"  包含代码的文章: {content_features['has_code']}")
        logger.info(f"  包含图片的文章: {content_features['has_images']}")
        logger.info(f"  包含数学公式的文章: {content_features['has_math']}")
        logger.info(f"  长篇文章 (>1000字): {content_features['long_articles']}")
        logger.info(f"  技术类文章: {content_features['tech_content']}")

        logger.info("\n" + "=" * 70)
        logger.info("Hexo主题推荐")
        logger.info("=" * 70)

        for i, rec in enumerate(recommendations[:5], 1):
            logger.info(f"\n[{i}] {rec['name']} - 评分: {rec['score']}")
            logger.info(f"    描述: {rec['description']}")
            logger.info(f"    官网: {rec['official_url']}")
            if rec['match_features']:
                logger.info(f"    匹配特性: {', '.join(rec['match_features'])}")
            if rec['missing_features']:
                logger.info(f"    缺失特性: {', '.join(rec['missing_features'])}")

        logger.info("\n推荐安装命令:")
        logger.info(f"  cd themes && git clone {recommendations[0]['official_url'].replace('https://', 'https://github.com/hexojs/').replace('hexo-theme-', '')} next")


# ==================== Git分支管理器 ====================
class GitBranchManager:
    """Git分支自动化管理"""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo = None
        try:
            self.repo = git.Repo(self.repo_path)
        except Exception as e:
            logger.error(f"无法初始化Git仓库: {e}")

    def create_branch(self, branch_name: str, from_branch: str = 'master') -> bool:
        """创建新分支"""
        try:
            if not self.repo:
                logger.error("Git仓库未初始化")
                return False

            # 检查分支是否已存在
            if branch_name in [ref.name for ref in self.repo.references]:
                logger.info(f"分支 '{branch_name}' 已存在，切换到该分支")
                self.repo.git.checkout(branch_name)
                return True

            # 创建并切换新分支
            self.repo.git.checkout(from_branch, b=branch_name)
            logger.info(f"成功创建并切换到分支: {branch_name}")
            return True

        except Exception as e:
            logger.error(f"创建分支失败: {e}")
            logger.debug(traceback.format_exc())
            return False

    def switch_branch(self, branch_name: str) -> bool:
        """切换分支"""
        try:
            if not self.repo:
                return False

            self.repo.git.checkout(branch_name)
            logger.info(f"切换到分支: {branch_name}")
            return True

        except Exception as e:
            logger.error(f"切换分支失败: {e}")
            return False

    def commit_changes(self, message: str) -> bool:
        """提交更改"""
        try:
            if not self.repo:
                return False

            # 添加所有更改
            self.repo.git.add(A=True)

            # 检查是否有更改
            if self.repo.is_dirty(untracked_files=True):
                self.repo.git.commit(m=message)
                logger.info(f"提交更改: {message}")
                return True
            else:
                logger.info("没有需要提交的更改")
                return True

        except Exception as e:
            logger.error(f"提交失败: {e}")
            return False

    def push_branch(self, branch_name: str, remote: str = 'origin') -> bool:
        """推送分支到远程"""
        try:
            if not self.repo:
                return False

            self.repo.git.push(remote, branch_name)
            logger.info(f"推送分支 '{branch_name}' 到远程 '{remote}'")
            return True

        except Exception as e:
            logger.error(f"推送失败: {e}")
            return False

    def merge_branch(self, source_branch: str, target_branch: str = 'master') -> bool:
        """合并分支"""
        try:
            if not self.repo:
                return False

            self.repo.git.checkout(target_branch)
            self.repo.git.merge(source_branch, no_ff=True)
            logger.info(f"合并 '{source_branch}' 到 '{target_branch}'")
            return True

        except Exception as e:
            logger.error(f"合并失败: {e}")
            return False

    def list_branches(self) -> List[str]:
        """列出所有分支"""
        try:
            if not self.repo:
                return []

            branches = [ref.name for ref in self.repo.references]
            return branches

        except Exception as e:
            logger.error(f"列出分支失败: {e}")
            return []

    def create_feature_branch(self, category: str) -> str:
        """根据内容分类创建特性分支"""
        branch_name = f"feature/{category}-{datetime.now().strftime('%Y%m%d')}"
        return branch_name if self.create_branch(branch_name) else ""


# ==================== HTML转换器 ====================
class MarkdownConverter:
    """HTML到Markdown转换器"""

    def __init__(self):
        self.articles = []
        self.converted_files = set()
        self.errors = []

    def parse_html_file(self, filepath: Path) -> Optional[Article]:
        """解析单个HTML文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            # 提取基本信息
            title = self._extract_title(soup, filepath)
            description = self._extract_meta(soup, 'og:description')
            date = self._extract_date(soup, filepath)
            category, tags = self._infer_category(filepath)
            article_content = self._extract_content(soup, filepath)

            # 跳过特定文件
            if self._should_skip(filepath, title):
                return None

            # 检查重复
            file_hash = f"{filepath.stem}-{category}"
            if file_hash in self.converted_files:
                logger.debug(f"跳过重复文件: {filepath}")
                return None
            self.converted_files.add(file_hash)

            # 创建文章对象
            article = Article(
                title=title,
                date=date,
                tags=tags,
                category=category,
                description=description[:200] if description else '',
                content=article_content or description,
                source_file=str(filepath)
            )

            self.articles.append(article)
            logger.info(f"解析成功: {title}")
            return article

        except Exception as e:
            error_msg = f"解析文件失败 {filepath}: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            logger.debug(traceback.format_exc())
            return None

    def _should_skip(self, filepath: Path, title: str) -> bool:
        """判断是否跳过该文件"""
        skip_keywords = ['toc', 'readme', 'index', 'hello-world']
        filename_lower = filepath.name.lower()

        if any(k in filename_lower for k in skip_keywords):
            return True

        if '/life/' in str(filepath):
            return True

        if not title or title == 'Ante Liu':
            return True

        return False

    def _extract_title(self, soup: BeautifulSoup, filepath: Path) -> str:
        """提取标题"""
        title_meta = soup.find('meta', property='og:title')
        if title_meta:
            title = title_meta.get('content', '').replace(' | Ante Liu', '')
            if title and title != 'Ante Liu':
                return title

        # 从文件名提取
        filename = filepath.stem
        filename = re.sub(r'^\d+[\.\-_]', '', filename)
        title = filename.replace('-', ' ').replace('_', ' ')
        title = ' '.join(word.capitalize() for word in title.split())
        return title

    def _extract_meta(self, soup: BeautifulSoup, property_name: str) -> str:
        """提取meta标签内容"""
        meta = soup.find('meta', property=property_name)
        return meta.get('content', '') if meta else ''

    def _extract_date(self, soup: BeautifulSoup, filepath: Path) -> str:
        """提取日期"""
        # 从URL提取
        url_meta = soup.find('meta', property='og:url')
        if url_meta:
            url = url_meta.get('content', '')
            date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', url)
            if date_match:
                year, month, day = date_match.groups()
                return f"{year}-{month}-{day}"

        # 从文件名提取
        filename = filepath.stem

        # 匹配 2015y 格式
        year_match = re.match(r'^(\d{4})y$', filename)
        if year_match:
            return f"{year_match.group(1)}-01-01"

        # 匹配季节格式
        season_match = re.match(r'^(\d{4})(spring|autumn)$', filename, re.IGNORECASE)
        if season_match:
            year, season = season_match.groups()
            month = "03" if season.lower() == 'spring' else "09"
            return f"{year}-{month}-01"

        return '2019-08-01'

    def _infer_category(self, filepath: Path) -> Tuple[str, List[str]]:
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

    def _extract_content(self, soup: BeautifulSoup, filepath: Path) -> str:
        """提取内容"""
        content_selectors = [
            'div.article-inner', 'article', 'div.post-content',
            'div.article-entry', 'div.entry-content', 'main',
            'div.content', 'div.article'
        ]

        content_element = None
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content_element = element
                break

        if not content_element:
            body = soup.find('body')
            if body:
                for unwanted in body.select('.left-col, .overlay, .mid-col, .right-col, header, footer, nav, .header-menu, .article-meta'):
                    unwanted.decompose()
                content_element = body

        if content_element:
            lines = self._parse_element(content_element)
            result = '\n'.join(lines)
            result = re.sub(r'\n{3,}', '\n\n', result)
            return result.strip()
        else:
            desc = self._extract_meta(soup, 'og:description')
            return self._clean_description(desc, filepath)

    def _parse_element(self, element) -> List[str]:
        """递归解析HTML元素"""
        lines = []

        for child in element.children:
            if child.name is None:
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
                lines.extend(self._parse_element(child))

        return lines

    def _clean_description(self, desc: str, filepath: Path) -> str:
        """清理description"""
        desc = ' '.join(desc.split())
        path_str = str(filepath).lower()

        if 'code' in path_str or 'leetcode' in path_str:
            leetcode_pattern = re.compile(r'(\d+\.\s*[A-Z][^.]+)')
            desc = leetcode_pattern.sub(r'\n\n## \1\n', desc)
            return desc

        if 'chocolate' in path_str:
            date_pattern = re.compile(r'(\d{4}\.\d{2}\.\d{2})')
            desc = date_pattern.sub(r'\n\n### \1\n', desc)
            sentences = re.split(r'(?<=[。！？.!?])\s+', desc)
            if len(sentences) > 3:
                return '\n\n'.join(sentences)

        return desc

    def save_markdown_files(self, output_dir: Path) -> int:
        """保存Markdown文件"""
        output_dir.mkdir(parents=True, exist_ok=True)

        for article in self.articles:
            date = article['date'][:10]
            title = re.sub(r'[^\w\s-]', '', article['title'])
            title = re.sub(r'[-\s]+', '-', title).strip('-')

            filename = f"{date}-{title}.md"
            filepath = output_dir / filename

            counter = 1
            while filepath.exists():
                filename = f"{date}-{title}-{counter}.md"
                filepath = output_dir / filename
                counter += 1

            tags_list = json.dumps(article['tags'], ensure_ascii=False)
            desc = article['description'][:200] if article['description'] else ''
            desc = desc.replace('\n', ' ').replace('\r', '')
            desc = re.sub(r'[^\w\s\u4e00-\u9fff.,;:!?-]', '', desc).strip()

            front_matter = f"""---
title: {article['title']}
date: {article['date']} 12:00:00
tags: {tags_list}
categories: {article['category']}
description: {desc}
---
"""

            full_content = front_matter + article['content']

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            logger.info(f"保存文件: {filename}")

        return len(self.articles)


# ==================== GitHub Actions配置生成器 ====================
class GitHubActionsGenerator:
    """生成GitHub Actions工作流配置"""

    @staticmethod
    def create_hexo_deploy_workflow(repo_name: str = 'Noeverer.github.io') -> str:
        """创建Hexo部署工作流"""
        workflow = f"""name: Hexo Deploy to GitHub Pages

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: |
          npm install hexo-cli -g
          npm install

      - name: Generate posts from HTML
        run: |
          if [ -f html2hexo.py ]; then
            python3 html2hexo.py
          fi

      - name: Build Hexo site
        run: |
          hexo clean
          hexo generate

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{{{ secrets.GITHUB_TOKEN }}}}
          publish_dir: ./public
          publish_branch: gh-pages
          cname: noeverer.github.io

      - name: Create git tag
        run: |
          TAG_NAME=deploy-$(date +%Y%m%d-%H%M%S)
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git tag -a $TAG_NAME -m "Auto deploy at $(date)"
          git push origin $TAG_NAME
"""
        return workflow

    @staticmethod
    def create_workflow_file(workflow_dir: Path):
        """创建GitHub Actions工作流文件"""
        workflow_dir.mkdir(parents=True, exist_ok=True)
        workflow_file = workflow_dir / 'hexo-deploy.yml'
        content = GitHubActionsGenerator.create_hexo_deploy_workflow()

        with open(workflow_file, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"创建GitHub Actions工作流: {workflow_file}")
        return workflow_file

    @staticmethod
    def create_readme_instructions() -> str:
        """创建README说明"""
        return """# Hexo自动部署系统

## 功能特性

1. **HTML转Markdown** - 自动将HTML博客文章转换为Markdown格式
2. **Git分支管理** - 智能创建和管理内容分支
3. **主题推荐** - 基于内容分析推荐适合的Hexo主题
4. **自动部署** - 通过GitHub Actions实现持续部署

## 使用方法

### 1. 首次设置

```bash
# 安装依赖
pip install beautifulsoup4 GitPython

# 安装Hexo
npm install -g hexo-cli
npm install

# 运行转换脚本
python3 html2hexo.py
```

### 2. 转换HTML文件

```bash
# 转换所有HTML文件
python3 html2hexo.py

# 转换指定目录
python3 html2hexo.py --dir ./chocolate
```

### 3. Git分支管理

```bash
# 为特定分类创建特性分支
python3 html2hexo.py --branch chocolate

# 合并到主分支
python3 html2hexo.py --merge feature/chocolate-20250105
```

### 4. 自动部署

推送到master分支即可触发自动部署：
```bash
git add .
git commit -m "Update posts"
git push origin master
```

## GitHub Actions配置

工作流文件位于：`.github/workflows/hexo-deploy.yml`

支持以下触发方式：
- 推送到master分支
- Pull Request到master
- 手动触发（workflow_dispatch）

## 主题推荐

运行脚本后会自动分析内容并推荐主题：
- NexT - 功能最全面
- Butterfly - 美观现代
- Fluid - 简洁优雅

查看详细推荐信息请运行：
```bash
python3 html2hexo.py --recommend
```

## 日志文件

转换日志保存在：`html2hexo.log`
"""


# ==================== 主控制器 ====================
class HTML2HexoController:
    """主控制器"""

    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.converter = MarkdownConverter()
        self.git_manager = GitBranchManager(str(self.base_dir))
        self.output_dir = self.base_dir / 'source' / '_posts'

    def scan_html_files(self) -> List[Path]:
        """扫描HTML文件"""
        html_files = []

        directories = [
            'chocolate', 'code', 'Fun_thing', 'work',
            'life', 'love', 'Problem-Encounted-in-Blogging'
        ]

        logger.info("开始扫描HTML文件...")

        # 扫描指定目录
        for dir_name in directories:
            dir_path = self.base_dir / dir_name
            if dir_path.exists():
                for filepath in dir_path.rglob('*.html'):
                    if 'node_modules' not in str(filepath):
                        html_files.append(filepath)

        # 扫描根目录
        for filepath in self.base_dir.glob('*.html'):
            skip_files = ['index.html', 'README.html', 'TOC.html', 'hello-world.html']
            if filepath.name not in skip_files:
                html_files.append(filepath)

        # 去重
        html_files = list(set(html_files))
        logger.info(f"找到 {len(html_files)} 个HTML文件")

        return html_files

    def convert_all(self) -> ConversionResult:
        """转换所有HTML文件"""
        html_files = self.scan_html_files()

        result = ConversionResult(
            total_files=len(html_files),
            converted_files=0,
            skipped_files=0,
            failed_files=0,
            articles=[],
            errors=[]
        )

        for html_file in html_files:
            article = self.converter.parse_html_file(html_file)
            if article:
                result.converted_files += 1
            else:
                result.skipped_files += 1

        result.articles = self.converter.articles
        result.errors = self.converter.errors
        result.failed_files = len(result.errors)

        return result

    def save_and_deploy(self, result: ConversionResult, create_branch: bool = True):
        """保存文件并准备部署"""
        # 保存Markdown文件
        logger.info("保存Markdown文件...")
        saved_count = self.converter.save_markdown_files(self.output_dir)
        logger.info(f"保存了 {saved_count} 个Markdown文件")

        # 统计分类
        category_count = {}
        for article in result.articles:
            cat = article['category']
            category_count[cat] = category_count.get(cat, 0) + 1

        logger.info("\n分类统计:")
        for cat, count in sorted(category_count.items()):
            logger.info(f"  - {cat}: {count} 篇")

        # 主题推荐
        recommendations = ThemeRecommender.recommend_theme(result.articles)
        ThemeRecommender.print_recommendations(result.articles)

        # Git操作
        if create_branch and result.converted_files > 0:
            logger.info("\n准备Git提交...")
            self.git_manager.commit_changes(f"Update {saved_count} posts from HTML")

    def setup_github_actions(self):
        """设置GitHub Actions"""
        workflow_dir = self.base_dir / '.github' / 'workflows'
        GitHubActionsGenerator.create_workflow_file(workflow_dir)
        logger.info("GitHub Actions工作流已创建")

    def create_deployment_setup(self):
        """创建部署相关文件"""
        # 创建README
        readme_path = self.base_dir / 'DEPLOYMENT.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(GitHubActionsGenerator.create_readme_instructions())
        logger.info(f"创建部署说明: {readme_path}")

        # 创建GitHub Actions工作流
        self.setup_github_actions()

    def run_full_conversion(self):
        """运行完整转换流程"""
        logger.info("=" * 70)
        logger.info("HTML到Hexo转换系统启动")
        logger.info("=" * 70)

        # 转换HTML
        result = self.convert_all()

        logger.info("\n" + "=" * 70)
        logger.info("转换结果统计")
        logger.info("=" * 70)
        logger.info(f"总文件数: {result.total_files}")
        logger.info(f"成功转换: {result.converted_files}")
        logger.info(f"跳过文件: {result.skipped_files}")
        logger.info(f"失败文件: {result.failed_files}")

        if result.errors:
            logger.info("\n错误列表:")
            for error in result.errors[:10]:
                logger.info(f"  - {error}")

        # 保存和部署
        self.save_and_deploy(result)

        # 创建部署设置
        self.create_deployment_setup()

        logger.info("\n" + "=" * 70)
        logger.info("转换完成!")
        logger.info("=" * 70)

        return result


# ==================== 命令行接口 ====================
def main():
    import argparse

    parser = argparse.ArgumentParser(description='HTML到Hexo转换系统')
    parser.add_argument('--dir', type=str, help='指定HTML文件目录')
    parser.add_argument('--branch', type=str, help='创建特性分支')
    parser.add_argument('--recommend', action='store_true', help='只显示主题推荐')
    parser.add_argument('--setup', action='store_true', help='设置GitHub Actions')

    args = parser.parse_args()

    controller = HTML2HexoController()

    if args.setup:
        controller.create_deployment_setup()
        return

    if args.recommend:
        result = controller.convert_all()
        ThemeRecommender.print_recommendations(result.articles)
        return

    if args.branch:
        branch_name = controller.git_manager.create_feature_branch(args.branch)
        logger.info(f"创建分支: {branch_name}")

    result = controller.run_full_conversion()


if __name__ == '__main__':
    main()
