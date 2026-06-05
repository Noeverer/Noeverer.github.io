---
title: Hermes Agent：会自学习的 AI 代理
date: 2026-06-05
tags:
  - AI
  - Agent
  - LLM
  - Nous Research
  - 开源
categories: tech
description: 深入解析 Nous Research 推出的自进化 AI 代理 Hermes Agent，了解它的核心特性、架构与使用方式
---

## 什么是 Hermes Agent？

Hermes Agent 是由 [Nous Research](https://nousresearch.com) 开发的开源 AI 代理。与传统的 LLM 聊天界面不同，Hermes 是一个**自带学习闭环的智能体**——它能从经验中创建技能，在使用中改进技能，主动持久化知识，搜索过往对话，并在跨会话中逐步构建对你的深度理解。

项目地址：[github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（目前 182k Stars，社区非常活跃）

## 为什么叫 Hermes？

Hermes（赫尔墨斯）是希腊神话中的信使神——速度极快、穿梭于各界之间。这个名字很贴切：这个代理可以在终端、Telegram、Discord、Slack 等多个平台之间穿梭，快速响应你的指令。

## 核心特性

### 1. 闭环学习系统

Hermes 最独特的设计是它的**内置学习循环**：

- **技能创建**：完成复杂任务后自动将解决方案封装为可复用技能
- **技能进化**：技能在使用过程中自我改进
- **记忆管理**：代理自主管理记忆并定期主动提醒
- **跨会话回溯**：通过 FTS5 全文搜索 + LLM 摘要，能在不同会话之间回忆

这意味着 Hermes 不是"用完即忘"的——和你相处越久，它就越了解你的习惯和工作方式。

### 2. 多平台覆盖

只需启动一个网关进程，Hermes 就能同时在多个平台为你服务：

| 平台 | 通信方式 |
|------|---------|
| 终端 CLI | `hermes` 命令启动 TUI |
| Telegram | 通过网关接入 |
| Discord | 通过网关接入 |
| Slack | 通过网关接入 |
| WhatsApp | 通过网关接入 |
| Signal | 通过网关接入 |

还支持语音备忘录转写，跨平台对话连续性。

### 3. 模型自由

Hermes 不绑定任何特定模型提供商。通过 `hermes model` 命令即可切换：

- Nous Portal（300+ 模型）
- OpenRouter（200+ 模型）
- OpenAI / Anthropic
- Hugging Face
- 自部署端点

无需修改代码，零锁定。

### 4. 随处运行

Hermes 提供了六种终端后端，可以根据需求灵活选择：

```
本地 → Docker → SSH → Singularity → Modal → Daytona
```

- **$5 VPS**：低成本长期运行
- **GPU 集群**：高性能计算场景
- **Serverless（Modal/Daytona）**：空闲时休眠，按需唤醒，几乎零成本

### 5. 定时自动化

内置 cron 调度器，可以用自然语言定义定时任务：

```
"每天早上 9 点给我发送项目进度报告"
"每周五晚上备份数据库"
```

自动投递到任意已配置的平台。

### 6. 子代理并行

Hermes 可以生成隔离的子代理来处理并行任务，还能通过 RPC 编写 Python 脚本调用工具，将多步操作压缩为单轮完成。

## 快速上手

### 安装

一行命令即可完成安装（支持 Linux、macOS、WSL2）：

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

安装完成后：

```bash
source ~/.bashrc
hermes              # 开始对话
hermes model        # 选择模型
hermes setup        # 完整配置向导
```

### 日常使用命令

```bash
hermes              # 启动交互式 CLI
hermes gateway      # 启动消息网关
hermes config set   # 修改配置
hermes doctor       # 诊断问题
hermes update       # 更新到最新版本
```

## 架构概览

Hermes 的架构核心是**代理循环（Agent Loop）**：

```
用户输入
    ↓
LLM 推理（选择模型）
    ↓
工具调用（40+ 内置工具 / MCP 服务器）
    ↓
结果处理 → 更新记忆 / 创建技能 / 继续推理
    ↓
输出响应
```

关键组件：

- **agent/**：核心代理循环逻辑
- **skills/**：技能系统（过程记忆）
- **tools/**：40+ 内置工具
- **gateway/**：多平台消息网关
- **cron/**：定时任务调度器
- **memory/**：持久化记忆管理

## 与 MCP 的关系

Hermes 深度集成了 [MCP 协议](/2026/05/20/mcp-protocol-introduction/)，可以连接任意 MCP 服务器来扩展能力。这意味着你可以让 Hermes 使用整个 MCP 生态中的工具——从文件操作到数据库查询，从 API 调用到浏览器自动化。

## 适用场景

| 场景 | 说明 |
|------|------|
| **个人助手** | 跨平台提醒、信息查询、日程管理 |
| **开发辅助** | 代码审查、调试、自动化脚本 |
| **运维监控** | 定时巡检、日志分析、告警通知 |
| **研究实验** | 批量轨迹生成、模型评估数据收集 |
| **团队协作** | Slack/Discord 机器人、工作流自动化 |

## 与其他 AI 代理的对比

| 特性 | Hermes | OpenAI Codex | Claude Code |
|------|--------|-------------|-------------|
| 开源 | ✅ MIT | ❌ | ❌ |
| 学习闭环 | ✅ | ❌ | ❌ |
| 多模型支持 | ✅ | ❌ | ❌ |
| 多平台 | ✅ | ❌ | ❌ |
| 定时任务 | ✅ | ❌ | ❌ |
| 子代理并行 | ✅ | ❌ | ❌ |
| 本地运行 | ✅ | ❌ | ❌ |

## 社区与生态

- **技能中心**：[agentskills.io](https://agentskills.io) — 社区分享的技能库
- **MCP 生态**：兼容所有 MCP 服务器
- **WeChat 桥接**：[HermesClaw](https://github.com/AaronWong1999/hermesclaw) — 社区开发的微信集成

## 总结

Hermes Agent 代表了一种新的 AI 代理范式——不再是"用完即走"的对话工具，而是**能持续学习和成长的数字伙伴**。它的开源特性、模型中立、多平台覆盖和闭环学习系统，使其在众多 AI 代理中独树一帜。无论你是想把它作为个人效率工具，还是作为 AI 研究的实验平台，Hermes 都值得一试。
