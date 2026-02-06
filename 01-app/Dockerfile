# 基于ARM架构的昇腾NPU环境Dockerfile
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.10
ENV ASCEND_BASE_PATH=/usr/local/Ascend

# 安装基础依赖
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    vim \
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
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python 3.10
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-dev python3.10-venv python3-pip && \
    ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.10 /usr/bin/python && \
    python3.10 -m pip install --upgrade pip setuptools wheel

# 设置pip镜像源（国内加速）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 创建工作目录
WORKDIR /app

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖（包括TensorFlow和PyTorch的NPU版本）
RUN pip install --no-cache-dir -r requirements.txt

# 安装昇腾CANN Toolkit（假设已经从华为官网下载）
# 注意：实际使用时需要替换为正确的CANN版本
RUN mkdir -p ${ASCEND_BASE_PATH}

# 安装Ascend包（这里假设已经挂载或复制了安装包）
# COPY Ascend-cann-toolkit_*_linux-aarch64.run /tmp/
# RUN chmod +x /tmp/Ascend-cann-toolkit_*_linux-aarch64.run && \
#     /tmp/Ascend-cann-toolkit_*_linux-aarch64.run --install --quiet && \
#     rm /tmp/Ascend-cann-toolkit_*_linux-aarch64.run

# 设置环境变量（CANN）
ENV PATH=${ASCEND_BASE_PATH}/latest/bin:${ASCEND_BASE_PATH}/latest/compiler/ccec_compiler/bin:${PATH}
ENV LD_LIBRARY_PATH=${ASCEND_BASE_PATH}/latest/lib64:${ASCEND_BASE_PATH}/latest/lib64/plugin/opskernel:${ASCEND_BASE_PATH}/latest/lib64/plugin/nnengine:${LD_LIBRARY_PATH}
ENV PYTHONPATH=${ASCEND_BASE_PATH}/latest/python/site-packages:${ASCEND_BASE_PATH}/latest/opp/built-in/op_impl/ai_core/tbe:${PYTHONPATH}
ENV ASCEND_OPP_PATH=${ASCEND_BASE_PATH}/latest/opp
ENV ASCEND_AICPU_PATH=${ASCEND_BASE_PATH}/latest
ENV ASCEND_HOME_PATH=${ASCEND_BASE_PATH}/latest
ENV TOOLCHAIN_HOME=${ASCEND_BASE_PATH}/latest/toolkit
ENV ASCEND_SLOG_PRINT_TO_STDOUT=0

# 暴露端口
EXPOSE 9999

# 设置工作目录
WORKDIR /app

# 默认命令
CMD ["python", "app.py"]
