#!/bin/bash
# 多架构Docker镜像构建脚本

set -e

# 配置
IMAGE_NAME="ascend-npu-app"
VERSION="1.0.0"
PLATFORMS="linux/amd64,linux/arm64"

echo "======================================"
echo "多架构Docker镜像构建"
echo "======================================"
echo "镜像名称: ${IMAGE_NAME}"
echo "版本: ${VERSION}"
echo "目标平台: ${PLATFORMS}"
echo "======================================"

# 检查docker buildx
echo "[1/5] 检查Docker Buildx..."
if ! docker buildx version >/dev/null 2>&1; then
    echo "错误: Docker Buildx 未安装"
    echo "请安装 Docker 20.10+ 版本"
    exit 1
fi
echo "✓ Docker Buildx 已安装"

# 创建buildx构建器
echo "[2/5] 创建多架构构建器..."
BUILDER_NAME="multiarch-builder"
if ! docker buildx ls | grep -q ${BUILDER_NAME}; then
    docker buildx create --name ${BUILDER_NAME} --driver docker-container --bootstrap
fi
docker buildx use ${BUILDER_NAME}
docker buildx inspect --bootstrap
echo "✓ 构建器准备完成"

# 为ARM64单独构建（带NPU支持）
echo ""
echo "[3/5] 构建 ARM64 镜像（带NPU支持）..."
docker buildx build \
    --platform linux/arm64 \
    --tag ${IMAGE_NAME}:${VERSION}-arm64 \
    --tag ${IMAGE_NAME}:latest-arm64 \
    --build-arg TARGETARCH=arm64 \
    -f Dockerfile.multiarch \
    --load \
    .

echo "✓ ARM64 镜像构建完成"

# 为x86_64单独构建（无NPU支持）
echo ""
echo "[4/5] 构建 x86_64 镜像..."
docker buildx build \
    --platform linux/amd64 \
    --tag ${IMAGE_NAME}:${VERSION}-amd64 \
    --tag ${IMAGE_NAME}:latest-amd64 \
    --build-arg TARGETARCH=amd64 \
    -f Dockerfile.multiarch \
    --load \
    .

echo "✓ x86_64 镜像构建完成"

# 创建多架构manifest
echo ""
echo "[5/5] 创建多架构Manifest..."
docker buildx build \
    --platform ${PLATFORMS} \
    --tag ${IMAGE_NAME}:${VERSION} \
    --tag ${IMAGE_NAME}:latest \
    -f Dockerfile.multiarch \
    --push \
    . 2>/dev/null || \
docker manifest create ${IMAGE_NAME}:${VERSION} \
    ${IMAGE_NAME}:${VERSION}-amd64 \
    ${IMAGE_NAME}:${VERSION}-arm64

echo "✓ 多架构Manifest创建完成"

# 查看镜像信息
echo ""
echo "======================================"
echo "镜像构建完成！"
echo "======================================"
echo ""
docker images ${IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
echo ""
echo "镜像列表:"
echo "  - ${IMAGE_NAME}:${VERSION}-amd64 (x86_64)"
echo "  - ${IMAGE_NAME}:${VERSION}-arm64 (ARM64)"
echo "  - ${IMAGE_NAME}:${VERSION} (多架构)"
echo ""
echo "使用方法:"
echo "  # ARM64 (带NPU支持)"
echo "  docker run -d --name ascend-app-arm64 \\"
echo "    --device /dev/davinci0 \\"
echo "    -p 9999:9999 \\"
echo "    ${IMAGE_NAME}:${VERSION}-arm64"
echo ""
echo "  # x86_64"
echo "  docker run -d --name ascend-app-amd64 \\"
echo "    -p 9999:9999 \\"
echo "    ${IMAGE_NAME}:${VERSION}-amd64"
echo ""
echo "  # 自动选择架构"
echo "  docker run -d --name ascend-app \\"
echo "    -p 9999:9999 \\"
echo "    ${IMAGE_NAME}:${VERSION}"
echo ""
echo "======================================"
