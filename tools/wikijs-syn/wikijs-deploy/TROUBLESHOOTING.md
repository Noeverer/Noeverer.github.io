# Wiki.js 部署故障排除

## 常见问题及解决方案

### 问题 1: Docker Compose 启动时出现 'ContainerConfig' 错误

**错误信息：**
```
ERROR: for wikijs  'ContainerConfig'
KeyError: 'ContainerConfig'
```

**原因：**
旧容器的镜像配置不完整或损坏。

**解决方案：**

1. 停止并删除所有容器和卷：
```bash
cd /home/ante/10-personal/Noeverer.github.io/tools/wikijs-syn/wikijs-deploy
docker-compose down -v
```

2. 清理 Docker 系统（可选）：
```bash
docker system prune -f
```

3. 重新启动服务：
```bash
./start.sh
```

4. 验证服务状态：
```bash
docker-compose ps
docker logs wikijs --tail 20
```

### 问题 2: 容器无法启动

**症状：**
容器状态显示 `Exit` 或 `Restarting`

**解决方案：**

1. 查看详细日志：
```bash
docker-compose logs wiki
docker-compose logs wiki-db
```

2. 检查端口占用：
```bash
sudo lsof -i :3000
sudo lsof -i :5432
```

3. 检查磁盘空间：
```bash
df -h
```

4. 重新启动：
```bash
docker-compose down
docker-compose up -d
```

### 问题 3: 数据库连接失败

**错误信息：**
```
Database Connection Failed
```

**解决方案：**

1. 检查数据库容器状态：
```bash
docker-compose ps wiki-db
```

2. 测试数据库连接：
```bash
docker exec wikijs-db pg_isready -U wikijs
```

3. 查看数据库日志：
```bash
docker logs wikijs-db
```

4. 验证环境变量：
```bash
cat .env
```

确保 `DB_PASSWORD` 在 `.env` 文件中正确设置。

### 问题 4: Wiki.js 初始化后无法访问

**症状：**
浏览器访问 `http://localhost:3000` 时无法连接

**解决方案：**

1. 检查容器健康状态：
```bash
docker-compose ps
```

2. 查看服务日志：
```bash
docker logs wikijs --tail 50
```

3. 检查防火墙：
```bash
sudo ufw status
# 如果需要，允许端口：
sudo ufw allow 3000
```

4. 测试 HTTP 连接：
```bash
curl -I http://localhost:3000
```

### 问题 5: Git 存储权限问题

**错误信息：**
```
/wiki/data/repo/.git: Permission denied
```

**解决方案：**

1. 方法 1: 删除旧数据卷并重建（推荐）
```bash
docker-compose down -v
docker volume rm wikijs-deploy_wiki-data
docker-compose up -d
```

2. 方法 2: 修复卷权限
```bash
docker run --rm -v wikijs-deploy_wiki-data:/data alpine chown -R 1000:1000 /data
```

3. 方法 3: 确认 UID/GID 配置
```bash
id -u  # 查看当前 UID
id -g  # 查看当前 GID

# 然后在 .env 文件中设置:
# UID=<你的 UID>
# GID=<你的 GID>
```

### 问题 6: Git 同步失败

**症状：**
Wiki.js 无法推送到 GitHub

**解决方案：**

1. 检查 PAT Token 是否过期
   - 访问 GitHub Settings → Developer settings → Personal access tokens
   - 验证 token 仍然有效

2. 验证仓库权限
   - 确认 PAT 具有 `repo` 权限
   - 确认仓库存在且可访问

3. 查看 Wiki.js 日志：
```bash
docker logs wikijs --tail 100 | grep -i git
```

4. 测试 Git 连接（在容器内）：
```bash
docker exec -it wikijs sh
cd /wiki/data/repo
git remote -v
git status
```

5. 手动触发同步（在 Wiki.js 管理界面）

### 问题 7: GitHub Actions 构建失败

**症状：**
GitHub Pages 无法构建

**解决方案：**

1. 检查 Actions 日志
   - 访问仓库的 Actions 标签
   - 查看具体的错误信息

2. 验证工作流配置
   - 检查 `.github/workflows/build-pages.yml` 语法
   - 确认 Node.js 版本正确

3. 验证依赖安装
```bash
cd /home/ante/10-personal/Noeverer.github.io/tools/wikijs-syn/wikijs-content
npm install
npm run build
```

4. 检查权限设置
   - Settings → Actions → General
   - 确保 Workflow permissions 设置正确

### 问题 8: VitePress 构建失败

