#!/bin/bash
# 内网导入脚本
# 用于在内网环境导入离线镜像和安装

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/opt/ascend-npu-app"
BACKUP_DIR="/opt/ascend-npu-app-backup"

echo "======================================"
echo "内网离线导入工具"
echo "======================================"
echo "脚本目录: ${SCRIPT_DIR}"
echo "安装目录: ${INSTALL_DIR}"
echo "======================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查root权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}错误: 需要使用root权限运行${NC}"
        exit 1
    fi
}

# 检测系统架构
detect_arch() {
    echo -e "${BLUE}[1/8] 检测系统架构...${NC}"
    ARCH=$(uname -m)
    case ${ARCH} in
        x86_64)
            PLATFORM="amd64"
            echo -e "${GREEN}✓ 检测到 x86_64 架构${NC}"
            ;;
        aarch64)
            PLATFORM="arm64"
            echo -e "${GREEN}✓ 检测到 ARM64 架构${NC}"
            ;;
        *)
            echo -e "${RED}错误: 不支持的架构 ${ARCH}${NC}"
            exit 1
            ;;
    esac
}

# 检查Docker
check_docker() {
    echo -e "${BLUE}[2/8] 检查Docker环境...${NC}"
    if ! which docker >/dev/null 2>&1; then
        echo -e "${YELLOW}! Docker未安装，尝试从离线包安装...${NC}"
        if [ -d "${SCRIPT_DIR}/docker-packages" ]; then
            install_docker_offline
        else
            echo -e "${RED}错误: 未找到Docker离线安装包${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✓ Docker已安装: $(docker --version)${NC}"
    fi
    
    # 检查Docker服务
    if ! systemctl is-active --quiet docker; then
        echo -e "${YELLOW}! 启动Docker服务...${NC}"
        systemctl start docker
        systemctl enable docker
    fi
}

# 离线安装Docker
install_docker_offline() {
    echo "从离线包安装Docker..."
    cd "${SCRIPT_DIR}/docker-packages"
    
    # Ubuntu/Debian
    if which dpkg >/dev/null 2>&1; then
        dpkg -i *.deb
    # CentOS/RHEL
    elif which rpm >/dev/null 2>&1; then
        rpm -ivh *.rpm --nodeps
    fi
    
    systemctl start docker
    systemctl enable docker
    echo -e "${GREEN}✓ Docker安装完成${NC}"
}

