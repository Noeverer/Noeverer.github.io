#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask应用主入口
支持高并发，运行在9999端口
支持NPU推理和训练任务
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 尝试导入NPU相关库
try:
    import acl
    NPU_AVAILABLE = True
    logger.info("NPU (Ascend) 环境已初始化")
except ImportError:
    NPU_AVAILABLE = False
    logger.warning("NPU环境未找到，将使用CPU模式")

# 首页 - 显示服务状态
@app.route('/')
def index():
    """服务状态页面"""
    status = {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "npu_available": NPU_AVAILABLE,
        "python_version": sys.version,
        "services": {
            "nlp_inference": "/nlp/inference",
            "nlp_training": "/nlp/training",
            "ocr_inference": "/ocr/inference",
            "ocr_training": "/ocr/training",
            "health": "/health"
        }
    }
    return jsonify(status)

# 健康检查接口
@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "npu_available": NPU_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    })

# NLP推理接口
@app.route('/nlp/inference', methods=['POST'])
def nlp_inference():
    """
    NLP推理接口
    接收文本，返回预测结果
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "请提供text字段"}), 400
        
        text = data['text']
        model_name = data.get('model', 'bert-base-chinese')
        
        # 这里调用NLP推理逻辑
        from examples.nlp_inference import run_inference
        result = run_inference(text, model_name, use_npu=NPU_AVAILABLE)
        
        return jsonify({
            "success": True,
            "text": text,
            "model": model_name,
            "result": result,
            "device": "NPU" if NPU_AVAILABLE else "CPU"
        })
    except Exception as e:
        logger.error(f"NLP推理错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# NLP训练接口
@app.route('/nlp/training', methods=['POST'])
def nlp_training():
    """
    NLP训练接口
    启动训练任务
    """
    try:
        data = request.get_json() or {}
        
        # 这里调用NLP训练逻辑
        from examples.nlp_training import start_training
        result = start_training(data, use_npu=NPU_AVAILABLE)
        
        return jsonify({
            "success": True,
            "message": "训练任务已启动",
            "result": result,
            "device": "NPU" if NPU_AVAILABLE else "CPU"
        })
    except Exception as e:
        logger.error(f"NLP训练错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# OCR推理接口
@app.route('/ocr/inference', methods=['POST'])
def ocr_inference():
    """
    OCR推理接口
    接收图片，返回识别结果
    """
    try:
        if 'image' not in request.files:
            return jsonify({"error": "请上传图片文件"}), 400
        
        image_file = request.files['image']
        model_type = request.form.get('model', 'paddleocr')
        
        # 这里调用OCR推理逻辑
        from examples.ocr_inference import run_ocr_inference
        result = run_ocr_inference(image_file, model_type, use_npu=NPU_AVAILABLE)
        
        return jsonify({
            "success": True,
            "model": model_type,
            "result": result,
            "device": "NPU" if NPU_AVAILABLE else "CPU"
        })
    except Exception as e:
        logger.error(f"OCR推理错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# OCR训练接口
@app.route('/ocr/training', methods=['POST'])
def ocr_training():
    """
    OCR训练接口
    启动OCR训练任务
    """
    try:
        data = request.get_json() or {}
        
        # 这里调用OCR训练逻辑
        from examples.ocr_training import start_ocr_training
        result = start_ocr_training(data, use_npu=NPU_AVAILABLE)
        
        return jsonify({
            "success": True,
            "message": "OCR训练任务已启动",
            "result": result,
            "device": "NPU" if NPU_AVAILABLE else "CPU"
        })
    except Exception as e:
        logger.error(f"OCR训练错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# NPU状态查询接口
@app.route('/npu/status', methods=['GET'])
def npu_status():
    """查询NPU状态"""
    if not NPU_AVAILABLE:
        return jsonify({
            "available": False,
            "message": "NPU环境未配置"
        })
    
    try:
        # 获取NPU信息
        ret = acl.init()
        device_count = acl.rt.get_device_count()
        
        devices = []
        for i in range(device_count):
            # 获取每个设备的信息
            devices.append({
                "id": i,
                "status": "available"
            })
        
        return jsonify({
            "available": True,
            "device_count": device_count,
            "devices": devices
        })
    except Exception as e:
        return jsonify({
            "available": False,
            "error": str(e)
        })

if __name__ == '__main__':
    # 开发模式运行
    # 生产环境请使用gunicorn
    app.run(host='0.0.0.0', port=9999, debug=False)
