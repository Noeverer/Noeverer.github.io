# Hexo博客迁移部署完整指南

## 📋 目录
1. [方案概述](#方案概述)
2. [文件结构](#文件结构)
3. [从HTML迁移到Markdown](#从html迁移到markdown)
4. [本地开发](#本地开发)
5. [GitHub自动部署配置](#github自动部署配置)
6. [日常维护](#日常维护)

---

## 方案概述

本项目采用 **GitHub Actions 自动部署方案**：

### 工作流程

```
本地编辑 (Markdown) → 推送GitHub → Actions自动构建 → 部署到GitHub Pages
```

### 优势
- ✅ 只需推送源文件（Markdown），仓库体积小
- ✅ GitHub Actions自动编译，无需本地构建
- ✅ 支持在GitHub上直接编辑文章
- ✅ 自动部署，效率高
- ✅ 支持版本控制

---

## 文件结构

### 推荐的项目结构

```
Noeverer.github.io/              # GitHub仓库根目录
├── source/                      # 源文件目录
│   └── _posts/                 # Markdown文章
│       ├── 2019-05-04-hello-world.md
│       └── 2024-01-01-new-post.md
├── themes/                      # Hexo主题（如果有自定义）
├── public/                      # 生成的静态文件（不提交）
├── _config.yml                 # Hexo配置
├── package.json                # npm依赖配置
├── .github/workflows/          # GitHub Actions
│   └── deploy.yml              # 自动部署工作流
├── html2md.py                  # HTML转Markdown工具
├── deploy.sh                   # 本地部署脚本
├── .gitignore                  # Git忽略文件
└── README.md                   # 项目说明
```

### 分支策略

| 分支 | 用途 | 说明 |
|------|------|------|
| `main` | 源码分支 | 存放Markdown、配置文件等源码 |
| `gh-pages` | 部署分支 | 存放生成的HTML/CSS/JS，由Actions自动管理 |

**注意**：`gh-pages` 分支完全由GitHub Actions自动管理，不要手动修改。

---

## 从HTML迁移到Markdown

### 步骤1：安装Python依赖

```bash
pip install beautifulsoup4 lxml
```

### 步骤2：运行转换脚本

```bash
python3 html2md.py
```

### 步骤3：检查生成的Markdown

转换后的文件保存在 `source/_posts/` 目录：

```
source/_posts/
├── 2019-05-04-My-First-Blog.md
├── 2019-05-05-Problem-Encounted-in-Blogging.md
├── 2021-07-24-blog定位说明.md
└── ...
```

### 步骤4：手动调整（可选）

由于HTML到Markdown的转换是近似的，可能需要手动调整：

1. **检查文章内容**：确保内容完整
2. **修复代码块**：代码格式可能需要调整
3. **更新图片路径**：确保图片链接正确
4. **调整Front Matter**：修改标题、标签等元数据

### 示例：Markdown文章格式

```markdown
---
title: blog定位说明
date: 2021-07-24 15:35:25
tags: ["work"]
categories: work
description: 本文主要阐述本站想建成可以有交流，有划水，可以随时添加工具
---

# 本文主要阐述

本站想建成可以：

1. 有交流，有划水
2. 可以随时添加工具或者上传文件，下载文件
3. 可以添加人员

## 功能说明

...
```

---

## 本地开发

### 初始化项目

```bash
# 进入项目目录
cd /mnt/workspace/01-personal/01-note/Noeverer.github.io

# 安装依赖
npm install

# 启动本地服务器
hexo server
# 或
npm run server
```

访问 http://localhost:4000 预览博客。

### 常用命令

```bash
# 新建文章
hexo new "文章标题"
# 生成的文件在 source/_posts/ 目录

# 清理缓存和生成的文件
hexo clean

# 生成静态文件
hexo generate

# 本地预览
hexo server

# 部署（不推荐，使用GitHub Actions）
hexo deploy
```

---

## GitHub自动部署配置

### 1. 创建GitHub仓库

确保仓库名为：`username.github.io`（你的GitHub用户名）

### 2. 设置GitHub Pages

1. 进入仓库 **Settings** → **Pages**
2. **Source** 选择 **Deploy from a branch**
3. **Branch** 选择 `gh-pages`，目录 `/root`
4. 点击 **Save**

### 3. 配置GitHub Actions

已创建的 `.github/workflows/deploy.yml` 会自动工作，无需额外配置。

### 4. 首次部署

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加远程仓库
git remote add origin https://github.com/Noeverer/Noeverer.github.io.git

# 添加所有文件
git add .

# 提交
git commit -m "初始化Hexo博客"

# 推送到main分支
git push -u origin main
```

### 5. 查看部署状态

1. 进入仓库的 **Actions** 标签
2. 查看工作流运行状态
3. 等待约1-2分钟，工作流完成后访问 https://noeverer.github.io

---

## 日常维护

### 新增文章

```bash
# 创建新文章
hexo new "新文章标题"

# 编辑Markdown文件
vim source/_posts/2024-01-01-新文章标题.md

# 提交到GitHub
git add source/_posts/
git commit -m "新增文章: 新文章标题"
git push origin main
```

等待Actions自动部署完成即可。

### 修改现有文章

```bash
# 编辑Markdown文件
vim source/_posts/2021-07-24-blog定位说明.md

# 提交更改
git add source/_posts/
git commit -m "修改文章: blog定位说明"
git push origin main
```

### 添加图片

1. 将图片放到 `source/images/` 或使用外部图床
2. 在Markdown中引用图片：

```markdown
![图片描述](/images/example.png)
```

### 配置修改

修改 `_config.yml` 后提交：

```bash
git add _config.yml
git commit -m "更新配置"
git push origin main
```

---

## .gitignore 说明

确保提交正确的文件：

```gitignore
# 忽略Node.js依赖
node_modules/

# 忽略生成的文件
public/
.deploy/

# 忽略日志
*.log

# 但保留源文件
!source/_posts/
```

---

## 故障排查

### 问题1：Actions部署失败

**检查方法**：
1. 进入仓库 **Actions** 标签查看错误日志
2. 常见原因：
   - `package.json` 缺少依赖
   - Markdown文件格式错误
   - GitHub Token权限问题

**解决方法**：
```bash
# 本地测试构建
hexo clean
hexo generate

# 如果成功，检查Actions配置
```

### 问题2：本地预览正常，线上404

**检查配置**：
```yaml
# _config.yml
url: https://noeverer.github.io
root: /
```

### 问题3：图片显示不正常

确保图片路径正确：
- 相对路径：`/images/example.png`
- 或使用CDN/图床

---

## 总结

### 完整工作流程

```mermaid
graph LR
    A[本地编辑Markdown] --> B[git add & commit]
    B --> C[git push to main]
    C --> D[GitHub Actions触发]
    D --> E[hexo generate]
    E --> F[部署到gh-pages]
    F --> G[GitHub Pages发布]
```

### 关键点

1. **只推送源文件**到 `main` 分支
2. **不要手动修改** `gh-pages` 分支
3. **检查Actions状态**确保部署成功
4. **本地测试**后再推送

---

**最后更新**: 2024
**作者**: Ante Liu
