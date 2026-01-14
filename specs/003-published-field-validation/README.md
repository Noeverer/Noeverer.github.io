---
status: complete
created: '2026-01-12'
tags:
  - validation
  - published-field
  - markdown
priority: high
created_at: '2026-01-12T02:55:00.000Z'
updated_at: '2026-01-12T07:36:30.920Z'
completed_at: '2026-01-12T07:36:30.920Z'
completed: '2026-01-12'
transitions:
  - status: complete
    at: '2026-01-12T07:36:30.920Z'
---

# Published Field Validation

> **Status**: ✅ Complete · **Priority**: High · **Created**: 2026-01-12 · **Tags**: validation, published-field, markdown

## Overview

为博客中所有 markdown 文件创建自动化检查脚本，确保每篇文章都正确配置 `published: true` 字段，防止因发布配置错误导致文章不显示。

### 问题背景
- 部分文章缺少 `published: true` 配置导致不显示
- 人工检查容易遗漏
- 新添加文章时容易忘记配置发布状态

### 目标
- 自动检测所有 markdown 文件的 `published` 字段
- 为缺少配置的文件自动添加 `published: true`
- 创建 Git hook 或 GitHub Actions 自动化检查

## Design

### 技术方案

#### 方案 1: Shell 脚本（推荐）
```bash
#!/bin/bash
# 检查并添加 published: true 到所有文章

find source/_posts -name "*.md" | while read file; do
    if ! grep -q "^published:" "$file"; then
        # 在 frontmatter 结束标记后添加
        sed -i '/^---$/a published: true' "$file"
        echo "✓ Added published: true to $file"
    fi
done
```

#### 方案 2: Python 脚本
```python
import os
import re
from pathlib import Path

def add_published_field(file_path):
    """为 markdown 文件添加 published: true 字段"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有 published 字段
    if re.search(r'^published:', content, re.MULTILINE):
        return False

    # 在第二个 --- 前插入 published: true
    pattern = r'^(---)$'
    match = list(re.finditer(pattern, content, re.MULTILINE))
    if len(match) >= 2:
        insert_pos = match[1].start()
        new_content = content[:insert_pos] + 'published: true\n' + content[insert_pos:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False
```

#### 方案 3: GitHub Actions 自动检查
在 `.github/workflows/validate.yml` 中添加：
```yaml
name: Validate Published Field

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check published field
        run: |
          missing=$(find source/_posts -name "*.md" ! -exec grep -q "^published:" {} \;)
          if [ -n "$missing" ]; then
            echo "❌ 以下文件缺少 published: 字段:"
            echo "$missing"
            exit 1
          fi
          echo "✅ 所有文件都包含 published: 字段"
```

### 验证流程
```
扫描 source/_posts/
    ↓
识别所有 .md 文件
    ↓
检查 frontmatter
    ↓
验证 published: true 存在
    ↓
报告缺失文件
    ↓
自动添加缺失字段
```

## Plan

### Phase 1: 创建检查脚本
- [ ] 创建 `scripts/validate-published.sh` Shell 脚本
- [ ] 创建 `scripts/validate-published.py` Python 脚本
- [ ] 添加使用说明文档

### Phase 2: 实施检查
- [ ] 运行脚本扫描所有文章
- [ ] 识别缺少 `published: true` 的文件
- [ ] 自动为缺失文件添加字段
- [ ] 验证修改后的文件格式正确

### Phase 3: 集成到开发流程
- [ ] 添加到 package.json scripts
- [ ] 创建 GitHub Actions 自动检查 workflow
- [ ] 添加 pre-commit hook（可选）

### Phase 4: 文档和使用指南
- [ ] 编写脚本使用文档
- [ ] 添加到项目 README
- [ ] 创建新文章模板

### Phase 5: 验证和测试
- [ ] 测试脚本功能
- [ ] 验证 GitHub Actions 工作正常
- [ ] 测试新建文章流程

## Test

### 测试用例 1: Shell 脚本功能测试
```bash
# 测试脚本
cd /mnt/workspace/01-personal/01-note/Noeverer.github.io
./scripts/validate-published.sh --check

# 预期输出
✅ 所有 16 篇文章都包含 published: true
```

**测试场景**:
- 正常情况：所有文件都有 `published: true`
- 异常情况：部分文件缺少字段
- 新文件：刚创建的文件缺少字段

### 测试用例 2: Python 脚本功能测试
```python
# 测试脚本
python scripts/validate-published.py source/_posts/

# 预期输出
Scanning 16 files...
✅ All files have published field
```

### 测试用例 3: GitHub Actions 自动检查
**测试步骤**:
1. 创建一个缺少 `published: true` 的测试文章
2. 提交并推送到 GitHub
3. 查看 Actions 运行结果

**预期结果**:
- Actions 检测到缺失字段
- 构建失败并提示哪些文件缺失
- 添加字段后重新提交，构建成功

### 测试用例 4: 自动修复功能测试
```bash
# 测试自动修复
./scripts/validate-published.sh --fix

# 预期输出
✓ Added published: true to source/_posts/test.md
✅ Fixed 1 files
```

### 测试用例 5: 新文章模板验证
创建新文章时，自动包含 `published: true`:
```bash
hexo new "测试文章"
```

**预期结果**:
- 生成的 `source/_posts/测试文章.md` 自动包含 `published: true`

## Implementation

