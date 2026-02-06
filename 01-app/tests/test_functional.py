#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能测试脚本
验证核心功能是否正常工作
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """测试关键依赖导入"""
    print("测试依赖导入...")
    errors = []
    
    # 基础依赖
    try:
        import flask
        print("  ✓ Flask")
    except ImportError as e:
        errors.append(f"Flask: {e}")
        print("  ✗ Flask")
    
    try:
        import numpy
        print("  ✓ NumPy")
    except ImportError as e:
        errors.append(f"NumPy: {e}")
        print("  ✗ NumPy")
    
    try:
        from PIL import Image
        print("  ✓ Pillow")
    except ImportError as e:
        errors.append(f"Pillow: {e}")
        print("  ✗ Pillow")
    
    # ML库
    try:
        import torch
        print(f"  ✓ PyTorch {torch.__version__}")
    except ImportError as e:
        errors.append(f"PyTorch: {e}")
        print("  ✗ PyTorch")
    
    try:
        import transformers
        print("  ✓ Transformers")
    except ImportError as e:
        errors.append(f"Transformers: {e}")
        print("  ✗ Transformers")
    
    try:
        import paddle
        print("  ✓ PaddlePaddle")
    except ImportError as e:
        errors.append(f"PaddlePaddle: {e}")
        print("  ⚠ PaddlePaddle (可选)")
    
    try:
        from paddleocr import PaddleOCR
        print("  ✓ PaddleOCR")
    except ImportError as e:
        errors.append(f"PaddleOCR: {e}")
        print("  ⚠ PaddleOCR (可选)")
    
    # NPU支持
    try:
        import torch_npu
        print("  ✓ torch_npu (NPU支持)")
    except ImportError:
        print("  ⚠ torch_npu (NPU支持未安装)")
    
    try:
        import acl
        print("  ✓ ACL (昇腾ACL)")
    except ImportError:
        print("  ⚠ ACL (昇腾ACL未安装)")
    
    if errors:
        print(f"\n警告: {len(errors)}个必需依赖未安装")
        return False
    return True


def test_nlp_basic():
    """测试NLP基础功能"""
    print("\n测试NLP基础功能...")
    
    try:
        from examples.nlp_inference import run_inference
        result = run_inference("这是一个测试", use_npu=False)
        if 'error' in result:
            print(f"  ✗ NLP推理失败: {result['error']}")
            return False
        print(f"  ✓ NLP推理成功: 类别={result.get('predicted_class', 'N/A')}")
        return True
    except Exception as e:
        print(f"  ✗ NLP推理异常: {e}")
        return False


def test_ocr_basic():
    """测试OCR基础功能"""
    print("\n测试OCR基础功能...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import tempfile
        
        # 创建测试图片
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            font = ImageFont.load_default()
        draw.text((50, 30), "Test", fill='black', font=font)
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(temp_file.name)
        
        # 测试OCR
        from examples.ocr_inference import run_ocr_inference
        result = run_ocr_inference(temp_file.name, use_npu=False)
        
        # 清理
        import os
        os.unlink(temp_file.name)
        
        if 'error' in result:
            print(f"  ⚠ OCR推理: {result['error']}")
            return False
        print(f"  ✓ OCR推理成功: 识别到 {len(result.get('texts', []))} 个区域")
        return True
    except Exception as e:
        print(f"  ⚠ OCR推理异常: {e}")
        return False


def test_flask_app():
    """测试Flask应用"""
    print("\n测试Flask应用...")
    
    try:
        from app import app
        client = app.test_client()
        
        # 测试健康检查
        response = client.get('/health')
        if response.status_code == 200:
            print(f"  ✓ 健康检查: HTTP {response.status_code}")
        else:
            print(f"  ✗ 健康检查: HTTP {response.status_code}")
            return False
        
        # 测试首页
        response = client.get('/')
        if response.status_code == 200:
            print(f"  ✓ 首页: HTTP {response.status_code}")
        else:
            print(f"  ✗ 首页: HTTP {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Flask应用异常: {e}")
        return False


def test_npu_detection():
    """测试NPU检测"""
    print("\n测试NPU检测...")
    
    try:
        import torch
        if hasattr(torch, 'npu') and torch.npu.is_available():
            print(f"  ✓ NPU可用: {torch.npu.device_count()} 个设备")
            return True
        else:
            print("  ⚠ NPU不可用 (将使用CPU)")
            return False
    except:
        print("  ⚠ NPU检测失败")
        return False


def main():
    """主函数"""
    print("="*60)
    print("功能测试")
    print("="*60)
    
    results = []
    
    # 运行所有测试
    results.append(("依赖导入", test_imports()))
    results.append(("NLP功能", test_nlp_basic()))
    results.append(("OCR功能", test_ocr_basic()))
    results.append(("Flask应用", test_flask_app()))
    results.append(("NPU检测", test_npu_detection()))
    
    # 打印总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:.<30} {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n✓ 所有测试通过！系统功能正常。")
        return 0
    else:
        print(f"\n⚠ {total - passed} 项测试未通过，请检查配置。")
        return 1


if __name__ == '__main__':
    sys.exit(main())
