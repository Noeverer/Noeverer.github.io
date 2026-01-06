# HTML to Hexo 快速开始指南

## 一键安装

```bash
bash install.sh
```

安装脚本会自动：
- 检查环境（Python3, Node.js, Git）
- 安装Python依赖（beautifulsoup4, GitPython）
- 安装Hexo CLI和npm依赖
- 设置脚本权限
- 创建必要目录

## 验证安装

```bash
python3 test_system.py
```

运行测试脚本验证所有组件是否正常工作。

## 快速使用

### 1. 转换HTML到Markdown

```bash
python3 html2hexo.py
```

这会：
- 扫描所有HTML文件
- 提取文章内容和元数据
- 转换为Markdown格式
- 保存到 `source/_posts/` 目录
- 显示主题推荐

### 2. 本地预览

```bash
python3 deploy_helper.py serve
```

访问 http://localhost:4000 查看效果。

### 3. 部署到GitHub Pages

```bash
# 提交更改
git add .
git commit -m "Update posts"
git push origin master
```

推送到master后会自动触发GitHub Actions部署。

## 主要功能

### 命令行选项

```bash
# 完整转换
python3 html2hexo.py

# 转换指定目录
python3 html2hexo.py --dir ./chocolate

# 创建特性分支
python3 html2hexo.py --branch chocolate

# 只显示主题推荐
python3 html2hexo.py --recommend

# 设置GitHub Actions
python3 html2hexo.py --setup
```

### 部署辅助命令

```bash
# 完整设置（安装依赖+转换+构建）
python3 deploy_helper.py setup

# 只转换HTML
python3 deploy_helper.py convert

# 构建站点
python3 deploy_helper.py build

# 启动服务器
python3 deploy_helper.py serve

# 创建新文章
python3 deploy_helper.py new --title "My Post"

# 查看状态
python3 deploy_helper.py status

# 部署
python3 deploy_helper.py deploy
```

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `html2hexo.py` | 主转换脚本 |
| `deploy_helper.py` | 部署辅助工具 |
| `test_system.py` | 系统测试脚本 |
| `install.sh` | 一键安装脚本 |
| `.github/workflows/hexo-deploy.yml` | GitHub Actions配置 |

## 文档

- **HTML2HEXO_README.md** - 完整使用说明
- **BRANCH_WORKFLOW.md** - Git分支管理工作流
- **QUICK_START.md** - 本文件

## 分支管理

### 创建特性分支

```bash
python3 html2hexo.py --branch chocolate
```

或手动创建：
```bash
git checkout -b feature/chocolate-20250105
python3 html2hexo.py
git add .
git commit -m "Add chocolate posts"
git push origin feature/chocolate-20250105
```

### 合并到主分支

```bash
git checkout master
git merge feature/chocolate-20250105
git push origin master
```

## 主题推荐

运行转换后会自动分析内容并推荐主题：

1. **NexT** (95分) - 功能最全面
2. **Butterfly** (92分) - 美观现代
3. **Fluid** (90分) - 简洁优雅

推荐安装命令：
```bash
cd themes
git clone https://github.com/next-theme/hexo-theme-next next
```

## 常见问题

### 安装失败

1. 确保已安装Python3、Node.js、Git
2. 检查网络连接
3. 使用国内镜像：
   ```bash
   pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple beautifulsoup4 GitPython
   npm config set registry https://registry.npmmirror.com
   ```

### 转换失败

1. 查看日志：`cat html2hexo.log`
2. 确保HTML文件编码为UTF-8
3. 检查文件路径是否正确

### 部署失败

1. 确认GitHub仓库启用了Pages
2. 检查GITHUB_TOKEN权限
3. 查看GitHub Actions运行日志

## 下一步

1. ✅ 运行安装脚本：`bash install.sh`
2. ✅ 验证安装：`python3 test_system.py`
3. ✅ 转换HTML：`python3 html2hexo.py`
4. ✅ 本地预览：`python3 deploy_helper.py serve`
5. ✅ 提交部署：`git push origin master`

## 获取帮助

- 查看日志文件：`html2hexo.log`
- 阅读完整文档：`HTML2HEXO_README.md`
- 分支管理：`BRANCH_WORKFLOW.md`
