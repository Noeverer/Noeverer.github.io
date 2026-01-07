# Hexo Butterfly 主题配置指南

本文档详细说明 Hexo + Butterfly 主题的配置方法和常用参数。

---

## 📁 配置文件结构

```
Noeverer.github.io/
├── _config.yml              # Hexo 主配置文件
└── _config.butterfly.yml    # Butterfly 主题配置文件
```

---

## 🔧 Hexo 主配置 (_config.yml)

### 基础信息

```yaml
# 站点信息
title: Ante Liu                      # 网站标题
subtitle: Thanks For Watching！      # 副标题
description: 个人简介描述            # 网站描述（SEO 用）
keywords: 理智,感性,AB型,codinginging # 关键词
author: Ante Liu                     # 作者名
language: zh-CN                      # 语言
timezone: Asia/Shanghai              # 时区
```

### URL 配置

```yaml
# URL
url: https://noeverer.github.io      # 网站地址
root: /                              # 网站根目录
permalink: :year/:month/:day/:title/ # 文章永久链接格式
```

**Permalink 可用变量：**
- `:year` - 年份 (4 位)
- `:month` - 月份 (2 位)
- `:day` - 日期 (2 位)
- `:title` - 文章标题

### 目录设置

```yaml
# 目录
source_dir: source        # 源文件目录
public_dir: public        # 生成的静态文件目录
tag_dir: tags             # 标签目录
archive_dir: archives     # 归档目录
category_dir: categories  # 分类目录
```

### 写作设置

```yaml
# 写作
new_post_name: :title.md              # 新建文章文件名格式
default_layout: post                  # 默认布局
post_asset_folder: false              # 是否创建同名资源文件夹
```

### 主题配置

```yaml
# 扩展
theme: butterfly  # 使用的主题名称
```

---

## 🎨 Butterfly 主题配置 (_config.butterfly.yml)

### 网站信息

```yaml
# 网站信息
site_name: 'Ante Liu'
site_author: 'Ante Liu'
site_description: '个人简介'
site_keywords: '关键词1,关键词2,关键词3'
```

### 导航菜单

```yaml
menu:
  首页: / || fas fa-home
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
  分类: /categories/ || fas fa-folder-open
  生活||fas fa-heart:              # 下拉菜单示例
    - 随笔 || /tags/随笔/
    - 感悟 || /tags/感悟/
  技术||fas fa-code:
    - LeetCode || /tags/LeetCode/
    - Python || /tags/Python/
  关于: /about/ || fas fa-address-card
```

**格式说明：**
- `菜单名: 链接 || 图标`
- 下拉菜单：`父菜单名||图标:` (冒号结尾)，然后子菜单用 `-` 缩进

**常用图标（Font Awesome）：**
- `fas fa-home` - 首页
- `fas fa-archive` - 归档
- `fas fa-tags` - 标签
- `fas fa-folder-open` - 分类
- `fas fa-heart` - 生活/心形
- `fas fa-code` - 代码
- `fas fa-envelope` - 邮件
- `fab fa-github` - GitHub

### 搜索功能

```yaml
# 搜索
local_search:
  enable: true    # 是否启用本地搜索
  preload: false  # 是否预加载搜索索引
```

### 代码高亮

```yaml
# 代码高亮
highlight_theme: mac light  # 代码高亮主题
```

**可用主题：**
- `mac light` - Mac 浅色
- `mac dark` - Mac 深色
- `atom one light` - Atom 浅色
- `atom one dark` - Atom 深色
- `github` - GitHub 风格

### 社交图标

```yaml
# 社交图标
social:
  fab fa-github: https://github.com/Noeverer || Github
  fas fa-envelope: mailto:your-email@example.com || Email
  fab fa-weixin: /img/wechat.png || 微信
```

**格式：** `图标类名: 链接 || 显示名称`

### 主题颜色

```yaml
# 主题色
theme_color:
  enable: true
  main: '#4C4948'              # 主色调
  paginator: '#00c4b6'         # 分页器颜色
  button_hover: '#FF7242'      # 按钮悬停颜色
  text_selection: '#00c4b6'    # 文本选择颜色
  link_color: '#99a9bf'        # 链接颜色
  hr_color: '#A4D8FA'          # 分割线颜色
```

### 字体设置

```yaml
# 字体
font:
  font-size: 15px              # 字体大小
  font-family: '-apple-system, BlinkMacSystemFont, "Segoe UI", ...'
```

### 头像配置

```yaml
# 头像
avatar:
  img: /img/monkey.jpg         # 头像图片路径
  effect: false                # 是否启用头像特效（旋转/呼吸）
```

**图片路径规则：**
- 绝对路径：`/img/monkey.jpg` - 从项目根目录的 img 文件夹读取
- 相对路径：`images/avatar.jpg` - 从 source 目录读取
- 外部链接：`https://example.com/avatar.jpg`

**当前项目图片资源位置：**
```
/img/monkey.jpg           # 当前头像
/img/photo.jpg            # 照片
/img/alipay.png           # 支付宝二维码
/img/wechat.png           # 微信二维码
```

