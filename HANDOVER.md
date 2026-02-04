# 项目交接文档

## 项目概述
这是一个基于 Hexo 框架的个人博客网站，托管在 GitHub Pages 上。

## 分支结构
- `master` 分支：存放博客文章、主题配置、源代码等
- `gh-pages` 分支：由 GitHub Action 自动构建生成的静态网站文件

## 关键文件说明
- `_config.yml`：Hexo 主配置文件
- `_config.butterfly.yml`：Butterfly 主题配置文件
- `source/`：博客文章和页面源文件
- `themes/butterfly/`：Butterfly 主题文件
- `public/`：构建后生成的静态网站文件（已忽略）

## GitHub Action 工作流
- 监听 `master` 分支的推送事件
- 自动执行 `hexo generate` 构建网站
- 将构建结果部署到 `gh-pages` 分支

## 常见问题及解决方案
### 1. GitHub Action 构建失败："index.html not found!"
- 原因：`.gitignore` 文件中包含了 `index.html`
- 解决：移除 `.gitignore` 中的 `index.html` 规则

### 2. 依赖管理
- `package.json` 和 `package-lock.json` 需要版本控制以确保构建一致性

### 3. 静态资源处理
- 图片、CSS、JS 等静态资源应放在 `source/` 目录下对应子目录

## 维护注意事项
1. 文章写作和配置修改在 `master` 分支进行
2. 不要手动修改 `gh-pages` 分支
3. 定期更新依赖包以保持安全性
4. 主题更新需谨慎测试后再部署