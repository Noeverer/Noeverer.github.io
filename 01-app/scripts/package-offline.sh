#!/bin/bash
# 离线安装包打包脚本
# 用于内网环境部署

set -e

# 配置
PACKAGE_NAME="ascend-npu-app-offline"
PACKAGE_VERSION="1.0.0"
BUILD_DATE=$(date +%Y%m%d)
ARCH=$(uname -m)
OUTPUT_DIR="./offline-packages/${PACKAGE_NAME}-${PACKAGE_VERSION}-${ARCH}-${BUILD_DATE}"

echo "======================================"
echo "离线安装包打包脚本"
echo "======================================"
echo "包名: ${PACKAGE_NAME}"
echo "版本: ${PACKAGE_VERSION}"
echo "架构: ${ARCH}"
echo "输出目录: ${OUTPUT_DIR}"
echo "======================================"

# 创建目录结构
mkdir -p ${OUTPUT_DIR}/{docker-images,python-packages,models,docs,scripts,config}

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[1/8] 打包Docker镜像...${NC}"

# 构建Docker镜像
docker build -t ascend-npu-app:${PACKAGE_VERSION} -f Dockerfile .

# 保存Docker镜像
docker save ascend-npu-app:${PACKAGE_VERSION} > ${OUTPUT_DIR}/docker-images/ascend-npu-app.tar
echo -e "${GREEN}✓ Docker镜像已保存${NC}"

# 保存基础镜像
BASE_IMAGES=("ubuntu:22.04")
for img in "${BASE_IMAGES[@]}"; do
    docker pull ${img} 2>/dev/null || true
    if docker images ${img} | grep -q ${img}; then
        filename=$(echo ${img} | tr '/' '_' | tr ':' '_')
        docker save ${img} > ${OUTPUT_DIR}/docker-images/${filename}.tar
        echo -e "${GREEN}✓ 基础镜像 ${img} 已保存${NC}"
    fi
done

echo -e "${YELLOW}[2/8] 下载Python依赖包...${NC}"

# 创建虚拟环境
python3 -m venv /tmp/venv_package
cd /tmp/venv_package
source bin/activate

# 升级pip
pip install --upgrade pip setuptools wheel

# 下载所有依赖包
pip download \
    -r ${OLDPWD}/requirements.txt \
    -d ${OLDPWD}/${OUTPUT_DIR}/python-packages \
    --only-binary=:all: \
    --platform manylinux2014_aarch64 \
    --python-version 310 \
    --implementation cp 2>/dev/null || \
pip download \
    -r ${OLDPWD}/requirements.txt \
    -d ${OLDPWD}/${OUTPUT_DIR}/python-packages

cd ${OLDPWD}
deactivate
rm -rf /tmp/venv_package

echo -e "${GREEN}✓ Python依赖包已下载${NC}"

echo -e "${YELLOW}[3/8] 复制项目文件...${NC}"

# 复制项目文件
cp -r app.py requirements.txt Dockerfile docker-compose.yml *.sh readme.md ${OUTPUT_DIR}/
cp -r examples ${OUTPUT_DIR}/
cp -r tests ${OUTPUT_DIR}/ 2>/dev/null || true

echo -e "${GREEN}✓ 项目文件已复制${NC}"

echo -e "${YELLOW}[4/8] 创建安装脚本...${NC}"

cat > ${OUTPUT_DIR}/install.sh << 'EOF'
#!/bin/bash
# 离线安装脚本

set -e

INSTALL_DIR="/opt/ascend-npu-app"
PACKAGE_VERSION="1.0.0"

echo "======================================"
echo "昇腾NPU应用离线安装"
echo "======================================"

# 检查root权限
if [ "$EUID" -ne 0 ]; then
    echo "请使用root权限运行"
    exit 1
fi

# 检查架构
ARCH=$(uname -m)
echo "检测到架构: ${ARCH}"

