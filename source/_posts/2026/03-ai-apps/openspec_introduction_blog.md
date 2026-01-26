---
title: OpenSpec：规范驱动开发的现代化解决方案
date: 2026-01-26 10:26:21
tags: [SDD, Specification Driven Development, 软件开发, 规范]
categories: [软件工程, 开发方法论]
---
# OpenSpec：规范驱动开发的现代化解决方案

## 引言

在现代软件开发过程中，随着项目规模的增长和团队协作的复杂性增加，如何有效地管理需求变更、确保代码质量和维护系统文档成为了一个重要挑战。OpenSpec是一种规范驱动开发（spec-driven development）的解决方案，它通过结构化的方式组织项目的需求、变更和实现，帮助团队保持代码与文档的一致性。

本文将详细介绍OpenSpec的概念、工作流程以及如何入门使用这一工具。

## 什么是OpenSpec？

OpenSpec是一个用于规范驱动开发的方法论和工具集，它提供了一套完整的流程来管理软件项目中的变更。核心思想是将项目的当前状态（specs）与待实现的变更（changes）分开管理，从而确保开发过程的透明性和可追踪性。

### 核心概念

OpenSpec的核心概念包括：

1. **specs/** - 存放当前已实现功能的规范，代表系统的当前真实状态
2. **changes/** - 存放待实现的变更提案，代表系统将来的变化
3. **archive/** - 存放已完成的变更，形成历史记录

这种设计使得团队能够清晰地了解系统当前的功能、正在开发的功能以及过去的变更历史。

## OpenSpec的目录结构

OpenSpec遵循一套标准化的目录结构，这有助于团队成员快速理解和定位所需信息：

```
openspec/
├── project.md              # 项目约定
├── specs/                  # 当前真实状态
│   └── [capability]/       # 单一专注的能力
│       ├── spec.md         # 需求和场景（使用SHALL/MUST）
│       └── design.md       # 技术模式
└── changes/                # 变更提案
    ├── [change-name]/
    │   ├── proposal.md     # 变更理由与影响
    │   ├── tasks.md        # 实施任务清单
    │   └── specs/          # 增量变更定义
    │       └── [capability]/spec.md # ADDED/MODIFIED/REMOVED
    └── archive/            # 已完成变更
```

## 三阶段工作流程

OpenSpec采用三阶段工作流程来管理项目变更：

### 第一阶段：创建变更提案

当需要添加新功能、进行破坏性变更、更改架构或模式、性能优化（改变行为）或更新安全模式时，需要创建变更提案。变更提案包括：

- **proposal.md** - 描述变更的原因、内容和影响
- **tasks.md** - 实施任务的清单
- **specs/** - 增量变更定义

需要注意的是，只有特定类型的变更需要创建提案。Bug修复、格式调整、注释修改、非破坏性依赖更新和配置更改等不需要创建提案。

### 第二阶段：实施变更

在实施阶段，开发者按照以下顺序执行任务：

1. 阅读 proposal.md - 理解要构建的内容
2. 阅读 design.md（如果有）- 查看技术决策
3. 阅读 tasks.md - 获取实施清单
4. 按照任务清单顺序完成各项任务
5. 在开始实施之前确保提案已审核通过

### 第三阶段：归档变更

部署后，需要通过独立的Pull Request将变更移至archive目录，并根据需要更新主specs，形成完整的历史记录。

## 规范文件格式

OpenSpec使用特定的格式来定义需求和场景：

- 使用 SHALL/MUST 表示规范性需求
- 每个需求必须至少有一个场景
- 场景格式必须是 `#### Scenario:`
- 增量操作分为 ADDED（新增）、MODIFIED（修改）、REMOVED（移除）三类

例如，一个典型的场景格式如下：

```markdown
#### Scenario: 用户登录成功
- **WHEN** 提供有效的凭据
- **THEN** 返回JWT令牌
```

## OpenSpec CLI命令

OpenSpec提供了丰富的命令行工具来辅助开发：

### 基本命令
```bash
openspec list                    # 列出活动变更
openspec list --specs            # 列出现有规范
openspec show [item]             # 显示变更或规范详情
openspec validate [item]         # 验证变更或规范
openspec archive <change-id>     # 归档已部署的变更
```

### 项目管理命令
```bash
openspec init [path]             # 初始化OpenSpec项目
openspec update [path]           # 更新指令文件
```

### 选项标志
- `--json` - 输出JSON格式
- `--type change|spec` - 指定项目类型
- `--strict` - 严格验证模式
- `--no-interactive` - 禁用交互提示
- `--yes`/`-y` - 跳过确认提示

## 实际应用示例

为了更好地理解OpenSpec的使用，我们来看一个实际的例子。假设我们需要为系统添加一个两因素认证功能。

### 1. 创建变更提案

首先，我们创建一个唯一的变更ID，如`add-two-factor-auth`，然后创建相应的目录结构：

```
openspec/changes/add-two-factor-auth/
├── proposal.md
├── tasks.md
└── specs/
    ├── auth/spec.md
    └── notifications/spec.md
```

### 2. 编写提案

在`proposal.md`中描述变更的目的和影响：

```markdown
# Change: Add Two-Factor Authentication

## Why
为增强系统安全性，需要引入两因素认证功能。

## What Changes
- 登录流程中添加OTP验证步骤
- 用户可以配置两因素认证选项
- **BREAKING**: 修改了登录API接口

## Impact
- 受影响的规范：auth
- 受影响的代码：认证服务、用户界面
```

### 3. 定义任务清单

在`tasks.md`中列出实现步骤：

```markdown
## 1. 实现
- [ ] 1.1 设计两因素认证数据库表
- [ ] 1.2 实现生成和验证OTP的API
- [ ] 1.3 更新登录流程
- [ ] 1.4 添加用户界面配置选项
- [ ] 1.5 编写集成测试
```

### 4. 定义规范变更

在`specs/auth/spec.md`中定义新的需求：

```markdown
## ADDED Requirements
### Requirement: Two-Factor Authentication
系统应在用户登录时提供两因素认证选项。

#### Scenario: OTP Required
- **WHEN** 用户启用了两因素认证且提供了有效凭据
- **THEN** 系统应要求用户提供一次性密码(OTP)
```

### 5. 验证并实施

使用CLI验证变更：

```bash
openspec validate add-two-factor-auth --strict --no-interactive
```

## 最佳实践

### 命名约定

- 变更ID使用kebab-case格式，动词开头（如 add-、update-、remove-、refactor-）
- 保持唯一性；如果ID已被占用，追加`-2`、`-3`等后缀

### 简单优先原则

- 默认实现小于100行的新代码
- 单文件实现直到证明需要更多结构
- 避免没有明确理由的框架使用
- 选择简单、成熟的模式

### 复杂性触发条件

只有在以下情况下才增加复杂性：
- 性能数据显示当前解决方案太慢
- 具体的规模需求（>1000用户，>100MB数据）
- 需要抽象的多个已证实的用例

## 总结

OpenSpec提供了一套完整的方法论和工具来管理软件开发过程中的变更。通过规范驱动开发的方式，它帮助团队：

1. 保持代码与文档的一致性
2. 清晰地追踪变更历史
3. 确保需求得到充分测试和验证
4. 提高团队协作效率

虽然学习曲线可能稍显陡峭，但长期来看，OpenSpec能够显著提高软件项目的质量和可维护性。对于需要处理复杂需求变更的团队来说，OpenSpec是一个值得考虑的解决方案。

开始使用OpenSpec的最佳方式是从一个小功能开始，逐步熟悉其工作流程和工具。随着经验的积累，团队将能够更好地利用OpenSpec的强大功能来管理复杂的软件开发项目。