---
title: MCP 协议：AI 与工具互联的开放标准
date: 2026-05-20
tags:
  - MCP
  - AI
  - protocol
  - LLM
categories: tech
description: 深入解析 Model Context Protocol，了解 Anthropic 推出的 AI 工具集成开放标准
---

## 什么是 MCP？

Model Context Protocol（MCP）是 Anthropic 推出的一种开放协议，旨在标准化应用程序如何向大语言模型（LLM）提供上下文信息和工具调用能力。你可以把它理解为 **AI 应用的 USB-C 接口**——提供一个统一的标准，让不同的 AI 客户端和工具服务端能够互相连接。

## 为什么需要 MCP？

在 MCP 出现之前，每个 AI 工具集成都需要定制开发：

- 每个 LLM 平台有自己的插件规范
- 每个工具需要独立的适配层
- 上下文传递方式各异，缺乏统一标准

MCP 试图解决这些痛点，提供一个通用的、开放的协议标准。

## 核心架构

MCP 采用典型的客户端-服务端（Client-Server）架构：

```
┌─────────────────┐      ┌─────────────────┐
│   MCP Client     │◄────►│   MCP Server    │
│  (AI 应用/IDE)   │      │  (工具/数据源)   │
└─────────────────┘      └─────────────────┘
        │                        │
        │                        ├── 本地文件系统
        │                        ├── 数据库
        │                        ├── API 服务
        │                        └── 开发工具
        │
  ┌─────┴──────┐
  │  LLM 服务   │
  │ (Claude等)  │
  └────────────┘
```

### MCP Host

MCP Host 是用户直接交互的应用程序，如 Claude Desktop、IDE 插件等。它负责：
- 加载和管理 MCP Server
- 将 LLM 的请求路由到对应的工具
- 将工具返回的结果传递给 LLM

### MCP Client

Client 是 Host 与 Server 之间的内部通道，每个 Server 对应一个 Client 实例。它维护一对一的连接状态。

### MCP Server

Server 是轻量级程序，通过 MCP 协议暴露特定功能。每个 Server 提供三类核心能力：

1. **Resources（资源）**：暴露可读的数据，如文件内容、API 响应
2. **Tools（工具）**：可执行的功能，如运行命令、调用 API
3. **Prompts（提示模板）**：预定义的 LLM 交互模板

## 传输层

MCP 目前支持两种传输方式：

### stdio（标准输入输出）

Server 作为子进程运行，通过标准输入/输出与 Client 通信。适合本地工具集成，延迟低，无需网络配置。

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

### SSE（Server-Sent Events）

通过 HTTP 进行通信，适合远程服务场景。Server 作为独立的 HTTP 服务运行，Client 通过 SSE 接口连接。

```
GET /sse  →  Server 推送事件
POST /message  →  Client 发送请求
```

## 核心协议功能

### 资源（Resources）

资源是 Server 暴露给 LLM 的结构化数据：

```
协议格式：scheme://path
示例：file:///home/user/config.json
     database://users/123
     api://weather/beijing
```

- 支持文本和二进制资源
- 支持资源的订阅和变更通知
- 通过 URI 进行唯一标识和引用

### 工具（Tools）

工具是 LLM 可以执行的函数，定义了清晰的输入输出接口：

```json
{
  "name": "get_weather",
  "description": "获取指定城市的天气信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名称"
      }
    },
    "required": ["city"]
  }
}
```

### 提示模板（Prompts）

预定义的交互模板，用于常见场景：

```json
{
  "name": "code_review",
  "arguments": [
    {
      "name": "code",
      "description": "待审查的代码",
      "required": true
    }
  ]
}
```

## 实际使用示例

### 本地文件系统集成

```json
// ~/.config/opencode/opencode.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    }
  }
}
```

### 数据库查询

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

### GitHub API 集成

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "<your_token>"
      }
    }
  }
}
```

## MCP 的优势

| 特性 | 传统方式 | MCP |
|------|---------|-----|
| 集成方式 | 定制开发 | 即插即用 |
| 协议标准 | 各自为政 | 统一开放 |
| 安全性 | 需自行实现 | 标准化权限控制 |
| 可复用性 | 低 | 高，Server 可共享 |
| 生态 | 碎片化 | 统一生态 |

## 生态现状

目前 MCP 生态已经相当丰富：

**官方 Server**：
- `@modelcontextprotocol/server-filesystem` — 文件系统访问
- `@modelcontextprotocol/server-postgres` — PostgreSQL 数据库
- `@modelcontextprotocol/server-github` — GitHub API
- `@modelcontextprotocol/server-puppeteer` — 浏览器自动化

**社区 Server**：
- 各种数据库（MySQL, Redis, MongoDB 等）
- 云服务（AWS, GCP 等）
- 开发工具（Git, Docker, Kubernetes 等）
- 第三方 API（Slack, Notion, Jira 等）

## 与 Function Calling 的区别

| | MCP | Function Calling |
|---|---|---|
| 范围 | 完整的工具集成协议 | 仅函数调用规范 |
| 资源管理 | 支持资源暴露和订阅 | 不支持 |
| 提示模板 | 内置支持 | 需自行实现 |
| 传输层 | 标准化的 stdio/SSE | 通常内嵌在 API 中 |
| 生态 | Server/Client 生态 | 平台绑定 |

## 总结

MCP 协议代表了 AI 工具集成的一个重要趋势——标准化和开放化。它通过定义清晰的协议边界，让 AI 应用和工具服务能够解耦发展，各自专注于自己的领域。

对于开发者来说，MCP 带来的好处是显而易见的：
- **即插即用**：标准化的 Server 可以无缝接入任何兼容的 Client
- **易于扩展**：编写一个 MCP Server 即可被所有 MCP Host 使用
- **安全可控**：Server 级别的权限控制，LLM 无法越权操作

随着更多平台和工具支持 MCP，它有望成为 AI 时代的通用集成标准。