# 加载Docker镜像
load_images() {
    echo -e "${BLUE}[3/8] 加载Docker镜像...${NC}"
    
    if [ ! -d "${SCRIPT_DIR}/docker-images" ]; then
        echo -e "${RED}错误: 未找到docker-images目录${NC}"
        exit 1
    fi
    
    local loaded_count=0
    for img in ${SCRIPT_DIR}/docker-images/*.tar; do
        if [ -f "$img" ]; then
            echo "加载镜像: $(basename $img)"
            docker load < "$img"
            ((loaded_count++))
        fi
    done
    
    if [ $loaded_count -eq 0 ]; then
        echo -e "${RED}错误: 没有找到可加载的镜像文件${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 已加载 ${loaded_count} 个镜像${NC}"
}

# 备份现有安装
backup_existing() {
    echo -e "${BLUE}[4/8] 检查现有安装...${NC}"
    if [ -d "${INSTALL_DIR}" ]; then
        echo -e "${YELLOW}! 发现现有安装，创建备份...${NC}"
        BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
        mkdir -p ${BACKUP_DIR}
        cp -r ${INSTALL_DIR} ${BACKUP_DIR}/${BACKUP_NAME}
        echo -e "${GREEN}✓ 备份已创建: ${BACKUP_DIR}/${BACKUP_NAME}${NC}"
    else
        echo -e "${GREEN}✓ 未发现现有安装${NC}"
    fi
}

# 创建安装目录
setup_directories() {
    echo -e "${BLUE}[5/8] 创建安装目录...${NC}"
    mkdir -p ${INSTALL_DIR}/{logs,models,data,examples}
    echo -e "${GREEN}✓ 目录创建完成${NC}"
}

# 复制项目文件
copy_files() {
    echo -e "${BLUE}[6/8] 复制项目文件...${NC}"
    
    # 复制主要文件
    cp -r ${SCRIPT_DIR}/app.py ${INSTALL_DIR}/
    cp -r ${SCRIPT_DIR}/examples ${INSTALL_DIR}/
    cp -r ${SCRIPT_DIR}/tests ${INSTALL_DIR}/ 2>/dev/null || true
    cp -r ${SCRIPT_DIR}/*.yml ${INSTALL_DIR}/
    cp -r ${SCRIPT_DIR}/*.sh ${INSTALL_DIR}/
    cp -r ${SCRIPT_DIR}/readme.md ${INSTALL_DIR}/ 2>/dev/null || true
    
    # 创建日志目录
    touch ${INSTALL_DIR}/logs/access.log
    touch ${INSTALL_DIR}/logs/error.log
    
    # 设置权限
    chmod +x ${INSTALL_DIR}/*.sh
    chmod 666 ${INSTALL_DIR}/logs/*.log
    
    echo -e "${GREEN}✓ 文件复制完成${NC}"
}

# 安装Python依赖
install_python_deps() {
    echo -e "${BLUE}[7/8] 安装Python依赖...${NC}"
    
    # 检查是否有离线包
    if [ -d "${SCRIPT_DIR}/python-packages" ]; then
        echo "从离线包安装Python依赖..."
        python3 -m pip install --no-index --find-links=${SCRIPT_DIR}/python-packages \
            -r ${SCRIPT_DIR}/requirements.txt 2>/dev/null || \
        python3 -m pip install --no-index --find-links=${SCRIPT_DIR}/python-packages \
            flask numpy pillow torch transformers
    else
        echo -e "${YELLOW}! 未找到离线Python包，尝试在线安装...${NC}"
        python3 -m pip install -r ${SCRIPT_DIR}/requirements.txt
    fi
    
    echo -e "${GREEN}✓ Python依赖安装完成${NC}"
}

# 创建系统服务
create_service() {
    echo -e "${BLUE}[8/8] 创建系统服务...${NC}"
    
    cat > /etc/systemd/system/ascend-npu-app.service << EOF
[Unit]
Description=Ascend NPU Application
After=docker.service network.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/start.sh
ExecStop=/usr/local/bin/docker-compose -f ${INSTALL_DIR}/docker-compose.yml down
User=root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable ascend-npu-app.service
    
    echo -e "${GREEN}✓ 系统服务创建完成${NC}"
}

# 运行测试
run_tests() {
    echo ""
    echo -e "${BLUE}运行功能测试...${NC}"
    
    cd ${INSTALL_DIR}
    
    # 运行Python测试
    if [ -f "tests/test_functional.py" ]; then
        python3 tests/test_functional.py || true
    fi
    
    echo -e "${GREEN}✓ 测试完成${NC}"
}

# 显示完成信息
show_completion() {
    echo ""
    echo "======================================"
    echo -e "${GREEN}内网导入完成！${NC}"
    echo "======================================"
    echo ""
    echo "安装目录: ${INSTALL_DIR}"
    echo ""
    echo "启动服务:"
    echo "  cd ${INSTALL_DIR}"
    echo "  ./start.sh"
    echo ""
    echo "或使用systemd:"
    echo "  systemctl start ascend-npu-app"
    echo ""
    echo "查看状态:"
    echo "  docker-compose ps"
    echo "  curl http://localhost:9999/health"
    echo ""
    echo "查看日志:"
    echo "  docker-compose logs -f"
    echo ""
    echo "======================================"
}

# 主函数
main() {
    check_root
    detect_arch
    check_docker
    load_images
    backup_existing
    setup_directories
    copy_files
    install_python_deps
    create_service
    run_tests
    show_completion
}

# 执行主函数
main "$@"