# 安装Docker
echo "[1/5] 检查Docker..."
if ! which docker >/dev/null 2>&1; then
    echo "安装Docker..."
    # 从离线包安装Docker
    if [ -f "docker-packages/docker-ce.deb" ]; then
        dpkg -i docker-packages/*.deb
        systemctl enable docker
        systemctl start docker
    else
        echo "警告: 未找到Docker离线安装包"
        echo "请先手动安装Docker"
    fi
else
    echo "Docker已安装"
fi

# 加载Docker镜像
echo "[2/5] 加载Docker镜像..."
for img in docker-images/*.tar; do
    echo "加载镜像: ${img}"
    docker load < "${img}"
done

# 安装Python依赖
echo "[3/5] 安装Python依赖..."
python3 -m pip install --no-index --find-links=./python-packages -r requirements.txt

# 创建安装目录
echo "[4/5] 创建安装目录..."
mkdir -p ${INSTALL_DIR}
cp -r app.py examples tests *.sh *.yml readme.md ${INSTALL_DIR}/

# 设置权限
chmod +x ${INSTALL_DIR}/*.sh

# 创建系统服务
echo "[5/5] 创建系统服务..."
cat > /etc/systemd/system/ascend-npu-app.service << EOL
[Unit]
Description=Ascend NPU Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/start.sh
ExecStop=${INSTALL_DIR}/docker-compose down
User=root

[Install]
WantedBy=multi-user.target
EOL

systemctl daemon-reload
systemctl enable ascend-npu-app.service

echo ""
echo "======================================"
echo "安装完成！"
echo "======================================"
echo "安装目录: ${INSTALL_DIR}"
echo ""
echo "启动服务:"
echo "  cd ${INSTALL_DIR} && ./start.sh"
echo ""
echo "或使用systemd:"
echo "  systemctl start ascend-npu-app"
echo "======================================"
EOF

chmod +x ${OUTPUT_DIR}/install.sh

echo -e "${GREEN}✓ 安装脚本已创建${NC}"

echo -e "${YELLOW}[5/8] 创建内网部署指南...${NC}"

cat > ${OUTPUT_DIR}/docs/内网部署指南.md << 'EOF'
# 内网离线部署指南

## 环境要求

### 服务器配置
- CPU: ARM64架构 (aarch64) 或 x86_64
- 内存: 建议32GB以上
- 磁盘: 建议100GB以上可用空间
- NPU: 昇腾310/310P芯片（可选）

### 操作系统
- Ubuntu 20.04/22.04 LTS
- 或 CentOS 7.6/8.x

### 必需软件
- Docker 20.10+
- Docker Compose 1.29+
- Python 3.10

## 快速部署

### 1. 传输安装包

将离线安装包传输到目标服务器：

```bash
scp -r ascend-npu-app-offline-1.0.0-aarch64-20240101 user@server:/opt/
```

### 2. 执行安装

```bash
cd /opt/ascend-npu-app-offline-1.0.0-aarch64-20240101
sudo ./install.sh
```

### 3. 启动服务

```bash
# 方式1: 使用脚本
cd /opt/ascend-npu-app
./start.sh

# 方式2: 使用systemd
systemctl start ascend-npu-app
```

### 4. 验证部署

```bash
# 查看服务状态
docker-compose ps

# 测试API
curl http://localhost:9999/health

# 查看日志
docker-compose logs -f
```

## 配置说明

### Docker配置

编辑 `docker-compose.yml` 调整以下参数：

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 16G  # 内存限制
    environment:
      - WORKERS=4    # 工作进程数
```

### NPU配置

如果使用NPU，确保以下配置正确：

```yaml
device:
  - /dev/davinci0:/dev/davinci0
  - /dev/davinci_manager:/dev/davinci_manager
```

## 故障排查

### 问题1: Docker无法加载镜像

```bash
# 检查Docker服务
systemctl status docker

# 手动加载镜像
docker load < docker-images/ascend-npu-app.tar
```

### 问题2: 端口被占用

```bash
# 修改端口映射
# 编辑 docker-compose.yml
ports:
  - "8080:9999"  # 改为8080端口
```

### 问题3: 内存不足

```bash
# 创建swap分区
dd if=/dev/zero of=/swapfile bs=1G count=16
mkswap /swapfile
swapon /swapfile

# 永久生效
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### 问题4: NPU设备未找到

```bash
# 检查驱动
npu-smi info

# 检查设备
ls -l /dev/davinci*

# 如果没有设备，需要安装昇腾驱动
```

## 安全建议

1. **修改默认端口**
   - 将9999端口改为非标准端口
   
2. **配置防火墙**
   ```bash
   ufw allow 9999/tcp
   ufw enable
   ```

3. **限制访问IP**
   ```bash
   # 编辑docker-compose.yml
   ports:
     - "127.0.0.1:9999:9999"  # 仅本机访问
   ```

4. **定期备份**
   ```bash
   # 备份数据
tar -czf backup-$(date +%Y%m%d).tar.gz models/ data/ logs/
   ```

## 更新升级

### 保留数据升级

```bash
# 1. 停止服务
docker-compose down

# 2. 备份数据
cp -r models models.bak
cp -r data data.bak

# 3. 加载新镜像
docker load < docker-images/ascend-npu-app-new.tar

# 4. 更新docker-compose.yml
cp docker-compose.yml.new docker-compose.yml

# 5. 启动服务
docker-compose up -d
```

## 联系支持

如有问题，请联系技术支持。
EOF

echo -e "${GREEN}✓ 内网部署指南已创建${NC}"

echo -e "${YELLOW}[6/8] 创建依赖清单...${NC}"

# 创建依赖清单
cat > ${OUTPUT_DIR}/docs/依赖清单.txt << EOF
离线安装包说明
================
包名: ${PACKAGE_NAME}
版本: ${PACKAGE_VERSION}
架构: ${ARCH}
打包日期: ${BUILD_DATE}

包含内容:
---------
1. Docker镜像 (docker-images/)
   - ascend-npu-app:${PACKAGE_VERSION}
   - ubuntu:22.04 (基础镜像)

2. Python依赖包 (python-packages/)
   - 所有requirements.txt中的依赖
   - 共 $(ls ${OUTPUT_DIR}/python-packages/*.whl 2>/dev/null | wc -l) 个wheel包

3. 项目文件
   - app.py (主应用)
   - examples/ (示例代码)
   - tests/ (测试代码)
   - *.sh (脚本文件)
   - docker-compose.yml

安装要求:
---------
- 操作系统: Ubuntu 20.04/22.04 或 CentOS 7.6/8.x
- 架构: ${ARCH}
- 内存: 最少8GB，建议32GB
- 磁盘: 最少20GB可用空间

安装步骤:
---------
1. 解压安装包到目标服务器
2. 运行 sudo ./install.sh
3. 运行 ./start.sh 启动服务
4. 访问 http://server-ip:9999

注意事项:
---------
- 安装需要root权限
- 确保Docker已安装
- 如果使用NPU，确保驱动已安装
- 默认端口9999，如需修改请编辑docker-compose.yml
EOF

echo -e "${GREEN}✓ 依赖清单已创建${NC}"

echo -e "${YELLOW}[7/8] 打包压缩...${NC}"

# 压缩安装包
cd $(dirname ${OUTPUT_DIR})
tar -czf $(basename ${OUTPUT_DIR}).tar.gz $(basename ${OUTPUT_DIR})
cd ${OLDPWD}

echo -e "${GREEN}✓ 安装包已打包${NC}"

echo -e "${YELLOW}[8/8] 生成校验文件...${NC}"

# 生成MD5校验
cd $(dirname ${OUTPUT_DIR})
md5sum $(basename ${OUTPUT_DIR}).tar.gz > $(basename ${OUTPUT_DIR}).tar.gz.md5
cd ${OLDPWD}

echo -e "${GREEN}✓ 校验文件已生成${NC}"

echo ""
echo "======================================"
echo "打包完成！"
echo "======================================"
echo ""
echo "安装包位置:"
echo "  ${OUTPUT_DIR}.tar.gz"
echo ""
echo "校验文件:"
echo "  ${OUTPUT_DIR}.tar.gz.md5"
echo ""
echo "文件大小:"
du -h ${OUTPUT_DIR}.tar.gz
echo ""
echo "MD5校验值:"
cat ${OUTPUT_DIR}.tar.gz.md5
echo ""
echo "======================================"
