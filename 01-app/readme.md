# Python 3.10 在昇腾机器ARM上环境搭建

本项目提供了一个完整的昇腾NPU（Ascend 310）推理和训练环境搭建方案，基于Python 3.10和ARM64架构。

## 功能特性

- **Python 3.10**: 使用最新稳定版Python
- **Docker容器化**: 完整的Docker镜像和编排配置
- **高并发框架**: 基于Flask + Gunicorn，支持端口9999
- **NPU支持**: 支持昇腾310/310P芯片的推理和训练
- **深度学习框架**: TensorFlow、PyTorch（含NPU版本）
- **NLP示例**: 基于BERT的中文文本分类（推理和训练）
- **OCR示例**: 基于PaddleOCR/EasyOCR的文字识别（推理和训练）

## 项目结构

```
.
├── app.py                      # Flask主应用
├── Dockerfile                  # Docker镜像构建文件
├── docker-compose.yml          # Docker编排配置
├── requirements.txt            # Python依赖
├── setup.sh                    # 环境搭建脚本
├── start.sh                    # 服务启动脚本
├── test_api.sh                 # API测试脚本
├── readme.md                   # 说明文档
└── examples/                   # 示例代码目录
    ├── __init__.py
    ├── nlp_inference.py        # NLP推理示例
    ├── nlp_training.py         # NLP训练示例
    ├── ocr_inference.py        # OCR推理示例
    └── ocr_training.py         # OCR训练示例
```

## 快速开始

### 1. 环境要求

- ARM64架构服务器
- 已安装昇腾驱动和CANN Toolkit
- Ubuntu 20.04/22.04 或 CentOS 7/8
- Docker 20.10+
- Docker Compose 1.29+

### 2. 自动安装（推荐）

```bash
# 使用root权限运行
sudo ./setup.sh
```

该脚本会自动完成：
- 系统架构检查
- 昇腾驱动检查
- 系统依赖安装
- Docker安装
- Python依赖安装
- Docker镜像构建

### 3. 手动安装

#### 3.1 安装系统依赖

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-dev python3-pip docker.io docker-compose
```

#### 3.2 安装CANN Toolkit

从华为官网下载并安装：
```bash
# 下载地址: https://www.hiascend.com/software/cann/community
chmod +x Ascend-cann-toolkit_*_linux-aarch64.run
./Ascend-cann-toolkit_*_linux-aarch64.run --install
```

#### 3.3 安装Python依赖

```bash
pip3 install -r requirements.txt
```

#### 3.4 构建Docker镜像

```bash
docker-compose build
```

### 4. 启动服务

```bash
# 使用启动脚本
./start.sh

# 或使用docker-compose
docker-compose up -d
```

服务启动后，可以通过以下地址访问：
- **API地址**: http://localhost:9999
- **健康检查**: http://localhost:9999/health

### 5. 测试API

```bash
./test_api.sh
```

## API接口说明

### 基础接口

#### 服务状态
```bash
GET /
```

#### 健康检查
```bash
GET /health
```

#### NPU状态
```bash
GET /npu/status
```

### NLP接口

#### NLP推理
```bash
POST /nlp/inference
Content-Type: application/json

{
  "text": "这是一个测试文本",
  "model": "bert-base-chinese"
}
```

#### NLP训练
```bash
POST /nlp/training
Content-Type: application/json

{
  "model": "bert-base-chinese",
  "epochs": 3,
  "batch_size": 16,
  "learning_rate": 2e-5
}
```

### OCR接口

#### OCR推理
```bash
POST /ocr/inference
Content-Type: multipart/form-data

image: <图片文件>
model: paddleocr
```

#### OCR训练
```bash
POST /ocr/training
Content-Type: application/json

{
  "model": "ch_PP-OCRv4",
  "epochs": 100,
  "batch_size": 128
}
```

## NLP示例详解

### 推理示例

```python
from examples.nlp_inference import NLPPredictor

# 创建预测器
predictor = NLPPredictor(
    model_name="bert-base-chinese",
    use_npu=True  # 使用NPU
)

# 单条推理
result = predictor.predict("这是一个非常好的产品！")
print(f"预测结果: {result['predicted_class']}")
print(f"置信度: {result['confidence']:.4f}")

# 批量推理
texts = ["文本1", "文本2", "文本3"]
results = predictor.batch_predict(texts)
```

### 训练示例

```python
from examples.nlp_training import NLPTrainer

