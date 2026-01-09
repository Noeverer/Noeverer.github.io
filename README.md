# Ante Liu 的博客

> 基于 Hexo + Butterfly，通过 GitHub Actions 自动部署

## 🌐 访问地址

**https://noeverer.github.io**

---

## 📝 写作方式

本地只需专注写作，推送到 GitHub 后自动发布。

### 新建文章

```bash
npm run new "文章标题"
# 或
hexo new "文章标题"
```

文章会在 `source/_posts/` 目录下创建，使用 Markdown 编写即可。

### 文章格式要求

所有文章必须包含 front matter（文章元数据）：

```markdown
---
title: 文章标题
date: YYYY-MM-DD HH:mm:ss
tags: ["标签1", "标签2"]
categories: 分类
description: 文章描述
---

文章内容...
```

### 预览本地效果（可选）

```bash
# 方式1：开发模式（推荐）
npm run dev

# 方式2：分步执行
npm install
npm run server
```

访问 http://localhost:4000

### 验证配置

```bash
# 验证博客配置是否正确
npm run verify

# 本地测试构建（模拟 GitHub Actions）
npm run test-build
```

### 发布文章

```bash
git add .
git commit -m "发布新文章"
git push origin master
```

推送到 `master` 分支后，GitHub Actions 会自动构建并部署。

---

## 📂 项目结构

```
Noeverer.github.io/
├── .github/workflows/deploy.yml    # GitHub Actions 自动部署
├── _config.yml                      # Hexo 主配置
├── _config.butterfly.yml            # Butterfly 主题配置
├── source/                          # 博客内容
│   ├── _posts/                      # 所有 Markdown 文章
│   └── about/                       # 关于页面
├── scripts/                         # 验证和测试脚本
│   ├── verify-blog.sh               # 博客配置验证
│   ├── local-test-build.sh          # 本地构建测试
│   └── README.md                    # 脚本使用说明
├── package.json                     # 依赖配置
└── .gitignore                       # Git 忽略规则
```

---

## 🤖 自动部署流程

当代码推送到 `master` 分支时，GitHub Actions 会自动：

1. 安装 Node.js 18 和 npm 依赖
2. 验证主题安装
3. 运行 `hexo clean` 和 `hexo generate` 生成静态网站
4. 验证构建输出（检查 index.html 是否生成）
5. 将生成的 `public/` 目录部署到 `gh-pages` 分支
6. 显示部署摘要

无需手动执行任何部署命令，专注于写作即可。

---

## 🔧 验证和测试工具

### 1. 验证博客配置

```bash
npm run verify
```

**检查内容：**
- 必要文件是否存在
- 依赖是否正确安装
- 源文件目录结构
- 所有 markdown 文件的 front matter
- Hexo 配置
- Git 仓库配置

### 2. 本地构建测试

```bash
npm run test-build
```

**执行步骤：**
- 检查依赖
- 清理缓存
- 生成静态文件
- 验证构建输出
- 显示构建摘要
- 可选启动本地服务器

### 3. 开发模式

```bash
npm run dev
```

自动执行：清理 + 生成 + 启动服务器

---

## 📊 内容统计

- **总文章数**: 16篇
- **Chocolate 系列**: 8篇（2015-2019年生活感悟）
- **技术文章**: 5篇（LeetCode + Python总结）
- **思维导图**: 2篇（数据结构、算法）
- **新添加**: openmanus 学习笔记、Wiki.js 部署指南

---

## 🎨 主题信息

- **主题**: [Butterfly](https://github.com/jerryc127/hexo-theme-butterfly) v5.5.3
- **特性**: 响应式设计、暗色模式、代码高亮、图片懒加载、本地搜索

---

## 📖 常用命令

```bash
# 开发模式（清理 + 生成 + 启动服务器）
npm run dev

# 验证配置
npm run verify

# 本地测试构建
npm run test-build

# 清理缓存
npm run clean

# 生成静态文件
npm run build

# 启动本地服务器
npm run server

# 新建文章
npm run new "文章标题"
```

---

## 🐛 故障排除

### 构建失败

```bash
# 清理缓存
npm run clean

# 重新安装依赖
rm -rf node_modules package-lock.json
npm install

# 验证配置
npm run verify

# 本地测试构建
npm run test-build
```

### Front Matter 错误

确保所有文章包含正确的 front matter：

```markdown
---
title: 文章标题
date: YYYY-MM-DD HH:mm:ss
tags: ["标签1", "标签2"]
categories: 分类
description: 文章描述
---
```

### 主题未加载

```bash
# 检查主题是否安装
ls node_modules/hexo-theme-butterfly

# 重新安装主题
npm install hexo-theme-butterfly
```

---

## 📄 许可证

MIT License

---

## 📚 更多文档

详细的脚本使用说明请查看：[scripts/README.md](scripts/README.md)

