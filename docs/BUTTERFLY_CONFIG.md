# Butterfly 主题配置说明

## 主题简介

Butterfly 是一个美观、功能丰富的 Hexo 主题，具有现代化的卡片式布局和优秀的响应式设计。

## 已安装的版本

- **主题版本**: 5.5.3
- **Hexo版本**: 7.2.0
- **渲染器**: hexo-renderer-pug, hexo-renderer-stylus

## 配置文件

- 主配置文件: `_config.yml` (设置 `theme: butterfly`)
- 主题配置文件: `_config.butterfly.yml`

## 主要功能特性

### ✨ 已启用的功能

1. **导航菜单**
   - 首页、归档、标签、分类
   - 生活分类（随笔、感悟）
   - 技术分类（LeetCode、Python）
   - 关于页面

2. **搜索功能**
   - 本地搜索已启用
   - 无需依赖外部服务

3. **代码高亮**
   - 使用 Mac Light 主题
   - 支持多种编程语言

4. **主题切换**
   - 亮色模式
   - 暗色模式
   - 自动切换（根据系统）

5. **图片优化**
   - 图片懒加载
   - Fancybox 图片放大查看
   - 自定义占位图

6. **侧边栏**
   - 作者卡片
   - 最新文章
   - 分类列表
   - 标签云
   - 归档时间轴

7. **文章功能**
   - 文章封面图
   - 版权声明
   - 文章目录（TOC）
   - 阅读时间统计

### ⚙️ 未启用的功能（可根据需要开启）

- 评论系统（Gitalk、Disqus 等）
- 音乐播放器
- 数学公式（MathJax、KaTeX）
- Mermaid 图表
- PWA 离线支持
- 友情链接
- 社交分享

## 颜色主题

```yaml
主题色: #4C4948
分页色: #00c4b6
按钮悬停: #FF7242
文字选择: #00c4b6
链接色: #99a9bf
```

## 字体配置

使用系统默认字体栈，支持多平台：
- Apple: -apple-system
- Windows: "Segoe UI"
- Linux: "Helvetica Neue", Arial
- Emoji: Apple Color Emoji

## 主题定制

### 修改主题颜色

编辑 `_config.butterfly.yml` 中的 `theme_color` 部分：

```yaml
theme_color:
  main: '#你的主色'
  button_hover: '#你的按钮颜色'
```

### 添加导航菜单

在 `_config.butterfly.yml` 的 `menu` 部分：

```yaml
menu:
  新分类: /categories/新分类/ || fas fa-icon-name
```

### 启用评论系统

在 `_config.butterfly.yml` 中：

```yaml
comments:
  use: gitalk  # 或其他评论系统
```

然后配置对应的评论系统参数。

### 自定义CSS/JS

在 `_config.butterfly.yml` 的 `inject` 部分：

```yaml
inject:
  head:
    - <link rel="stylesheet" href="/css/custom.css">
  bottom:
    - <script src="/js/custom.js"></script>
```

## 图片资源

### 头像

- 位置: `img/photo.jpg`
- 如需更换，替换 `img/photo.jpg` 文件

### 文章封面图

- 支持在 Front Matter 中指定：
  ```yaml
  cover: /images/cover.jpg
  ```

### 404页面

- 自定义404页面背景图
- 路径可在 `_config.butterfly.yml` 中修改

## 兼容性优化

### 移动端适配

- 完全响应式设计
- 移动端菜单优化
- 触摸友好

### 浏览器兼容

- Chrome/Edge: ✅ 完全支持
- Firefox: ✅ 完全支持
- Safari: ✅ 完全支持
- IE: ❌ 不支持

### 性能优化

- CSS/JS 压缩
- 图片懒加载
- CDN 加速（FontAwesome）
- 代码分割

## 常见问题

### Q: 主题样式没有生效？

A: 运行以下命令清理缓存：
```bash
hexo clean
hexo generate
```

### Q: 图片显示不出来？

A: 检查图片路径是否正确，确保图片在 `source/img/` 或 `source/images/` 目录下。

### Q: 代码高亮不显示？

A: 确保已安装 `hexo-renderer-marked` 插件，并在 Front Matter 中使用正确的代码块格式。

### Q: 如何更新主题？

A: 更新 package.json 中的版本号，然后运行：
```bash
npm update hexo-theme-butterfly
```

### Q: 暗色模式自动切换不工作？

A: 检查浏览器是否允许网站检测系统主题设置。

## 更多配置选项

详细的配置选项请参考 Butterfly 官方文档：
https://butterfly.js.org/posts/21cfbf15/

## 主题预览

查看你的博客：https://noeverer.github.io

## 脚本文件说明

Python 转换脚本已移至 `scripts_tools_backup/` 目录，避免与 Hexo 冲突。

如需使用转换工具：
```bash
cd scripts_tools_backup
python3 convert_html_to_md.py
```
