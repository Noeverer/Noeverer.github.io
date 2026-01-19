#!/bin/bash
#
# VitePress 初始化脚本
# 用法: ./vitepress/init-vitepress.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$PROJECT_ROOT"

echo "========================================="
echo "  VitePress 初始化脚本"
echo "========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}错误: 未安装 Node.js${NC}"
    echo "请先安装 Node.js: https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}Node.js 版本: $(node -v)${NC}"

# 初始化 npm 项目
echo ""
echo -e "${GREEN}[1/5] 初始化 npm 项目...${NC}"
if [ ! -f package.json ]; then
    npm init -y
else
    echo "package.json 已存在，跳过"
fi

# 安装 VitePress
echo ""
echo -e "${GREEN}[2/5] 安装 VitePress...${NC}"
npm install -D vitepress

# 创建目录结构
echo ""
echo -e "${GREEN}[3/5] 创建目录结构...${NC}"
mkdir -p docs/programming
mkdir -p docs/study
mkdir -p docs/life
mkdir -p .vitepress

# 创建 VitePress 配置
echo ""
echo -e "${GREEN}[4/5] 创建 VitePress 配置...${NC}"
cat > .vitepress/config.ts << 'EOF'
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Ante's Wiki",
  description: '个人知识库 - 记录、整理、分享',
  lang: 'zh-CN',
  base: '/wiki/',

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '编程', link: '/programming/' },
      { text: '学习', link: '/study/' },
      { text: '生活', link: '/life/' },
      {
        text: 'GitHub',
        link: 'https://github.com/Noeverer/Noeverer.github.io'
      }
    ],

    sidebar: [
      {
        text: '编程',
        items: [
          { text: 'Python', link: '/programming/python.md' },
          { text: 'Docker', link: '/programming/docker.md' },
        ]
      },
      {
        text: '学习',
        items: [
          { text: '学习笔记', link: '/study/notes.md' },
          { text: '思维导图', link: '/study/mindmap.md' },
        ]
      },
      {
        text: '生活',
        items: [
          { text: '感悟', link: '/life/thoughts.md' },
        ]
      }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2015-present Ante Liu'
    },

    editLink: {
      pattern: 'https://github.com/Noeverer/Noeverer.github.io/edit/main/source/resources/wikijs/docs/:path',
      text: '在 GitHub 上编辑此页'
    },

    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium'
      }
    }
  },

  markdown: {
    lineNumbers: true,
    config: (md) => {
      // 可以添加 markdown-it 插件
    }
  }
})
EOF

# 创建首页
echo ""
echo -e "${GREEN}[5/5] 创建首页和示例文档...${NC}"
cat > docs/index.md << 'EOF'
---
layout: home

hero:
  name: "Ante's Wiki"
  text: "个人知识库"
  tagline: "记录、整理、分享"
  image:
    src: /logo.svg
    alt: Ante's Wiki
  actions:
    - theme: brand
      text: 开始阅读
      link: /programming/
    - theme: alt
      text: 在 GitHub 查看
      link: https://github.com/Noeverer/Noeverer.github.io

features:
  - title: 🚀 快速
    details: 基于 VitePress 构建，加载速度快，开发体验好
  - title: 📝 Markdown
    details: 使用 Markdown 编写，支持代码高亮、数学公式等
  - title: 🔁 自动同步
    details: 通过 Wiki.js + GitHub Actions 实现自动发布
  - title: 📱 响应式
    details: 完美适配各种设备，随时随地访问
---

## 欢迎来到我的知识库

这里是我使用 Wiki.js 管理的个人知识库，通过 GitHub Actions 自动发布到 GitHub Pages。

### 内容分类

- **编程**: Python、Docker、开发工具等
- **学习**: 学习笔记、思维导图、技术总结
- **生活**: 感悟、随笔、日常记录

### 技术栈

- [Wiki.js](https://js.wiki/) - 本地知识管理
- [VitePress](https://vitepress.dev/) - 静态站点生成
- [GitHub Pages](https://pages.github.com/) - 免费托管
- [GitHub Actions](https://github.com/features/actions) - 自动部署

### 快速开始

1. 访问 Wiki.js 管理界面
2. 创建或编辑文档
3. 内容自动同步到 GitHub
4. GitHub Actions 自动构建发布

### 联系方式

- GitHub: [@Noeverer](https://github.com/Noeverer)
- Email: robotliu0327@gmail.com
EOF

# 创建示例文档
cat > docs/programming/python.md << 'EOF'
# Python

Python 学习笔记和常用代码片段。

## 基础语法

```python
print("Hello, World!")
```

## 常用库

### NumPy

```python
import numpy as np

arr = np.array([1, 2, 3])
print(arr)
```

### Pandas

```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
print(df)
```
EOF

cat > docs/study/notes.md << 'EOF'
# 学习笔记

这里记录我的学习笔记。
EOF

cat > docs/life/thoughts.md << 'EOF'
# 感悟

生活不止眼前的苟且，还有诗和远方。
EOF

# 更新 package.json
echo ""
echo "添加 npm scripts..."
node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg.scripts = {
  'dev': 'vitepress dev',
  'build': 'vitepress build',
  'preview': 'vitepress preview'
};
pkg.type = 'module';
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
"

# 创建 .gitignore
cat > .gitignore << 'EOF'
node_modules/
.vitepress/cache/
.vitepress/dist/
.DS_Store
*.log
.env
EOF

echo ""
echo "========================================="
echo "  初始化完成"
echo "========================================="
echo ""
echo -e "${GREEN}下一步操作:${NC}"
echo "1. 本地预览: npm run dev"
echo "2. 构建站点: npm run build"
echo "3. 预览构建: npm run preview"
echo ""
echo -e "${YELLOW}提示:${NC}"
echo "- 将此目录复制到你的 Wiki.js Git 仓库中"
echo "- Wiki.js 的内容会自动同步到 docs/ 目录"
echo "- 推送到 GitHub 后会自动触发构建"
echo ""
