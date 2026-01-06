# HTML to Hexo 转换系统

完整的自动化脚本，用于将HTML博客文章转换为Hexo格式，并集成GitHub Actions实现持续部署。

## 功能特性

### 1. HTML转Markdown转换
- 智能解析HTML文件提取文章内容
- 自动提取标题、日期、标签、分类
- 保留原始格式（代码块、列表、引用等）
- 错误处理和日志记录

### 2. Git分支管理
- 自动创建特性分支（按分类）
- 智能合并和推送
- 版本标签管理

### 3. GitHub Actions集成
- 自动构建Hexo站点
- 持续部署到GitHub Pages
- 支持手动触发

### 4. 智能主题推荐
- 基于内容分析推荐最适合的Hexo主题
- 考虑代码高亮、响应式设计、SEO等因素
- 提供详细的匹配度评分

## 安装依赖

```bash
# Python依赖
pip install beautifulsoup4 GitPython

# Hexo依赖
npm install -g hexo-cli
npm install
```

## 使用方法

### 基本使用

```bash
# 运行完整转换流程
python3 html2hexo.py

# 转换指定目录
python3 html2hexo.py --dir ./chocolate

# 创建特性分支
python3 html2hexo.py --branch chocolate

# 查看主题推荐
python3 html2hexo.py --recommend

# 设置GitHub Actions
python3 html2hexo.py --setup
```

### Git分支工作流

```bash
# 为特定内容创建分支
python3 html2hexo.py --branch code

# 手动管理Git
git checkout -b feature/new-content
python3 html2hexo.py
git add .
git commit -m "Add new posts"
git push origin feature/new-content
```

### 自动部署

推送到master分支后，GitHub Actions会自动部署：

```bash
git checkout master
git merge feature/new-content
git push origin master
```

## 项目结构

```
Noeverer.github.io/
├── html2hexo.py              # 主脚本
├── html2hexo.log            # 转换日志
├── source/_posts/           # Markdown输出目录
├── .github/workflows/
│   └── hexo-deploy.yml      # GitHub Actions配置
├── DEPLOYMENT.md            # 部署说明
└── [HTML源目录]             # 待转换的HTML文件
```

## 主题推荐系统

系统会自动分析文章内容并推荐主题：

### 支持的主题
- **NexT** - 功能最全面，推荐度95%
- **Butterfly** - 美观现代，推荐度92%
- **Fluid** - 简洁优雅，推荐度90%
- **Stun** - 极简主义，推荐度85%
- **Cactus** - 轻量级，推荐度80%

### 分析维度
- 代码内容比例
- 图片数量
- 数学公式使用
- 文章长度
- 技术内容占比

## 日志记录

所有操作记录在 `html2hexo.log` 文件中：

```
2026-01-05 10:00:00 - html2hexo - INFO - 开始扫描HTML文件...
2026-01-05 10:00:05 - html2hexo - INFO - 找到 50 个HTML文件
2026-01-05 10:00:10 - html2hexo - INFO - 解析成功: Example Article Title
```

## GitHub Actions配置

工作流文件位于 `.github/workflows/hexo-deploy.yml`

### 触发条件
- 推送到master分支
- Pull Request到master
- 手动触发（在Actions页面）

### 部署流程
1. 检出代码
2. 设置Node.js环境
3. 安装依赖
4. 运行HTML转换
5. 构建Hexo站点
6. 部署到GitHub Pages
7. 创建版本标签

## 错误处理

脚本包含完善的错误处理机制：

- 文件读取失败会记录到日志
- 解析错误不会中断整个流程
- 重复文件会被自动跳过
- 所有错误信息汇总显示

## 自定义配置

### 修改输出目录

```python
# 在html2hexo.py中修改
self.output_dir = self.base_dir / 'custom_output_dir'
```

### 添加新的HTML目录

```python
# 在scan_html_files方法中添加
directories = [
    'chocolate',
    'your_new_directory',  # 添加新目录
    ...
]
```

### 自定义主题推荐

```python
# 在ThemeRecommender.THEMES中添加新主题
'your_theme': {
    'name': 'Your Theme Name',
    'description': 'Description',
    'features': {...},
    'suitability_score': 90,
    'official_url': 'https://...'
}
```

## 故障排除

### 问题：转换失败
- 检查HTML文件编码是否为UTF-8
- 查看日志文件了解详细错误
- 确保beautifulsoup4和GitPython已安装

### 问题：GitHub Actions失败
- 检查GITHUB_TOKEN权限
- 确认仓库设置启用了Pages
- 查看Actions运行日志

### 问题：主题推荐不合适
- 使用`--recommend`选项查看详细分析
- 根据实际需求手动选择主题
- 可以手动安装任意Hexo主题

## 最佳实践

1. **定期转换** - 每次更新HTML后运行脚本
2. **分支管理** - 为不同类型内容使用不同分支
3. **主题选择** - 根据推荐选择合适的主题
4. **监控日志** - 定期检查日志文件
5. **版本控制** - 及时提交和推送更改

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
