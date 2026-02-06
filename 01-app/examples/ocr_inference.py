#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR推理示例
使用PaddleOCR进行文字识别
支持NPU和CPU推理
"""

import os
import logging
import cv2
import numpy as np
from PIL import Image
import io
from typing import Dict, List, Union
import tempfile

logger = logging.getLogger(__name__)

# 尝试导入PaddleOCR
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    logger.warning("PaddleOCR未安装")

# 尝试导入EasyOCR
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logger.warning("EasyOCR未安装")

# 尝试导入昇腾ACL
try:
    import acl
    ACL_AVAILABLE = True
except ImportError:
    ACL_AVAILABLE = False


class OCREngine:
    """OCR引擎类"""
    
    def __init__(self, model_type: str = "paddleocr", use_npu: bool = True, lang: str = 'ch'):
        """
        初始化OCR引擎
        
        Args:
            model_type: 模型类型 ('paddleocr', 'easyocr')
            use_npu: 是否使用NPU
            lang: 语言 ('ch', 'en', 'ch_sim', 等)
        """
        self.model_type = model_type
        self.use_npu = use_npu
        self.lang = lang
        self.ocr = None
        
        self._initialize()
    
    def _initialize(self):
        """初始化OCR引擎"""
        if self.model_type == "paddleocr":
            if not PADDLEOCR_AVAILABLE:
                raise ImportError("PaddleOCR未安装")
            
            logger.info("初始化PaddleOCR引擎")
            # PaddleOCR配置
            use_gpu = False  # 昇腾NPU通过paddle-custom-npu使用
            
            # 检查是否有NPU支持
            try:
                import paddle
                if paddle.is_compiled_with_custom_device('npu') and self.use_npu:
                    use_gpu = True
                    paddle.set_device('npu:0')
                    logger.info("PaddleOCR使用NPU设备")
                else:
                    paddle.set_device('cpu')
                    logger.info("PaddleOCR使用CPU设备")
            except:
                logger.info("PaddleOCR使用CPU设备")
            
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.lang,
                use_gpu=use_gpu,
                show_log=False
            )
            
        elif self.model_type == "easyocr":
            if not EASYOCR_AVAILABLE:
                raise ImportError("EasyOCR未安装")
            
            logger.info("初始化EasyOCR引擎")
            # EasyOCR配置
            gpu = self.use_npu and ACL_AVAILABLE
            
            self.ocr = easyocr.Reader(
                [self.lang],
                gpu=gpu
            )
        else:
            raise ValueError(f"不支持的OCR模型类型: {self.model_type}")
    
    def recognize(self, image_path: str) -> Dict:
        """
        识别图片中的文字
        
        Args:
            image_path: 图片路径
            
        Returns:
            识别结果字典
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        logger.info(f"识别图片: {image_path}")
        
        if self.model_type == "paddleocr":
            return self._recognize_paddleocr(image_path)
        elif self.model_type == "easyocr":
            return self._recognize_easyocr(image_path)
    
    def _recognize_paddleocr(self, image_path: str) -> Dict:
        """使用PaddleOCR识别"""
        result = self.ocr.ocr(image_path, cls=True)
        
        texts = []
        boxes = []
        scores = []
        
        if result and result[0]:
            for line in result[0]:
                box = line[0]
                text = line[1][0]
                score = line[1][1]
                
                boxes.append(box)
                texts.append(text)
                scores.append(score)
        
        return {
            "model": "paddleocr",
            "texts": texts,
            "boxes": boxes,
            "scores": scores,
            "full_text": "\n".join(texts),
            "device": "NPU" if self.use_npu else "CPU"
        }
    
    def _recognize_easyocr(self, image_path: str) -> Dict:
        """使用EasyOCR识别"""
        result = self.ocr.readtext(image_path)
        
        texts = []
        boxes = []
        scores = []
        
        for detection in result:
            box = detection[0]
            text = detection[1]
            score = detection[2]
            
            boxes.append(box)
            texts.append(text)
            scores.append(score)
        
        return {
            "model": "easyocr",
            "texts": texts,
            "boxes": boxes,
            "scores": scores,
            "full_text": "\n".join(texts),
            "device": "NPU" if self.use_npu else "CPU"
        }
    
    def recognize_bytes(self, image_bytes: bytes) -> Dict:
        """
        从字节数据识别文字
        
        Args:
            image_bytes: 图片字节数据
            
        Returns:
            识别结果字典
        """
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(image_bytes)
            temp_path = f.name
        
        try:
            result = self.recognize(temp_path)
            return result
        finally:
            # 删除临时文件
            os.unlink(temp_path)


# 全局OCR引擎实例
_ocr_engines = {}


def get_ocr_engine(model_type: str = "paddleocr", use_npu: bool = True, lang: str = 'ch'):
    """获取OCR引擎实例（单例模式）"""
    global _ocr_engines
    key = f"{model_type}_{use_npu}_{lang}"
    
    if key not in _ocr_engines:
        _ocr_engines[key] = OCREngine(model_type, use_npu, lang)
    
    return _ocr_engines[key]


def run_ocr_inference(image_file, model_type: str = "paddleocr", use_npu: bool = True) -> Dict:
    """
    运行OCR推理
    
    Args:
        image_file: 图片文件对象或路径
        model_type: 模型类型
        use_npu: 是否使用NPU
        
    Returns:
        识别结果
    """
    try:
        ocr_engine = get_ocr_engine(model_type, use_npu)
        
        # 处理文件对象
        if hasattr(image_file, 'read'):
            image_bytes = image_file.read()
            result = ocr_engine.recognize_bytes(image_bytes)
        else:
            # 文件路径
            result = ocr_engine.recognize(image_file)
        
        return result
    except Exception as e:
        logger.error(f"OCR识别失败: {str(e)}")
        return {"error": str(e)}


# 独立运行示例
if __name__ == "__main__":
    print("OCR推理示例")
    print("=" * 50)
    
    # 创建一个测试图片
    from PIL import Image, ImageDraw, ImageFont
    
    # 创建测试图片
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体，如果没有则使用默认
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 80), "Hello World\n你好世界", fill='black', font=font)
    
    # 保存测试图片
    test_image_path = "/tmp/test_ocr.jpg"
    img.save(test_image_path)
    print(f"创建测试图片: {test_image_path}")
    
    # 测试PaddleOCR
    if PADDLEOCR_AVAILABLE:
        print("\n使用PaddleOCR识别:")
        print("-" * 50)
        
        try:
            ocr = OCREngine(model_type="paddleocr", use_npu=False, lang='en')
            result = ocr.recognize(test_image_path)
            
            print(f"识别文本数: {len(result['texts'])}")
            print(f"识别结果:")
            for i, text in enumerate(result['texts']):
                print(f"  {i+1}. {text} (置信度: {result['scores'][i]:.4f})")
        except Exception as e:
            print(f"PaddleOCR错误: {e}")
    
    # 测试EasyOCR
    if EASYOCR_AVAILABLE:
        print("\n使用EasyOCR识别:")
        print("-" * 50)
        
        try:
            ocr = OCREngine(model_type="easyocr", use_npu=False, lang='ch_sim')
            result = ocr.recognize(test_image_path)
            
            print(f"识别文本数: {len(result['texts'])}")
            print(f"识别结果:")
            for i, text in enumerate(result['texts']):
                print(f"  {i+1}. {text} (置信度: {result['scores'][i]:.4f})")
        except Exception as e:
            print(f"EasyOCR错误: {e}")
    
    # 清理
    os.unlink(test_image_path)
    print("\n测试完成")
