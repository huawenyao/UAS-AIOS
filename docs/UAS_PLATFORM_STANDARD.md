# UAS Platform 标准

## 平台定义

UAS 不是松散的用户、Agent、系统拼装体，而是一个标准化的 Agent 构建与运行一体化平台：

`UAS-Platform = (I, K, R, A, S, G, E, Π)`

其中：

- `I` = Intent Layer（意图与目标层）
- `K` = Knowledge Substrate（知识底座，默认采用 ASUI）
- `R` = Autonomous Agent Runtime（自主智能体运行时）
- `A` = Agent Fabric（Agent 编织层）
- `S` = System Mesh（专业系统网格层）
- `G` = Governance Plane（治理平面）
- `E` = Evolution Loop（演化回路）
- `Π` = Protocol Stack（协议栈）

## 企业 AGI 定义

企业 AGI 是：

**目标驱动 + 知识驱动 + Agent 协作 + 系统执行 + 审计治理 + 演化闭环 的平台化统一。**

## 平台标准

### 1. 所有 UAS 业务应用的技术底座默认是 ASUI

禁止把 UAS 业务应用实现为：

- 纯 Prompt 工程
- 纯工作流拼接
- 无知识资产沉淀的脚本集合

### 2. 所有 UAS 业务应用的运行架构默认是 autonomous_agent runtime

必须具备：

- 上下文注入
- 状态隔离
- 权限控制
- 审计留痕
- 回滚能力
- 演化入口

### 3. 所有业务项目都应作为 sub uas app 生成

默认目录：

- `projects/<business-app>/`

标准资产至少包括：

- `CLAUDE.md`
- `.claude/skills/`
- `configs/platform_manifest.json`
- `configs/workflow_config.json`
- `configs/swarm_agents.json`
- `configs/runtime_config.json`
- `configs/governance_policy.json`
- `configs/evolution_policy.json`
- `configs/system_registry.json`
- `docs/`
- `scripts/`
- `database/`
- `reports/`

## 平台能力

### Studio

- 定义意图
- 设计知识层
- 规划 agent fabric
- 配置 governance
- 生成 sub app

### Runtime

- autonomous_agent 执行
- task orchestration
- audit / rollback
- context injection
- 多 subapp 统一发现与运行（UAS Runtime Service）

### System Hub

- MCP 工具与系统接入
- 数据语义映射
- 知识系统接入

### Evolution Center

- 指标采样
- 偏差检测
- 迭代建议
- 知识更新

## 共享 Runtime Service

平台级共享运行入口：

- `python3 scripts/run_uas_runtime_service.py list`
- `python3 scripts/run_uas_runtime_service.py validate --app-id <subapp>`
- `python3 scripts/run_uas_runtime_service.py run --app-id <subapp> --topic "<业务议题>" --evaluate`

这意味着多个 `projects/<business-app>/` 不必各自实现运行服务，而是统一挂接到共享 `UASRuntimeService`。
