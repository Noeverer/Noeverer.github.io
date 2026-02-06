#!/bin/bash
# 导出Docker镜像到本地文件夹（不需要重新构建）

set -e

OUTPUT_DIR="./docker-export-$(date +%Y%m%d_%H%M%S)"

echo "======================================"
echo "Docker镜像导出工具"
echo "======================================"

mkdir -p ${OUTPUT_DIR}

# 检查现有镜像
echo ""
echo "检查现有镜像..."
docker images ascend-npu-app --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# 导出镜像
echo ""
echo "导出镜像到 ${OUTPUT_DIR}/..."

# 导出应用镜像（带压缩）
if docker images ascend-npu-app:latest -q | grep -q .; then
    echo "导出 ascend-npu-app:latest..."
    docker save ascend-npu-app:latest | gzip > ${OUTPUT_DIR}/ascend-npu-app-latest.tar.gz
    echo "✓ 已导出: ascend-npu-app-latest.tar.gz"
fi

# 导出版本标签
if docker images ascend-npu-app:1.0.0 -q | grep -q .; then
    echo "导出 ascend-npu-app:1.0.0..."
    docker save ascend-npu-app:1.0.0 | gzip > ${OUTPUT_DIR}/ascend-npu-app-1.0.0.tar.gz
    echo "✓ 已导出: ascend-npu-app-1.0.0.tar.gz"
fi

# 导出ARM版本
if docker images ascend-npu-app:latest-arm64 -q | grep -q .; then
    echo "导出 ascend-npu-app:latest-arm64..."
    docker save ascend-npu-app:latest-arm64 | gzip > ${OUTPUT_DIR}/ascend-npu-app-arm64.tar.gz
    echo "✓ 已导出: ascend-npu-app-arm64.tar.gz"
fi

# 导出x86版本
if docker images ascend-npu-app:latest-amd64 -q | grep -q .; then
    echo "导出 ascend-npu-app:latest-amd64..."
    docker save ascend-npu-app:latest-amd64 | gzip > ${OUTPUT_DIR}/ascend-npu-app-amd64.tar.gz
    echo "✓ 已导出: ascend-npu-app-amd64.tar.gz"
fi

# 导出基础镜像
echo ""
echo "导出基础镜像..."
docker save ubuntu:22.04 | gzip > ${OUTPUT_DIR}/ubuntu-22.04.tar.gz
echo "✓ 已导出: ubuntu-22.04.tar.gz"

# 创建加载脚本
cat > ${OUTPUT_DIR}/load-images.sh << 'EOF'
#!/bin/bash
# 加载Docker镜像脚本

echo "加载Docker镜像..."
for img in *.tar.gz; do
    if [ -f "$img" ]; then
        echo "加载: $img"
        gunzip -c "$img" | docker load
    fi
done
echo "✓ 所有镜像加载完成"
echo ""
docker images | grep -E "(ascend-npu-app|ubuntu)"
EOF

chmod +x ${OUTPUT_DIR}/load-images.sh

# 创建使用说明
cat > ${OUTPUT_DIR}/README.txt << EOF
Docker镜像导出包
================

导出时间: $(date)

文件列表:
$(ls -lh ${OUTPUT_DIR}/*.tar.gz 2>/dev/null || echo "无tar.gz文件")

使用方法:

1. 加载镜像:
   ./load-images.sh
   
   或手动加载:
   gunzip -c ascend-npu-app-latest.tar.gz | docker load

2. 查看镜像:
   docker images

3. 启动服务:
   docker-compose up -d

注意:
- 需要Docker环境
- 需要足够的磁盘空间
EOF

echo ""
echo "======================================"
echo "导出完成！"
echo "======================================"
echo ""
echo "输出目录: ${OUTPUT_DIR}"
echo ""
echo "文件列表:"
ls -lh ${OUTPUT_DIR}/
echo ""
echo "总大小:"
du -sh ${OUTPUT_DIR}
echo ""
echo "使用方法:"
echo "  1. 将 ${OUTPUT_DIR}/ 传输到目标服务器"
echo "  2. 在目标服务器运行: ./load-images.sh"
echo "  3. 启动服务: docker-compose up -d"
echo ""
