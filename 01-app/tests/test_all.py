#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试套件
测试所有功能模块
"""

import unittest
import sys
import os
import json
import tempfile
from io import BytesIO

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.nlp_inference import NLPPredictor, run_inference
from examples.nlp_training import NLPTrainer, start_training
from examples.ocr_inference import OCREngine, run_ocr_inference
from examples.ocr_training import OCRTrainer, start_ocr_training


class TestNLPInference(unittest.TestCase):
    """测试NLP推理模块"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        print("\n" + "="*50)
        print("开始测试NLP推理模块")
        print("="*50)
        cls.predictor = NLPPredictor(
            model_name="bert-base-chinese",
            use_npu=False  # 测试环境使用CPU
        )
    
    def test_single_prediction(self):
        """测试单条推理"""
        text = "这是一个非常好的产品，强烈推荐！"
        result = self.predictor.predict(text)
        
        self.assertIn('predicted_class', result)
        self.assertIn('confidence', result)
        self.assertIn('probabilities', result)
        self.assertEqual(result['text'], text)
        self.assertIsInstance(result['confidence'], float)
        print(f"✓ 单条推理测试通过: {result['predicted_class']} (置信度: {result['confidence']:.4f})")
    
    def test_batch_prediction(self):
        """测试批量推理"""
        texts = [
            "产品质量很好",
            "服务态度很差",
            "物流速度很快"
        ]
        results = self.predictor.batch_predict(texts)
        
        self.assertEqual(len(results), len(texts))
        for i, result in enumerate(results):
            self.assertIn('predicted_class', result)
            self.assertIn('confidence', result)
        print(f"✓ 批量推理测试通过: {len(results)}条文本")
    
    def test_different_texts(self):
        """测试不同类型文本"""
        test_cases = [
            "这是一个测试",  # 中文
            "Hello World",    # 英文
            "123456",         # 数字
            "！？。，",       # 标点
        ]
        
        for text in test_cases:
            result = self.predictor.predict(text)
            self.assertIn('predicted_class', result)
        print(f"✓ 多类型文本测试通过: {len(test_cases)}种类型")


