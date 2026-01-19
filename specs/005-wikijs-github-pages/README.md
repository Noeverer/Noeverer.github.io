---
status: completed
created: '2026-01-14'
tags:
  - wikijs
  - github-pages
  - deployment
  - automation
priority: medium
created_at: '2026-01-14T00:00:00.000Z'
updated_at: '2026-01-14T12:00:00.000Z'
transitions:
  - status: completed
    at: '2026-01-14T12:00:00.000Z'
---

# Wiki.js 部署联动 GitHub Pages

> **Status**: 📋 Todo · **Priority**: Medium · **Created**: 2026-01-14 · **Tags**: wikijs, github-pages, deployment, automation

## Overview

将 Wiki.js 本地部署与 GitHub Pages 进行联动，实现知识库内容自动发布到 GitHub Pages 静态站点。

### 背景
- 当前已有本地部署的 Wiki.js 系统
- 需要将 Wiki.js 内容发布到 GitHub Pages
- 实现内容的双向同步
- 保持与现有 Hexo 博客的兼容性

### 目标
1. 在 Linux 服务器上部署 Wiki.js
2. 配置 Wiki.js 与 GitHub 仓库的 Git 存储
3. 设置 GitHub Actions 自动构建 GitHub Pages
4. 实现内容自动同步和发布
5. 配置域名和 HTTPS

### 非目标
- Wiki.js 的用户认证系统改造
- 复杂的内容格式转换
- 修改现有 Hexo 博客结构

## Design

### 1. 系统架构

```
┌─────────────────┐
│   Wiki.js       │ (Linux 本地部署)
│   localhost:3000│
│                 │
│   - 内容编辑     │
│   - 文档管理     │
│   - Git 存储     │
└────────┬────────┘
         │ Git Push
         ↓
┌─────────────────┐
│   GitHub        │
│   Wiki Content  │
│   Repository    │
│   (私有仓库)    │
└────────┬────────┘
         │ GitHub Actions
         ↓
┌─────────────────┐
│   GitHub Pages  │
│   静态 Wiki 站点 │
│   wiki.noeverer│
│   .github.io    │
└─────────────────┘
```

### 2. 技术选型

| 组件 | 技术方案 | 说明 |
|------|---------|------|
| Wiki.js | Docker 部署 | 易于管理和升级 |
| 数据库 | PostgreSQL 15 | 稳定可靠 |
| 静态站点生成 | VitePress | 轻量快速，Markdown 原生 |
| 反向代理 | Nginx | 提供访问入口 |
| 域名 | wiki.noeverer.github.io | GitHub Pages 子域名 |
| SSL | Let's Encrypt | 免费 HTTPS |

### 3. 仓库结构

```
Noeverer.github.io/          # 现有 Hexo 博客
├── source/
├── _config.butterfly.yml
└── ...

wikijs-content/             # Wiki.js 内容仓库（新建）
├── .github/
│   └── workflows/
│       └── build-pages.yml # GitHub Actions 工作流
├── docs/                   # Wiki 内容目录
│   ├── index.md
│   ├── programming/
│   ├── study/
│   └── ...
├── .vitepress/             # VitePress 配置
│   ├── config.ts
│   └── theme/
└── README.md

wikijs-deploy/              # 本地部署配置（新建）
├── docker-compose.yml
├── nginx/
│   └── wikijs.conf
└── backup/
    └── backup.sh
```

### 4. Wiki.js Git 存储配置

```yaml
存储标识符: github-wiki
存储模式: 读写
Git URL: https://github.com/Noeverer/Noeverer.github.io.git
分支: master
验证方式: HTTPS
用户名: Noeverer
密码: [PAT Token]
同步间隔: 5 分钟
本地仓库路径: /wiki/data/repo
```

### 5. GitHub Pages 工作流

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

### 6. VitePress 配置

```typescript
// .vitepress/config.ts
export default {
  title: 'Ante\'s Wiki',
  description: '知识库文档',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '编程', link: '/programming/' },
      { text: '学习', link: '/study/' },
    ],
    sidebar: [
      {
        text: '编程',
        items: [
          { text: 'Python', link: '/programming/python.md' },
        ]
      },
      {
        text: '学习',
        items: [
          { text: '学习笔记', link: '/study/notes.md' },
        ]
      }
    ]
  }
}
```