### 顶部图

```yaml
# 顶部图
index_site_info_top: null
default_top_img: linear-gradient(20deg, #0062be, #925696, #cc426e, #f43059)
```

**可用选项：**
- `null` - 不显示顶部图
- 颜色渐变：`linear-gradient(...)`
- 图片 URL：`https://example.com/banner.jpg`

### 文章元数据

```yaml
# 文章元数据
post_meta:
  page:
    date_type: both
    date_format: 'YYYY-MM-DD HH:mm:ss'
    categories: true
    tags: true
    label: true
  post:
    date_type: both
    date_format: 'YYYY-MM-DD HH:mm:ss'
    categories: true
    tags: true
    label: true
```

### 文章封面

```yaml
# 文章封面
cover_index_enable: true        # 首页文章封面
cover_archive_enable: false      # 归档页封面
cover_tag_enable: false         # 标签页封面
cover_category_enable: false    # 分类页封面
random_cover: false             # 随机封面
```

### 分页设置

```yaml
# 分页
pagination_style: 3
```

**可选样式：**
- `1` - 简约风格
- `2` - 带数字
- `3` - 当前页高亮

### 侧边栏

```yaml
# 侧边栏
aside:
  enable: true          # 是否启用侧边栏
  hide: false           # 是否隐藏侧边栏
  button: true          # 是否显示侧边栏切换按钮
  mobile: true          # 移动端是否显示
  position: right       # 位置：left / right
  display:
    archive: true       # 归档
    tag: true           # 标签
    category: true      # 分类
```

#### 侧边栏卡片

```yaml
aside:
  card_author:
    enable: true
    description: '生活不止眼前的苟且，还有诗和远方'
    button:
      enable: true
      icon: fab fa-github
      text: Github
      link: https://github.com/Noeverer
  card_recent_post:
    enable: true
    limit: 5            # 显示文章数量
    sort: date         # 排序方式：date / updated
    sort_order: -1      # 排序顺序：-1 (降序) / 1 (升序)
  card_categories:
    enable: true
    limit: 10
    expand: none       # 展开/收起
    sort_order: -1
  card_tags:
    enable: true
    limit: 20
    orderby: random     # 排序方式：random / count
    order: count
  card_archives:
    enable: true
    type: monthly      # 类型：yearly / monthly
    format: MMMM YYYY
    order: -1
    limit: 10
```

### 页脚

```yaml
# 页脚
footer:
  owner:
    enable: true
    since: 2015         # 建站年份
  custom_text: 'Thank you for visiting my blog'
  copyright: true
```

### 运行时间

```yaml
# 运行时间
runtimeshow:
  enable: true
  publish_date: '01/01/2015 00:00:00'
  unit: '天'
```

### 文章目录 (TOC)

```yaml
# 文章目录
toc:
  enable: true
  number: true          # 是否显示序号
  expand_all: false     # 是否全部展开
  init_open: true       # 默认打开到第几级
  layout: right         # 位置：right / left
```

### 评论功能

```yaml
# 评论
comments:
  use: false            # 是否启用评论
  text: 'Just go home'
```

### 显示模式

```yaml
# 显示模式（亮/暗）
display_mode:
  light:
    enable: true
    icon: 'fa fa-sun'
    theme: 'light'
  dark:
    enable: true
    icon: 'fa fa-moon'
    theme: 'dark'
  auto:
    enable: true
    icon: 'fa fa-adjust'
```

### 版权声明

```yaml
# 版权声明
post_copyright:
  enable: true
  decode: true
  author_href:
  license: CC BY-NC-SA 4.0
  license_url: https://creativecommons.org/licenses/by-nc-sa/4.0/
```

### 图片懒加载

```yaml
# 图片懒加载
lazyload:
  enable: true
  field: site           # 站点范围：site / post
  placeholder: /img/loading.gif
  errorimg: /img/error.gif
```

### FancyBox 图片灯箱

```yaml
# FancyBox
fancybox: true
```

---

## 📝 文章 Front Matter 配置

每篇文章开头的 Front Matter 配置示例：

```yaml
---
title: 文章标题
date: 2026-01-07 00:00:00
updated: 2026-01-07 00:00:00
tags:
  - 标签1
  - 标签2
categories:
  - 分类1
cover: /img/cover.jpg    # 文章封面图
top_img: /img/banner.jpg # 顶部图（可选）
toc: true                # 是否显示目录
copyright: true          # 是否显示版权
---
```

---

## 🔄 配置修改后生效

修改配置文件后需要重新生成：

```bash
# 本地预览
hexo clean
hexo server

# 推送到 GitHub 后自动重新部署
git add .
git commit -m "更新配置"
git push
```

---

## 🔗 相关资源

- [Butterfly 官方文档](https://butterfly.js.org/)
- [Hexo 官方文档](https://hexo.io/zh-cn/docs/)
- [Font Awesome 图标库](https://fontawesome.com/icons)
