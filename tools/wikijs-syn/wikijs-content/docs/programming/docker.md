# Docker

Docker 容器化技术学习笔记。

## 基础概念

### 镜像 (Image)
只读的模板，用于创建容器。

### 容器 (Container)
镜像的运行实例。

### 仓库 (Repository)
存储镜像的地方。

## 常用命令

### 镜像操作

```bash
# 拉取镜像
docker pull ubuntu:20.04

# 查看本地镜像
docker images

# 删除镜像
docker rmi <image-id>
```

### 容器操作

```bash
# 运行容器
docker run -d -p 8080:80 nginx

# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 停止容器
docker stop <container-id>

# 启动容器
docker start <container-id>

# 删除容器
docker rm <container-id>
```

## Docker Compose

Docker Compose 用于定义和运行多容器应用。

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "80:80"

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
```

### 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f
```

## 最佳实践

- 使用多阶段构建减小镜像大小
- 使用 `.dockerignore` 排除不必要的文件
- 使用非 root 用户运行容器
- 定期更新基础镜像

## 资源

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