## Plan

### Phase 1: 本地环境准备（1天）
- [ ] 在 Linux 服务器安装 Docker 和 Docker Compose
- [ ] 准备 PostgreSQL 数据库
- [ ] 创建必要的目录结构
- [ ] 配置 Nginx 反向代理

### Phase 2: Wiki.js 部署（1天）
- [ ] 创建 docker-compose.yml 配置
- [ ] 启动 Wiki.js 容器
- [ ] 完成 Wiki.js 初始化配置
- [ ] 测试访问和管理界面
- [ ] 配置管理员账户

### Phase 3: GitHub 仓库设置（0.5天）
- [ ] 创建 wikijs-content 仓库
- [ ] 生成 GitHub Personal Access Token
- [ ] 初始化 VitePress 项目结构
- [ ] 配置 VitePress 基本设置

### Phase 4: Wiki.js Git 存储配置（0.5天）
- [ ] 在 Wiki.js 管理界面配置 Git 存储
- [ ] 验证 Git 连接和权限
- [ ] 测试内容推送
- [ ] 测试内容拉取

### Phase 5: GitHub Actions 配置（0.5天）
- [ ] 创建 GitHub Actions 工作流文件
- [ ] 配置自动构建和部署
- [ ] 测试工作流执行
- [ ] 验证 GitHub Pages 访问

### Phase 6: 域名和 SSL 配置（0.5天）
- [ ] 配置 GitHub Pages 自定义域名
- [ ] 添加 DNS 记录（如需要）
- [ ] 配置 HTTPS
- [ ] 测试域名访问

### Phase 7: 测试和优化（1天）
- [ ] 端到端测试内容同步流程
- [ ] 验证双向同步功能
- [ ] 测试访问速度和稳定性
- [ ] 配置备份策略
- [ ] 编写使用文档

## Test

### 测试用例 1: Wiki.js 本地访问
**测试步骤**:
1. 启动 Wiki.js 服务
2. 访问 http://your-server:3000
3. 验证管理员登录
4. 创建测试文章

**预期结果**:
- [ ] Wiki.js 界面正常显示
- [ ] 可以成功登录
- [ ] 可以创建和编辑文章

### 测试用例 2: Git 推送测试
**测试步骤**:
1. 在 Wiki.js 创建新文章
2. 手动触发 Git 同步
3. 检查 GitHub 仓库是否更新

**预期结果**:
- [ ] 文章成功推送到 GitHub
- [ ] Markdown 文件格式正确
- [ ] 文件路径符合预期

### 测试用例 3: GitHub Actions 构建测试
**测试步骤**:
1. 推送更新到 GitHub
2. 查看 Actions 执行状态
3. 验证构建成功

**预期结果**:
- [ ] Actions 执行成功
- [ ] 构建无错误
- [ ] 部署到 GitHub Pages

### 测试用例 4: GitHub Pages 访问测试
**测试步骤**:
1. 访问 https://wiki.noeverer.github.io
2. 浏览不同页面
3. 检查导航和链接

**预期结果**:
- [ ] 站点正常加载
- [ ] 所有页面可访问
- [ ] 样式显示正确
- [ ] HTTPS 有效

### 测试用例 5: 内容同步延迟测试
**测试步骤**:
1. 在 Wiki.js 修改文章
2. 记录修改时间
3. 等待 GitHub Actions 执行
4. 检查 GitHub Pages 更新时间

**预期结果**:
- [ ] 同步延迟 < 10 分钟
- [ ] 内容完整更新
- [ ] 无数据丢失

### 测试用例 6: 回滚测试
**测试步骤**:
1. 在 Wiki.js 修改文章
2. 在 GitHub 仓库回滚提交
3. 等待同步

**预期结果**:
- [ ] 回滚成功
- [ ] Wiki.js 内容更新
- [ ] GitHub Pages 同步回滚

## Implementation

### 1. Docker Compose 配置

