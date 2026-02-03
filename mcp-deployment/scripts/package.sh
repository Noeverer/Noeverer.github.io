#!/bin/bash

# MCP 环境打包脚本
# 用于将 MCP 环境打包以便内网部署

set -e

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PACKAGE_NAME="mcp-server-$(date +%Y%m%d_%H%M%S)"
PACKAGE_DIR="/tmp/$PACKAGE_NAME"
OUTPUT_DIR="$PROJECT_ROOT/dist"

echo "=== MCP 环境打包脚本 ==="
echo "项目根目录: $PROJECT_ROOT"
echo "包名: $PACKAGE_NAME"
echo "输出目录: $OUTPUT_DIR"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 清理并创建临时目录
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

echo "步骤 1: 复制核心文件..."

# 复制核心代码
echo "  - 复制应用代码..."
mkdir -p "$PACKAGE_DIR/app"
cp -r "$PROJECT_ROOT/app" "$PACKAGE_DIR/"

# 复制 MCP 指南内容
echo "  - 复制 MCP 指南..."
mkdir -p "$PACKAGE_DIR/docs"
cp -r "$PROJECT_ROOT/blog/source/_posts/2026/01-tools/mcp-guide" "$PACKAGE_DIR/docs/guide"

# 复制配置文件
echo "  - 复制配置文件..."
mkdir -p "$PACKAGE_DIR/config"
cp -r "$PROJECT_ROOT/mcp-deployment/config"/* "$PACKAGE_DIR/config/"

# 复制 Docker 配置
echo "  - 复制 Docker 配置..."
mkdir -p "$PACKAGE_DIR/docker"
cp -r "$PROJECT_ROOT/mcp-deployment/docker"/* "$PACKAGE_DIR/docker/"

# 复制脚本
echo "  - 复制部署脚本..."
mkdir -p "$PACKAGE_DIR/scripts"
cp -r "$PROJECT_ROOT/mcp-deployment/scripts"/* "$PACKAGE_DIR/scripts/" 2>/dev/null || true

echo "步骤 2: 生成依赖文件..."

# 生成 requirements.txt
echo "  - 生成 Python 依赖..."
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    cp "$PROJECT_ROOT/requirements.txt" "$PACKAGE_DIR/"
fi

if [ -f "$PROJECT_ROOT/requirements-prod.txt" ]; then
    cp "$PROJECT_ROOT/requirements-prod.txt" "$PACKAGE_DIR/"
else
    # 如果没有生产环境依赖文件，生成一个基础的
    cat > "$PACKAGE_DIR/requirements-prod.txt" << EOF
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
aiofiles>=23.2.1
redis>=5.0.1
sqlalchemy>=2.0.23
alembic>=1.13.0
httpx>=0.25.2
pyyaml>=6.0.1
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
chromadb>=0.4.18
sentence-transformers>=2.2.2
numpy>=1.24.0
pandas>=2.1.4
prometheus-client>=0.19.0
structlog>=23.2.0
EOF
fi

echo "步骤 3: 生成部署文档..."

# 生成部署脚本
cat > "$PACKAGE_DIR/deploy.sh" << 'DEPLOY_SCRIPT_EOF'
#!/bin/bash

# MCP 内网部署脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== MCP 内网部署向导 ==="

# 检查依赖
check_dependencies() {
    echo "检查系统依赖..."
    
    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        echo "错误: 未找到 Docker，请先安装 Docker"
        exit 1
    fi
    
    # 检查 Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "错误: 未找到 Docker Compose，请先安装 Docker Compose"
        exit 1
    fi
    
    echo "✓ 依赖检查通过"
}

# 配置环境
configure_environment() {
    echo "配置环境变量..."
    
    if [ ! -f "$SCRIPT_DIR/config/.env" ]; then
        echo "错误: 未找到环境变量配置文件"
        exit 1
    fi
    
    # 提示用户修改重要配置
    echo "⚠️  请在部署前修改以下配置项："
    echo "  - MCP_SECRET_KEY: 设置强密钥"
    echo "  - MCP_JWT_SECRET: 设置 JWT 密钥"
    echo "  - MCP_POSTGRES_PASSWORD: 设置数据库密码"
    echo "  - MCP_REDIS_PASSWORD: 设置 Redis 密码"
    echo ""
    read -p "是否已经配置好环境变量？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "请先配置好环境变量后再运行此脚本"
        exit 1
    fi
}

# 创建目录结构
create_directories() {
    echo "创建目录结构..."
    
    mkdir -p /opt/mcp/{data,logs,config,skills,vectors}
    mkdir -p /opt/mcp/ssl
    
    # 设置权限
    chmod 755 /opt/mcp
    chmod -R 755 /opt/mcp/{data,logs,config,skills,vectors}
    
    echo "✓ 目录结构创建完成"
}

# 部署服务
deploy_services() {
    echo "部署 MCP 服务..."
    
    cd "$SCRIPT_DIR/docker"
    
    # 启动基础服务
    echo "启动基础服务..."
    docker-compose up -d redis
    
    # 等待 Redis 启动
    echo "等待 Redis 启动..."
    sleep 10
    
    # 启动主服务
    echo "启动 MCP 主服务..."
    docker-compose up -d mcp-server
    
    # 可选服务
    read -p "是否启用 PostgreSQL 数据库？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "启动 PostgreSQL..."
        docker-compose --profile postgres up -d postgres
        sleep 15
    fi
    
    read -p "是否启用 Nginx 反向代理？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "启动 Nginx..."
        docker-compose --profile nginx up -d nginx
    fi
    
    read -p "是否启用监控服务？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "启动监控服务..."
        docker-compose --profile monitoring up -d prometheus grafana
    fi
}

# 验证部署
verify_deployment() {
    echo "验证部署状态..."
    
    # 检查服务状态
    echo "服务状态:"
    docker-compose ps
    
    # 健康检查
    echo "执行健康检查..."
    sleep 30
    
    if curl -f http://localhost:8080/health > /dev/null 2>&1; then
        echo "✓ MCP 服务健康检查通过"
    else
        echo "⚠️  MCP 服务健康检查失败，请检查日志"
    fi
}

# 显示访问信息
show_access_info() {
    echo ""
    echo "=== 部署完成 ==="
    echo "服务访问地址:"
    echo "  - MCP 服务: http://localhost:8080"
    echo "  - 健康检查: http://localhost:8080/health"
    echo "  - 指标接口: http://localhost:9090/metrics"
    
    if docker-compose ps | grep -q nginx; then
        echo "  - Nginx 代理: http://localhost"
    fi
    
    if docker-compose ps | grep -q grafana; then
        echo "  - Grafana 监控: http://localhost:3000 (admin/admin123)"
    fi
    
    echo ""
    echo "配置文件位置: /opt/mcp/config"
    echo "日志文件位置: /opt/mcp/logs"
    echo "数据存储位置: /opt/mcp/data"
    
    echo ""
    echo "管理命令:"
    echo "  - 查看服务状态: cd $SCRIPT_DIR/docker && docker-compose ps"
    echo "  - 查看服务日志: cd $SCRIPT_DIR/docker && docker-compose logs -f"
    echo "  - 重启服务: cd $SCRIPT_DIR/docker && docker-compose restart"
}

# 主函数
main() {
    check_dependencies
    configure_environment
    create_directories
    deploy_services
    verify_deployment
    show_access_info
}

# 执行主函数
main "$@"
DEPLOY_SCRIPT_EOF

chmod +x "$PACKAGE_DIR/deploy.sh"

# 生成卸载脚本
cat > "$PACKAGE_DIR/uninstall.sh" << 'UNINSTALL_SCRIPT_EOF'
#!/bin/bash

# MCP 卸载脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== MCP 卸载向导 ==="

# 确认卸载
read -p "确定要卸载 MCP 服务吗？这将删除所有数据。(y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消卸载"
    exit 0
fi

# 停止并删除容器
echo "停止并删除 Docker 容器..."
cd "$SCRIPT_DIR/docker"
docker-compose down --volumes --remove-orphans

# 删除 Docker 镜像（可选）
read -p "是否删除 Docker 镜像？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose down --rmi all
fi

# 删除本地数据（可选）
read -p "是否删除本地数据和配置？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo rm -rf /opt/mcp
fi

echo "✓ MCP 卸载完成"
UNINSTALL_SCRIPT_EOF

chmod +x "$PACKAGE_DIR/uninstall.sh"

echo "步骤 4: 生成文档..."

# 生成 README.md
cat > "$PACKAGE_DIR/README.md" << 'README_EOF'
# MCP 内网部署包

这是一个完整的 MCP (Model Context Protocol) 内网部署包，包含所有必要的组件和配置文件。

## 📦 包内容

- `app/` - MCP 应用程序代码
- `config/` - 配置文件
- `docker/` - Docker 相关配置
- `scripts/` - 部署和管理脚本
- `docs/guide/` - MCP 系统指南文档

## 🚀 快速部署

### 前置要求

- Linux 操作系统 (推荐 CentOS 7+/Ubuntu 18+)
- Docker 20.10+
- Docker Compose 1.29+
- 至少 2GB 内存
- 至少 10GB 可用磁盘空间

### 部署步骤

1. **解压部署包**
   ```bash
   tar -xzf mcp-server-*.tar.gz
   cd mcp-server-*
   ```

2. **配置环境变量**
   ```bash
   # 编辑配置文件
   vim config/.env
   
   # 至少修改以下关键配置：
   # MCP_SECRET_KEY=your-strong-secret-key
   # MCP_JWT_SECRET=your-jwt-secret
   # MCP_POSTGRES_PASSWORD=your-db-password
   # MCP_REDIS_PASSWORD=your-redis-password
   ```

3. **执行部署**
   ```bash
   sudo ./deploy.sh
   ```

4. **验证部署**
   ```bash
   curl http://localhost:8080/health
   ```

## 🔧 服务组件

### 核心服务

- **MCP Server** (端口 8080) - 主服务，提供 API 接口
- **Redis** (端口 6379) - 缓存服务
- **Metrics Server** (端口 9090) - 监控指标

### 可选服务

- **PostgreSQL** (端口 5432) - 生产数据库
- **Nginx** (端口 80/443) - 反向代理和负载均衡
- **Prometheus** (端口 9091) - 指标收集
- **Grafana** (端口 3000) - 监控面板

## 📊 访问地址

- MCP API: http://localhost:8080
- 健康检查: http://localhost:8080/health
- 监控指标: http://localhost:9090/metrics
- Grafana 监控: http://localhost:3000 (如启用)

## 🛠️ 管理命令

```bash
# 查看服务状态
cd docker && docker-compose ps

# 查看服务日志
cd docker && docker-compose logs -f

# 重启服务
cd docker && docker-compose restart

# 停止服务
cd docker && docker-compose stop

# 完全卸载
./uninstall.sh
```

## 📁 目录结构

```
/opt/mcp/
├── data/          # 数据存储
├── logs/          # 日志文件
├── config/        # 配置文件
├── skills/        # 技能插件
└── vectors/       # 向量数据库
```

## 🔐 安全配置

### 1. 修改默认密码

部署前务必修改以下配置：

```bash
# config/.env
MCP_SECRET_KEY=your-very-strong-secret-key
MCP_JWT_SECRET=your-jwt-secret-key
MCP_POSTGRES_PASSWORD=your-db-password
MCP_REDIS_PASSWORD=your-redis-password
MCP_GRAFANA_PASSWORD=your-grafana-password
```

### 2. 网络访问控制

默认配置允许所有 IP 访问，生产环境建议限制：

```nginx
# nginx.conf 中添加 IP 白名单
allow 192.168.1.0/24;
deny all;
```

### 3. SSL/TLS 配置

生产环境建议启用 HTTPS：

```bash
# 生成 SSL 证书
mkdir -p /opt/mcp/ssl
openssl req -x509 -newkey rsa:4096 -keyout /opt/mcp/ssl/key.pem \
    -out /opt/mcp/ssl/cert.pem -days 365 -nodes

# 修改 nginx.conf
# 取消 HTTPS 配置的注释
```

## 📈 监控和日志

### 日志位置

- 应用日志: `/opt/mcp/logs/mcp-server.log`
- Nginx 日志: `/opt/mcp/logs/nginx.log`
- Supervisor 日志: `/opt/mcp/logs/supervisord.log`

### 监控指标

访问 http://localhost:9090/metrics 查看 Prometheus 格式的指标。

### Grafana 面板

如果启用监控服务，可访问 http://localhost:3000 查看监控面板：
- 用户名: admin
- 密码: admin123 (请修改)

## 🔧 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   # 检查端口占用
   netstat -tlnp | grep :8080
   
   # 查看服务日志
   cd docker && docker-compose logs mcp-server
   ```

2. **健康检查失败**
   ```bash
   # 检查服务状态
   curl http://localhost:8080/health
   
   # 检查防火墙
   sudo firewall-cmd --list-all
   ```

3. **权限问题**
   ```bash
   # 检查目录权限
   ls -la /opt/mcp/
   
   # 修复权限
   sudo chown -R mcp:mcp /opt/mcp
   ```

### 日志分析

```bash
# 实时查看日志
tail -f /opt/mcp/logs/mcp-server.log

# 搜索错误
grep ERROR /opt/mcp/logs/mcp-server.log

# 查看特定时间段日志
grep "2024-01-01" /opt/mcp/logs/mcp-server.log
```

## 📞 技术支持

如遇问题，请：

1. 查看日志文件定位问题
2. 检查配置文件是否正确
3. 确认系统资源是否充足
4. 参考 MCP 系统指南文档

## 📄 许可证

本部署包遵循 MIT 许可证。
README_EOF

echo "步骤 5: 创建压缩包..."

# 创建压缩包
cd "/tmp"
tar -czf "$PACKAGE_NAME.tar.gz" "$PACKAGE_NAME"

# 移动到输出目录
mv "$PACKAGE_NAME.tar.gz" "$OUTPUT_DIR/"

# 清理临时目录
rm -rf "$PACKAGE_DIR"

echo ""
echo "=== 打包完成 ==="
echo "包文件: $OUTPUT_DIR/$PACKAGE_NAME.tar.gz"
echo "大小: $(du -h "$OUTPUT_DIR/$PACKAGE_NAME.tar.gz" | cut -f1)"
echo ""
echo "部署包已准备就绪，可以传输到内网环境进行部署。"
echo "部署步骤请参考包内的 README.md 文件。"