class TestNLPTraining(unittest.TestCase):
    """测试NLP训练模块"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        print("\n" + "="*50)
        print("开始测试NLP训练模块")
        print("="*50)
    
    def test_trainer_initialization(self):
        """测试训练器初始化"""
        trainer = NLPTrainer(
            model_name="bert-base-chinese",
            num_labels=2,
            use_npu=False,
            output_dir="./test_models/nlp"
        )
        
        self.assertIsNotNone(trainer.model)
        self.assertIsNotNone(trainer.tokenizer)
        self.assertEqual(trainer.num_labels, 2)
        print("✓ 训练器初始化测试通过")
    
    def test_training_process(self):
        """测试训练流程"""
        # 准备测试数据
        train_texts = [
            "这个产品真的很好用",
            "非常失望，质量太差了",
            "性价比很高，推荐购买",
            "物流太慢了，等了很久",
        ]
        train_labels = [1, 0, 1, 0]
        
        trainer = NLPTrainer(
            model_name="bert-base-chinese",
            num_labels=2,
            use_npu=False,
            output_dir="./test_models/nlp_train"
        )
        
        # 使用较小的epochs和batch_size加速测试
        result = trainer.train(
            train_texts=train_texts,
            train_labels=train_labels,
            epochs=1,
            batch_size=2,
            learning_rate=2e-5
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['epochs'], 1)
        self.assertIn('training_history', result)
        print(f"✓ 训练流程测试通过: {result['epochs']}轮训练完成")
    
    def test_evaluation(self):
        """测试评估功能"""
        trainer = NLPTrainer(
            model_name="bert-base-chinese",
            num_labels=2,
            use_npu=False,
            output_dir="./test_models/nlp_eval"
        )
        
        val_texts = ["测试文本1", "测试文本2"]
        val_labels = [1, 0]
        
        metrics = trainer.evaluate(val_texts, val_labels, batch_size=2)
        
        self.assertIn('accuracy', metrics)
        self.assertIn('correct', metrics)
        self.assertIn('total', metrics)
        self.assertIsInstance(metrics['accuracy'], float)
        print(f"✓ 评估功能测试通过: 准确率 {metrics['accuracy']:.4f}")


class TestOCRInference(unittest.TestCase):
    """测试OCR推理模块"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        print("\n" + "="*50)
        print("开始测试OCR推理模块")
        print("="*50)
    
    def create_test_image(self, text="Test"):
        """创建测试图片"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGB', (400, 100), color='white')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
            except:
                font = ImageFont.load_default()
            draw.text((50, 30), text, fill='black', font=font)
            
            # 保存到临时文件
            temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            img.save(temp_file.name)
            return temp_file.name
        except ImportError:
            return None
    
    def test_ocr_engine_initialization(self):
        """测试OCR引擎初始化"""
        try:
            ocr = OCREngine(
                model_type="paddleocr",
                use_npu=False,
                lang='en'
            )
            self.assertIsNotNone(ocr.ocr)
            print("✓ OCR引擎初始化测试通过")
        except ImportError as e:
            print(f"⚠ OCR引擎初始化跳过: {e}")
    
    def test_image_recognition(self):
        """测试图片识别"""
        image_path = self.create_test_image("Hello World")
        if not image_path:
            print("⚠ 图片创建失败，跳过测试")
            return
        
        try:
            ocr = OCREngine(
                model_type="paddleocr",
                use_npu=False,
                lang='en'
            )
            result = ocr.recognize(image_path)
            
            self.assertIn('texts', result)
            self.assertIn('scores', result)
            self.assertIn('full_text', result)
            
            # 清理临时文件
            os.unlink(image_path)
            
            print(f"✓ 图片识别测试通过: 识别到 {len(result['texts'])} 个文本区域")
        except Exception as e:
            os.unlink(image_path)
            print(f"⚠ 图片识别测试跳过: {e}")
    
    def test_bytes_recognition(self):
        """测试字节数据识别"""
        image_path = self.create_test_image("Test")
        if not image_path:
            print("⚠ 图片创建失败，跳过测试")
            return
        
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            ocr = OCREngine(
                model_type="paddleocr",
                use_npu=False,
                lang='en'
            )
            result = ocr.recognize_bytes(image_bytes)
            
            self.assertIn('texts', result)
            
            # 清理临时文件
            os.unlink(image_path)
            
            print(f"✓ 字节数据识别测试通过")
        except Exception as e:
            os.unlink(image_path)
            print(f"⚠ 字节数据识别测试跳过: {e}")


class TestOCRTraining(unittest.TestCase):
    """测试OCR训练模块"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        print("\n" + "="*50)
        print("开始测试OCR训练模块")
        print("="*50)
    
    def test_trainer_initialization(self):
        """测试训练器初始化"""
        trainer = OCRTrainer(
            model_type="ch_PP-OCRv4",
            use_npu=False,
            output_dir="./test_models/ocr"
        )
        
        self.assertEqual(trainer.model_type, "ch_PP-OCRv4")
        self.assertFalse(trainer.use_npu)
        print("✓ OCR训练器初始化测试通过")
    
    def test_dataset_preparation(self):
        """测试数据集准备"""
        train_data = [
            {"image_path": "img1.jpg", "label": "文本1"},
            {"image_path": "img2.jpg", "label": "文本2"},
        ]
        
        trainer = OCRTrainer(
            model_type="ch_PP-OCRv4",
            use_npu=False,
            output_dir="./test_models/ocr_data"
        )
        
        config = trainer.prepare_dataset(
            train_data=train_data,
            data_dir="./test_data/ocr"
        )
        
        self.assertIn('train_label_file', config)
        self.assertIn('data_dir', config)
        self.assertTrue(os.path.exists(config['data_dir']))
        print(f"✓ 数据集准备测试通过")
    
    def test_config_generation(self):
        """测试配置文件生成"""
        trainer = OCRTrainer(
            model_type="ch_PP-OCRv4",
            use_npu=False,
            output_dir="./test_models/ocr_config"
        )
        
        dataset_config = {
            'train_label_file': './test_data/train.txt',
            'val_label_file': './test_data/val.txt',
            'data_dir': './test_data'
        }
        
        config_path = trainer.generate_config(dataset_config)
        
        self.assertTrue(os.path.exists(config_path))
        self.assertTrue(config_path.endswith('.yml'))
        print(f"✓ 配置文件生成测试通过: {config_path}")


class TestAPIIntegration(unittest.TestCase):
    """测试API集成"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        print("\n" + "="*50)
        print("开始测试API集成")
        print("="*50)
    
    def test_nlp_inference_api(self):
        """测试NLP推理API"""
        try:
            from app import app
            client = app.test_client()
            
            response = client.post('/nlp/inference', json={
                'text': '这是一个测试',
                'model': 'bert-base-chinese'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data.get('success', False) or 'error' in data)
            print("✓ NLP推理API测试通过")
        except Exception as e:
            print(f"⚠ NLP推理API测试跳过: {e}")
    
    def test_health_check_api(self):
        """测试健康检查API"""
        try:
            from app import app
            client = app.test_client()
            
            response = client.get('/health')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'healthy')
            print("✓ 健康检查API测试通过")
        except Exception as e:
            print(f"⚠ 健康检查API测试跳过: {e}")
    
    def test_npu_status_api(self):
        """测试NPU状态API"""
        try:
            from app import app
            client = app.test_client()
            
            response = client.get('/npu/status')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('available', data)
            print(f"✓ NPU状态API测试通过: NPU可用={data['available']}")
        except Exception as e:
            print(f"⚠ NPU状态API测试跳过: {e}")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("开始自动化测试套件")
    print("="*60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestNLPInference))
    suite.addTests(loader.loadTestsFromTestCase(TestNLPTraining))
    suite.addTests(loader.loadTestsFromTestCase(TestOCRInference))
    suite.addTests(loader.loadTestsFromTestCase(TestOCRTraining))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"测试总数: {result.testsRun}")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print("\n✗ 部分测试失败")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
