#!/bin/bash
# API测试脚本

BASE_URL="http://localhost:9999"

echo "======================================"
echo "API测试脚本"
echo "======================================"

# 测试1: 健康检查
echo ""
echo "[1] 测试健康检查接口..."
curl -s "${BASE_URL}/health" | python3 -m json.tool

# 测试2: 服务状态
echo ""
echo "[2] 测试服务状态接口..."
curl -s "${BASE_URL}/" | python3 -m json.tool

# 测试3: NLP推理
echo ""
echo "[3] 测试NLP推理接口..."
curl -s -X POST "${BASE_URL}/nlp/inference" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是一个非常好的产品，强烈推荐！",
    "model": "bert-base-chinese"
  }' | python3 -m json.tool

# 测试4: NLP训练
echo ""
echo "[4] 测试NLP训练接口..."
curl -s -X POST "${BASE_URL}/nlp/training" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bert-base-chinese",
    "epochs": 2,
    "batch_size": 4
  }' | python3 -m json.tool

# 测试5: NPU状态
echo ""
echo "[5] 测试NPU状态接口..."
curl -s "${BASE_URL}/npu/status" | python3 -m json.tool

# 测试6: OCR推理（需要图片文件）
echo ""
echo "[6] 测试OCR推理接口..."
# 创建一个简单的测试图片
python3 << 'EOF'
from PIL import Image, ImageDraw, ImageFont
import os

img = Image.new('RGB', (400, 100), color='white')
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
except:
    font = ImageFont.load_default()
draw.text((50, 30), "Hello World", fill='black', font=font)
img.save("/tmp/test_ocr.jpg")
print("测试图片已创建: /tmp/test_ocr.jpg")
EOF

if [ -f "/tmp/test_ocr.jpg" ]; then
    curl -s -X POST "${BASE_URL}/ocr/inference" \
      -F "image=@/tmp/test_ocr.jpg" \
      -F "model=paddleocr" | python3 -m json.tool
    rm /tmp/test_ocr.jpg
fi

# 测试7: OCR训练
echo ""
echo "[7] 测试OCR训练接口..."
curl -s -X POST "${BASE_URL}/ocr/training" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ch_PP-OCRv4",
    "epochs": 10,
    "batch_size": 32
  }' | python3 -m json.tool

echo ""
echo "======================================"
echo "测试完成"
echo "======================================"
