# 使用官方 Wiki.js 镜像作为基础镜像
FROM ghcr.io/requarks/wiki:2

# 设置工作目录
WORKDIR /wiki

# 复制配置文件（如果有的话）
# COPY config.yml /wiki/config.yml

# 暴露端口
EXPOSE 3000

# 启动 Wiki.js
CMD ["node", "server"]