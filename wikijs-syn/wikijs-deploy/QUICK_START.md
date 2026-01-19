# Wiki.js 部署 - 快速开始指南

本文档帮助你快速部署 Wiki.js 并配置与 GitHub Pages 的联动。

## 目录

- [前提条件](#前提条件)
- [快速部署](#快速部署)
- [Wiki.js 初始化](#wikijs-初始化)
- [配置 Git 存储](#配置-git-存储)
- [GitHub Pages 部署](#github-pages-部署)
- [日常使用](#日常使用)
- [故障排查](#故障排查)

## 前提条件

### 系统要求
- Linux 系统（Ubuntu 20.04+ 推荐）
- Docker 和 Docker Compose
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

### 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 添加当前用户到 docker 组
sudo usermod -aG docker $USER

# 重新登录或运行
newgrp docker
```

### 安装 Docker Compose

```bash
# Docker Compose 通常随 Docker 一起安装
docker-compose --version

# 如果未安装，使用以下命令
sudo apt-get install docker-compose
```

## 快速部署

### 1. 克隆或下载配置文件

```bash
# 进入项目目录
cd /home/ante/10-personal/wikijs-deploy
```

### 2. 配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，设置数据库密码
nano .env
```

`.env` 文件内容：
```bash
DB_PASSWORD=your_secure_password_here
```

### 3. 启动服务

```bash
# 方式 1: 使用快速启动脚本
./start.sh

# 方式 2: 使用部署脚本
./deploy.sh

# 方式 3: 直接使用 Docker Compose
docker-compose up -d
```

### 4. 检查服务状态

```bash
# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 检查端口监听
netstat -tlnp | grep 3000
```

### 5. 验证服务

```bash
# 测试 HTTP 访问
curl -I http://localhost:3000
```

## Wiki.js 初始化

### 首次访问

1. 打开浏览器访问: `http://localhost:3000`
2. 首次访问会显示初始化向导

### 初始化步骤

#### 步骤 1: 选择数据库

- 数据库类型: PostgreSQL
- 数据库主机: `wiki-db`
- 数据库端口: `5432`
- 数据库用户名: `wikijs`
- 数据库密码: 你在 `.env` 中设置的密码
- 数据库名称: `wikijs`

#### 步骤 2: 配置超级管理员

- 管理员邮箱: `admin@example.com`
- 管理员密码: 设置强密码
- 确认密码: 重复输入密码

#### 步骤 3: 配置站点信息

- 站点名称: `Ante's Wiki`
- 站点 URL: `http://localhost:3000` 或你的域名
- 站点描述: `个人知识库`

#### 步骤 4: 完成

点击 "完成" 按钮，Wiki.js 会自动初始化。

### 登录

使用创建的管理员账户登录 Wiki.js 管理界面。

## 配置 Git 存储

### 1. 创建 GitHub 仓库

1. 访问 GitHub，创建新仓库 `wikijs-content`
2. 可以选择私有或公开

### 2. 生成 Personal Access Token

1. 进入 GitHub Settings → Developer Settings → Personal access tokens
2. 点击 "Generate new token (classic)"
3. 设置权限:
   - `repo` (完整仓库访问权限)
4. 生成后复制并保存 token

### 3. 在 Wiki.js 中配置 Git 存储

1. 登录 Wiki.js 管理后台
2. 导航至 `模块` → `存储` → `Git`
3. 点击 `创建存储`

配置参数：

| 参数 | 值 |
|------|---|
| 存储标识符 | `github-wiki` |
| 存储模式 | 读写 |
| Git URL | `https://github.com/Noeverer/wikijs-content.git` |
| 分支 | `main` |
| 验证方式 | HTTPS |
| 用户名 | `Noeverer` |
| 密码 | [你的 PAT Token] |
| 提交作者名 | `Ante Liu` |
| 提交作者邮箱 | `your.email@example.com` |
| 提交消息 | `Update wiki content` |
| 同步间隔 | `5 minutes` |

### 4. 初始化同步

1. 点击 `初始化同步`
2. 等待首次同步完成
3. 检查 GitHub 仓库是否有内容

### 5. 测试双向同步

#### Wiki.js → GitHub
1. 在 Wiki.js 创建测试文章
2. 手动触发 Git 同步或等待 5 分钟
3. 检查 GitHub 仓库是否更新

#### GitHub → Wiki.js
1. 在 GitHub 直接编辑或添加文件
2. 在 Wiki.js 触发同步
3. 检查文章是否出现在 Wiki.js

## GitHub Pages 部署

### 1. 启用 GitHub Pages

1. 进入 GitHub 仓库 `wikijs-content`
2. Settings → Pages
3. Source 选择: `GitHub Actions`
4. 保存设置

### 2. 配置 Actions

工作流文件 `.github/workflows/build-pages.yml` 已经配置好。

### 3. 触发构建

```bash
# 在 wikijs-content 目录
cd /home/ante/10-personal/wikijs-content

# 安装依赖
npm install

# 提交并推送
git add .
git commit -m "Initial commit"
git push origin main
```

### 4. 查看 Actions

访问 GitHub 仓库 → Actions 标签，查看构建状态。

### 5. 访问 GitHub Pages

构建完成后，访问: `https://noeverer.github.io/wikijs-content/`

或配置自定义域名后访问。

## 日常使用

### 启动和停止

```bash
# 启动
cd /home/ante/10-personal/wikijs-deploy
docker-compose up -d

# 停止
docker-compose down

# 重启
docker-compose restart

# 查看状态
docker-compose ps
```

### 查看日志

```bash
# 查看所有日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f wiki
docker-compose logs -f wiki-db

# 查看最近 100 行
docker-compose logs --tail=100
```

### 备份数据

```bash
# 运行备份脚本
./backup/backup.sh
```

备份文件会保存在 `backup/backups/` 目录。

### 更新 Wiki.js

```bash
# 拉取最新镜像
docker-compose pull

# 重新创建容器
docker-compose up -d

# 清理旧镜像
docker image prune -f
```

## 故障排查

### 问题 1: 容器无法启动

```bash
# 查看日志
docker-compose logs

# 检查端口占用
sudo lsof -i :3000

# 检查磁盘空间
df -h

# 重新启动
docker-compose down
docker-compose up -d
```

### 问题 2: 数据库连接失败

```bash
# 检查数据库容器状态
docker ps | grep wikijs-db

# 测试数据库连接
docker exec wikijs-db pg_isready -U wikijs

# 查看数据库日志
docker logs wikijs-db
```

### 问题 3: Git 存储权限问题 (/wiki/data/repo/.git: Permission denied)

**症状**: 在 Wiki.js 配置 Git 存储时提示权限错误

**解决方案**:

```bash
# 方法 1: 删除旧数据卷并重建（推荐）
cd /home/ante/10-personal/wikijs-deploy
docker-compose down
docker volume rm wikijs-deploy_wiki-data
docker-compose up -d

# 方法 2: 修复卷权限
docker run --rm -v wikijs-deploy_wiki-data:/data alpine chown -R 1000:1000 /data

# 方法 3: 确认 UID/GID 配置
id -u  # 查看当前 UID
id -g  # 查看当前 GID

# 然后在 .env 文件中设置:
# UID=<你的 UID>
# GID=<你的 GID>
```

**预防措施**: 确保 `.env` 文件中设置了正确的 UID 和 GID（默认 1000）

### 问题 4: Git 同步失败

1. 检查 PAT Token 是否过期
2. 验证仓库权限
3. 检查网络连接
4. 查看 Wiki.js 日志

### 问题 5: GitHub Actions 失败

1. 检查工作流配置语法
2. 验证 Node.js 版本
3. 查看构建日志
4. 确认权限设置

### 问题 6: GitHub Pages 无法访问

1. 检查 Pages 设置
2. 验证 Actions 成功
3. 等待 DNS 传播（最多 10 分钟）
4. 检查自定义域名配置

## 常用命令

```bash
# Docker 命令
docker ps                      # 查看运行中的容器
docker ps -a                   # 查看所有容器
docker images                   # 查看镜像
docker volume ls                # 查看数据卷
docker stats                    # 查看资源使用

# Docker Compose 命令
docker-compose up -d            # 后台启动
docker-compose down             # 停止并删除容器
docker-compose restart           # 重启服务
docker-compose logs              # 查看日志
docker-compose pull              # 拉取最新镜像

# 日志查看
docker-compose logs wiki --tail 100     # 最近 100 行
docker-compose logs wiki -f             # 持续跟踪
docker logs wikijs --since 5m           # 最近 5 分钟

# 数据库操作
docker exec wikijs-db psql -U wikijs -d wikijs  # 进入数据库
docker exec wikijs-db pg_dump -U wikijs wikijs > backup.sql  # 备份
```

## 维护建议

### 定期任务

- **每周**: 检查备份完整性
- **每月**: 更新 Docker 镜像
- **每季度**: 检查安全更新

### 监控指标

- CPU 使用率
- 内存使用量
- 磁盘空间
- 服务响应时间

### 安全建议

1. 使用强密码
2. 定期更换 PAT Token
3. 限制数据库访问
4. 启用 HTTPS
5. 配置防火墙

## 进一步阅读

- [Wiki.js 官方文档](https://docs.requarks.io/)
- [Docker 官方文档](https://docs.docker.com/)
- [VitePress 文档](https://vitepress.dev/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

## 支持

如遇到问题，请查看：
1. 故障排查章节
2. 各组件的官方文档
3. GitHub Issues
