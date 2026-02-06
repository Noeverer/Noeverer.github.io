#!/bin/bash
# 离线打包脚本 - 导出所有需要的文件到本地目录

set -e

# 配置
PACKAGE_NAME="ascend-npu-app-offline"
VERSION="1.0.0"
BUILD_DATE=$(date +%Y%m%d_%H%M%S)
ARCH=$(uname -m)
OUTPUT_DIR="./offline-packages/${PACKAGE_NAME}-${VERSION}-${ARCH}-${BUILD_DATE}"

echo "======================================"
echo "离线打包脚本"
echo "======================================"
echo "输出目录: ${OUTPUT_DIR}"
echo "架构: ${ARCH}"
echo "======================================"

# 创建目录
mkdir -p ${OUTPUT_DIR}/{docker-images,python-packages,scripts,docs}

# 1. 构建Docker镜像
echo ""
echo "[1/4] 构建Docker镜像..."
if [ "${ARCH}" = "aarch64" ]; then
    echo "构建ARM64镜像..."
    docker build --build-arg TARGETARCH=arm64 -t ${PACKAGE_NAME}:${VERSION} -f Dockerfile.multiarch .
elif [ "${ARCH}" = "x86_64" ]; then
    echo "构建x86_64镜像..."
    docker build --build-arg TARGETARCH=amd64 -t ${PACKAGE_NAME}:${VERSION} -f Dockerfile.multiarch .
else
    echo "错误: 不支持的架构 ${ARCH}"
    exit 1
fi
echo "✓ Docker镜像构建完成"

# 2. 导出Docker镜像
echo ""
echo "[2/4] 导出Docker镜像..."

# 保存应用镜像
echo "保存应用镜像..."
docker save ${PACKAGE_NAME}:${VERSION} | gzip > ${OUTPUT_DIR}/docker-images/${PACKAGE_NAME}-${VERSION}.tar.gz

# 保存基础镜像
echo "保存基础镜像..."
docker pull ubuntu:22.04
docker save ubuntu:22.04 | gzip > ${OUTPUT_DIR}/docker-images/ubuntu-22.04.tar.gz

# 列出所有镜像
echo ""
echo "已保存的镜像:"
ls -lh ${OUTPUT_DIR}/docker-images/

# 3. 导出Python依赖
echo ""
echo "[3/4] 导出Python依赖..."

# 创建临时容器来导出依赖
echo "从容器导出已安装的包..."
CONTAINER_ID=$(docker create ${PACKAGE_NAME}:${VERSION})
docker cp ${CONTAINER_ID}:/usr/local/lib/python3.10/dist-packages ./temp-packages 2>/dev/null || \
docker cp ${CONTAINER_ID}:/usr/lib/python3/dist-packages ./temp-packages 2>/dev/null || \
echo "使用pip download方式..."

# 如果容器复制失败，使用pip download
if [ ! -d "./temp-packages" ]; then
    echo "使用pip下载依赖..."
    # 安装pip-tools
    pip install pip-tools -q
    
    # 生成requirements-lock.txt
    pip-compile requirements.txt --output-file ${OUTPUT_DIR}/python-packages/requirements-lock.txt 2>/dev/null || \
    cp requirements.txt ${OUTPUT_DIR}/python-packages/requirements.txt
    
    # 下载wheel包
    pip download -r requirements.txt -d ${OUTPUT_DIR}/python-packages --only-binary=:all: 2>/dev/null || \
    pip download -r requirements.txt -d ${OUTPUT_DIR}/python-packages
else
    # 打包已安装的包
    echo "打包已安装的Python包..."
    tar -czf ${OUTPUT_DIR}/python-packages/python-packages.tar.gz -C ./temp-packages .
    rm -rf ./temp-packages
fi

docker rm ${CONTAINER_ID}

echo "✓ Python依赖导出完成"

# 4. 复制项目文件
echo ""
echo "[4/4] 复制项目文件..."

# 复制核心文件
cp -r app.py examples tests docker-compose.yml readme.md ${OUTPUT_DIR}/

# 复制脚本
cp -r start.sh setup.sh test_api.sh run-tests.sh ${OUTPUT_DIR}/scripts/ 2>/dev/null || true

