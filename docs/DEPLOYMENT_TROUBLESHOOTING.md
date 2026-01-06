# GitHub Pages 部署故障排除

## 已解决的问题

### 问题1: 404 错误 - File not found

**原因**:
- `hexo-renderer-pug` 依赖问题
- Markdown 文件的 YAML front matter 格式错误
- GitHub Actions 部署配置问题

**解决方案**:
1. 重新安装 `hexo-renderer-pug`
2. 修复 Markdown 文件的 front matter
3. 更新 GitHub Actions workflow 到最新版本

### 问题2: actions-gh-pages 废弃警告

**原因**: 使用了 v3 版本

**解决方案**: 升级到 v4
```yaml
uses: peaceiris/actions-gh-pages@v4
```

### 问题3: index.html 是 Pug 模板而非 HTML

**原因**: Pug 渲染器配置错误

**解决方案**:
- 清理 node_modules 和缓存
- 重新安装依赖
- 确保主题的 `.pug` 文件正确编译

## 当前配置

### GitHub Actions Workflow
- 使用 `actions/checkout@v4`
- 使用 `actions/setup-node@v4`
- 使用 `peaceiris/actions-gh-pages@v4`
- Node.js 版本: 18

### 主题配置
- 主题: Butterfly v5.5.3
- 渲染器: hexo-renderer-pug, hexo-renderer-stylus
- Hexo 版本: 7.2.0

## 验证部署

### 本地测试
```bash
# 清理缓存
hexo clean

# 生成静态文件
hexo generate

# 检查生成的 index.html
head public/index.html

# 启动本地服务器
hexo server
```

访问 http://localhost:4000 验证主题是否正常工作

### GitHub Actions 检查
1. 访问仓库的 Actions 标签页
2. 检查最新 workflow 的运行状态
3. 查看部署日志是否有错误

### GitHub Pages 设置
1. 进入仓库 Settings → Pages
2. 确认 Source 设置为: Deploy from a branch
3. Branch: gh-pages / (root)
4. 检查自定义域名（如有）

## 常见问题

### Q: 部署成功但网站显示 404

**A**: 检查以下几点：
1. GitHub Pages 的 Branch 设置是否正确
2. gh-pages 分支是否有 index.html
3. 等待几分钟（GitHub Pages 需要时间同步）

### Q: 主题样式没有加载

**A**:
1. 检查 public/css/ 目录是否有 CSS 文件
2. 确认主题配置文件路径正确
3. 清理浏览器缓存

### Q: 图片无法显示

**A**:
1. 检查图片路径是否正确
2. 确认图片在 `source/img/` 或 `source/images/` 目录
3. GitHub Pages 大小限制（单文件 100MB）

### Q: 文章无法生成

**A**:
1. 检查 Markdown 文件的 YAML front matter 格式
2. 确保使用 3 个横线分隔 front matter
3. 检查特殊字符是否正确转义

## 当前状态

✅ GitHub Actions 正常运行
✅ Butterfly 主题已正确配置
✅ 62 个文件成功生成
✅ index.html 是有效的 HTML 文档
✅ 部署到 gh-pages 分支

## 下一步

1. 监控 GitHub Actions 运行状态
2. 验证 https://noeverer.github.io 是否可访问
3. 检查所有页面和功能是否正常
4. 根据需要调整主题配置

## 部署日志查看

GitHub Actions 日志位置:
`仓库 → Actions → Hexo Deploy to GitHub Pages → 选择运行记录`

## 相关文档

- Hexo 官方文档: https://hexo.io/
- Butterfly 主题文档: https://butterfly.js.org/
- GitHub Actions 文档: https://docs.github.com/actions