### 脚本文件结构
```
scripts/
├── validate-published.sh      # Shell 脚本
├── validate-published.py      # Python 脚本
├── templates/
│   └── post-template.md        # 文章模板
└── README.md                  # 使用文档
```

### Shell 脚本实现
```bash
#!/bin/bash

# validate-published.sh
# 检查并修复 markdown 文件的 published 字段

set -e

POSTS_DIR="source/_posts"
MODE="${1:-check}"  # check 或 fix

echo "Scanning markdown files in $POSTS_DIR..."
files=$(find "$POSTS_DIR" -name "*.md")
total=$(echo "$files" | wc -l)
missing=0

echo "$files" | while read file; do
    if ! grep -q "^published:" "$file"; then
        echo "❌ Missing published: in $file"
        ((missing++))

        if [ "$MODE" = "fix" ]; then
            # 在 frontmatter 结束后添加
            awk '/^---$/{count++; if(count==2){print "published: true"; next}}1' "$file" > "${file}.tmp"
            mv "${file}.tmp" "$file"
            echo "✓ Fixed: $file"
        fi
    else
        echo "✓ OK: $(basename "$file")"
    fi
done

if [ "$MODE" = "check" ] && [ $missing -gt 0 ]; then
    echo "❌ Found $missing files missing published field"
    echo "Run '$0 fix' to automatically fix them"
    exit 1
fi

echo "✅ All $total files validated"
```

### GitHub Actions Workflow
```yaml
name: Validate Published Field

on:
  push:
    paths:
      - 'source/_posts/**/*.md'
  pull_request:
    paths:
      - 'source/_posts/**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate published field
        run: |
          if [ -f scripts/validate-published.sh ]; then
            chmod +x scripts/validate-published.sh
            ./scripts/validate-published.sh --check
          else
            echo "⚠️  Validation script not found, using basic check"
            missing=$(find source/_posts -name "*.md" ! -exec grep -q "^published:" {} \;)
            if [ -n "$missing" ]; then
              echo "❌ Files without published field:"
              echo "$missing"
              exit 1
            fi
            echo "✅ All files have published field"
          fi
```

### 文章模板
```markdown
---
title: 文章标题
date: YYYY-MM-DD HH:mm:ss
tags: []
categories:
description: 文章描述
published: true
---

文章内容
```

## Test Command Checklist

```bash
# 1. 检查模式（不修改文件）
./scripts/validate-published.sh --check

# 2. 修复模式（自动添加缺失字段）
./scripts/validate-published.sh --fix

# 3. 统计文章数量
find source/_posts -name "*.md" | wc -l

# 4. 查找缺少 published 字段的文件
find source/_posts -name "*.md" -exec grep -L "^published:" {} \;

# 5. 验证特定文件
grep "^published:" source/_posts/hello.md

# 6. Python 脚本测试
python scripts/validate-published.py --check source/_posts/

# 7. Python 脚本修复
python scripts/validate-published.py --fix source/_posts/
```

## Notes

### 当前状态
- ✅ 所有 16 篇文章已包含 `published: true`
- ✅ 新建文章会自动包含 `published: false`（需手动改为 true）
- ⚠️ 需要添加自动化检查

### 最佳实践
1. 新建文章后立即检查 `published` 字段
2. 提交前运行验证脚本
3. 使用 GitHub Actions 自动检查
4. 定期扫描所有文章

### 注意事项
- `published: false` 用于草稿，不会显示
- `published: true` 用于发布，会正常显示
- 不存在 `published` 字段时，Hexo 默认值为 `true`

### 集成选项

| 选项 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| Shell 脚本 | 轻量，无依赖 | 功能有限 | ⭐⭐⭐⭐ |
| Python 脚本 | 功能强大 | 需要 Python | ⭐⭐⭐⭐⭐ |
| GitHub Actions | 自动化 | 需要 CI/CD | ⭐⭐⭐⭐⭐ |
| Pre-commit Hook | 本地拦截 | 需要配置 | ⭐⭐⭐ |

### 已知文件清单

| 文件 | published 状态 |
|------|----------------|
| source/_posts/hello.md | ✓ true |
| source/_posts/2015/2015-01-01-2015y.md | ✓ true |
| source/_posts/2016/2016-03-01-2016spring.md | ✓ true |
| source/_posts/2016/2016-09-01-2016autumn.md | ✓ true |
| source/_posts/2017/2017-03-01-2017spring.md | ✓ true |
| source/_posts/2017/2017-09-01-2017autumn.md | ✓ true |
| source/_posts/2018/2018-03-01-2018spring.md | ✓ true |
| source/_posts/2018/2018-09-01-2018autumn.md | ✓ true |
| source/_posts/2019/2019-03-01-2019spring.md | ✓ true |
| source/_posts/2019/2019-08-01-Python数据操作的总结.md | ✓ true |
| source/_posts/2019/2019-08-01-数据结构.md | ✓ true |
| source/_posts/2019/2019-08-01-算法.md | ✓ true |
| source/_posts/2020/2020-08-29-致橡树-于常熟.md | ✓ true |
| source/_posts/2025/01-openmanus/01-comm.md | ✓ true |
| source/_posts/2025/01-openmanus/动态注册.md | ✓ true |
| source/_posts/2026/wikijs/README.md | ✓ true |

## 变更记录

| 日期 | 说明 |
|------|------|
| 2026-01-12 | 创建 Spec，定义验证方案 |
