#!/bin/bash

# 博客验证脚本 - 检查 Hexo 博客配置和文件是否正确

set -e  # 遇到错误立即退出

echo "=== Hexo 博客验证脚本 ==="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
PASS=0
FAIL=0
WARN=0

# 检查函数
check_pass() {
    echo -e "${GREEN}✅${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}❌${NC} $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠️ ${NC} $1"
    ((WARN++))
}

# 1. 检查必要文件
echo "1. 检查必要文件..."
if [ -f "_config.yml" ]; then
    check_pass "_config.yml 存在"
else
    check_fail "_config.yml 不存在"
fi

if [ -f "_config.butterfly.yml" ]; then
    check_pass "_config.butterfly.yml 存在"
else
    check_fail "_config.butterfly.yml 不存在"
fi

if [ -f "package.json" ]; then
    check_pass "package.json 存在"
else
    check_fail "package.json 不存在"
fi

if [ -f ".github/workflows/deploy.yml" ]; then
    check_pass "GitHub Actions 工作流存在"
else
    check_fail "GitHub Actions 工作流不存在"
fi

# 2. 检查 node_modules
echo ""
echo "2. 检查依赖..."
if [ -d "node_modules" ]; then
    check_pass "node_modules 目录存在"
    
    if [ -d "node_modules/hexo" ]; then
        check_pass "hexo 已安装"
    else
        check_fail "hexo 未安装"
    fi
    
    if [ -d "node_modules/hexo-theme-butterfly" ]; then
        check_pass "butterfly 主题已安装"
    else
        check_fail "butterfly 主题未安装"
    fi
else
    check_fail "node_modules 不存在，请运行 npm install"
fi

# 3. 检查 source 目录
echo ""
echo "3. 检查源文件..."
if [ -d "source" ]; then
    check_pass "source 目录存在"
    
    if [ -d "source/_posts" ]; then
        check_pass "source/_posts 目录存在"
        
        # 统计 markdown 文件数量
        MD_COUNT=$(find source/_posts -name "*.md" -type f 2>/dev/null | wc -l)
        if [ "$MD_COUNT" -gt 0 ]; then
            check_pass "找到 $MD_COUNT 个 markdown 文件"
        else
            check_fail "没有找到 markdown 文件"
        fi
    else
        check_fail "source/_posts 目录不存在"
    fi
else
    check_fail "source 目录不存在"
fi

# 4. 检查所有 markdown 文件的 front matter
echo ""
echo "4. 检查 markdown 文件的 front matter..."
find source/_posts -name "*.md" -type f | while read file; do
    # 检查是否以 --- 开头
    if head -n 1 "$file" | grep -q "^---"; then
        # 检查是否包含必要的字段
        if head -n 20 "$file" | grep -q "title:" && head -n 20 "$file" | grep -q "date:"; then
            check_pass "$(basename "$file") - front matter 正确"
        else
            check_fail "$(basename "$file") - 缺少必要的 front matter 字段"
        fi
    else
        check_fail "$(basename "$file") - 缺少 front matter"
    fi
done

# 5. 检查 Hexo 配置
echo ""
echo "5. 检查 Hexo 配置..."
if grep -q "^theme: butterfly" _config.yml; then
    check_pass "主题设置为 butterfly"
else
    check_fail "主题设置不正确"
fi

if grep -q "^url: https://noeverer.github.io" _config.yml; then
    check_pass "URL 配置正确"
else
    check_warn "URL 配置可能不正确"
fi

# 6. 检查 .gitignore
echo ""
echo "6. 检查 .gitignore..."
if [ -f ".gitignore" ]; then
    check_pass ".gitignore 存在"
    
    if grep -q "node_modules/" .gitignore; then
        check_pass "node_modules 已被忽略"
    else
        check_warn "node_modules 未在 .gitignore 中"
    fi
    
    if grep -q "public/" .gitignore; then
        check_pass "public/ 已被忽略"
    else
        check_warn "public/ 未在 .gitignore 中"
    fi
else
    check_fail ".gitignore 不存在"
fi

# 7. 检查 GitHub 仓库配置
echo ""
echo "7. 检查 Git 配置..."
if git remote get-url origin >/dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    if [[ "$REMOTE_URL" == *"Noeverer.github.io"* ]]; then
        check_pass "Git remote 配置正确: $REMOTE_URL"
    else
        check_warn "Git remote URL 可能不正确: $REMOTE_URL"
    fi
else
    check_fail "Git remote 未配置"
fi

# 8. 检查当前分支
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
if [ "$CURRENT_BRANCH" == "master" ] || [ "$CURRENT_BRANCH" == "main" ]; then
    check_pass "当前分支: $CURRENT_BRANCH"
else
    check_warn "当前分支: $CURRENT_BRANCH (建议使用 master 或 main)"
fi

# 总结
echo ""
echo "=== 验证总结 ==="
echo -e "${GREEN}通过: $PASS${NC}"
echo -e "${YELLOW}警告: $WARN${NC}"
echo -e "${RED}失败: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 所有检查通过！博客配置正确。${NC}"
    echo ""
    echo "下一步操作:"
    echo "1. 运行 'npm install' 安装依赖（如果还未安装）"
    echo "2. 运行 'hexo clean && hexo generate' 生成静态文件"
    echo "3. 运行 'hexo server' 启动本地服务器预览"
    echo "4. 提交更改到 Git 并推送到 GitHub"
    echo "5. GitHub Actions 将自动部署到 gh-pages 分支"
    exit 0
else
    echo -e "${RED}❌ 发现 $FAIL 个问题，请修复后重试。${NC}"
    exit 1
fi
