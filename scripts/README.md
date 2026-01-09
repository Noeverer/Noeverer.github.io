# 博客验证和测试脚本

本目录包含用于验证和测试 Hexo 博客的脚本。

## 脚本说明

### 1. verify-blog.sh - 博客配置验证

验证博客配置和文件是否正确。

```bash
npm run verify
# 或
bash scripts/verify-blog.sh
```

**检查内容：**
- 必要文件是否存在（_config.yml, package.json 等）
- 依赖是否正确安装（hexo, butterfly 主题等）
- 源文件目录结构是否正确
- 所有 markdown 文件是否有正确的 front matter
- Hexo 配置是否正确
- .gitignore 配置是否正确
- Git 仓库配置是否正确
- 当前分支是否正确

### 2. local-test-build.sh - 本地构建测试

模拟 GitHub Actions 构建过程，在本地测试构建是否成功。

```bash
npm run test-build
# 或
bash scripts/local-test-build.sh
```

**执行步骤：**
1. 显示环境信息
2. 检查依赖（如未安装则自动安装）
3. 检查主题
4. 清理 Hexo 缓存
5. 生成静态文件
6. 验证构建输出
7. 检查文章页面
8. 检查分类和标签页面
9. 显示构建摘要
10. 可选：启动本地服务器

## 使用流程

### 1. 首次设置

```bash
# 1. 安装依赖
npm install

# 2. 验证配置
npm run verify

# 3. 本地测试构建
npm run test-build
```

### 2. 日常开发

```bash
# 1. 创建新文章
npm run new "文章标题"

# 2. 编辑文章（在 source/_posts/ 目录下）

# 3. 本地预览
npm run dev
# 访问 http://localhost:4000

# 4. 提交更改
git add .
git commit -m "Update blog"
git push origin master
```

### 3. 部署到 GitHub Pages

推送更改到 `master` 分支后，GitHub Actions 会自动：
1. 清理缓存
2. 安装依赖
3. 生成静态文件
4. 验证构建输出
5. 部署到 `gh-pages` 分支
6. 发布到 https://noeverer.github.io

## 故障排除

### 构建失败

如果构建失败，运行以下命令：

```bash
# 1. 清理缓存
npm run clean

# 2. 重新安装依赖
rm -rf node_modules package-lock.json
npm install

# 3. 验证配置
npm run verify

# 4. 本地测试构建
npm run test-build
```

### Front Matter 错误

如果文章因为缺少 front matter 而无法发布，检查：

```bash
# 所有文章必须有以下格式：
---
title: 文章标题
date: YYYY-MM-DD HH:mm:ss
tags: ["标签1", "标签2"]
categories: 分类
description: 文章描述
---

文章内容...
```

### 主题未加载

如果主题未正确加载：

```bash
# 检查主题是否安装
ls node_modules/hexo-theme-butterfly

# 重新安装主题
npm install hexo-theme-butterfly
```

## GitHub Actions 工作流

工作流文件：`.github/workflows/deploy.yml`

**触发条件：**
- 推送到 `master` 分支
- 手动触发（workflow_dispatch）

**部署步骤：**
1. 检出代码
2. 设置 Node.js 环境
3. 安装依赖
4. 验证主题安装
5. 清理缓存
6. 生成静态文件
7. 验证构建输出
8. 上传构建产物
9. 部署到 gh-pages 分支
10. 显示部署摘要

**权限：**
- 需要 `contents: write` 权限来写入 gh-pages 分支

## 有用的命令

```bash
# 清理缓存
npm run clean
# 或
npx hexo clean

# 生成静态文件
npm run build
# 或
npx hexo generate

# 启动本地服务器
npm run server
# 或
npx hexo server

# 创建新文章
npm run new "文章标题"
# 或
npx hexo new "文章标题"

# 验证配置
npm run verify

# 本地测试构建
npm run test-build

# 开发模式（清理 + 生成 + 启动服务器）
npm run dev
```

## 部署状态

查看 GitHub Actions 部署状态：
- 访问：https://github.com/Noeverer/Noeverer.github.io/actions
- 查看 "Deploy Blog" 工作流

## 访问博客

- 本地预览：http://localhost:4000
- 生产环境：https://noeverer.github.io
