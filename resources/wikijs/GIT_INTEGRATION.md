# Wiki.js 与 GitHub 集成配置指南

## 概述

本文档介绍如何配置 Wiki.js 的 Git 存储功能，以实现与 GitHub 仓库的双向同步。

## 准备工作

### 1. 创建 GitHub 仓库

首先，您需要创建一个专门用于存放 Wiki.js 内容的 GitHub 仓库：

1. 登录 GitHub
2. 创建新的仓库，例如 `wikijs-content`
3. 如果是私有仓库，需要生成访问令牌

### 2. 生成 Personal Access Token (PAT)

如果您使用私有仓库或需要写入权限：

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token"
3. 选择适当的权限：
   - `repo` - 用于访问仓库
   - `workflow` - 如果需要触发 GitHub Actions
4. 复制生成的令牌，稍后会用到

## 配置 Wiki.js Git 存储

### 1. 初始化 Wiki.js

首先，完成 Wiki.js 的初始设置：

1. 访问 `http://your-server:3000`
2. 完成初始配置向导
3. 登录管理员账户

### 2. 配置 Git 存储

1. 进入管理面板 (Admin Panel)
2. 导航到 Storage 部分
3. 点击 "Git" 存储类型
4. 填写以下配置：

```
STORAGE: Git
MODE: Read/Write
GIT URL: https://github.com/Noeverer/wikijs-content.git
BRANCH: main
AUTHENTICATION: HTTPS
USERNAME: your-github-username
PASSWORD / TOKEN: your-generated-token
COMMIT MERGE STRATEGY: Merge
SYNC INTERVAL: 300 (seconds)
LOCAL REPO PATH: /wiki/data/repo
```

5. 点击 "Install" 安装存储驱动
6. 点击 "Test" 验证连接
7. 点击 "Save" 保存配置

### 3. 配置 Git 选项

在 Git 存储配置中，还可以设置：

- Author Name: Wiki.js Bot
- Author Email: bot@noeverer.github.io
- Commit Message Template: 可自定义提交消息格式

## GitHub Actions 配置

GitHub Actions 将自动处理从 Git 仓库到 GitHub Pages 的部署：

### 工作流文件

GitHub Actions 工作流文件应位于 `.github/workflows/build-pages.yml`：

```yaml
name: Build Wiki GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install VitePress
        run: |
          npm install -D vitepress
          npm install

      - name: Build Site
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: .vitepress/dist
          cname: wiki.noeverer.github.io
```

## 验证集成

### 1. 测试 Git 同步

1. 在 Wiki.js 中创建一个新的页面
2. 等待同步间隔（默认5分钟）或手动触发同步
3. 检查 GitHub 仓库是否收到了新的 Markdown 文件

### 2. 测试 GitHub Actions

1. 手动推送一个变更到 GitHub 仓库
2. 检查 GitHub Actions 是否触发构建
3. 验证 GitHub Pages 是否更新

### 3. 监控同步状态

1. 在 Wiki.js 管理面板中查看存储日志
2. 检查 GitHub 仓库的提交历史
3. 监控 GitHub Pages 的更新

## 故障排除

### 常见问题

1. **Git 连接失败**:
   - 检查用户名和令牌是否正确
   - 确认令牌具有适当的权限
   - 验证仓库 URL 是否正确

2. **同步延迟**:
   - 检查同步间隔设置
   - 查看 Wiki.js 日志是否有错误
   - 确认网络连接正常

3. **GitHub Actions 失败**:
   - 检查工作流文件语法
   - 验证 Node.js 版本
   - 确认构建依赖是否正确

### 调试步骤

1. 检查 Wiki.js 日志:
   ```bash
   docker-compose logs -f wiki
   ```

2. 验证 Git 连接:
   ```bash
   # 进入 Wiki.js 容器
   docker exec -it wikijs /bin/sh
   
   # 检查本地仓库
   cd /wiki/data/repo
   git status
   git remote -v
   ```

3. 手动触发同步:
   - 在 Wiki.js 管理面板中找到存储设置
   - 点击同步按钮强制同步

## 最佳实践

1. **安全**:
   - 使用专用的 GitHub 用户名和令牌
   - 定期轮换访问令牌
   - 限制令牌的权限范围

2. **备份**:
   - 定期备份数据库
   - 保持 Git 仓库作为内容的主要备份

3. **监控**:
   - 定期检查同步日志
   - 监控 GitHub Pages 的可用性

## 维护

1. **定期更新**:
   - 保持 Wiki.js 镜像更新
   - 更新 GitHub Actions 工作流

2. **内容审核**:
   - 定期审查 Git 提交历史
   - 确保内容质量

通过以上配置，您可以实现 Wiki.js 与 GitHub Pages 的完全自动化联动部署。