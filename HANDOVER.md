# 项目交接文档

## 项目概述
这是一个基于 Hexo 框架的个人博客网站，托管在 GitHub Pages 上。项目不仅包含个人博客内容，还集成了完整的 MCP (Model Context Protocol) 系统指南和内网部署解决方案。

## 分支结构
- `master` 分支：存放博客文章、主题配置、源代码等
- `gh-pages` 分支：由 GitHub Action 自动构建生成的静态网站文件

## 关键文件说明
- `_config.yml`：Hexo 主配置文件
- `_config.butterfly.yml`：Butterfly 主题配置文件
- `source/`：博客文章和页面源文件
- `themes/butterfly/`：Butterfly 主题文件
- `public/`：构建后生成的静态网站文件（已忽略）
- `mcp-deployment/`：MCP 内网部署相关文件
- `blog/source/_posts/2026/01-tools/mcp-guide/`：技术实现导向的 MCP 系统指南
- `blog/source/_posts/2026/mcp-guide/`：概念应用导向的 MCP 系统指南
- `.mcp.json`：MCP 服务器配置文件
- `MCP_GUIDE_ORGANIZATION.md`：MCP 指南内容组织说明

## GitHub Action 工作流
- 监听 `master` 分支的推送事件
- 自动执行 `hexo generate` 构建网站
- 将构建结果部署到 `gh-pages` 分支

## MCP (Model Context Protocol) 项目说明

### 项目组成
- **MCP 系统指南**：包含 MCP 基础、AI Agents、Skills 系统、Memories 系统、Rules 系统等完整技术文档
- **内网部署解决方案**：完整的 MCP 服务器内网部署包，包含 Docker 容器化部署、配置管理、监控日志等功能
- **开发工具**：自动化打包和部署工具、配置模板、监控面板等

### MCP 配置
- `.mcp.json` 文件定义了 MCP 服务器的启动方式，使用 @leanspec/mcp 包来运行 MCP 服务
- 配置中指定了项目路径和运行参数

### 部署架构
- **MCP Server**：主服务，提供 AI Agent 和技能管理
- **Redis 缓存**：提供高速缓存服务
- **PostgreSQL 数据库**：存储持久化数据
- **技能系统**：扩展 AI 能力的插件系统
- **记忆系统**：提供长期记忆功能
- **Nginx 代理**：提供反向代理和负载均衡

## 常见问题及解决方案
### 1. GitHub Action 构建失败："index.html not found!"
- 原因：`.gitignore` 文件中包含了 `index.html`
- 解决：移除 `.gitignore` 中的 `index.html` 规则

### 2. 依赖管理
- `package.json` 和 `package-lock.json` 需要版本控制以确保构建一致性

### 3. 静态资源处理
- 图片、CSS、JS 等静态资源应放在 `source/` 目录下对应子目录

### 4. MCP 相关问题
- 如需更新 MCP 指南内容，可使用 `tools/update-mcp-guide.sh` 脚本
- MCP 内网部署包位于 `mcp-deployment/` 目录，包含完整的部署文档和脚本
- MCP 指南有两个版本：技术实现导向（`blog/source/_posts/2026/01-tools/mcp-guide/`）和概念应用导向（`blog/source/_posts/2026/mcp-guide/`）
- 更新 MCP 指南时，需注意两个版本的内容一致性，请参考 `MCP_GUIDE_ORGANIZATION.md` 了解详细组织结构

## 维护注意事项
1. 文章写作和配置修改在 `master` 分支进行
2. 不要手动修改 `gh-pages` 分支
3. 定期更新依赖包以保持安全性
4. 主题更新需谨慎测试后再部署
5. MCP 相关文档更新时，注意同步更新 `MCP_OVERVIEW.md` 和本交接文档
6. 内网部署相关变更需在 `mcp-deployment/` 目录中进行，并更新 `MCP-DEPLOYMENT.md` 文档