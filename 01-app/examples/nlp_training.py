#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP训练示例
使用BERT模型进行文本分类训练
支持NPU和CPU训练
"""

import os
import logging
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import (
    BertTokenizer, 
    BertForSequenceClassification,
    AdamW,
    get_linear_schedule_with_warmup
)
from typing import Dict, List, Optional
from tqdm import tqdm
import json

logger = logging.getLogger(__name__)

# 尝试导入NPU支持
try:
    import torch_npu
    from torch_npu.contrib import transfer_to_npu
    NPU_AVAILABLE = True
except ImportError:
    NPU_AVAILABLE = False
    logger.warning("torch_npu未安装，将使用CPU模式")


class TextDataset(Dataset):
    """文本数据集"""
    
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


class NLPTrainer:
    """NLP训练器类"""
    
    def __init__(
        self,
        model_name: str = "bert-base-chinese",
        num_labels: int = 2,
        use_npu: bool = True,
        output_dir: str = "./models/nlp_model"
    ):
        """
        初始化NLP训练器
        
        Args:
            model_name: 预训练模型名称
            num_labels: 分类数量
            use_npu: 是否使用NPU
            output_dir: 模型输出目录
        """
        self.model_name = model_name
        self.num_labels = num_labels
        self.use_npu = use_npu and NPU_AVAILABLE
        self.output_dir = output_dir
        self.device = None
        self.model = None
        self.tokenizer = None
        
        os.makedirs(output_dir, exist_ok=True)
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
            num_labels=self.num_labels
        )
        self.model.to(self.device)
    
    def train(
        self,
        train_texts: List[str],
        train_labels: List[int],
        val_texts: Optional[List[str]] = None,
        val_labels: Optional[List[int]] = None,
        epochs: int = 3,
        batch_size: int = 16,
        learning_rate: float = 2e-5,
        warmup_steps: int = 100
    ) -> Dict:
        """
        训练模型
        
        Args:
            train_texts: 训练文本列表
            train_labels: 训练标签列表
            val_texts: 验证文本列表
            val_labels: 验证标签列表
            epochs: 训练轮数
            batch_size: 批次大小
            learning_rate: 学习率
            warmup_steps: 预热步数
            
        Returns:
            训练结果字典
        """
        # 创建数据集
        train_dataset = TextDataset(train_texts, train_labels, self.tokenizer)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
        # 优化器和学习率调度器
        optimizer = AdamW(self.model.parameters(), lr=learning_rate)
        total_steps = len(train_loader) * epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps=total_steps
        )
        
        # 训练循环
        logger.info(f"开始训练，总步数: {total_steps}")
        self.model.train()
        
        training_history = []
        
        for epoch in range(epochs):
            epoch_loss = 0
            progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}")
            
            for batch in progress_bar:
                # 移动数据到设备
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                # 清零梯度
                optimizer.zero_grad()
                
                # 前向传播
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                loss = outputs.loss
                
                # 反向传播
                loss.backward()
                optimizer.step()
                scheduler.step()
                
                epoch_loss += loss.item()
                progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})
            
            avg_loss = epoch_loss / len(train_loader)
            logger.info(f"Epoch {epoch+1} 平均损失: {avg_loss:.4f}")
            
            training_history.append({
                'epoch': epoch + 1,
                'loss': avg_loss
            })
            
            # 验证
            if val_texts is not None and val_labels is not None:
                val_metrics = self.evaluate(val_texts, val_labels, batch_size)
                logger.info(f"验证准确率: {val_metrics['accuracy']:.4f}")
                training_history[-1]['val_accuracy'] = val_metrics['accuracy']
        
        # 保存模型
        self.save_model()
        
        return {
            "success": True,
            "epochs": epochs,
            "training_history": training_history,
            "model_path": self.output_dir,
            "device": str(self.device)
        }
    
    def evaluate(
        self,
        texts: List[str],
        labels: List[int],
        batch_size: int = 16
    ) -> Dict:
        """
        评估模型
        
        Args:
            texts: 文本列表
            labels: 标签列表
            batch_size: 批次大小
            
        Returns:
            评估指标
        """
        dataset = TextDataset(texts, labels, self.tokenizer)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
        
        self.model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch in loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
                predictions = torch.argmax(outputs.logits, dim=-1)
                correct += (predictions == labels).sum().item()
                total += labels.size(0)
        
        accuracy = correct / total
        return {"accuracy": accuracy, "correct": correct, "total": total}
    
    def save_model(self):
        """保存模型"""
        logger.info(f"保存模型到: {self.output_dir}")
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)


def start_training(config: Dict, use_npu: bool = True) -> Dict:
    """
    启动训练任务
    
    Args:
        config: 配置字典
        use_npu: 是否使用NPU
        
    Returns:
        训练结果
    """
    try:
        # 示例数据（实际使用时从配置文件或数据库加载）
        train_texts = [
            "这个产品真的很好用",
            "非常失望，质量太差了",
            "性价比很高，推荐购买",
            "物流太慢了，等了很久",
            "服务态度很好",
            "包装破损，不满意"
        ]
        train_labels = [1, 0, 1, 0, 1, 0]  # 1=正面, 0=负面
        
        val_texts = [
            "使用体验不错",
            "完全不符合描述"
        ]
        val_labels = [1, 0]
        
        # 创建训练器
        trainer = NLPTrainer(
            model_name=config.get('model', 'bert-base-chinese'),
            num_labels=config.get('num_labels', 2),
            use_npu=use_npu,
            output_dir=config.get('output_dir', './models/nlp_model')
        )
        
        # 开始训练
        result = trainer.train(
            train_texts=train_texts,
            train_labels=train_labels,
            val_texts=val_texts,
            val_labels=val_labels,
            epochs=config.get('epochs', 3),
            batch_size=config.get('batch_size', 16),
            learning_rate=config.get('learning_rate', 2e-5)
        )
        
        return result
        
    except Exception as e:
        logger.error(f"训练失败: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    # 独立运行示例
    print("NLP训练示例")
    print("=" * 50)
    
    config = {
        "model": "bert-base-chinese",
        "epochs": 2,
        "batch_size": 4,
        "learning_rate": 2e-5,
        "output_dir": "./models/nlp_model_demo"
    }
    
    result = start_training(config, use_npu=False)
    print("\n训练结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
