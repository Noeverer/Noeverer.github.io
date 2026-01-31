# Hexo 使用说明

## 项目结构

这是一个基于 Hexo 的静态博客项目，可以直接生成静态 HTML 文件并部署到 GitHub Pages。

## 常用 Hexo 命令

### 1. 初始化新的 Hexo 项目（如果需要重新搭建）
```bash
npm install -g hexo-cli
hexo init blog
cd blog
npm install
```

### 2. 新建文章
```bash
hexo new "文章标题"
# 或者使用别名
hexo n "文章标题"
```

### 3. 生成静态文件
```bash
hexo generate
# 或者使用别名
hexo g
```

### 4. 启动本地服务器预览
```bash
hexo server
# 或者使用别名
hexo s
```
默认访问地址: http://localhost:4000

### 5. 清理缓存文件
```bash
hexo clean
```

### 6. 部署到 GitHub Pages
```bash
hexo deploy
# 或者使用别名
hexo d
```

### 7. 一键生成并部署
```bash
hexo generate --deploy
# 或者
hexo g -d
```

### 8. 一键生成并启动服务器
```bash
hexo server --generate
# 或者
hexo s -g
```

## 本项目自动化脚本

本项目包含一个自动化部署脚本 [deploy.sh](deploy.sh)，可以一键执行清理、生成和部署操作。

使用方法：
```bash
chmod +x deploy.sh
./deploy.sh
```

该脚本会自动检查环境依赖，安装必要的组件，并执行完整的部署流程。

## 项目配置

主要配置文件：
- `_config.yml`: 站点配置文件
- `themes/[theme]/_config.yml`: 主题配置文件

## 写作流程

1. 使用 `hexo new "文章名"` 创建新文章
2. 在 `source/_posts/` 目录下编辑生成的 Markdown 文件
3. 使用 `hexo server` 预览效果
4. 使用 `hexo generate` 生成静态文件
5. 使用 `hexo deploy` 部署到 GitHub Pages