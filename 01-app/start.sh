#!/bin/bash
# 启动脚本

echo "启动昇腾NPU推理服务..."

# 创建必要目录
mkdir -p logs models data

# 检查Docker是否安装
if ! which docker >/dev/null 2>&1; then
    echo "错误: Docker未安装"
    exit 1
fi

# 检查docker-compose是否安装
if ! which docker-compose >/dev/null 2>&1; then
    echo "错误: docker-compose未安装"
    exit 1
fi

# 检查NPU设备是否存在
if [ ! -e "/dev/davinci0" ]; then
    echo "警告: NPU设备未找到，将以CPU模式运行"
    echo "如果需要使用NPU，请确保:"
    echo "  1. 昇腾驱动已正确安装"
    echo "  2. NPU设备已连接"
fi

# 启动服务
echo "正在启动服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 5

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "======================================"
    echo "服务启动成功!"
    echo "======================================"
    echo ""
    echo "API地址: http://localhost:9999"
    echo "健康检查: http://localhost:9999/health"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker-compose logs -f app"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart"
    echo ""
    echo "测试API:"
    echo "  curl http://localhost:9999/health"
    echo "======================================"
else
    echo ""
    echo "服务启动失败，请检查日志:"
    docker-compose logs app
fi
