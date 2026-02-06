#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR训练示例
使用PaddleOCR训练自定义文字识别模型
支持NPU和CPU训练
"""

import os
import logging
import json
import shutil
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# 尝试导入Paddle
try:
    import paddle
    from paddle import nn
    from paddle.optimizer import Adam
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False
    logger.warning("Paddle未安装")


def check_npu_support():
    """检查NPU支持"""
    if not PADDLE_AVAILABLE:
        return False
    
    try:
        # 检查是否编译了NPU支持
        if paddle.is_compiled_with_custom_device('npu'):
            # 检查NPU是否可用
            paddle.set_device('npu:0')
            return True
    except:
        pass
    
    return False


class OCRTrainer:
    """OCR训练器类"""
    
    def __init__(
        self,
        model_type: str = "ch_PP-OCRv4",
        use_npu: bool = True,
        output_dir: str = "./models/ocr_model",
        pretrained_model: Optional[str] = None
    ):
        """
        初始化OCR训练器
        
        Args:
            model_type: 模型类型
            use_npu: 是否使用NPU
            output_dir: 输出目录
            pretrained_model: 预训练模型路径
        """
        self.model_type = model_type
        self.use_npu = use_npu and check_npu_support()
        self.output_dir = output_dir
        self.pretrained_model = pretrained_model
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 设置设备
        if self.use_npu:
            paddle.set_device('npu:0')
            logger.info("使用NPU设备进行训练")
        else:
            paddle.set_device('cpu')
            logger.info("使用CPU设备进行训练")
    
    def prepare_dataset(
        self,
        train_data: List[Dict],
        val_data: Optional[List[Dict]] = None,
        data_dir: str = "./data/ocr"
    ) -> Dict:
        """
        准备数据集
        
        Args:
            train_data: 训练数据列表，每个元素包含image_path和label
            val_data: 验证数据列表
            data_dir: 数据目录
            
        Returns:
            数据集配置信息
        """
        logger.info("准备数据集...")
        
        # 创建数据目录
        train_dir = os.path.join(data_dir, "train")
        val_dir = os.path.join(data_dir, "val")
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)
        
        # 生成标签文件
        train_label_file = os.path.join(data_dir, "train.txt")
        val_label_file = os.path.join(data_dir, "val.txt")
        
        # 写入训练集
        with open(train_label_file, 'w', encoding='utf-8') as f:
            for item in train_data:
                img_path = item['image_path']
                label = item['label']
                f.write(f"{img_path}\t{label}\n")
        
        # 写入验证集
        if val_data:
            with open(val_label_file, 'w', encoding='utf-8') as f:
                for item in val_data:
                    img_path = item['image_path']
                    label = item['label']
                    f.write(f"{img_path}\t{label}\n")
        
        logger.info(f"训练样本数: {len(train_data)}")
        logger.info(f"验证样本数: {len(val_data) if val_data else 0}")
        
        return {
            "train_label_file": train_label_file,
            "val_label_file": val_label_file if val_data else None,
            "data_dir": data_dir
        }
    
    def generate_config(self, dataset_config: Dict, num_classes: int = 6625) -> str:
        """
        生成PaddleOCR配置文件
        
        Args:
            dataset_config: 数据集配置
            num_classes: 字符类别数
            
        Returns:
            配置文件路径
        """
        config_content = f"""
Global:
  debug: false
  use_gpu: {str(self.use_npu).lower()}
  epoch_num: 100
  log_smooth_window: 20
  print_batch_step: 10
  save_model_dir: {self.output_dir}
  save_epoch_step: 10
  eval_batch_step: [0, 500]
  cal_metric_during_train: true
  pretrained_model: {self.pretrained_model or ''}
  checkpoints:
  save_inference_dir: {os.path.join(self.output_dir, 'inference')}
  use_visualdl: true
  infer_img: doc/imgs_words/ch/word_1.jpg
  character_dict_path: ppocr/utils/ppocr_keys_v1.txt
  max_text_length: 25
  infer_mode: false
  use_space_char: true
  distributed: true
  save_res_path: ./checkpoints/rec/predicts_ppocrv3.txt

Optimizer:
  name: Adam
  beta1: 0.9
  beta2: 0.999
  lr:
    name: Cosine
    learning_rate: 0.001
    warmup_epoch: 5
  regularizer:
    name: L2
    factor: 3.0e-05

Architecture:
  model_type: rec
  algorithm: SVTR_LCNet
  Transform:
  Backbone:
    name: PPLCNetV3
    scale: 0.95
  Head:
    name: MultiHead
    out_channels_list:
      CTCLabelDecode: {num_classes}
      SARLabelDecode: {num_classes + 2}
    # ... 其他配置

Loss:
  name: MultiLoss
  loss_config_list:
    - CTCLoss:
    - SARLoss:

PostProcess:
  name: CTCLabelDecode

Metric:
  name: RecMetric
  main_indicator: acc
  ignore_space: false

