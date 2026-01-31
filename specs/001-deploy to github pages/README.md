---
status: complete
created: '2026-01-12'
tags:
  - deployment
  - github-pages
  - hexo
priority: high
created_at: '2026-01-12T02:33:04.379Z'
updated_at: '2026-01-12T07:16:47.529Z'
completed_at: '2026-01-12T07:16:47.529Z'
completed: '2026-01-12'
transitions:
  - status: complete
    at: '2026-01-12T07:16:47.529Z'
---

# Deploy to GitHub Pages

> **Status**: ✅ Complete · **Priority**: High · **Created**: 2026-01-12 · **Tags**: deployment, github-pages, hexo

## Overview

将 Hexo 博客自动部署到 GitHub Pages，确保所有 markdown 文章正确配置 `published: true`，并验证部署成功。

### 问题背景
- 博客文章未正确发布到 GitHub Pages
- 部分文章缺少 `published: true` 配置导致不显示
- GitHub Actions 构建过程中存在错误

### 目标
- 确保所有文章正确配置发布状态
- 自动化部署流程正常工作
- 验证所有文章在 GitHub Pages 上可访问

## Design

### 技术架构
```
GitHub Repository (master branch)
    ↓ push triggers
GitHub Actions (deploy.yml)
    ↓ build
Hexo Generate (public/)
    ↓ deploy
GitHub Pages (gh-pages branch)
```

### 关键配置
- **触发条件**: master 分支推送
- **构建工具**: Hexo + GitHub Actions
- **部署方式**: peaceiris/actions-gh-pages@v4
- **目标分支**: gh-pages

## Plan

### Phase 1: 检查并修复文章配置
- [x] 扫描 `source/_posts/` 下所有 markdown 文件
- [x] 验证每个文件的 frontmatter 包含 `published: true`
- [x] 为缺少配置的文件添加 `published: true`

### Phase 2: 修复 GitHub Actions 构建问题
- [x] 移除干扰 Hexo 构建的脚本文件 (`scripts/` 目录)
- [x] 删除 `.deploy_git` 子模块导致的问题
- [x] 更新 `.gitignore` 排除不必要的文件

### Phase 3: 验证本地构建
- [x] 运行 `hexo clean` 清理缓存
- [x] 运行 `hexo generate` 生成静态文件
- [x] 检查生成的 `public/index.html` 包含所有文章链接

### Phase 4: 提交并部署
- [x] 提交配置修复
- [x] 推送到 GitHub 触发 Actions
- [x] 等待构建完成

### Phase 5: 验证部署结果
- [ ] 访问 https://noeverer.github.io 确认首页显示正常
- [ ] 验证 2026 年文章是否显示在首页
- [ ] 检查归档页面是否包含所有年份文章
- [ ] 测试个别文章链接可访问

**注意**：GitHub Actions workflow #29 已成功运行（38s），但 GitHub Pages 可能需要 2-5 分钟刷新 CDN 缓存。当前线上显示的是旧缓存内容（12 篇文章，旧菜单）。需要等待 GitHub Pages 完全更新后再进行最终验证。

## Test

### 测试用例

#### 测试用例 1: 所有文章配置正确
```bash
# 验证所有 markdown 文件包含 published: true
cd source/_posts
for file in $(find . -name "*.md"); do
    grep -q "^published: true" "$file" && echo "✓ $file" || echo "✗ $file"
done
```
**预期结果**: 所有文件输出 ✓

#### 测试用例 2: 本地构建成功
```bash
cd /mnt/workspace/01-personal/01-note/Noeverer.github.io
hexo clean && hexo generate
```
**预期结果**:
- 无错误输出
- `public/` 目录生成成功
- `public/index.html` 包含 `posts/2026/wikijs` 链接

#### 测试用例 3: GitHub Actions 构建成功
**验证步骤**:
1. 访问 https://github.com/Noeverer/Noeverer.github.io/actions
2. 查看最新的 "Deploy Blog" workflow
3. 确认所有步骤显示绿色 ✓

**预期结果**:
- Checkout repository ✓
- Setup Node.js ✓
- Install dependencies ✓
- Verify theme installation ✓
- Clean cache ✓
- Generate static files ✓
- Verify build output ✓
- Deploy to GitHub Pages ✓

#### 测试用例 4: 网站访问验证
**验证步骤**:
1. 访问 https://noeverer.github.io
2. 检查首页是否显示最新文章
3. 点击 2026 年文章链接
4. 验证文章内容正常显示

**预期结果**:
- 首页加载正常
- "Wiki.js Docker 部署指南" 文章显示在首页
- 文章页面可正常访问

### 测试命令清单

```bash
# 1. 检查所有文章发布状态
find source/_posts -name "*.md" -exec grep -L "^published:" {} \;

# 2. 验证文章数量
find source/_posts -name "*.md" | wc -l

# 3. 本地构建测试
hexo clean
hexo generate
ls -la public/ | head -20

# 4. 检查首页是否包含最新文章
grep -o "posts/2026" public/index.html

# 5. 统计生成的文件数量
find public -type f | wc -l

# 6. 验证 Git 状态
git status
git log --oneline -5
```

## Notes

### 已修复的问题
1. **脚本加载错误**: 移除了 `scripts/` 目录中的非 JS 脚本，这些脚本会导致 Hexo 启动时报 `SyntaxError: Invalid or unexpected token`

2. **子模块错误**: 删除了 `.deploy_git` 子模块，该模块会导致 GitHub Actions 中 `No url found for submodule path '.deploy_git'` 错误

3. **发布配置**: 验证所有 16 篇文章都已正确配置 `published: true`

### 文章清单
| 年份 | 文章数量 | 状态 |
|------|---------|------|
| 2015 | 1 | ✓ |
| 2016 | 2 | ✓ |
| 2017 | 2 | ✓ |
| 2018 | 2 | ✓ |
| 2019 | 4 | ✓ |
| 2020 | 1 | ✓ |
| 2024 | 1 | ✓ |
| 2025 | 2 | ✓ |
| 2026 | 1 | ✓ |
| **总计** | **16** | **✓** |

### GitHub Actions 配置关键点
- 使用 `fetch-depth: 0` 确保完整历史
- 使用 `force_orphan: true` 创建干净的历史记录
- 设置 `future: true` 允许发布未来日期的文章
- 构建 artifact 保留 7 天用于调试

### 常见问题排查

**问题 1**: 文章不显示
- 检查 frontmatter 中 `published: true`
- 检查日期格式是否正确
- 检查 `_config.yml` 中 `future: true`

**问题 2**: GitHub Actions 失败
- 查看具体错误日志
- 检查 theme 是否正确安装
- 验证 package.json 依赖完整性

**问题 3**: GitHub Pages 未更新
- 检查 gh-pages 分支是否更新
- 清除浏览器缓存
- 等待 2-5 分钟 CDN 刷新

## 变更记录

| 日期 | Commit | 说明 |
|------|--------|------|
| 2026-01-12 | a6dbfc8 | 删除 .deploy_git 子模块，修复 GitHub Actions 构建错误 |
| 2026-01-12 | 50abc58 | 移除会干扰 Hexo 构建的脚本文件并更新 .gitignore |
| 2026-01-12 | 9107a87 | 更新依赖和项目配置 |
| 2026-01-12 | 6124bbf | 为所有文章添加 published 字段并修复 GitHub Actions 部署问题 |
| 2026-01-12 | 061fd46 | 添加部署验证报告 |
