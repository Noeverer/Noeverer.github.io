# 示例模块初始化文件
from .nlp_inference import NLPPredictor, run_inference
from .nlp_training import NLPTrainer, start_training
from .ocr_inference import OCREngine, run_ocr_inference
from .ocr_training import OCRTrainer, start_ocr_training

__all__ = [
    'NLPPredictor',
    'run_inference',
    'NLPTrainer',
    'start_training',
    'OCREngine',
    'run_ocr_inference',
    'OCRTrainer',
    'start_ocr_training'
]
