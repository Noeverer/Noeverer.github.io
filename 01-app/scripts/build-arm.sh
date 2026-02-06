#!/bin/bash
# ARM架构构建脚本（带NPU支持）

set -e

VERSION="1.0.0"
IMAGE_NAME="ascend-npu-app"

echo "======================================"
echo "ARM64架构构建（带NPU支持）"
echo "======================================"
echo ""

# 检查架构
ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
    echo "警告: 当前架构为 $ARCH，此脚本专为ARM64设计"
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查NPU驱动
echo "[1/4] 检查NPU驱动..."
if [ -d "/usr/local/Ascend/driver" ]; then
    echo "✓ 昇腾驱动已安装"
    if which npu-smi >/dev/null 2>&1; then
        npu-smi info
    fi
else
    echo "警告: 未检测到昇腾驱动"
fi

# 检查Docker
echo ""
echo "[2/4] 检查Docker..."
if ! which docker >/dev/null 2>&1; then
    echo "错误: Docker未安装"
    exit 1
fi
echo "✓ Docker已安装: $(docker --version)"

# 构建ARM镜像
echo ""
echo "[3/4] 构建ARM64 Docker镜像..."
docker build \
    --build-arg TARGETARCH=arm64 \
    --tag ${IMAGE_NAME}:${VERSION}-arm64 \
    --tag ${IMAGE_NAME}:latest-arm64 \
    -f Dockerfile.multiarch \
    .

echo "✓ ARM64镜像构建完成"

# 保存镜像
echo ""
echo "[4/4] 保存镜像..."
mkdir -p ./docker-images
docker save ${IMAGE_NAME}:${VERSION}-arm64 > ./docker-images/${IMAGE_NAME}-${VERSION}-arm64.tar
docker save ubuntu:22.04 > ./docker-images/ubuntu-22.04-arm64.tar 2>/dev/null || true

echo "✓ 镜像已保存到 ./docker-images/"

# 显示信息
echo ""
echo "======================================"
echo "构建完成！"
echo "======================================"
echo ""
docker images ${IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
echo ""
echo "使用方法（带NPU）:"
echo "  docker run -d --name ascend-app \\"
echo "    --device /dev/davinci0 \\"
echo "    --device /dev/davinci_manager \\"
echo "    --device /dev/devmm_svm \\"
echo "    -p 9999:9999 \\"
echo "    ${IMAGE_NAME}:${VERSION}-arm64"
echo ""
