#!/bin/bash
# 快速测试脚本
# 运行所有测试

echo "======================================"
echo "快速功能测试"
echo "======================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3未安装"
    exit 1
fi

# 运行测试
cd "$(dirname "$0")"

echo "[1/2] 运行功能测试..."
python3 tests/test_functional.py
echo ""

echo "[2/2] 运行完整测试套件..."
python3 tests/test_all.py
echo ""

echo "======================================"
echo "测试完成！"
echo "======================================"
