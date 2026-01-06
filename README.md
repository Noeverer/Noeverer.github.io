# Noeverer GitHub.io 博客项目

基于 Hexo + Butterfly 的个人博客，使用 GitHub Actions 自动部署到 GitHub Pages。

## 🎨 主题

- **主题**: [Butterfly](https://github.com/jerryc127/hexo-theme-butterfly) v5.5.3
- **风格**: 现代卡片式布局，支持暗色模式
- **特性**: 响应式设计、代码高亮、图片懒加载、本地搜索

## 项目结构

```
Noeverer.github.io/
├── .github/
│   └── workflows/
│       └── hexo-deploy.yml      # GitHub Actions 自动部署配置
├── _config.yml                   # Hexo 主配置文件
├── _config.butterfly.yml         # Butterfly 主题配置
├── scripts_tools_backup/         # 备份的脚本工具（避免Hexo冲突）
│   ├── conversion/               # HTML转Markdown转换脚本
│   ├── deployment/               # 部署脚本
│   └── tools/                    # 工具脚本
├── source/                       # 博客源文件
│   └── _posts/                   # Markdown 格式文章（16篇）
├── public/                       # Hexo 生成的静态网站
├── assets/                       # 静态资源（CSS/JS）
├── docs/                         # 项目文档
├── fonts/                        # 字体文件
├── images/                       # 图片资源
├── img/                          # 图片资源
├── mind/                         # 思维导图文件
├── _config.yml                   # Hexo 主配置文件
├── _config.next.yml              # 备用配置文件
├── package.json                  # Node.js 依赖配置
├── package-lock.json             # 依赖锁定文件
├── .gitignore                    # Git 忽略文件
├── .nojekyll                     # 禁用 Jekyll 处理
├── main.0cf68a.css               # 构建产物
├── main.0cf68a.js                # 构建产物
├── mobile.992cbe.js              # 构建产物
└── slider.e37972.js              # 构建产物
```

## 文章统计

目前包含 **16篇** 博客文章：

- **Chocolate 系列**（生活感悟）: 8篇
  - 2015-2019 年春季/秋季感悟
- **LeetCode 技术文章**: 5篇
  - 包含完整的 Python 代码解答
- **Python 总结**: 1篇
  - Python 数据操作总结
- **思维导图**: 2篇
  - 数据结构
  - 算法

## 本地开发

### 安装依赖

```bash
npm install
npm install hexo-cli -g
```

### 安装 Python 依赖

```bash
pip3 install beautifulsoup4 GitPython
```

### 启动本地服务器

```bash
hexo server
```

访问: http://localhost:4000

### 新建文章

```bash
hexo new "文章标题"
```

### 生成静态文件

```bash
hexo clean
hexo generate
```

## HTML 转换

如果需要将 HTML 文件转换为 Markdown 格式：

```bash
cd scripts_tools_backup
python3 conversion/restore_and_convert_final.py
```

## GitHub Actions 自动部署

项目配置了 GitHub Actions，当代码推送到 `master` 分支时会自动：

1. 安装 Node.js 和 npm 依赖
2. 安装 Python 依赖
3. 运行 HTML 转换脚本（如果存在）
4. 生成 Hexo 静态站点
5. 部署到 GitHub Pages (`gh-pages` 分支)
6. 创建部署标签
7. 通知部署状态

### 访问博客

🌐 https://noeverer.github.io

## 项目文档

详细的项目文档和迁移记录位于 `docs/` 目录：

- `FINAL_CONVERSION_REPORT.md` - HTML 转 Markdown 最终报告
- `MIGRATION_GUIDE.md` - 迁移指南
- `QUICK_START.md` - 快速开始
- `THEME_RECOMMENDATION.md` - 主题推荐
- 其他技术文档...

## 许可证

MIT License
