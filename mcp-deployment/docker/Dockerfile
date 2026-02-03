# MCP 内网部署 Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /opt/mcp

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    git \
    sqlite3 \
    redis-tools \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 创建应用用户
RUN useradd -m -u 1000 mcp && \
    mkdir -p /opt/mcp/{data,logs,config,skills,vectors} && \
    chown -R mcp:mcp /opt/mcp

# 复制 requirements 文件
COPY requirements.txt .
COPY requirements-prod.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements-prod.txt

# 复制应用代码
COPY . .

# 复制配置文件
COPY mcp-deployment/config/mcp-config.json /opt/mcp/config/
COPY mcp-deployment/docker/supervisord.conf /etc/supervisor/conf.d/
COPY mcp-deployment/docker/nginx.conf /etc/nginx/sites-available/

# 设置权限
RUN chmod +x scripts/*.sh && \
    chown -R mcp:mcp /opt/mcp

# 切换到应用用户
USER mcp

# 暴露端口
EXPOSE 8080 9090

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 启动命令
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]