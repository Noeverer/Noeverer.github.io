# Noeverer.github.io

> 个人博客项目 - 基于 Hexo 的静态博客系统

## 📖 项目概述

这是一个个人博客项目，使用 Hexo 框架构建。该项目包含完整的博客内容、主题配置和自动化脚本。

## 🏗️ 目录结构

```
Noeverer.github.io/
├── blog/                 # Hexo 博客源文件
│   ├── _config.yml       # Hexo 主配置
│   ├── _config.butterfly.yml  # Butterfly 主题配置
│   ├── source/           # 博客源文件
│   │   ├── _posts/       # 博客文章
│   │   └── ...           # 其他页面
│   ├── themes/           # 主题文件
│   └── scaffolds/        # 模板文件
├── public/               # 生成的静态文件
├── scripts/              # 自动化脚本
├── resources/            # 资源文件
├── specs/                # 规范文档
├── tools/                # 工具脚本
└── deploy.sh             # 部署脚本
```

## 🚀 快速开始

### 环境要求

- Node.js (>= 14.0.0)
- npm
- Git

### 安装依赖

```bash
cd blog
npm install
```

### 本地开发

```bash
# 启动本地服务器
npm run dev

# 或者使用 hexo 命令
hexo server
```

### 生成静态文件

```bash
hexo generate
```

### 部署

```bash
# 使用部署脚本
./deploy.sh
```

## 📝 博客内容

博客文章位于 `blog/source/_posts/` 目录中，按照年份/月份/工具分类组织：

- `2026/01-tools/` - 工具相关文章
- `2026/03-ai-apps/` - AI 应用相关文章
- `2025/01-openmanus/` - OpenManus 项目相关
- `2026/00-personal-goal/` - 个人目标相关

## 🎨 主题配置

使用 Butterfly 主题，配置文件位于：

- `_config.butterfly.yml` - 主题配置
- `_config.yml` - Hexo 配置

## 🤖 自动化功能

项目包含多种自动化脚本：

- `scripts/` - 转换和处理脚本
- `tools/` - 工具脚本
- `resources/` - 资源文件
- `specs/` - 项目规范

## 📚 MCP 系统指南

本博客包含一个完整的 MCP（Model Context Protocol）系统指南，分为以下章节：

1. [MCP 基础](blog/source/_posts/2026/01-tools/01-what-is-mcp.md)
2. [AI Agents](blog/source/_posts/2026/01-tools/02-ai-agents.md)
3. [Skills 系统](blog/source/_posts/2026/01-tools/03-skills-system.md)
4. [Memories 系统](blog/source/_posts/2026/01-tools/04-memories-system.md)
5. [Rules 系统](blog/source/_posts/2026/01-tools/05-rules-system.md)
6. [系统集成最佳实践](blog/source/_posts/2026/01-tools/06-integration-best-practices.md)

## 🛠️ 维护脚本

- `archive_changes.sh` - 归档更改脚本
- `deploy.sh` - 部署脚本
- 各种自动化处理脚本

## 📄 许可证

MIT License