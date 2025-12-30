# Ante Liu's Hexo Blog

基于Hexo的个人博客，使用GitHub Actions自动部署。

## 📁 项目结构

```
Noeverer.github.io/
├── source/              # 博客源文件（Markdown）
│   └── _posts/         # 文章目录
├── themes/             # Hexo主题
├── _config.yml         # Hexo配置文件
├── package.json        # 项目依赖
├── .github/workflows/  # GitHub Actions配置
│   └── deploy.yml      # 自动部署工作流
├── html2md.py          # HTML转Markdown工具
└── deploy.sh           # 本地部署脚本
```

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 本地开发

```bash
# 启动本地服务器
hexo server
# 或使用 npm
npm run server

# 访问 http://localhost:4000
```

### 3. 新建文章

```bash
hexo new "文章标题"
# 或
npm run new "文章标题"
```

### 4. 构建部署

本地构建（不推荐，推荐使用GitHub Actions）：
```bash
hexo clean
hexo generate
```

## 🔄 工作流程

### 方案一：GitHub Actions自动部署（推荐）

**流程说明：**
1. 在本地创建/编辑Markdown文章（存放在 `source/_posts/` 目录）
2. 使用Git推送到GitHub的 `main` 分支
3. GitHub Actions自动触发，执行：
   - 安装依赖
   - 生成静态文件（`hexo generate`）
   - 部署到 `gh-pages` 分支
4. GitHub Pages自动从 `gh-pages` 分支发布网站

**命令：**
```bash
# 添加所有更改
git add .

# 提交
git commit -m "新增文章: xxx"

# 推送到GitHub
git push origin main
```

等待约1-2分钟，访问 https://noeverer.github.io 即可看到更新。

### 方案二：HTML转Markdown迁移

如果你有现有的HTML文章，使用以下脚本转换为Markdown：

```bash
# 安装Python依赖
pip install beautifulsoup4

# 运行转换脚本
python3 html2md.py
# 或
npm run migrate
```

转换后的Markdown文件会保存到 `source/_posts/` 目录。

## 📝 文章格式

每篇文章需要包含Front Matter：

```markdown
---
title: 文章标题
date: 2024-01-01 12:00:00
tags: [标签1, 标签2]
categories: 分类
description: 文章描述
---

这里是文章内容...
```

## 🛠️ 常用命令

```bash
# 新建文章
hexo new "文章名"

# 清理缓存
hexo clean

# 生成静态文件
hexo generate

# 启动本地服务器
hexo server

# 部署（如需要）
hexo deploy
```

## ⚙️ GitHub Pages设置

1. 进入仓库 **Settings** → **Pages**
2. **Source** 选择 **Deploy from a branch**
3. **Branch** 选择 `gh-pages`，目录选择 `/root`
4. 保存设置

## 🔍 从HTML迁移

### 步骤说明

1. **放置HTML文件**：将原有的HTML文件放在项目根目录

2. **运行转换脚本**：
   ```bash
   python3 html2md.py
   ```

3. **检查生成的Markdown文件**：
   - 查看生成的 `source/_posts/` 目录
   - 检查文章内容和格式
   - 手动调整需要的部分

4. **提交到GitHub**：
   ```bash
   git add source/_posts/
   git commit -m "从HTML迁移文章"
   git push origin main
   ```

5. **等待自动部署**：GitHub Actions会自动构建并发布

### 注意事项

- HTML到Markdown的转换是近似转换，可能需要手动调整
- 图片路径可能需要更新
- 代码块格式可能需要调整
- 建议逐篇检查转换后的文章

## 📌 分支策略

- **main**：存放源文件（Markdown、配置文件等）
- **gh-pages**：存放生成的静态文件（HTML、CSS、JS），由GitHub Actions自动生成

**注意**：不需要手动推送到 `gh-pages` 分支，完全由Actions自动处理。

## 🔗 访问链接

- 博客地址：https://noeverer.github.io
- GitHub仓库：https://github.com/Noeverer/Noeverer.github.io

## ❓ 常见问题

### Q: 部署后没有更新？
A: 检查GitHub Actions是否运行成功，等待2-3分钟后刷新页面。

### Q: 本地预览正常，但线上不正常？
A: 可能是路径问题，检查 `_config.yml` 中的 `url` 和 `root` 配置。

### Q: 如何添加主题？
A: 将主题放到 `themes/` 目录，并在 `_config.yml` 中设置 `theme` 字段。

---

**Author**: Ante Liu
**Last Updated**: 2024