**错误信息：**
```
Build failed with errors
```

**解决方案：**

1. 检查 VitePress 配置
```bash
cat /home/ante/10-personal/Noeverer.github.io/tools/wikijs-syn/wikijs-content/.vitepress/config.ts
```

2. 清理缓存并重新构建
```bash
rm -rf node_modules
rm -rf .vitepress/cache
npm install
npm run build
```

3. 检查文档格式
   - 确保所有 Markdown 文件格式正确
   - 检查是否有语法错误

4. 查看详细错误信息
```bash
npm run build 2>&1 | tee build.log
```

### 问题 9: 端口已被占用

**错误信息：**
```
Bind for 0.0.0.0:3000 failed: port is already allocated
```

**解决方案：**

1. 查找占用端口的进程：
```bash
sudo lsof -i :3000
```

2. 停止占用端口的进程：
```bash
# 如果是其他容器
docker stop <container_name>

# 如果是其他服务
sudo kill <PID>
```

3. 或者修改 docker-compose.yml 中的端口映射：
```yaml
ports:
  - "3001:3000"  # 使用 3001 端口
```

### 问题 10: 数据丢失

**症状：**
重启容器后数据丢失

**解决方案：**

1. 检查卷挂载配置：
```bash
docker inspect wikijs | grep -A 10 Mounts
```

2. 确认卷持久化：
```bash
docker volume ls
```

3. 恢复备份：
```bash
cd /home/ante/10-personal/Noeverer.github.io/tools/wikijs-syn/wikijs-deploy
./backup/restore.sh <backup_file>
```

4. 验证 .env 配置
   - 确认数据路径正确
   - 确认卷配置正确

## 调试命令速查

### 容器管理
```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 查看容器详细信息
docker inspect wikijs

# 进入容器
docker exec -it wikijs sh

# 查看容器资源使用
docker stats wikijs
```

### 日志查看
```bash
# 查看所有日志
docker-compose logs

# 查看特定服务日志
docker-compose logs wiki
docker-compose logs wiki-db

# 持续跟踪日志
docker-compose logs -f

# 查看最近 100 行
docker-compose logs --tail=100
```

### 网络调试
```bash
# 检查网络连通性
docker exec wikijs ping wiki-db

# 检查端口监听
docker exec wikijs netstat -tlnp

# 测试 HTTP 连接
docker exec wikijs wget -O- http://localhost:3000
```

### 数据库调试
```bash
# 进入数据库
docker exec -it wikijs-db psql -U wikijs -d wikijs

# 查看数据库列表
\l

# 查看表列表
\dt

# 查看表结构
\d table_name

# 查询数据
SELECT * FROM users LIMIT 10;

# 退出
\q
```

### 卷和备份
```bash
# 查看所有卷
docker volume ls

# 查看卷详细信息
docker volume inspect wikijs-deploy_wiki-db-data

# 备份数据库
docker exec wikijs-db pg_dump -U wikijs wikijs > backup.sql

# 恢复数据库
docker exec -i wikijs-db psql -U wikijs wikijs < backup.sql

# 备份卷
docker run --rm -v wikijs-deploy_wiki-db-data:/data -v $(pwd):/backup alpine tar czf /backup/db-backup.tar.gz -C /data .
```

## 预防措施

1. **定期备份**
   - 设置自动备份任务
   - 验证备份完整性

2. **监控日志**
   - 定期检查错误日志
   - 设置日志轮转

3. **更新镜像**
   - 定期更新 Docker 镜像
   - 测试后再部署到生产环境

4. **安全配置**
   - 使用强密码
   - 定期更换 PAT Token
   - 配置防火墙规则

5. **文档记录**
   - 记录配置变更
   - 保留故障排除记录

## 获取帮助

如果以上方法都无法解决问题：

1. 查看官方文档：
   - [Wiki.js 官方文档](https://docs.requarks.io/)
   - [Docker 官方文档](https://docs.docker.com/)
   - [VitePress 文档](https://vitepress.dev/)

2. 查看日志文件：
   ```bash
   cat /home/ante/10-personal/Noeverer.github.io/tools/wikijs-syn/wikijs-deploy/logs/*.log
   ```

3. 提交问题：
   - 检查 GitHub Issues
   - 搜索类似问题
   - 创建新问题并提供详细信息

## 相关文档

- [快速开始指南](QUICK_START.md)
- [Git 集成配置](../wikijs/GIT_INTEGRATION.md)
- [实现总结](../../specs/005-wikijs-github-pages/IMPLEMENTATION.md)
