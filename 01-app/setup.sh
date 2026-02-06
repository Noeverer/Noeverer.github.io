#!/bin/bash
# 昇腾NPU环境搭建脚本
# 适用于ARM架构服务器

set -e

echo "======================================"
echo "昇腾NPU环境搭建脚本"
echo "======================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为ARM架构
check_architecture() {
    echo -e "${YELLOW}[1/8] 检查系统架构...${NC}"
    ARCH=$(uname -m)
    if [ "$ARCH" != "aarch64" ]; then
        echo -e "${RED}警告: 当前架构为 $ARCH，此脚本针对ARM64(aarch64)架构优化${NC}"
        read -p "是否继续? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo -e "${GREEN}✓ 检测到ARM64架构${NC}"
    fi
}

# 检查昇腾驱动
check_ascend_driver() {
    echo -e "${YELLOW}[2/8] 检查昇腾驱动...${NC}"
    if [ -d "/usr/local/Ascend/driver" ]; then
        echo -e "${GREEN}✓ 昇腾驱动已安装${NC}"
        
        # 检查NPU设备
        if [ -e "/dev/davinci0" ]; then
            echo -e "${GREEN}✓ NPU设备已识别${NC}"
            npu-smi info 2>/dev/null || echo "npu-smi命令不可用"
        else
            echo -e "${RED}✗ NPU设备未识别，请检查驱动安装${NC}"
        fi
    else
        echo -e "${RED}✗ 昇腾驱动未安装${NC}"
        echo "请从华为官网下载并安装CANN Toolkit和驱动"
        exit 1
    fi
}

# 安装系统依赖
install_dependencies() {
    echo -e "${YELLOW}[3/8] 安装系统依赖...${NC}"
    apt-get update
    apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        curl \
        vim \
        python3.10 \
        python3.10-dev \
        python3.10-venv \
        python3-pip \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        llvm \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev
    
    # 设置Python 3.10为默认
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
    
    echo -e "${GREEN}✓ 系统依赖安装完成${NC}"
}

# 安装Docker
install_docker() {
    echo -e "${YELLOW}[4/8] 安装Docker...${NC}"
    if ! which docker >/dev/null 2>&1; then
        curl -fsSL https://get.docker.com | sh
        usermod -aG docker $USER
        systemctl enable docker
        systemctl start docker
        echo -e "${GREEN}✓ Docker安装完成${NC}"
    else
        echo -e "${GREEN}✓ Docker已安装: $(docker --version)${NC}"
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        pip3 install docker-compose
        echo -e "${GREEN}✓ Docker Compose安装完成${NC}"
    else
        echo -e "${GREEN}✓ Docker Compose已安装${NC}"
    fi
}

# 安装CANN Toolkit
install_cann() {
    echo -e "${YELLOW}[5/8] 检查CANN Toolkit...${NC}"
    if [ -d "/usr/local/Ascend/ascend-toolkit" ]; then
        echo -e "${GREEN}✓ CANN Toolkit已安装${NC}"
        source /usr/local/Ascend/ascend-toolkit/set_env.sh 2>/dev/null || true
    else
        echo -e "${YELLOW}! CANN Toolkit未安装，请手动安装${NC}"
        echo "下载地址: https://www.hiascend.com/software/cann/community"
        echo "安装命令示例:"
        echo "  chmod +x Ascend-cann-toolkit_*.run"
        echo "  ./Ascend-cann-toolkit_*.run --install"
    fi
}

# 安装Python依赖
install_python_deps() {
    echo -e "${YELLOW}[6/8] 安装Python依赖...${NC}"
    python3 -m pip install --upgrade pip setuptools wheel
    
    # 设置pip镜像源（中国用户）
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
    
    # 安装基础依赖
    pip install flask gunicorn gevent eventlet requests numpy pillow opencv-python
    
    # 安装PyTorch CPU版本（NPU版本需要特殊安装）
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    
    # 安装transformers
    pip install transformers tokenizers sentencepiece
    
    # 安装OCR相关
    pip install paddlepaddle paddleocr pytesseract
    
    # 安装其他ML库
    pip install scikit-learn scipy matplotlib tqdm pandas datasets tensorboard
    
    echo -e "${GREEN}✓ Python依赖安装完成${NC}"
}

# 安装昇腾PyTorch插件
install_ascend_pytorch() {
    echo -e "${YELLOW}[7/8] 安装昇腾PyTorch插件...${NC}"
    
    # 检查是否需要安装torch_npu
    if python3 -c "import torch_npu" 2>/dev/null; then
        echo -e "${GREEN}✓ torch_npu已安装${NC}"
    else
        echo -e "${YELLOW}! torch_npu未安装，请从华为仓库安装${NC}"
        echo "安装命令:"
        echo "  pip install torch_npu -f https://download.pytorch.org/whl/torch_npu.html"
        echo "或从源码编译安装"
    fi
}

# 构建Docker镜像
build_docker_image() {
    echo -e "${YELLOW}[8/8] 构建Docker镜像...${NC}"
    
    # 创建必要的目录
    mkdir -p logs models data
    
    # 构建镜像
    docker-compose build
    
    echo -e "${GREEN}✓ Docker镜像构建完成${NC}"
}

# 显示使用说明
show_usage() {
    echo ""
    echo "======================================"
echo "安装完成！使用说明:"
    echo "======================================"
    echo ""
    echo "1. 启动服务:"
    echo "   docker-compose up -d"
    echo ""
    echo "2. 查看服务状态:"
    echo "   docker-compose ps"
    echo ""
    echo "3. 查看日志:"
    echo "   docker-compose logs -f app"
    echo ""
    echo "4. 停止服务:"
    echo "   docker-compose down"
    echo ""
    echo "5. API访问地址:"
    echo "   http://localhost:9999"
    echo ""
    echo "6. 测试API:"
    echo "   curl http://localhost:9999/health"
    echo ""
    echo "======================================"
}

# 主函数
main() {
    # 检查是否以root权限运行
    if [ "$EUID" -ne 0 ]; then 
        echo -e "${RED}请使用root权限运行此脚本${NC}"
        exit 1
    fi
    
    check_architecture
    check_ascend_driver
    install_dependencies
    install_docker
    install_cann
    install_python_deps
    install_ascend_pytorch
    build_docker_image
    
    echo ""
    echo -e "${GREEN}======================================"
    echo "环境搭建完成!"
    echo "======================================${NC}"
    
    show_usage
}

# 运行主函数
main