# 创建安装脚本
cat > ${OUTPUT_DIR}/install.sh << 'EOFSCRIPT'
#!/bin/bash
# 离线安装脚本

set -e

INSTALL_DIR="/opt/ascend-npu-app"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================"
echo "离线安装"
echo "======================================"

# 检查root权限
if [ "$EUID" -ne 0 ]; then 
    echo "请使用root权限运行"
    exit 1
fi

# 创建安装目录
mkdir -p ${INSTALL_DIR}

# 加载Docker镜像
echo "[1/3] 加载Docker镜像..."
for img in ${SCRIPT_DIR}/docker-images/*.tar.gz; do
    if [ -f "$img" ]; then
        echo "加载: $(basename $img)"
        gunzip -c "$img" | docker load
    fi
done

# 复制项目文件
echo "[2/3] 复制项目文件..."
cp -r ${SCRIPT_DIR}/app.py ${INSTALL_DIR}/
cp -r ${SCRIPT_DIR}/examples ${INSTALL_DIR}/
cp -r ${SCRIPT_DIR}/tests ${INSTALL_DIR}/
cp -r ${SCRIPT_DIR}/docker-compose.yml ${INSTALL_DIR}/
cp -r ${SCRIPT_DIR}/readme.md ${INSTALL_DIR}/

# 设置权限
chmod +x ${INSTALL_DIR}/scripts/*.sh 2>/dev/null || true

echo "[3/3] 安装完成"
echo ""
echo "安装目录: ${INSTALL_DIR}"
echo ""
echo "启动服务:"
echo "  cd ${INSTALL_DIR}"
echo "  docker-compose up -d"
echo ""
EOFSCRIPT

chmod +x ${OUTPUT_DIR}/install.sh

# 创建README
cat > ${OUTPUT_DIR}/README-INSTALL.md << 'EOFREADME'
# 离线安装包

## 文件说明

- `docker-images/` - Docker镜像文件（.tar.gz格式）
- `python-packages/` - Python依赖包
- `scripts/` - 辅助脚本
- `app.py` - 主应用程序
- `examples/` - 示例代码
- `tests/` - 测试代码
- `install.sh` - 安装脚本

## 安装步骤

1. 将本目录传输到目标服务器

2. 运行安装脚本：
```bash
sudo ./install.sh
```

3. 启动服务：
```bash
cd /opt/ascend-npu-app
docker-compose up -d
```

4. 验证：
```bash
curl http://localhost:9999/health
```

## 手动加载镜像

如果自动安装失败，可以手动加载：

```bash
# 加载应用镜像
gunzip -c docker-images/ascend-npu-app-offline-1.0.0.tar.gz | docker load

# 加载基础镜像
gunzip -c docker-images/ubuntu-22.04.tar.gz | docker load

# 启动
docker-compose up -d
```
EOFREADME

echo "✓ 项目文件复制完成"

# 5. 生成校验和
echo ""
echo "[5/5] 生成校验文件..."
cd ${OUTPUT_DIR}
find . -type f -exec md5sum {} \; > checksums.md5
cd - > /dev/null

# 完成
echo ""
echo "======================================"
echo "打包完成！"
echo "======================================"
echo ""
echo "输出目录: ${OUTPUT_DIR}"
echo ""
echo "目录结构:"
tree -L 2 ${OUTPUT_DIR} 2>/dev/null || find ${OUTPUT_DIR} -maxdepth 2 -type f

echo ""
echo "总大小:"
du -sh ${OUTPUT_DIR}

echo ""
echo "打包文件:"
cd $(dirname ${OUTPUT_DIR})
tar -czf $(basename ${OUTPUT_DIR}).tar.gz $(basename ${OUTPUT_DIR})
echo "✓ 已创建: $(basename ${OUTPUT_DIR}).tar.gz"
cd - > /dev/null

echo ""
echo "使用方法:"
echo "  1. 将 ${OUTPUT_DIR}.tar.gz 传输到目标服务器"
echo "  2. 解压: tar -xzf ${OUTPUT_DIR}.tar.gz"
echo "  3. 安装: cd $(basename ${OUTPUT_DIR}) && sudo ./install.sh"
echo ""
echo "======================================"
