# 博客配置快速参考

快速查阅常用配置和命令。

---

## 📂 核心配置文件

| 文件 | 用途 |
|------|------|
| `_config.yml` | Hexo 主配置 |
| `_config.butterfly.yml` | Butterfly 主题配置 |
| `package.json` | Node.js 依赖 |
| `.github/workflows/deploy.yml` | GitHub Actions 部署配置 |

---

## 🖼️ 图片路径规则

### 绝对路径（推荐）
```yaml
avatar:
  img: /img/monkey.jpg
```
- 从项目根目录读取
- 适合头像、通用图片

### 相对路径
```yaml
cover: images/cover.jpg
```
- 从 `source` 目录读取
- 适合文章封面

### 外部链接
```yaml
cover: https://example.com/image.jpg
```
- 使用外部图片托管

---

## 🚀 常用命令

### 文章管理
```bash
# 新建文章
hexo new "文章标题"

# 新建页面
hexo new page "about"

# 新建草稿
hexo new draft "草稿标题"
```

### 本地开发
```bash
# 安装依赖
npm install
npm install hexo-cli -g

# 启动服务器
hexo server
# 访问 http://localhost:4000

# 清理缓存
hexo clean
```

### 构建和部署
```bash
# 生成静态文件（本地测试用）
hexo generate

# Git 操作
git add .
git commit -m "提交信息"
git push origin master
```

---

## 🎨 快速配置修改

### 修改头像
编辑 `_config.butterfly.yml`：

```yaml
avatar:
  img: /img/你的图片.jpg
```

### 修改导航菜单
编辑 `_config.butterfly.yml`：

```yaml
menu:
  首页: / || fas fa-home
  首页: http://example.com || fas fa-home  # 外部链接
```

### 修改主题颜色
编辑 `_config.butterfly.yml`：

```yaml
theme_color:
  main: '#4C4948'
  paginator: '#00c4b6'
```

### 修改顶部图
编辑 `_config.butterfly.yml`：

```yaml
default_top_img: linear-gradient(20deg, #0062be, #925696, #cc426e, #f43059)
# 或使用图片
# default_top_img: /img/banner.jpg
```

---

## 📝 文章 Front Matter

```yaml
---
title: 文章标题
date: 2026-01-07 00:00:00
updated: 2026-01-07 00:00:00
tags:
  - 标签1
  - 标签2
categories:
  - 分类1
cover: /img/cover.jpg    # 封面图
toc: true                # 显示目录
copyright: true          # 显示版权
top: true                # 置顶文章
---
```

---

## 🔗 GitHub Pages 设置

### 正确的设置

```
Settings → Pages

Source: Deploy from a branch
Branch: gh-pages
Folder: / (root)
```

### 常见问题

- **404 错误**：检查 `gh-pages` 分支是否存在，检查 Settings → Pages 设置
- **样式丢失**：检查 `.nojekyll` 文件是否存在
- **图片不显示**：检查图片路径是否正确

---

## 🤖 GitHub Actions 工作流

### 触发条件
- 推送到 `master` 分支
- 在 Actions 页面手动触发

### 部署流程
1. 检出代码
2. 安装 Node.js
3. 安装依赖
4. 构建站点
5. 验证构建
6. 部署到 gh-pages

### 查看日志
```
仓库首页 → Actions 标签 → 点击工作流记录
```

---

## 📊 项目结构

```
Noeverer.github.io/
├── .github/workflows/
│   └── deploy.yml           # GitHub Actions 配置
├── source/
│   ├── _posts/              # 所有文章
│   ├── about/               # 关于页面
│   ├── categories/          # 分类页（自动生成）
│   └── tags/                # 标签页（自动生成）
├── img/                     # 图片资源
│   ├── monkey.jpg           # 头像
│   ├── photo.jpg            # 照片
│   ├── wechat.png           # 微信二维码
│   └── alipay.png           # 支付宝二维码
├── images/                  # 更多图片资源
├── fonts/                   # 字体文件
├── docs/                    # 项目文档
├── _config.yml              # Hexo 配置
├── _config.butterfly.yml    # 主题配置
├── package.json             # 依赖配置
├── .gitignore               # Git 忽略规则
└── .nojekyll                # 禁用 Jekyll
```

---

## ⌨️ 常用快捷键

### Markdown 编辑
- `Ctrl + B` - 粗体
- `Ctrl + I` - 斜体
- `Ctrl + K` - 插入链接
- `Ctrl + Shift + K` - 插入代码块

### Git
- `git status` - 查看状态
- `git diff` - 查看改动
- `git log --oneline -10` - 查看最近10条提交

---

## 🔧 故障排查

### 本地预览正常，部署后 404
1. 检查 GitHub Pages 设置
2. 确认 `.nojekyll` 文件存在
3. 查看 Actions 日志

### 图片不显示
1. 检查图片路径
2. 确认图片文件存在
3. 清除浏览器缓存

### 样式错乱
1. 运行 `hexo clean`
2. 重新构建部署
3. 强制刷新浏览器（Ctrl + Shift + R）

---

## 📱 移动端适配

Butterfly 主题默认支持响应式设计，无需额外配置。

### 移动端菜单设置
```yaml
aside:
  mobile: true  # 启用移动端侧边栏
```

---

## 🔐 隐私和版权

### 启用版权声明
```yaml
post_copyright:
  enable: true
  license: CC BY-NC-SA 4.0
  license_url: https://creativecommons.org/licenses/by-nc-sa/4.0/
```

### 禁用评论
```yaml
comments:
  use: false
```

---

## 🌐 访问地址

- **本地预览**: http://localhost:4000
- **线上访问**: https://noeverer.github.io
- **GitHub 仓库**: https://github.com/Noeverer/Noeverer.github.io
- **Actions 页面**: https://github.com/Noeverer/Noeverer.github.io/actions
