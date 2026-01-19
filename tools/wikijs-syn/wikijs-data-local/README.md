# Wiki.js 本地数据存储

Wiki.js 的 Git 存储内容将保存在此目录中。

## 目录结构

```
wikijs-data-local/
├── .git/              # Git 仓库
├── docs/              # Wiki 文档
├── .gitignore         # Git 忽略规则
└── README.md         # 说明文档
```

## 使用说明

### 1. 初始化 Git 仓库

```bash
cd /home/ante/10-personal/wikijs-data-local
git init
git add .
git commit -m "Initial Wiki.js content"
```

### 2. 关联到远程仓库

```bash
# 方式 1: 关联到 wikijs-content 仓库
git remote add origin https://github.com/Noeverer/wikijs-content.git

# 方式 2: 使用 SSH（推荐）
git remote add origin git@github.com:Noeverer/wikijs-content.git
```

### 3. 推送到 GitHub

```bash
git push -u origin main
```

### 4. Wiki.js 配置 Git 存储

在 Wiki.js 管理界面配置 Git 存储：

| 参数 | 值 |
|------|---|
| 本地仓库路径 | `/wiki/data/repo` |
| Git URL | `https://github.com/Noeverer/wikijs-content.git` |
| 分支 | `main` |

## 自动同步脚本

### 同步到 GitHub

```bash
cd /home/ante/10-personal/wikijs-data-local
git add .
git commit -m "Update wiki content"
git push
```

### 从 GitHub 拉取

```bash
cd /home/ante/10-personal/wikijs-data-local
git pull
```

## 定时同步

使用 cron 定时同步：

```bash
# 编辑 crontab
crontab -e

# 添加每 5 分钟同步一次
*/5 * * * * cd /home/ante/10-personal/wikijs-data-local && git pull --quiet && git add . && git commit -m "Auto-sync $(date '+%Y-%m-%d %H:%M')" && git push --quiet
```

## 注意事项

1. **冲突处理**: 手动编辑和 Wiki.js 编辑可能产生冲突，需要手动解决
2. **大文件**: 上传的大文件存储在 Docker 卷中，不在 Git 中
3. **敏感信息**: 不要在 Wiki 中存放敏感信息
4. **备份**: 建议定期备份数据库

## 与 VitePress 的关系

- 此目录是 Wiki.js 的 Git 存储源
- `wikijs-content/` 目录用于 VitePress 构建
- 可以通过脚本将内容复制到 `wikijs-content/docs/`

## 相关命令

```bash
# 查看状态
git status

# 查看改动
git diff

# 查看提交历史
git log --oneline

# 回滚到指定提交
git reset --hard <commit-id>

# 创建新分支
git checkout -b feature-branch

# 合并分支
git merge feature-branch
```
