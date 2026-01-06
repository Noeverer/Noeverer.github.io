# Git分支管理工作流

本文档说明如何使用自动化系统管理Git分支进行内容开发。

## 分支策略

### 主分支
- `master` - 主分支，用于生产环境
- `gh-pages` - GitHub Pages部署分支（自动生成）

### 特性分支
- `feature/{category}-{date}` - 按内容分类创建的特性分支
  - 例如: `feature/chocolate-20250105`
  - 例如: `feature/code-20250105`

### 其他分支
- `dev` - 开发分支
- `hotfix/{description}` - 紧急修复分支

## 工作流程

### 1. 开始新内容

```bash
# 为chocolate分类创建新分支
python3 html2hexo.py --branch chocolate
```

或手动创建：
```bash
git checkout -b feature/chocolate-20250105
```

### 2. 转换和编辑内容

```bash
# 运行HTML转换
python3 html2hexo.py

# 手动编辑Markdown文件
vim source/_posts/2019-01-01-example.md
```

### 3. 提交更改

```bash
# 查看更改
git status

# 添加文件
git add .

# 提交
git commit -m "Add new chocolate posts"
```

### 4. 推送分支

```bash
git push origin feature/chocolate-20250105
```

### 5. 创建Pull Request

1. 在GitHub上创建Pull Request
2. 等待代码审查
3. 合并到master分支

### 6. 自动部署

合并到master后，GitHub Actions会自动：
- 构建Hexo站点
- 部署到GitHub Pages
- 创建版本标签

## 命令参考

### 查看所有分支

```bash
git branch -a
```

### 创建新分支

```bash
# 使用脚本创建
python3 html2hexo.py --branch <category>

# 手动创建
git checkout -b <branch-name>
```

### 切换分支

```bash
git checkout <branch-name>
```

### 合并分支

```bash
# 合并到master
git checkout master
git merge feature/chocolate-20250105

# 删除已合并的分支
git branch -d feature/chocolate-20250105
git push origin --delete feature/chocolate-20250105
```

### 查看分支差异

```bash
# 查看差异
git diff master..feature/chocolate-20250105

# 查看特定文件差异
git diff master..feature/chocolate-20250105 -- source/_posts/
```

## 多人协作

### 1. 同步最新代码

```bash
git checkout master
git pull origin master
```

### 2. 在特性分支上同步master

```bash
git checkout feature/chocolate-20250105
git merge master
```

### 3. 解决冲突

```bash
# 查看冲突文件
git status

# 编辑冲突文件
vim source/_posts/conflict-file.md

# 标记为已解决
git add source/_posts/conflict-file.md
git commit
```

## 最佳实践

### 1. 分支命名规范

- 特性分支: `feature/{category}-{YYYYMMDD}`
- 修复分支: `fix/{description}-{YYYYMMDD}`
- 紧急修复: `hotfix/{description}`

### 2. 提交信息规范

```
<type>: <subject>

<body>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

示例：
```
feat: add new chocolate posts

- Convert HTML files to Markdown
- Update categories and tags
- Add front matter metadata

Closes #123
```

### 3. 工作流程建议

1. 小步提交
2. 频繁推送
3. 及时同步master
4. 保持分支简短
5. 删除已合并分支

### 4. 安全措施

- 不要直接在master上提交
- 使用Pull Request进行代码审查
- 合并前先测试
- 重要更改先备份

## 常见问题

### Q: 如何处理分支冲突？

A:
```bash
git checkout master
git pull origin master
git checkout feature/your-branch
git merge master
# 手动解决冲突
git add .
git commit
```

### Q: 如何恢复误删的分支？

A:
```bash
git reflog
# 找到分支的commit hash
git branch feature/your-branch <commit-hash>
```

### Q: 如何查看分支历史？

A:
```bash
# 查看分支提交历史
git log feature/chocolate-20250105 --oneline

# 查看分支关系图
git log --graph --oneline --all
```

### Q: 如何临时保存工作？

A:
```bash
# 保存当前工作
git stash

# 恢复工作
git stash pop

# 查看stash列表
git stash list
```

## 自动化脚本集成

自动化脚本支持以下分支操作：

```bash
# 创建并转换
python3 html2hexo.py --branch chocolate

# 只转换不创建分支
python3 html2hexo.py

# 查看主题推荐
python3 html2hexo.py --recommend
```

## 资源链接

- [Git Branching Basics](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Hexo Documentation](https://hexo.io/docs/)
