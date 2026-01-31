# 快速启动指南

## GitHub Actions 自动部署已配置 ✅

项目已配置 GitHub Actions，代码推送到 `master` 分支后会自动部署到 GitHub Pages。

### 部署流程

1. 推送代码到 master 分支
2. GitHub Actions 自动触发
3. 安装依赖（Node.js + Python）
4. 运行 HTML 转换（如果需要）
5. 生成 Hexo 静态站点
6. 部署到 `gh-pages` 分支
7. 发布到 https://noeverer.github.io

### 监控部署状态

访问 GitHub 仓库的 **Actions** 标签页查看部署状态。

### 手动触发部署

在 GitHub 网页上：
1. 进入仓库的 **Actions** 页面
2. 选择 **Hexo Deploy to GitHub Pages** workflow
3. 点击 **Run workflow** 按钮

## 本地开发

### 1. 安装依赖

```bash
npm install
npm install hexo-cli -g
pip3 install beautifulsoup4 GitPython
```

### 2. 启动本地服务器

```bash
hexo server
```

访问: http://localhost:4000

### 3. 创建新文章

```bash
hexo new "文章标题"
```

编辑生成的 Markdown 文件位于 `source/_posts/`。

### 4. 生成静态文件

```bash
hexo clean
hexo generate
```

### 5. 本地预览

```bash
hexo server
```

### 6. 提交并推送

```bash
git add .
git commit -m "描述"
git push origin master
```

GitHub Actions 会自动部署！

## 项目结构

```
Noeverer.github.io/
├── source/_posts/       # 博客文章（Markdown格式）
├── scripts/             # 脚本工具
│   ├── conversion/      # HTML转换脚本
│   ├── deployment/     # 部署脚本
│   └── tools/           # 辅助工具
├── docs/                # 项目文档
├── assets/              # 静态资源（CSS/JS）
├── images/              # 图片资源
├── fonts/               # 字体文件
├── _config.yml          # Hexo配置
└── README.md            # 项目说明
```

## 当前博客统计

- **总文章数**: 17 篇
- **Chocolate 系列**: 8 篇（生活感悟）
- **LeetCode**: 5 篇（技术文章）
- **Python**: 1 篇（数据操作总结）
- **思维导图**: 2 篇（数据结构、算法）
- **其他**: 1 篇

## 常见问题

### Q: 如何修改博客主题？
A: 编辑 `_config.yml` 文件中的 `theme` 配置项。

### Q: 如何添加自定义页面？
A: 在 `source/` 目录下创建新的 Markdown 文件，例如 `source/about.md`。

### Q: 如何添加图片？
A: 将图片放到 `images/` 或 `img/` 目录，然后在 Markdown 中引用：
```
![图片描述](/images/图片名.jpg)
```

### Q: 部署失败怎么办？
A: 查看 GitHub Actions 的日志输出，检查是否有错误信息。

### Q: 如何从 HTML 转换到 Markdown？
A: 运行转换脚本：
```bash
python3 scripts/conversion/restore_and_convert_final.py
```

## 需要帮助？

查看详细文档：
- `README.md` - 完整项目说明
- `docs/MIGRATION_GUIDE.md` - 迁移指南
- `docs/FINAL_CONVERSION_REPORT.md` - 转换报告

---

🌐 博客地址: https://noeverer.github.io
