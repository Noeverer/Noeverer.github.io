# MCP (Model Context Protocol) 项目说明

## 项目概述

MCP (Model Context Protocol) 是一个模型上下文协议系统，该项目包含完整的MCP系统指南和技术文档，旨在提供AI Agent和技能系统的完整解决方案。

## 项目组成部分

### 1. MCP 系统指南
- **MCP 基础概念** - 介绍MCP协议的基本原理和架构
- **AI Agents 系统** - 详细解释AI Agent的设计和实现
- **Skills 系统** - 技能系统的开发和管理指南
- **Memories 系统** - 记忆系统的实现和使用方法
- **Rules 系统** - 规则引擎的配置和应用
- **系统集成最佳实践** - 实际应用中的最佳实践和经验分享

### 2. 内网部署解决方案
- **完整部署包** - 包含所有必要组件的内网部署方案
- **Docker 容器化** - 完整的容器化部署解决方案
- **配置管理** - 生产级配置模板
- **监控日志** - 完整的可观测性方案

### 3. 技术文档
- **MCP Guide 教科书** - 系统化的技术指南
- **内网部署指南** - 详细的部署和维护文档
- **最佳实践** - 安全和性能优化指南

### 4. 开发工具
- **打包脚本** - 自动化打包和部署工具
- **配置模板** - 可定制的配置文件
- **监控面板** - Grafana 和 Prometheus 集成

## 目录结构

```
Noeverer.github.io/
├── blog/source/_posts/2026/01-tools/mcp-guide/  # MCP指南文章
│   ├── 00-index.md
│   ├── 01-mcp-fundamentals.md
│   ├── 02-ai-agents.md
│   ├── 03-skills-system.md
│   ├── 04-memories-system.md
│   └── 05-rules-system.md
├── mcp-deployment/                    # MCP内网部署包
│   ├── config/                        # 配置文件
│   ├── docker/                        # Docker相关文件
│   ├── docs/                          # 部署文档
│   └── scripts/                       # 部署脚本
├── tools/update-mcp-guide.sh          # MCP指南更新脚本
├── MCP-DEPLOYMENT.md                  # MCP部署说明主文档
├── .mcp.json                          # MCP服务器配置
└── README.md                          # 项目总览
```

## MCP 配置文件

### .mcp.json
```json
{
  "mcpServers": {
    "lean-spec": {
      "command": "npx",
      "args": [
        "-y",
        "@leanspec/mcp",
        "--project",
        "${workspaceFolder}"
      ]
    }
  }
}
```

这个配置文件定义了MCP服务器的启动方式，使用 @leanspec/mcp 包来运行MCP服务。

## 部署方式

### 内网部署
1. 环境准备（Linux, Docker, Docker Compose）
2. 获取部署包并传输到内网环境
3. 配置环境变量
4. 执行部署脚本
5. 验证部署结果

### 服务架构
- MCP Server - 主服务，提供 AI Agent 和技能管理
- Redis 缓存 - 提供高速缓存服务
- PostgreSQL 数据库 - 存储持久化数据
- 技能系统 - 扩展AI能力的插件系统
- 记忆系统 - 提供长期记忆功能
- Nginx 代理 - 提供反向代理和负载均衡

## 主要特性

### 安全性
- 基于角色的访问控制 (RBAC)
- JWT 令牌认证
- 资源访问限制
- SSL/TLS 加密支持

### 高性能
- 异步处理架构
- Redis 缓存优化
- 连接池管理
- 负载均衡支持

### 可扩展性
- 插件化技能系统
- 微服务架构
- 水平扩展支持
- 容器化部署

### 可观测性
- Prometheus 指标收集
- Grafana 监控面板
- 结构化日志记录
- 健康检查机制

## 维护和更新

### 更新MCP指南
使用 `tools/update-mcp-guide.sh` 脚本来更新MCP指南内容。

### 部署管理
- 启动服务: `docker-compose up -d`
- 查看状态: `docker-compose ps`
- 查看日志: `docker-compose logs -f`
- 停止服务: `docker-compose down`

## 适用场景

MCP系统适用于以下场景：
1. 需要构建AI Agent的应用
2. 需要扩展AI能力的技能系统
3. 需要长期记忆功能的对话系统
4. 需要规则引擎的业务逻辑处理
5. 内网环境下部署AI相关服务

## 技术栈

- 核心协议: Model Context Protocol (MCP)
- 容器化: Docker & Docker Compose
- 数据库: PostgreSQL (可选其他数据库)
- 缓存: Redis
- Web服务器: Nginx
- 监控: Prometheus + Grafana
- 开发语言: 根据具体实现而定