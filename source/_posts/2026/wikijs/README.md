---
title: Wiki.js Docker 部署指南
date: 2026-01-01 12:00:00
tags: ["wikijs", "docker", "部署"]
categories: tech
description: 基于 Docker 的 Wiki.js 部署方案，实现 Web 界面流畅书写笔记，并将笔记保存在 GitHub 仓库中
published: true
---

# Wiki.js Docker 部署指南

基于 Docker 的 Wiki.js 部署方案，实现 Web 界面流畅书写笔记，并将笔记保存在 GitHub 仓库中。

## 功能特性

- ✓ Web 界面编辑笔记
- ✓ 笔记自动同步到 GitHub 仓库
- ✓ Markdown 格式存储
- ✓ 版本控制
- ✓ 图像上传支持
- ✓ SQLite/PostgreSQL 数据库支持
- ✓ Docker 容器化部署

## 快速开始

### 1. 前置要求

- Docker
- Docker Compose
- GitHub 账户

### 2. 一键部署

```bash
# 赋予执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

按照提示输入 GitHub 用户名和仓库名，脚本将自动完成配置和部署。

### 3. 手动部署

#### 3.1 配置文件

编辑 `docker-compose.yml` 和 `config.yml`，替换以下变量：

- `YOUR_USERNAME`: 你的 GitHub 用户名
- `YOUR_REPO`: 你的 GitHub 仓库名

#### 3.2 启动服务

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 4. 初始化配置

1. 访问 http://localhost:3000
2. 创建管理员账户
3. 在管理后台配置 Git 存储设置
4. 设置 GitHub 仓库地址和认证信息

## 配置说明

### Docker Compose 配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| PORT | 服务端口 | 3000 |
| DB_TYPE | 数据库类型 | postgres |
| GIT_REPOSITORY_URL | Git 仓库地址 | - |
| GIT_BRANCH | Git 分支 | main |

### 环境变量

```yaml
# 数据库配置
DB_TYPE: postgres
DB_HOST: postgres
DB_PORT: 5432
DB_USER: wikijs
DB_PASS: wikijs_password
DB_NAME: wikijs

# Git 配置
GIT_REPOSITORY_URL: https://github.com/YOUR_USERNAME/YOUR_REPO.git
GIT_BRANCH: main

# 其他配置
TZ: Asia/Shanghai
PORT: 3000
```

### Git 存储配置

支持两种 Git 认证方式：

#### HTTPS 方式
```yaml
git:
  url: https://github.com/username/repo.git
  auth:
    type: basic
    username: YOUR_USERNAME
    password: YOUR_PERSONAL_TOKEN
```

#### SSH 方式
```yaml
git:
  url: git@github.com:username/repo.git
  auth:
    type: ssh
    privateKey: /wiki/data/git/id_rsa
```

## 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f wikijs

# 进入容器
docker exec -it wikijs bash

# 备份数据库
docker exec wikijs-postgres pg_dump -U wikijs wikijs > backup.sql

# 恢复数据库
docker exec -i wikijs-postgres psql -U wikijs wikijs < backup.sql
```

## 数据持久化

数据存储在 Docker Volume 中：

- `wikijs-data`: Wiki.js 数据
- `postgres-data`: PostgreSQL 数据库

## 备份与恢复

### 备份

```bash
# 备份数据库
docker exec wikijs-postgres pg_dump -U wikijs wikijs > backup-$(date +%Y%m%d).sql

# 备份 Git 仓库
tar -czf git-backup-$(date +%Y%m%d).tar.gz ./data/git
```

### 恢复

```bash
# 恢复数据库
docker exec -i wikijs-postgres psql -U wikijs wikijs < backup-20240101.sql
```

## 故障排除

### 无法访问服务

```bash
# 检查容器状态
docker-compose ps

# 查看日志
docker-compose logs wikijs

# 检查端口占用
netstat -tuln | grep 3000
```

### Git 同步失败

1. 检查 Git 配置是否正确
2. 验证 GitHub 认证信息
3. 确保仓库有写入权限
4. 检查 SSH 密钥配置

### 数据库连接失败

```bash
# 检查数据库容器
docker-compose ps postgres

# 查看数据库日志
docker-compose logs postgres
```

## 安全建议

1. 修改默认数据库密码
2. 使用 GitHub Personal Access Token 而非密码
3. 配置防火墙规则
4. 定期备份数据
5. 使用 HTTPS 访问（生产环境）

## 更新升级

```bash
# 拉取最新镜像
docker-compose pull

# 重新构建和启动
docker-compose up -d --build
```

## 参考资源

- [Wiki.js 官方文档](https://docs.requarks.io/)
- [Docker 官方文档](https://docs.docker.com/)
- [GitHub API 文档](https://docs.github.com/en/rest)

## 许可证

MIT License
