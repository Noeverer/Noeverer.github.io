---
status: planned
created: '2026-01-12'
tags: [navigation, menu, 404-fix]
priority: high
created_at: '2026-01-12T03:00:00.000Z'
---

# Fix Menu 404 Errors

> **Status**: 📅 Planned · **Priority**: High · **Created**: 2026-01-12

## Overview

修复顶部导航栏下拉菜单中的 404 错误问题，确保所有菜单链接都能正常访问。

### 问题背景
当前顶部导航栏配置的下拉菜单链接存在 404 错误：

| 菜单项 | 当前链接 | 实际标签 | 状态 |
|--------|---------|---------|------|
| 生活 → 随笔 | /tags/随笔/ | 不存在 | ❌ 404 |
| 生活 → 感悟 | /tags/感悟/ | 存在 (9篇文章) | ✓ 200 |
| 技术 → LeetCode | /tags/LeetCode/ | 不存在 | ❌ 404 |
| 技术 → Python | /tags/Python/ | 不存在 | ❌ 404 |

### 目标
- 修复所有 404 菜单链接
- 更新为实际存在的标签或页面
- 保持导航栏结构清晰合理

## Design

### 当前菜单配置
```yaml
menu:
  首页: / || fas fa-home
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
  分类: /categories/ || fas fa-folder-open
  生活||fas fa-heart:
    - 随笔 || /tags/随笔/
    - 感悟 || /tags/感悟/
  技术||fas fa-code:
    - LeetCode || /tags/LeetCode/
    - Python || /tags/Python/
  关于: /about/ || fas fa-address-card
```

### 实际标签分析
通过扫描所有文章，发现实际存在的标签：

| 标签 | 文章数量 | 菜单状态 |
|------|---------|---------|
| chocolate | 9 | 未配置 |
| life | 9 | 未配置 |
| 感悟 | 9 | ✓ 已配置 |
| mindmap | 2 | 未配置 |
| study | 2 | 未配置 |
| python | 1 | 已配置为 "Python" |
| code | 1 | 未配置 |
| openmanus | 2 | 未配置 |
| wikijs | 1 | 未配置 |
| docker | 1 | 未配置 |
| LeetCode | 0 | ❌ 不存在 |
| 随笔 | 0 | ❌ 不存在 |

### 修复方案

#### 方案 1: 修正为实际存在的标签（推荐）
```yaml
menu:
  首页: / || fas fa-home
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
  分类: /categories/ || fas fa-folder-open
  生活||fas fa-heart:
    - 感悟 || /tags/感悟/
  技术||fas fa-code:
    - 编程 || /tags/code/
    - Python || /tags/python/
  学习||fas fa-book:
    - 学习笔记 || /tags/study/
    - 思维导图 || /tags/mindmap/
  关于: /about/ || fas fa-address-card
```

#### 方案 2: 添加缺失的标签到文章
为文章添加 "随笔"、"LeetCode" 等标签

#### 方案 3: 移除下拉菜单，保留顶层菜单
简化导航，只保留主要页面

### 分类分析
检查实际存在的分类：

| 分类 | 文章数量 |
|------|---------|
| chocolate | 10 |
| code | 2 |
| tech | 1 |
| test | 1 |

## Plan

### Phase 1: 分析现有标签和分类
- [ ] 扫描所有文章的 tags 字段
- [ ] 统计各标签的文章数量
- [ ] 扫描所有文章的 categories 字段
- [ ] 统计各分类的文章数量

### Phase 2: 设计新菜单结构
- [ ] 根据实际数据设计合理的菜单
- [ ] 确保所有链接有效
- [ ] 保持菜单层级清晰
- [ ] 更新图标和描述

### Phase 3: 更新配置文件
- [ ] 修改 `_config.butterfly.yml` 中的 menu 配置
- [ ] 测试新配置
- [ ] 验证链接正确性

### Phase 4: 可选 - 添加缺失标签（如果需要）
- [ ] 为相关文章添加 "随笔" 标签
- [ ] 为相关文章添加 "LeetCode" 标签
- [ ] 更新文章 frontmatter

### Phase 5: 验证和测试
- [ ] 本地构建测试
- [ ] 访问所有菜单链接
- [ ] 确认无 404 错误
- [ ] 推送并验证线上效果

## Test

### 测试用例 1: 验证所有菜单链接有效
**测试步骤**:
1. 访问 https://noeverer.github.io
2. 点击导航栏中的每个菜单项
3. 检查每个链接的 HTTP 状态码

**验证清单**:
- [ ] 首页 (/) - 200 OK
- [ ] 归档 (/archives/) - 200 OK
- [ ] 标签 (/tags/) - 200 OK
- [ ] 分类 (/categories/) - 200 OK
- [ ] 生活 → 感悟 (/tags/感悟/) - 200 OK
- [ ] 技术 → 编程 (/tags/code/) - 200 OK
- [ ] 技术 → Python (/tags/python/) - 200 OK
- [ ] 学习 → 学习笔记 (/tags/study/) - 200 OK
- [ ] 学习 → 思维导图 (/tags/mindmap/) - 200 OK
- [ ] 关于 (/about/) - 200 OK

**测试命令**:
```bash
# 检查 HTTP 状态码
curl -I https://noeverer.github.io/tags/感悟/
curl -I https://noeverer.github.io/tags/code/
curl -I https://noeverer.github.io/tags/python/
```

### 测试用例 2: 验证菜单显示
**检查项**:
- [ ] 导航栏宽度适应屏幕
- [ ] 下拉菜单正常展开
- [ ] 图标显示正确
- [ ] 移动端菜单正常工作

