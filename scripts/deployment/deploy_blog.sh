#!/bin/bash

# 博客部署脚本
# 用于部署不同分支的Hexo博客到GitHub Pages

set -e  # 遇到错误时退出

echo "==========================================="
echo "博客部署脚本"
echo "==========================================="

# 检查是否安装了hexo-cli
if ! command -v hexo &> /dev/null; then
    echo "正在安装hexo-cli..."
    npm install -g hexo-cli
fi

# 部署函数
deploy_branch() {
    local branch_name=$1
    local branch_desc=$2
    
    echo ""
    echo "部署 $branch_desc ($branch_name 分支)..."
    echo "-------------------------------------------"
    
    cd "/workspace/distributed/$branch_name"
    
    # 安装依赖
    echo "安装依赖..."
    npm install
    
    # 生成静态文件
    echo "生成静态文件..."
    hexo clean
    hexo generate
    
    # 显示生成的文件数量
    local post_count=$(ls source/_posts/ | grep -c "\.md$")
    local file_count=$(find public -type f | wc -l)
    echo "已处理 $post_count 篇文章，生成 $file_count 个文件"
    
    # 如果提供了部署参数，则执行部署
    if [ "$3" = "deploy" ]; then
        echo "部署到GitHub Pages..."
        hexo deploy
        echo "$branch_desc 分支部署完成！"
    else
        echo "$branch_desc 分支生成完成！文件位于: /workspace/distributed/$branch_name/public"
    fi
    
    cd - > /dev/null
}

# 主菜单
show_menu() {
    echo ""
    echo "请选择要执行的操作："
    echo "1) 生成所有分支的静态文件"
    echo "2) 部署所有分支到GitHub Pages"
    echo "3) 仅生成个人生活分支"
    echo "4) 仅生成技术博客分支"
    echo "5) 仅生成工作记录分支"
    echo "6) 部署个人生活分支"
    echo "7) 部署技术博客分支"
    echo "8) 部署工作记录分支"
    echo "9) 查看博客统计信息"
    echo "0) 退出"
    echo ""
    read -p "请输入选项 (0-9): " choice
    
    case $choice in
        1)
            deploy_branch "personal" "个人生活" "generate"
            deploy_branch "tech" "技术博客" "generate"
            deploy_branch "work" "工作记录" "generate"
            echo ""
            echo "所有分支生成完成！"
            ;;
        2)
            deploy_branch "personal" "个人生活" "deploy"
            deploy_branch "tech" "技术博客" "deploy"
            deploy_branch "work" "工作记录" "deploy"
            echo ""
            echo "所有分支部署完成！"
            ;;
        3)
            deploy_branch "personal" "个人生活" "generate"
            ;;
        4)
            deploy_branch "tech" "技术博客" "generate"
            ;;
        5)
            deploy_branch "work" "工作记录" "generate"
            ;;
        6)
            deploy_branch "personal" "个人生活" "deploy"
            ;;
        7)
            deploy_branch "tech" "技术博客" "deploy"
            ;;
        8)
            deploy_branch "work" "工作记录" "deploy"
            ;;
        9)
            show_stats
            ;;
        0)
            echo "退出脚本。"
            exit 0
            ;;
        *)
            echo "无效选项，请重试。"
            show_menu
            ;;
    esac
}

# 显示统计信息
show_stats() {
    echo ""
    echo "博客统计信息："
    echo "==========================================="
    
    for branch in personal tech work; do
        if [ -d "/workspace/distributed/$branch/source/_posts" ]; then
            post_count=$(ls "/workspace/distributed/$branch/source/_posts/" | grep -c "\.md$" 2>/dev/null || echo 0)
            echo "$branch 分支: $post_count 篇文章"
            
            # 显示最近的几篇文章
            echo "  最新文章:"
            ls -t "/workspace/distributed/$branch/source/_posts/" | head -3 | while read file; do
                echo "    - $file"
            done
            echo ""
        fi
    done
}

# 如果脚本被直接执行（而不是被source），则运行菜单
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_menu
fi