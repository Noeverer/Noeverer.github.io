# GitHub Actions 自动部署指南

本文档详细说明如何使用 GitHub Actions 自动部署 Hexo 博客到 GitHub Pages。

---

## 🎯 工作流程概述

```
本地编写文章 → git push → GitHub Actions 自动构建 → 部署到 GitHub Pages
```

---

## 📋 部署架构

```
┌─────────────────┐
│  master 分支     │  ← 存放源代码、文章、配置
├─────────────────┤
│  gh-pages 分支   │  ← 存放生成的静态网站（自动管理）
└─────────────────┘
```

- **master 分支**：保存所有源文件（文章、配置、资源）
- **gh-pages 分支**：由 GitHub Actions 自动生成和管理，无需手动操作

---

## ⚙️ GitHub Actions 配置文件

位置：`.github/workflows/deploy.yml`

### 完整配置说明

```yaml
name: Deploy Blog  # 工作流名称

on:  # 触发条件
  push:
    branches: [ master ]  # 推送到 master 分支时触发
  workflow_dispatch:     # 支持手动触发

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest  # 运行环境

    steps:  # 执行步骤

      # 1. 检出代码
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 2. 设置 Node.js 环境
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      # 3. 安装依赖
      - name: Install dependencies
        run: |
          npm install hexo-cli -g
          npm install

      # 4. 构建站点
      - name: Build site
        run: |
          hexo clean
          hexo generate

      # 5. 验证构建结果
      - name: Verify build output
        run: |
          echo "Checking if index.html exists..."
          ls -la public/
          if [ ! -f "public/index.html" ]; then
            echo "Error: index.html not found!"
            exit 1
          fi
          echo "✅ Build successful, index.html exists"

      # 6. 部署到 GitHub Pages
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          publish_branch: gh-pages
          force_orphan: true
          user_name: 'github-actions[bot]'
          user_email: 'github-actions[bot]@users.noreply.github.com'

      # 7. 部署摘要
      - name: Deployment summary
        if: success()
        run: |
          echo "✅ Deployment successful!"
          echo "🌐 https://noeverer.github.io"
```

---

## 🚀 使用方式

### 自动部署（推荐）

1. 本地创建/编辑文章

```bash
hexo new "文章标题"
```

2. 编辑文章内容

```bash
vim source/_posts/文章标题.md
```

3. 提交并推送

```bash
git add .
git commit -m "发布新文章"
git push origin master
```

4. GitHub Actions 自动执行：
   - 检出代码
   - 安装依赖
   - 构建站点
   - 部署到 GitHub Pages

5. 等待 1-2 分钟后访问：https://noeverer.github.io

### 手动触发部署

在 GitHub 仓库页面：

1. 进入 **Actions** 标签
2. 选择 **Deploy Blog** 工作流
3. 点击 **Run workflow** 按钮
4. 选择 master 分支
5. 点击绿色 **Run workflow** 按钮

---

## 🔍 查看部署状态

### 1. 查看工作流执行状态

**位置：** 仓库首页 → Actions 标签

- ✅ 绿色勾：部署成功
- ❌ 红色叉：部署失败
- 🔄 蓝色圆：正在执行

### 2. 查看详细日志

点击具体的工作流运行记录，可以看到：
- 每个步骤的执行时间
- 详细输出日志
- 错误信息（如果失败）

### 3. 部署历史

每次成功部署都会创建一个标签：

```bash
git tag -l
# 输出示例：
# deploy-20260107-103045
# deploy-20260107-123045
```

---

## ⚠️ 常见问题排查

### 1. 部署失败：404 File not found

**原因：** GitHub Pages 设置不正确

**解决方法：**

1. 进入仓库 **Settings** → **Pages**
2. 确认以下设置：
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages` 和 `/ (root)`
   - **Custom domain**: 如果没有域名，此项留空

3. 检查 `.nojekyll` 文件是否存在

```bash
ls -la .nojekyll
```

如果不存在，创建它：

```bash
touch .nojekyll
git add .nojekyll
git commit -m "Add .nojekyll file"
git push
```

### 2. 部署失败：npm install 错误

**原因：** Node.js 版本不兼容或网络问题

**解决方法：**

1. 检查 `package.json` 中的依赖版本
2. 确认工作流中 Node.js 版本正确（当前使用 18）
3. 如遇网络问题，可等待几分钟后重试

### 3. 构建失败：hexo generate 错误

**原因：** 配置文件语法错误或文章格式错误

**解决方法：**

1. 本地运行构建命令验证：

```bash
hexo clean
hexo generate
```

2. 检查 `_config.yml` 和 `_config.butterfly.yml` 语法
3. 检查文章的 Front Matter 格式

### 4. 图片加载失败

**原因：** 图片路径不正确

**解决方法：**

1. 确认图片在正确位置：

```bash
ls -la img/
```

2. 检查配置文件中的路径：

```yaml
# 正确格式
avatar:
  img: /img/monkey.jpg
```

3. 图片路径规则：
   - 绝对路径：`/img/xxx.jpg` - 从根目录读取
   - 相对路径：`images/xxx.jpg` - 从 source 目录读取

### 5. 更新后网站未变化

**原因：** 缓存问题

**解决方法：**

1. 浏览器强制刷新（Ctrl + Shift + R）
2. 清除浏览器缓存
3. 等待 1-2 分钟让 GitHub Pages 完成部署

---

## 🔧 工作流自定义

### 修改 Node.js 版本

编辑 `.github/workflows/deploy.yml`：

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'  # 修改为你需要的版本
```

### 添加部署通知

在部署成功后添加通知步骤：

```yaml
- name: Notify deployment
  if: success()
  run: |
    echo "Deployment completed successfully"
    # 可以添加邮件、Slack 等通知
```

### 修改部署分支

如果需要部署到其他分支：

```yaml
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v4
  with:
    publish_branch: your-branch-name  # 修改分支名
```

---

## 📊 工作流优化建议

### 1. 减少构建时间

- 使用 `cache: 'npm'` 缓存依赖（已配置）
- 减少 `fetch-depth`（如果不需要完整 git 历史）

### 2. 增加构建验证

已在配置中添加 `Verify build output` 步骤，确保构建产物正确

### 3. 分环境部署

可创建多个工作流：
- `deploy-prod.yml` - 生产环境
- `deploy-dev.yml` - 开发环境

### 4. 自动测试

在部署前添加测试步骤：

```yaml
- name: Run tests
  run: |
    # 添加你的测试命令
```

---

## 📖 相关资源

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [peaceiris/actions-gh-pages](https://github.com/peaceiris/actions-gh-pages)
- [GitHub Pages 官方文档](https://docs.github.com/en/pages)

---

## 💡 最佳实践

1. **本地预览后再推送**：使用 `hexo server` 预览效果
2. **定期检查 Actions 日志**：及时发现潜在问题
3. **保持依赖更新**：定期更新 npm 包
4. **备份配置**：重要配置添加到版本控制
5. **监控网站状态**：使用 Uptime 监控网站可用性

---

## 🔄 完整工作流程示例

```bash
# 1. 创建新文章
hexo new "我的新文章"

# 2. 编辑文章
vim source/_posts/我的新文章.md

# 3. 本地预览（可选）
hexo server
# 访问 http://localhost:4000

# 4. 提交更改
git add .
git commit -m "发布新文章：我的新文章"
git push origin master

# 5. GitHub Actions 自动执行
# 访问 https://github.com/Noeverer/Noeverer.github.io/actions 查看进度

# 6. 等待部署完成（约 1-2 分钟）
# 访问 https://noeverer.github.io 查看效果
```
