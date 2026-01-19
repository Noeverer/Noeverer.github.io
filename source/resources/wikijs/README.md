# Wiki.js 部署联动 GitHub Pages

## 目录结构

```
wikijs/
├── docker-compose.yml          # Docker Compose 配置
├── .env.example                # 环境变量示例
├── nginx/
│   └── wikijs.conf            # Nginx 反向代理配置
├── backup/
│   ├── backup.sh              # 备份脚本
│   └── restore.sh             # 恢复脚本
├── vitepress/
│   └── init-vitepress.sh      # VitePress 初始化脚本
├── scripts/
│   └── deploy.sh              # 部署脚本
└── .github/
    └── workflows/
        └── build-wiki-pages.yml # GitHub Actions 工作流
```

## 快速开始

### 1. 环境准备

确保已安装以下软件：
- Docker 和 Docker Compose
- Node.js 18+
- Nginx

### 2. 部署 Wiki.js

```bash
# 1. 复制环境变量配置
cp .env.example .env

# 2. 编辑 .env 文件，设置数据库密码
nano .env

# 3. 运行部署脚本
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# 4. 访问 Wiki.js 完成初始化
# http://your-server:3000
```

### 3. 配置 Git 存储

在 Wiki.js 管理界面中配置 Git 存储：

1. 登录 Wiki.js 管理后台
2. 导航至：`模块` → `存储` → `Git`
3. 点击 `创建存储`
4. 填写配置：

| 配置项 | 值 |
|--------|-----|
| 存储标识符 | github-wiki |
| 存储模式 | 读写 (双向同步) |
| Git URL | https://github.com/Noeverer/Noeverer.github.io.git |
| 分支 | master |
| 验证方式 | HTTPS |
| 用户名 | Noeverer |
| 密码 | [你的 GitHub PAT] |
| 同步间隔 | 5 分钟 |

### 4. 初始化 VitePress

```bash
# 运行初始化脚本
chmod +x vitepress/init-vitepress.sh
./vitepress/init-vitepress.sh

# 本地预览
cd vitepress
npm run dev
```

### 5. 推送到 GitHub

```bash
# 提交更改
git add .
git commit -m "feat: add Wiki.js deployment"

# 推送到 GitHub
git push origin master
```

GitHub Actions 会自动构建并部署到 GitHub Pages。

### 6. 配置 Nginx（可选）

```bash
# 复制 Nginx 配置
sudo cp nginx/wikijs.conf /etc/nginx/sites-available/wikijs

# 启用配置
sudo ln -s /etc/nginx/sites-available/wikijs /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重新加载 Nginx
sudo systemctl reload nginx
```

## 常用命令

### Wiki.js 管理

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 更新 Wiki.js
docker-compose pull
docker-compose up -d
```

### 备份与恢复

```bash
# 手动备份
chmod +x backup/backup.sh
./backup/backup.sh

# 恢复数据
chmod +x backup/restore.sh
./backup/restore.sh 20260114_120000

# 设置定时备份（每天凌晨 2 点）
crontab -e
# 添加以下行：
# 0 2 * * * /path/to/wikijs/backup/backup.sh >> /var/log/wikijs-backup.log 2>&1
```

### VitePress 开发

```bash
cd vitepress

# 安装依赖
npm install

# 本地开发
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

## 配置说明

### 环境变量 (.env)

| 变量 | 说明 | 示例 |
|------|------|------|
| DB_PASSWORD | 数据库密码 | your_secure_password |
| GITHUB_PAT | GitHub Personal Access Token | ghp_xxx... |
| GITHUB_REPO | GitHub 仓库 | Noeverer/Noeverer.github.io |
| GITHUB_BRANCH | 分支名称 | master |
| SYNC_INTERVAL | 同步间隔（分钟） | 5 |

### GitHub PAT 生成

1. 访问 GitHub Settings
2. Developer settings → Personal access tokens
3. Generate new token (classic)
4. 选择权限：
   - `repo` (完整仓库访问权限)
   - `workflow` (GitHub Actions 权限)
5. 复制 token 到 .env 文件

## 故障排查

### Wiki.js 无法启动

```bash
# 查看日志
docker-compose logs wiki

# 检查数据库连接
docker-compose logs wiki-db

# 重启服务
docker-compose restart
```

### Git 同步失败

1. 检查 PAT 是否过期
2. 验证仓库权限
3. 查看 Wiki.js 日志中的错误信息
4. 确认网络连接正常

### GitHub Actions 构建失败

1. 检查 GitHub Actions 日志
2. 验证 Node.js 版本
3. 确认 VitePress 配置正确
4. 检查依赖安装是否完整

### GitHub Pages 无法访问

1. 检查 Pages 设置是否启用
2. 验证仓库分支是否正确
3. 确认构建是否成功
4. 检查 CNAME 配置（如使用自定义域名）

## 维护建议

### 定期维护

- 每周检查备份完整性
- 每月更新 Docker 镜像
- 每季度更新依赖包
- 定期检查 GitHub Actions 执行状态

### 安全加固

- 使用强密码
- 定期更换 GitHub PAT
- 启用 HTTPS
- 配置防火墙规则
- 限制 3000 端口仅本地访问

## 参考资料

- [Wiki.js 官方文档](https://docs.requarks.io/)
- [Docker 文档](https://docs.docker.com/)
- [VitePress 文档](https://vitepress.dev/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
