#!/usr/bin/env python3
"""
MCP Server - Model Context Protocol Server
内网部署版本主入口文件
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
except ImportError as e:
    print(f"错误: 缺少必要的依赖包 {e}")
    print("请运行: pip install -r requirements-prod.txt")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="MCP Server",
    description="Model Context Protocol Server - 内网部署版本",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("MCP_ENV", "development"),
        "timestamp": "2024-01-01T00:00:00Z",
    }


# 基础 API 端点
@app.get("/")
async def root():
    """根端点"""
    return {"message": "MCP Server is running", "docs": "/docs", "health": "/health"}


# 基础工具 API
@app.post("/v1/tools/echo")
async def echo_tool(data: dict):
    """回显工具 - 用于测试"""
    return {"result": data, "tool": "echo", "timestamp": "2024-01-01T00:00:00Z"}


# 文件操作 API（基础）
@app.post("/v1/tools/file_info")
async def file_info_tool(data: dict):
    """获取文件信息"""
    file_path = data.get("path", "")

    try:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            return {
                "result": {
                    "path": file_path,
                    "exists": True,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "is_directory": os.path.isdir(file_path),
                    "is_file": os.path.isfile(file_path),
                }
            }
        else:
            return {"result": {"path": file_path, "exists": False}}
    except Exception as e:
        return {"error": str(e), "path": file_path}


# 文本处理 API
@app.post("/v1/tools/text_analyze")
async def text_analyze_tool(data: dict):
    """文本分析工具"""
    text = data.get("text", "")

    if not text:
        return {"error": "Text is required"}

    # 简单的文本统计
    result = {
        "char_count": len(text),
        "word_count": len(text.split()),
        "line_count": len(text.splitlines()),
        "language": "unknown",  # 可以集成语言检测
    }

    return {"result": result}


# 错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error", "detail": str(exc)}
    )


def main():
    """主函数"""
    # 获取配置
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", 8080))
    workers = int(os.getenv("MCP_WORKERS", 1))

    logger.info(f"Starting MCP Server on {host}:{port}")
    logger.info(f"Environment: {os.getenv('MCP_ENV', 'development')}")
    logger.info(f"Workers: {workers}")

    # 启动服务器
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        reload=False,
        access_log=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
