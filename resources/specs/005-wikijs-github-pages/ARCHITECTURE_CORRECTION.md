# Spec 005 架构修正总结

## 修正日期
2026-01-19

## 修正内容

### 问题
之前的实现使用了额外的 git 脚本来实现版本控制，而不是利用 Wiki.js 内置的 Git 存储功能。

### 解决方案
完全依赖 Wiki.js 内置的 Git 存储功能，删除所有不必要的 git 脚本。

## 修正前后的对比

### 修正前的错误架构

```
Wiki.js → 手动 git 脚本 → GitHub → GitHub Actions → GitHub Pages
         ❌ sync-to-git.sh
         ❌ sync-to-vitepress.sh
         ❌ 定时任务（cron）
```

### 修正后的正确架构

```
Wiki.js 内置 Git 存储 → GitHub → GitHub Actions → GitHub Pages
         ✅ 自动同步
         ✅ 无需脚本
         ✅ 官方支持
```

## 删除的文件和目录

### 1. `tools/wikijs-syn/wikijs-data-local/` 目录
- ❌ `sync-to-git.sh` - 不需要手动 git 同步
- ❌ `.gitignore` - Git 管理由 Wiki.js 内部处理
- ❌ `README.md` - 相关说明整合到主文档
- ❌ 整个目录 - Wiki.js 内部管理 Git 数据

### 2. `tools/wikijs-syn/wikijs-deploy/sync-to-vitepress.sh`
- ❌ 不需要 - 内容通过 Wiki.js Git 自动同步到 GitHub

### 3. `source/resources/wikijs/` 目录（之前已删除）
- 完整的重复目录，所有文件都与 `tools/wikijs-syn/` 重复

## 新增的文件

### 1. `GIT_STORAGE_ARCHITECTURE.md`
详细说明了 Wiki.js 内置 Git 存储功能的正确使用方法。

内容包括：
- 架构原则
- Wiki.js Git 存储配置
- 工作流程
- 优势对比
- 配置验证
- 注意事项

### 2. 更新的文档
- ✅ `README.md` - 强调使用 Wiki.js 内置功能
- ✅ `QUICK_START.md` - 添加架构说明章节
- ✅ `IMPLEMENTATION.md` - 完全重写，反映正确架构
- ✅ `wikijs-content/README.md` - 说明 Wiki.js 自动同步机制
- ✅ `docker-compose.yml` - 简化配置，使用 Docker 卷而非本地目录

## 修正后的正确工作流程

### 1. 启动 Wiki.js
```bash
cd /home/ante/10-personal/Noeverer.github.io/tools/wikijs-syn/wikijs-deploy
./start.sh
```

### 2. 初始化 VitePress 仓库
```bash
cd /home/ante/10-personal/Noeverer.github.io/tools/wikijs-syn/wikijs-content
./init-vitepress.sh

# 初始化 Git 仓库
git init
git add .
git commit -m "Initial VitePress setup"

# 推送到 GitHub
git remote add origin https://github.com/Noeverer/wikijs-content.git
git branch -M main
git push -u origin main
```

### 3. 配置 Wiki.js Git 存储
在 Wiki.js 管理后台配置 Git 存储（**使用 Wiki.js 内置功能**）

| 参数 | 值 |
|------|-----|
| 存储标识符 | `github-wiki` |
| 存储模式 | 读写 |
| Git URL | `https://github.com/Noeverer/wikijs-content.git` |
| 分支 | `main` |
| 验证方式 | HTTPS |
| 用户名 | `Noeverer` |
| 密码 | `[你的 GitHub PAT]` |
| 同步间隔 | `5 分钟` |

### 4. 创建和编辑内容
在 Wiki.js 界面中创建和编辑内容，Wiki.js 会自动同步到 GitHub。

### 5. GitHub Pages 自动构建
GitHub Actions 检测到推送后自动构建并部署。

## 最终目录结构

```
tools/wikijs-syn/
├── wikijs-deploy/              # Wiki.js 部署配置
│   ├── docker-compose.yml      # Docker Compose 配置
│   ├── .env                   # 环境变量
│   ├── .env.example           # 环境变量示例
│   ├── start.sh               # 快速启动脚本
│   ├── deploy.sh              # 部署脚本
│   ├── QUICK_START.md         # 快速开始指南
│   ├── TROUBLESHOOTING.md     # 故障排除指南
│   ├── GIT_STORAGE_ARCHITECTURE.md # Git 存储架构说明
│   ├── backup/
│   │   └── backup.sh          # 备份脚本
│   ├── logs/                  # 日志目录
│   └── nginx/
│       └── wikijs.conf       # Nginx 配置
│
└── wikijs-content/            # VitePress 内容（Git 仓库）
    ├── docs/                  # 文档内容（Wiki.js 自动同步）
    ├── .vitepress/
    │   └── config.ts         # VitePress 配置
    ├── .github/
    │   └── workflows/
    │       └── build-pages.yml # GitHub Actions 工作流
    ├── package.json          # NPM 配置
    ├── README.md             # 仓库说明
    ├── .gitignore            # Git 忽略规则
    └── init-vitepress.sh     # 初始化脚本
```

## 修正效果

### 文件精简
- ✅ 删除了 `wikijs-data-local/` 整个目录
- ✅ 删除了 `sync-to-git.sh` 脚本
- ✅ 删除了 `sync-to-vitepress.sh` 脚本
- ✅ 减少了约 10+ 个不必要的文件

### 架构简化
- ✅ 完全依赖 Wiki.js 内置 Git 功能
- ✅ 无需维护额外的 git 脚本
- ✅ 无需设置定时任务（cron job）
- ✅ 简化了运维复杂度

### 功能提升
- ✅ 双向同步支持（Wiki.js ↔ GitHub）
- ✅ 自动冲突处理
- ✅ 完整的版本历史
- ✅ 界面友好的 Git 状态查看

## 优势对比

| 特性 | 修正前（额外脚本） | 修正后（Wiki.js 内置） |
|------|------------------|---------------------|
| 自动化程度 | ❌ 需要手动/定时任务 | ✅ 完全自动化 |
| 可靠性 | ❌ 脚本可能出错 | ✅ 官方支持，充分测试 |
| 维护成本 | ❌ 需要维护脚本 | ✅ 无需维护 |
| 冲突处理 | ❌ 需要手动处理 | ✅ 内置冲突解决机制 |
| 同步方式 | ❌ 单向同步 | ✅ 双向同步 |
| 复杂性 | ❌ 复杂 | ✅ 简单 |
| 官方支持 | ❌ 无 | ✅ 有 |

## 相关文档

- [Git 存储架构说明](../tools/wikijs-syn/wikijs-deploy/GIT_STORAGE_ARCHITECTURE.md)
- [实现总结](IMPLEMENTATION.md)
- [快速开始指南](../tools/wikijs-syn/wikijs-deploy/QUICK_START.md)
- [故障排除指南](../tools/wikijs-syn/wikijs-deploy/TROUBLESHOOTING.md)
