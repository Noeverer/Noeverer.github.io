# 分支说明

此仓库使用以下分支结构：

- `master` 分支：存放博客文章源码和其他配置文件
- `gh-pages` 分支：由 GitHub Action 自动构建和部署，用于 GitHub Pages 展示

## 注意事项

1. 文章写作和配置修改应在 `master` 分支进行
2. `gh-pages` 分支由 CI/CD 流程自动管理，不要手动推送更改
3. GitHub Action 会监听 `master` 分支的更改，并自动构建静态页面到 `gh-pages` 分支
4. 构建后的网站文件（包括 `index.html`）会出现在 `gh-pages` 分支中