# 博客访问控制和书籍展示系统

## 功能说明

此系统允许您：

1. 控制博客内容的发布权限
2. 将博客内容以书籍形式展示
3. 管理访问权限

## 配置选项

### 发布控制

在文章的 front-matter 中添加以下字段：

```yaml
---
title: 文章标题
date: YYYY-MM-DD HH:mm:ss
tags: ["标签1", "标签2"]
categories: 分类
description: 文章描述
published: true          # 设为 false 可控制发布
access_level: public     # public, registered, premium, private
book_chapter: true       # 设为 true 可包含在书籍中
---
```

### 访问级别说明

- `public`: 所有人都可访问
- `registered`: 仅注册用户可访问
- `premium`: 仅付费用户可访问
- `private`: 仅作者可访问

## 使用方法

### 1. 生成书籍格式

```bash
npm run generate-book
```

### 2. 检查访问权限

```bash
npm run check-access
```

### 3. 批量更新文章权限

```bash
npm run update-access -- --level=premium --pattern="2026/*"
```

## 工作流程

1. 文章按常规方式编写，但在 front-matter 中添加访问控制字段
2. 构建系统根据访问级别过滤内容
3. 书籍生成器收集标记为 `book_chapter: true` 的文章
4. 部署时根据配置生成不同版本的站点