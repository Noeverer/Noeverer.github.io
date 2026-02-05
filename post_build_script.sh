#!/bin/bash

# 构建后脚本：确保根目录有 index.html 文件
echo "=== Post-build script ==="
echo "Creating root index.html if it doesn't exist..."

# 检查是否已有根目录的 index.html
if [ ! -f "public/index.html" ]; then
    echo "Root index.html not found, creating redirect..."
    
    # 创建一个简单的 index.html，重定向到 index/index.html
    cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0; url=./index/index.html">
    <link rel="canonical" href="./index/index.html">
</head>
<body>
    <h1>Redirecting...</h1>
    <a href="./index/index.html">Click here if you are not redirected</a>
</body>
</html>
EOF
    
    echo "Created root index.html with redirect to index/index.html"
else
    echo "Root index.html already exists"
fi

echo "Post-build script completed."