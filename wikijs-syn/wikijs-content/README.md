# Wiki.js Content for GitHub Pages

这是 Wiki.js 内容仓库，用于自动发布到 GitHub Pages。

## 工作流程

```
Wiki.js (本地编辑) → Git Push → GitHub Actions → GitHub Pages
```

## 目录结构

```
.
├── docs/              # 文档内容
│   ├── index.md
│   ├── programming/
│   ├── study/
│   └── life/
├── .vitepress/        # VitePress 配置
│   └── config.ts
├── .github/
│   └── workflows/
│       └── build-pages.yml
└── package.json
```

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

## Wiki.js 配置

在 Wiki.js 管理后台配置 Git 存储：

- **存储标识符**: github-wiki
- **存储模式**: 读写
- **Git URL**: `https://github.com/Noeverer/wikijs-content.git`
- **分支**: main
- **验证方式**: HTTPS
- **同步间隔**: 5 分钟

## 相关链接

- [Wiki.js 官方文档](https://docs.requarks.io/)
- [VitePress 文档](https://vitepress.dev/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)

## License

MIT