```yaml
# wikijs-deploy/docker-compose.yml
version: '3.8'

services:
  wiki-db:
    image: postgres:15-alpine
    container_name: wikijs-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: wikijs
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: wikijs
    volumes:
      - wiki-db-data:/var/lib/postgresql/data
    networks:
      - wiki-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U wikijs"]
      interval: 10s
      timeout: 5s
      retries: 5

  wiki:
    image: ghcr.io/requarks/wiki:2
    container_name: wikijs
    restart: unless-stopped
    depends_on:
      wiki-db:
        condition: service_healthy
    environment:
      DB_TYPE: postgres
      DB_HOST: wiki-db
      DB_PORT: 5432
      DB_USER: wikijs
      DB_PASS: ${DB_PASSWORD}
      DB_NAME: wikijs
      NODE_ENV: production
    ports:
      - "3000:3000"
    volumes:
      - wiki-data:/wiki/data/repo
    networks:
      - wiki-network
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  wiki-db-data:
  wiki-data:

networks:
  wiki-network:
    driver: bridge
```

### 2. Nginx 配置

```nginx
# wikijs-deploy/nginx/wikijs.conf
server {
    listen 80;
    server_name wiki.yourdomain.com;  # 替换为你的域名

    client_max_body_size 50m;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 3. 环境变量文件

```bash
# wikijs-deploy/.env
DB_PASSWORD=your_secure_password_here
```

### 4. 部署脚本

```bash
#!/bin/bash
# wikijs-deploy/deploy.sh

set -e

echo "=== 部署 Wiki.js ==="

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "错误: .env 文件不存在"
    echo "请先复制 .env.example 并配置密码"
    exit 1
fi

# 创建目录
mkdir -p backup logs

# 备份现有数据（如果存在）
if [ -d "wiki-data" ]; then
    echo "备份现有数据..."
    tar -czf backup/wiki-data-$(date +%Y%m%d-%H%M%S).tar.gz wiki-data
fi

# 启动服务
echo "启动 Docker 容器..."
docker-compose up -d

# 等待服务就绪
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

echo "=== 部署完成 ==="
echo "访问地址: http://your-server:3000"
echo "查看日志: docker-compose logs -f"
```

### 5. 备份脚本

```bash
#!/bin/bash
# wikijs-deploy/backup/backup.sh

set -e

BACKUP_DIR="/path/to/backup"
DATE=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="wikijs-db"
DB_USER="wikijs"
DB_NAME="wikijs"

mkdir -p "$BACKUP_DIR"

echo "=== 开始备份 ($DATE) ==="

# 备份数据库
echo "备份数据库..."
docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/db_backup_$DATE.sql"

# 备份 Wiki 数据
echo "备份 Wiki 数据..."
docker run --rm -v wikijs_wiki-data:/data -v "$BACKUP_DIR:/backup" alpine tar czf "/backup/wiki_data_$DATE.tar.gz" -C /data .

