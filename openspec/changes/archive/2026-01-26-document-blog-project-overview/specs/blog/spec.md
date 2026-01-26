# 博客项目规范

## 项目概述

这是一个基于 Hexo + Butterfly 主题的博客项目，部署在 GitHub Pages 上，通过 GitHub Actions 自动部署，实现了本地写作、自动发布的便捷流程。

## 功能规范

### 自动化工作流
- 本地专注写作，推送后自动发布
- 验证配置、本地测试构建等功能
- 完整的故障排除指南

### 技术架构
- **框架**: Hexo (基于 Node.js)
- **主题**: Butterfly v5.5.3
- **部署**: GitHub Actions + GitHub Pages
- **辅助工具**: npm, Docker (用于 Wiki.js)

### 内容管理
- 文章使用 Markdown 格式编写
- 使用 Front Matter 管理文章元数据（标题、日期、标签、分类等）
- 按年份组织文章文件

### 部署机制
- 代码推送到 `master` 分支后自动触发构建
- 运行 `hexo clean` 和 `hexo generate` 生成静态网站
- 验证构建输出并部署到 `gh-pages` 分支

## 场景

#### 场景: 发布新文章
当作者完成一篇新文章后：
1. 将文章以 Markdown 格式保存到 `source/_posts/` 目录
2. 提交并推送代码到 GitHub 仓库
3. GitHub Actions 自动构建并部署到 GitHub Pages
4. 1-2 分钟后可在公开网站查看新文章

#### 场景: 更新配置
当需要更新博客配置时：
1. 修改 `_config.yml` 或 `_config.butterfly.yml` 文件
2. 推送更改到 GitHub 仓库
3. GitHub Actions 自动应用新配置并重建网站

#### 场景: 维护主题
当需要更新主题时：
1. 更新 `hexo-theme-butterfly` 依赖
2. 检查主题更新对现有内容的影响
3. 推送更改并验证网站显示正常