### 测试用例 3: 验证标签页面内容
**测试步骤**:
1. 访问 /tags/感悟/
2. 确认显示所有相关文章
3. 检查文章列表数量（应为 9 篇）

### 测试用例 4: 验证分类页面内容
**测试步骤**:
1. 访问 /categories/chocolate/
2. 确认显示所有相关文章
3. 检查文章列表数量

## Implementation

### 推荐的最终配置

```yaml
menu:
  首页: / || fas fa-home
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
  分类: /categories/ || fas fa-folder-open
  生活||fas fa-heart:
    - 感悟 || /tags/感悟/
  技术||fas fa-code:
    - 编程 || /tags/code/
    - Python || /tags/python/
  学习||fas fa-book:
    - 学习笔记 || /tags/study/
    - 思维导图 || /tags/mindmap/
  关于: /about/ || fas fa-address-card
```

### 替代方案：基于分类的菜单

```yaml
menu:
  首页: / || fas fa-home
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
  分类: /categories/ || fas fa-folder-open
  生活随笔||fas fa-heart:
    - 随笔感悟 || /categories/chocolate/
  技术学习||fas fa-code:
    - 技术文章 || /categories/code/
  关于: /about/ || fas fa-address-card
```

### 脚本：生成标签统计

```bash
#!/bin/bash
# 统计所有标签

echo "=== 标签统计 ==="
grep -h "^tags:" source/_posts/**/*.md | \
  sed 's/tags: //' | \
  sed "s/['\"]//g" | \
  sed 's/\[//g; s/\]//g' | \
  tr ',' '\n' | \
  sort | uniq -c | sort -rn

echo -e "\n=== 分类统计 ==="
grep -h "^categories:" source/_posts/**/*.md | \
  sed 's/categories: //' | \
  sed "s/['\"]//g" | \
  sort | uniq -c | sort -rn
```

### 脚本：验证链接有效性

```bash
#!/bin/bash
# 验证菜单链接

base_url="https://noeverer.github.io"

# 测试链接数组
links=(
  "/"
  "/archives/"
  "/tags/"
  "/categories/"
  "/tags/感悟/"
  "/tags/code/"
  "/tags/python/"
  "/tags/study/"
  "/tags/mindmap/"
)

echo "=== 验证菜单链接 ==="
for link in "${links[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "${base_url}${link}")
  if [ "$status" = "200" ]; then
    echo "✓ ${link} - 200 OK"
  else
    echo "✗ ${link} - ${status}"
  fi
done
```

## Test Command Checklist

```bash
# 1. 统计标签
grep -h "^tags:" source/_posts/**/*.md | sort | uniq -c | sort -rn

# 2. 统计分类
grep -h "^categories:" source/_posts/**/*.md | sort | uniq -c | sort -rn

# 3. 本地构建测试
hexo clean && hexo generate
ls -la public/tags/

# 4. 验证特定标签页是否存在
ls -la public/tags/感悟/
ls -la public/tags/python/

# 5. 查找使用特定标签的文章
grep -r "tags.*感悟" source/_posts/

# 6. 生成标签报告
./scripts/generate-tag-report.sh
```

## Notes

### 当前问题详细说明

**问题 1: /tags/随笔/ 返回 404**
- 原因：没有任何文章使用 "随笔" 标签
- 解决：移除此菜单项，或为相关文章添加标签

**问题 2: /tags/LeetCode/ 返回 404**
- 原因：没有任何文章使用 "LeetCode" 标签
- 解决：移除此菜单项，或为相关文章添加标签

**问题 3: /tags/Python/ 返回 404**
- 原因：文章中使用的是 "python"（小写）
- 解决：修改菜单链接为 /tags/python/

### 文章标签详情

| 文章 | 标签 |
|------|------|
| 2015-2017 所有文章 | chocolate, life, 感悟 |
| 2018spring | mindmap, study |
| 2019spring | mindmap, study |
| Python数据操作 | python, code |
| Wiki.js 部署指南 | wikijs, docker |
| 动态注册 | mindmap, study |
| 学习openmanus代码 | openmanus, code |

### 文章分类详情

| 文章 | 分类 |
|------|------|
| 2015-2020 文章 | chocolate |
| 2018spring, 2019spring, 动态注册 | code |
| Python数据操作, 学习openmanus代码 | code |
| Wiki.js 部署指南 | tech |
| hello | test |

### 修复优先级

| 优先级 | 菜单项 | 问题 | 建议 |
|--------|--------|------|------|
| P0 | 技术 → Python | 大小写不匹配 | 改为 /tags/python/ |
| P1 | 生活 → 随笔 | 标签不存在 | 移除或改为 "感悟" |
| P1 | 技术 → LeetCode | 标签不存在 | 移除或添加标签 |
| P2 | 整体优化 | 菜单结构不够合理 | 重新设计 |

### 推荐的菜单结构变更

**变更前**:
```
首页 | 归档 | 标签 | 分类 | 生活(2) | 技术(2) | 关于
       ↓                随笔 ✗   LeetCode ✗
                      感悟 ✓   Python ✗
```

**变更后**:
```
首页 | 归档 | 标签 | 分类 | 生活(1) | 技术(2) | 学习(2) | 关于
                     感悟 ✓   编程 ✓   学习笔记 ✓
                             Python ✓  思维导图 ✓
```

## 变更记录

| 日期 | 说明 |
|------|------|
| 2026-01-12 | 创建 Spec，分析 404 问题 |