# 删除 7 天前的备份
echo "清理旧备份..."
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "=== 备份完成 ==="
ls -lh "$BACKUP_DIR"/*$DATE.*
```

### 6. VitePress 初始化脚本

```bash
#!/bin/bash
# 在 wikijs-content 仓库中执行

# 安装 VitePress
npm init -y
npm install -D vitepress
npx vitepress init

# 创建目录结构
mkdir -p docs/programming
mkdir -p docs/study
mkdir -p docs/life

# 创建首页
cat > docs/index.md << 'EOF'
---
layout: home

hero:
  name: "Ante's Wiki"
  text: "个人知识库"
  tagline: "记录、整理、分享"
  actions:
    - theme: brand
      text: 开始阅读
      link: /programming/
    - theme: alt
      text: 在 GitHub 查看
      link: https://github.com/Noeverer/wikijs-content
---

## 欢迎

这是我的个人知识库，使用 Wiki.js 管理内容，通过 GitHub Actions 自动发布。
EOF

echo "VitePress 初始化完成"
```

### 7. package.json

```json
{
  "name": "wikijs-content",
  "version": "1.0.0",
  "description": "Wiki.js content for GitHub Pages",
  "scripts": {
    "dev": "vitepress dev",
    "build": "vitepress build",
    "preview": "vitepress preview"
  },
  "devDependencies": {
    "vitepress": "^1.0.0"
  }
}
```

## Test Command Checklist

```bash
# 1. 本地部署 Wiki.js
cd ~/wikijs-deploy
cp .env.example .env
# 编辑 .env 设置密码
nano .env
./deploy.sh

# 2. 检查容器状态
docker-compose ps
docker-compose logs -f wiki

# 3. 测试访问
curl -I http://localhost:3000

# 4. 备份数据
./backup/backup.sh

# 5. 初始化 Wiki.js
# 访问 http://your-server:3000
# 完成初始化向导

# 6. 在 Wiki.js 配置 Git 存储
# 管理后台 → 存储 → Git
# 填写仓库信息和 PAT

# 7. 测试 Git 同步
# 在 Wiki.js 创建测试文章
# 等待 5 分钟或手动触发同步

# 8. 在 GitHub 仓库初始化 VitePress
cd ~/wikijs-content
npm init -y
npm install -D vitepress

# 9. 本地测试构建
npm run build
npm run preview

# 10. 推送并测试 GitHub Actions
git add .
git commit -m "Initial VitePress setup"
git push origin main

# 11. 检查 Actions 状态
# 访问 GitHub 仓库 → Actions 标签

# 12. 测试 GitHub Pages
# 访问 https://wiki.noeverer.github.io

# 13. 验证域名配置
nslookup wiki.noeverer.github.io
curl -I https://wiki.noeverer.github.io

# 14. 完整流程测试
# Wiki.js 编辑文章 → Git Push → GitHub Actions → GitHub Pages
# 验证每个环节

# 15. 查看日志排查问题
docker-compose logs wiki --tail 100
docker-compose logs wiki-db --tail 100
```

## Notes

### 安全注意事项

1. **数据库密码**
   - 使用强密码
   - 不要提交到 Git
   - 定期更换

2. **GitHub PAT**
   - 使用最小权限原则
   - 只授予 `repo` 权限
   - 设置过期时间
   - 存储在安全位置

3. **防火墙配置**
   - 限制 3000 端口仅本地访问
   - 通过 Nginx 代理访问
   - 启用 HTTPS

### 同步策略

| 场景 | 方向 | 触发方式 | 频率 |
|------|------|---------|------|
| Wiki.js → GitHub | 推送 | 定时/手动 | 5分钟 |
| GitHub → Wiki.js | 拉取 | 定时/手动 | 5分钟 |
| GitHub → GitHub Pages | 构建 | Push | 自动 |

### 备份策略

1. **数据库备份**: 每日凌晨 2 点
2. **文件备份**: 每日凌晨 2 点
3. **保留期**: 7 天
4. **异地备份**: 可选，使用 S3 或其他云存储

### 性能优化

1. **Wiki.js**
   - 启用缓存
   - 优化数据库查询
   - 使用 CDN 加载静态资源

2. **GitHub Pages**
   - 使用 VitePress 的懒加载
   - 优化图片大小
   - 配置 CDN（可选）

### 故障排查

**问题 1: Wiki.js 无法启动**
```bash
# 查看日志
docker-compose logs wiki

# 检查数据库连接
docker-compose logs wiki-db

# 重启服务
docker-compose restart
```

**问题 2: Git 同步失败**
- 检查 PAT 是否过期
- 验证仓库权限
- 查看 Wiki.js 日志

**问题 3: GitHub Actions 失败**
- 检查工作流配置
- 验证 Node.js 版本
- 查看构建日志

**问题 4: GitHub Pages 无法访问**
- 检查 Pages 设置
- 验证域名配置
- 确认构建成功

### 维护任务

| 任务 | 频率 | 说明 |
|------|------|------|
| 备份检查 | 每周 | 验证备份完整性 |
| 日志清理 | 每周 | 清理旧日志 |
| 系统更新 | 每月 | 更新 Docker 镜像 |
| 依赖更新 | 每月 | 更新 npm 包 |
| 安全审计 | 每季度 | 检查安全漏洞 |

## 变更记录

| 日期 | 说明 |
|------|------|
| 2026-01-14 | 创建 Spec，定义架构和实施方案 |
