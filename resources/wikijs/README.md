# Wiki.js 与 GitHub Pages 联动部署

## 项目概述

本项目实现了 Wiki.js 与 GitHub Pages 的联动部署，提供了一套完整的知识管理系统。Wiki.js 用于内容创作和管理，GitHub Pages 用于公开发布静态内容。

## 架构设计

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

## 部署组件

### 1. 本地部署组件

- [docker-compose.yml](../../wikijs-deploy/docker-compose.yml): Docker 配置文件
- [.env](../../wikijs-deploy/.env): 环境变量配置
- [deploy.sh](../../wikijs-deploy/deploy.sh): 自动部署脚本
- [nginx/wikijs.conf](../../wikijs-deploy/nginx/wikijs.conf): Nginx 反向代理配置
- [backup/backup.sh](../../wikijs-deploy/backup/backup.sh): 备份脚本

### 2. GitHub Pages 组件

- [package.json](../../../wikijs-content/package.json): Node.js 依赖配置
- [.vitepress/config.ts](../../../wikijs-content/.vitepress/config.ts): VitePress 配置
- [.github/workflows/build-pages.yml](../../../wikijs-content/.github/workflows/build-pages.yml): GitHub Actions 工作流

## 部署步骤

### 1. 本地部署 Wiki.js

```bash
# 进入部署目录
cd /home/ante/10-personal/Noeverer.github.io/wikijs-deploy

# 配置数据库密码
cp .env .env.example
# 编辑 .env 文件设置密码
nano .env

# 启动服务
./deploy.sh
```

### 2. 初始化 Wiki.js

1. 访问 `http://your-server:3000`
2. 完成初始化向导
3. 配置管理员账户

### 3. 配置 Git 存储

参考 [GIT_INTEGRATION.md](GIT_INTEGRATION.md) 文档配置与 GitHub 的集成。

### 4. 验证部署

运行验证脚本：

```bash
./validate-deployment.sh
```

## 维护和管理

### 日常维护

- 定期备份：运行 `./backup/backup.sh`
- 监控日志：`docker-compose logs -f`
- 检查服务状态：`docker-compose ps`

### 安全建议

- 使用强密码保护数据库
- 定期更新访问令牌
- 限制服务器访问权限
- 定期更新 Docker 镜像

## 故障排除

如果遇到问题，请按以下步骤检查：

1. 检查容器状态：`docker-compose ps`
2. 查看日志：`docker-compose logs wiki`
3. 验证端口连通性：`curl -I http://localhost:3000`
4. 检查配置文件是否正确

## 许可证

MIT License