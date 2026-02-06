#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP推理示例
使用BERT模型进行文本分类
支持NPU和CPU推理
"""

import os
import logging
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification
from typing import Dict, List, Union

logger = logging.getLogger(__name__)

# 尝试导入NPU支持
try:
    import torch_npu
    from torch_npu.contrib import transfer_to_npu
    NPU_AVAILABLE = True
except ImportError:
    NPU_AVAILABLE = False
    logger.warning("torch_npu未安装，将使用CPU模式")


class NLPPredictor:
    """NLP预测器类"""
    
    def __init__(self, model_name: str = "bert-base-chinese", use_npu: bool = True):
        """
        初始化NLP预测器
        
        Args:
            model_name: 模型名称
            use_npu: 是否使用NPU
        """
        self.model_name = model_name
        self.use_npu = use_npu and NPU_AVAILABLE
        self.device = None
        self.model = None
        self.tokenizer = None
        
        self._initialize()
    
    def _initialize(self):
        """初始化模型和设备"""
        # 设置设备
        if self.use_npu:
            self.device = torch.device("npu:0" if torch.npu.is_available() else "cpu")
            logger.info(f"使用NPU设备: {self.device}")
        else:
            self.device = torch.device("cpu")
            logger.info(f"使用CPU设备")
        
        # 加载tokenizer
        logger.info(f"加载tokenizer: {self.model_name}")
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        
        # 加载模型
        logger.info(f"加载模型: {self.model_name}")
        self.model = BertForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=2  # 二分类示例
        )
        self.model.to(self.device)
        self.model.eval()
    
    def predict(self, text: str) -> Dict:
        """
        进行文本分类预测
        
        Args:
            text: 输入文本
            
        Returns:
            预测结果字典
        """
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        
        # 移动到设备
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # 推理
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).item()
        
        # 返回结果
        return {
            "text": text,
            "predicted_class": predicted_class,
            "confidence": probabilities[0][predicted_class].item(),
            "probabilities": probabilities[0].cpu().numpy().tolist(),
            "device": str(self.device)
        }
    
    def batch_predict(self, texts: List[str]) -> List[Dict]:
        """
        批量预测
        
        Args:
            texts: 文本列表
            
        Returns:
            预测结果列表
        """
        results = []
        for text in texts:
            result = self.predict(text)
            results.append(result)
        return results


# 全局预测器实例
_predictor = None


def get_predictor(model_name: str = "bert-base-chinese", use_npu: bool = True):
    """获取预测器实例（单例模式）"""
    global _predictor
    if _predictor is None:
        _predictor = NLPPredictor(model_name, use_npu)
    return _predictor


def run_inference(text: str, model_name: str = "bert-base-chinese", use_npu: bool = True) -> Dict:
    """
    运行NLP推理
    
    Args:
        text: 输入文本
        model_name: 模型名称
        use_npu: 是否使用NPU
        
    Returns:
        预测结果
    """
    try:
        predictor = get_predictor(model_name, use_npu)
        result = predictor.predict(text)
        return result
    except Exception as e:
        logger.error(f"推理失败: {str(e)}")
        return {"error": str(e), "text": text}


# 独立运行示例
if __name__ == "__main__":
    # 测试文本
    test_texts = [
        "这是一个非常好的产品，强烈推荐！",
        "产品质量很差，不推荐购买。",
        "服务态度很好，物流也很快。"
    ]
    
    # 创建预测器
    predictor = NLPPredictor(model_name="bert-base-chinese", use_npu=False)
    
    # 单条推理
    print("=" * 50)
    print("单条推理示例:")
    print("=" * 50)
    for text in test_texts:
        result = predictor.predict(text)
        print(f"\n文本: {result['text']}")
        print(f"预测类别: {result['predicted_class']}")
        print(f"置信度: {result['confidence']:.4f}")
        print(f"设备: {result['device']}")
    
    # 批量推理
    print("\n" + "=" * 50)
    print("批量推理示例:")
    print("=" * 50)
    results = predictor.batch_predict(test_texts)
    for i, result in enumerate(results):
        print(f"\n样本 {i+1}:")
        print(f"  预测类别: {result['predicted_class']}")
        print(f"  置信度: {result['confidence']:.4f}")
