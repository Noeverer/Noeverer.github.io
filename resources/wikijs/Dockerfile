# Wiki.js Docker 镜像构建文件
# 基于官方镜像进行自定义配置

FROM ghcr.io/requarks/wiki:latest

# 设置时区
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的工具
RUN apk add --no-cache \
    git \
    openssh-client \
    tzdata

# 创建 Git SSH 密钥目录
RUN mkdir -p /wiki/data/git && \
    chmod 700 /wiki/data/git

# 复制自定义配置
COPY config.yml /wiki/config.yml

# 设置工作目录
WORKDIR /wiki

# 暴露端口
EXPOSE 3000

# 启动 Wiki.js
CMD ["node", "server"]
