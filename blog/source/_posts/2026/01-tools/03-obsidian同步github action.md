---
title: 工具整理
date: 2026-01-28 12:00:00
tags:
  - 笔记工具
categories: 工具
description: obsidian工具整理
published: true
---
# 方案

实现从obsidian通过插件实现笔记软件同步到github 最后使用action 方式进行发布

# 配置

```yml
name: pages-build-deployment

on:
  push:
    branches: [ master ]
  workflow_dispatch:
    inputs:
      manual_trigger:
        description: 'Manual deployment trigger'
        required: false
        default: 'manual'

# 设置 GitHub Pages 权限
permissions:
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          submodules: recursive

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Display environment info
        run: |
          echo "Node version: $(node --version)"
          echo "NPM version: $(npm --version)"
          echo "Working directory: $(pwd)"

      - name: Install dependencies
        run: |
          npm install hexo-cli -g
          npm ci --production=false

      - name: Verify theme installation
        run: |
          echo "Checking theme installation..."
          if [ ! -d "node_modules/hexo-theme-butterfly" ]; then
            echo "❌ Error: hexo-theme-butterfly not found!"
            exit 1
          fi
          echo "✅ Theme installed successfully"

      - name: Clean cache
        run: |
          echo "Cleaning Hexo cache..."
          hexo clean || true

      - name: Generate static files
        run: |
          echo "Generating static files..."
          hexo generate
          echo "✅ Generation completed"

      - name: Verify build output
        run: |
          echo "=== Build Verification ==="
          echo "Public directory contents:"
          ls -la public/
          echo ""
          
          if [ ! -d "public" ]; then
            echo "❌ Error: public directory not found!"
            exit 1
          fi
          
          if [ ! -f "public/index.html" ]; then
            echo "❌ Error: index.html not found!"
            exit 1
          fi
          
          echo "✅ index.html exists"
          
          # 检查是否生成了文章页面
          if [ -f "public/index.html" ]; then
            echo "✅ Checking for article links in index.html..."
            if grep -q "posts/" public/index.html; then
              echo "✅ Article links found in index.html"
            else
              echo "⚠️  Warning: No article links found in index.html"
            fi
          fi
          
          # 统计生成的文件数量
          FILE_COUNT=$(find public -type f | wc -l)
          echo "📊 Total files generated: $FILE_COUNT"
          
          if [ "$FILE_COUNT" -lt 10 ]; then
            echo "⚠️  Warning: Generated file count seems low ($FILE_COUNT files)"
          fi

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: hexo-build-output
          path: public/
          retention-days: 7

      - name: Deploy to GitHub Pages
        id: deployment
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          publish_branch: gh-pages
          force_orphan: true
          user_name: 'github-actions[bot]'
          user_email: 'github-actions[bot]@users.noreply.github.com'
          commit_message: 'Deploy Hexo blog - ${{ github.event.head_commit.message }}'
          force: true

      - name: Deployment summary
        if: success()
        run: |
          echo "=== 🎉 Deployment Summary ==="
          echo "✅ Build successful!"
          echo "✅ Deployment to gh-pages completed!"
          echo "🌐 Blog URL: https://noeverer.github.io"
          echo "📅 Deployment time: $(date)"
          echo "👤 Triggered by: ${{ github.actor }}"
          echo "📝 Commit: ${{ github.sha }}"

      - name: Deployment failure notification
        if: failure()
        run: |
          echo "=== ❌ Deployment Failed ==="
          echo "❌ Deployment to gh-pages failed!"
          echo "Please check the logs above for details."
          echo "GitHub Actions URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```


- [ ] #task 实现github仓库简介化  📅 2026-02-03 
- [ ] #task 添加代办任务 ⏳ 2023-04-14
- [ ] #task 与邮箱联动 🛫 2023-04-15

- [ ] 🛫 2026-01-28 实现邮箱联动 📅 2026-02-03 ⏬ 

- [ ] This is a task [priority:: high] [start:: 2023-04-24] [due:: 2023-05-01]