Train:
  dataset:
    name: SimpleDataSet
    data_dir: {dataset_config['data_dir']}
    ext_op_transform_idx: 1
    label_file_list: [{dataset_config['train_label_file']}]
    transforms:
      - DecodeImage:
          img_mode: BGR
          channel_first: false
      - RecConAug:
      - RecAug:
      - CTCLabelEncode:
      - RecResizeImg:
          image_shape: [3, 48, 320]
      - KeepKeys:
          keep_keys: ['image', 'label', 'length']
  loader:
    shuffle: true
    batch_size_per_card: 128
    drop_last: true
    num_workers: 8

Eval:
  dataset:
    name: SimpleDataSet
    data_dir: {dataset_config['data_dir']}
    label_file_list: [{dataset_config.get('val_label_file', dataset_config['train_label_file'])}]
    transforms:
      - DecodeImage:
          img_mode: BGR
          channel_first: false
      - CTCLabelEncode:
      - RecResizeImg:
          image_shape: [3, 48, 320]
      - KeepKeys:
          keep_keys: ['image', 'label', 'length']
  loader:
    shuffle: false
    drop_last: false
    batch_size_per_card: 128
    num_workers: 4
"""
        
        config_path = os.path.join(self.output_dir, "train_config.yml")
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        logger.info(f"配置文件已生成: {config_path}")
        return config_path
    
    def train(
        self,
        train_data: List[Dict],
        val_data: Optional[List[Dict]] = None,
        epochs: int = 100,
        batch_size: int = 128,
        learning_rate: float = 0.001
    ) -> Dict:
        """
        训练OCR模型
        
        Args:
            train_data: 训练数据
            val_data: 验证数据
            epochs: 训练轮数
            batch_size: 批次大小
            learning_rate: 学习率
            
        Returns:
            训练结果
        """
        if not PADDLE_AVAILABLE:
            return {"error": "Paddle未安装，无法训练"}
        
        try:
            # 准备数据集
            dataset_config = self.prepare_dataset(train_data, val_data)
            
            # 生成配置文件
            config_path = self.generate_config(dataset_config)
            
            # 记录训练开始时间
            start_time = datetime.now()
            
            logger.info(f"开始训练，配置:")
            logger.info(f"  模型类型: {self.model_type}")
            logger.info(f"  设备: {'NPU' if self.use_npu else 'CPU'}")
            logger.info(f"  训练轮数: {epochs}")
            logger.info(f"  批次大小: {batch_size}")
            logger.info(f"  学习率: {learning_rate}")
            
            # 实际训练命令（需要在PaddleOCR环境中运行）
            train_command = f"""
            # 使用PaddleOCR训练脚本
            python3 -m paddle.distributed.launch --gpus '0' \
                tools/train.py \
                -c {config_path}
            """
            
            logger.info(f"训练命令:\n{train_command}")
            
            # 返回训练配置信息
            return {
                "success": True,
                "message": "OCR训练配置已生成",
                "config_path": config_path,
                "output_dir": self.output_dir,
                "device": "NPU" if self.use_npu else "CPU",
                "train_command": train_command.strip(),
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "start_time": start_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"训练失败: {str(e)}")
            return {"error": str(e)}


def start_ocr_training(config: Dict, use_npu: bool = True) -> Dict:
    """
    启动OCR训练任务
    
    Args:
        config: 配置字典
        use_npu: 是否使用NPU
        
    Returns:
        训练结果
    """
    try:
        # 示例训练数据
        train_data = [
            {"image_path": "/data/ocr/train/img_001.jpg", "label": "示例文本1"},
            {"image_path": "/data/ocr/train/img_002.jpg", "label": "示例文本2"},
            {"image_path": "/data/ocr/train/img_003.jpg", "label": "Hello World"},
        ]
        
        val_data = [
            {"image_path": "/data/ocr/val/img_001.jpg", "label": "验证文本1"},
            {"image_path": "/data/ocr/val/img_002.jpg", "label": "验证文本2"},
        ]
        
        # 创建训练器
        trainer = OCRTrainer(
            model_type=config.get('model', 'ch_PP-OCRv4'),
            use_npu=use_npu,
            output_dir=config.get('output_dir', './models/ocr_model'),
            pretrained_model=config.get('pretrained_model')
        )
        
        # 开始训练
        result = trainer.train(
            train_data=train_data,
            val_data=val_data,
            epochs=config.get('epochs', 100),
            batch_size=config.get('batch_size', 128),
            learning_rate=config.get('learning_rate', 0.001)
        )
        
        return result
        
    except Exception as e:
        logger.error(f"OCR训练启动失败: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    # 独立运行示例
    print("OCR训练示例")
    print("=" * 50)
    
    config = {
        "model": "ch_PP-OCRv4",
        "epochs": 100,
        "batch_size": 128,
        "learning_rate": 0.001,
        "output_dir": "./models/ocr_model_demo"
    }
    
    result = start_ocr_training(config, use_npu=False)
    print("\n训练配置:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
