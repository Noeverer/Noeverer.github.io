#!/bin/bash
# x86架构构建脚本（用于在内网环境构建）

set -e

VERSION="1.0.0"
IMAGE_NAME="ascend-npu-app"

echo "======================================"
echo "x86_64架构构建"
echo "======================================"
echo ""

# 检查Docker
echo "[1/3] 检查Docker..."
if ! which docker >/dev/null 2>&1; then
    echo "错误: Docker未安装"
    exit 1
fi
echo "✓ Docker已安装: $(docker --version)"

# 构建x86镜像
echo ""
echo "[2/3] 构建x86_64 Docker镜像..."
docker build \
    --build-arg TARGETARCH=amd64 \
    --tag ${IMAGE_NAME}:${VERSION}-amd64 \
    --tag ${IMAGE_NAME}:latest-amd64 \
    -f Dockerfile.multiarch \
    .

echo "✓ x86_64镜像构建完成"

# 保存镜像
echo ""
echo "[3/3] 保存镜像..."
mkdir -p ./docker-images
docker save ${IMAGE_NAME}:${VERSION}-amd64 > ./docker-images/${IMAGE_NAME}-${VERSION}-amd64.tar
docker save ubuntu:22.04 > ./docker-images/ubuntu-22.04-amd64.tar 2>/dev/null || true

echo "✓ 镜像已保存到 ./docker-images/"

# 显示信息
echo ""
echo "======================================"
echo "构建完成！"
echo "======================================"
echo ""
docker images ${IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
echo ""
echo "使用方法:"
echo "  docker run -d -p 9999:9999 ${IMAGE_NAME}:${VERSION}-amd64"
echo ""