# 创建训练器
trainer = NLPTrainer(
    model_name="bert-base-chinese",
    num_labels=2,
    use_npu=True,
    output_dir="./models/my_model"
)

# 训练数据
train_texts = ["正例1", "负例1", "正例2"]
train_labels = [1, 0, 1]

# 开始训练
result = trainer.train(
    train_texts=train_texts,
    train_labels=train_labels,
    epochs=3,
    batch_size=16
)
```

## OCR示例详解

### 推理示例

```python
from examples.ocr_inference import OCREngine

# 创建OCR引擎
ocr = OCREngine(
    model_type="paddleocr",  # 或 "easyocr"
    use_npu=True,
    lang="ch"  # 中文
)

# 识别图片
result = ocr.recognize("/path/to/image.jpg")
print(f"识别文本: {result['full_text']}")
print(f"置信度: {result['scores']}")
```

### 训练示例

```python
from examples.ocr_training import OCRTrainer

# 创建训练器
trainer = OCRTrainer(
    model_type="ch_PP-OCRv4",
    use_npu=True,
    output_dir="./models/ocr_model"
)

# 准备数据
train_data = [
    {"image_path": "img1.jpg", "label": "文本1"},
    {"image_path": "img2.jpg", "label": "文本2"}
]

# 开始训练
result = trainer.train(
    train_data=train_data,
    epochs=100,
    batch_size=128
)
```

## 高并发配置

本项目使用Gunicorn作为WSGI服务器，配置了以下参数：

- **Worker数**: 4（根据CPU核心数调整）
- **Worker类型**: gevent（协程模式）
- **端口**: 9999
- **超时**: 120秒
- **最大请求数**: 1000（自动重启，防止内存泄漏）

可通过修改`docker-compose.yml`调整并发参数：

```yaml
command: >
  gunicorn -w 8  # 增加worker数
  -k gevent
  --bind 0.0.0.0:9999
  --timeout 300  # 增加超时时间
  ...
```

## 昇腾NPU配置

### 安装NPU驱动

确保已安装昇腾驱动和固件：
```bash
# 检查驱动
npu-smi info

# 检查设备
ls -l /dev/davinci*
```

### PyTorch NPU支持

安装torch_npu插件：
```bash
# 方法1: 使用预编译包
pip install torch_npu -f https://download.pytorch.org/whl/torch_npu.html

# 方法2: 从源码编译
git clone https://gitee.com/ascend/pytorch.git
cd pytorch
bash ci/build.sh --python=3.10
```

### Paddle NPU支持

安装paddle-custom-npu：
```bash
pip install paddlepaddle==2.5.1
pip install paddle-custom-npu
```

## 日志和监控

### 查看日志

```bash
# 查看应用日志
docker-compose logs -f app

# 查看错误日志
tail -f logs/error.log
```

### TensorBoard

```bash
# 启动TensorBoard服务
docker-compose --profile monitoring up -d tensorboard

# 访问 http://localhost:6006
```

### Jupyter Notebook

```bash
# 启动Jupyter服务
docker-compose --profile dev up -d jupyter

# 访问 http://localhost:8888
```

## 常见问题

### 1. NPU设备未找到

```bash
# 检查驱动
npu-smi info

# 检查设备节点
ls -l /dev/davinci*

# 如果设备不存在，重新加载驱动
modprobe drv
```

### 2. Docker无法访问NPU

确保docker-compose.yml中正确挂载了设备：
```yaml
devices:
  - /dev/davinci0:/dev/davinci0
  - /dev/davinci_manager:/dev/davinci_manager
```

### 3. 内存不足

调整batch_size或减小模型规模：
```python
# NLP训练
trainer.train(batch_size=8)  # 减小batch_size

# OCR训练
trainer.train(batch_size=64)  # 减小batch_size
```

### 4. 模型下载失败

设置镜像源：
```bash
# HuggingFace镜像
export HF_ENDPOINT=https://hf-mirror.com

# PyTorch镜像
pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 性能优化建议

1. **使用混合精度训练**
```python
trainer.train(fp16=True)  # 启用FP16
```

2. **调整Worker数**
根据CPU核心数调整Gunicorn worker数量。

3. **启用NPU图优化**
```python
# PyTorch
import torch_npu
torch.npu.set_compile_mode(jit_compile=False)
```

4. **数据预处理优化**
使用多进程数据加载：
```python
DataLoader(num_workers=4, pin_memory=True)
```

## 许可证

MIT License

## 联系方式

如有问题，请提交Issue或联系维护者。
