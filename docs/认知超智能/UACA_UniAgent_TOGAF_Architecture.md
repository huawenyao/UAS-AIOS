# UniAgent 标准化与群体网络构建生态智能 —— 完整版

> **目标**：明确 Unit Agent 标准、群体网络构建与交互机制；算法只借用有文献/工程共识的模型（消息传递、共识、任务分配、共享状态并发控制、控制论反馈、多臂赌博机、合同网、信息论度量、经济机制设计）。

> **世界模型**：wm_unit_agent_macro_brain.md、wm_system_logic_and_product_stack.md。
> **TOGAF**：见附录；正文不以其为主线。

---

## 一、标准化要解决什么问题（Problem Statement）

| 编号 | 问题 | 不解决则出现的系统故障 |
|------|------|----------------------|
| PS1 | 互操作 | 每个 Agent 一套私有 API，无法组网和替换实现 |
| PS2 | 可观测 | 无法归因「谁基于什么状态做了什么」 |
| PS3 | 安全与资源 | 无统一背压、配额、权限，网络级雪崩或越权 |
| PS4 | 一致性 | 多写者共享图/事件时，冲突语义不清，静默丢更新 |
| PS5 | 可测试 | 无法做一致性测试、仿真回放、合规审计 |
| PS6 | 任务与信用 | 多步协作无法分配责任与奖励（RL/运营都不可用） |
| PS7 | 适应性 | 网络无法根据运行反馈调整拓扑、路由与任务分配 |
| PS8 | 接地性 | Agent 写入世界模型的内容无法验证是否对应真实状态 |
| PS9 | 韧性 | 单点故障或行为异常导致级联失效，无优雅降级路径 |
| PS10 | 激励 | 无经济机制防止搭便车、资源滥用或任务拒绝 |

**结论**：标准化的是能力声明、状态外沿、消息语义、网络拓扑规则、提交到世界模型的契约、适应与激励接口——不是标准化「有多聪明」。

---

## 二、隐含假设的显式化

以下假设被框架依赖但未声明，须显式约定。

### 2.1 时钟同步

分布式系统中时钟不同步是常态。框架采用混合时钟方案：

- **物理时钟**：用于日志排序、审计时间戳，依赖 NTP 同步
- **逻辑时钟**：用于因果序判定，采用 Vector Clock
- **容差声明**：`max_clock_skew_ms` 可配置，超出容差的事件排序以逻辑时钟为准

```
L0 字段：
{
  "clock_mode": "hybrid",
  "physical_clock_sync": "ntp_required",
  "logical_clock_type": "vector_clock",
  "max_clock_skew_ms": 100
}
```

### 2.2 信任模型

所有已注册 Agent 不同等可信。信任分级：

| 信任级别 | 说明 | 能力权限 |
|---------|------|---------|
| `probation` | 新加入或刚从隔离恢复 | 仅 sense、repr、comm.send，无 world.propose |
| `standard` | 正常运行 | 全部 manifest 声明能力 |
| `elevated` | 高信誉、关键节点 | 额外的协调与仲裁权限 |
| `critical` | 基础设施节点 | 网络策略变更、全局配置写入 |

### 2.3 可组合性保证

能力之间存在允许的执行链约束。并非任意输出都能作为任意输入：

```json
{
  "capability_pipeline": {
    "allowed_chains": [
      ["sense.stream", "repr.patch.local", "world.propose"],
      ["sense.poll", "reason.rules", "world.propose"],
      ["sense.poll", "reason.llm", "reason.rules", "world.propose"],
      ["world.query", "reason.llm", "comm.send"],
      ["sense.poll", "repr.patch.local", "comm.broadcast"]
    ],
    "require_validation_before_world_commit": true
  }
}
```

---

## 三、标准化到什么程度（分层）

采用 **七层**，上层依赖下层；通过下层一致性测试才能声称兼容。横切层贯穿所有层级。

```
┌─────────────────────────────────────────────────────┐
│  L5   World Commit                                  │  对共享世界模型的提交契约
├─────────────────────────────────────────────────────┤
│  L4   Network Policy                                │  通信权限、速率、路由、信任
├─────────────────────────────────────────────────────┤
│  L3   Messaging                                     │  消息类型、语义、流控
├─────────────────────────────────────────────────────┤
│  L2   State Envelope                                │  对外可同步的有界状态摘要
├─────────────────────────────────────────────────────┤
│  L1   Capability Manifest                           │  机器可读的能力清单与约束
├─────────────────────────────────────────────────────┤
│  L0   Identity & Lifecycle                          │  身份、版本、生命周期、时钟
├─────────────────────────────────────────────────────┤
│  ★ Adaptation Engine    (横切)                      │  在线学习与策略优化
│  ★ Economics Engine     (横切)                      │  信用、信誉、定价
│  ★ Observability        (横切)                      │  指标、告警、审计
└─────────────────────────────────────────────────────┘
```

### 3.1 各层规范内容与验收方式

| 层级 | 名称 | 规范内容 | 验收方式 |
|------|------|---------|---------|
| L0 | 身份与生命周期 | `unit_id`（全局唯一）、版本、启动/停止/心跳、时钟语义、`lifecycle_state`、`trust_level`、`shadows` | 注册中心 + 健康检查 + 时钟偏差测试 |
| L1 | 能力清单 | 机器可读的带类型能力列表、`capability_pipeline`（组合约束）、`adaptation_policy`、`economics` 字段 | Schema 校验 + 静态扫描 + 管道合法性检查 |
| L2 | 状态包络 | 有界状态摘要（大小上限、字段 schema）、`information_value`、`staleness_score`、不含私有 LLM 全上下文 | 序列化 round-trip + 大小阈值测试 + 信息价值计算 |
| L3 | 交互原语 | 消息类型、字段、超时、重试、幂等键、错误码、背压信号 | 协议一致性测试套件 |
| L4 | 网络策略 | 通信权限、速率、路由、隔离域、`trust_level` 约束、`circuit_breaker` 状态 | 策略单测 + 模糊测试 + 断路器状态机验证 |
| L5 | 世界提交 | `propose → validate → commit/reject` 语义、版本向量/时钟、`grounding_chain`（证据链）、接地一致性校验 | 事务/版本向量 + 冲突注入测试 + 接地验证测试 |

### 3.2 刻意不标准化

- 内部推理算法、是否用 LLM、提示词——归属实现细节
- 只要求 L2/L5 输出形状合法

---

## 四、如何标准化

| 工件 | 说明 |
|------|------|
| 规范文档 | 本文 |
| Schema 定义 | JSON Schema / Protobuf 定义 L0–L5 载荷 |
| 参考实现 | 最小 UniAgent SDK（心跳、manifest、消息类型、graph patch、ledger update） |
| 一致性测试套件 | 双写冲突、乱序投递、重复投递、超时、分区恢复、接地一致性、断路器状态机 |
| 仿真器 | 给定拓扑与能力 manifest，跑确定性场景（回放日志） |
| 版本协商 | `proto_version` 与 `schema_version` 握手；拒绝不兼容组合 |

---

## 五、Unit Agent 能力模型

能力是**类型化令牌**，运行时只允许执行 manifest 已声明的能力；策略引擎据此授权。

### 5.1 能力命名空间（可扩展，扩展需走版本）

| 能力类 | 能力 ID（示例） | 输入/输出概要 | 说明 |
|--------|---------------|-------------|------|
| 感知 | `sense.stream` | 订阅外部 channel → 观测记录 | 接地入口 |
| | `sense.poll` | 查询 → 观测记录 | |
| 表征 | `repr.patch.local` | 局部信念/笔记 → L2 摘要增量 | 不直接写共享世界 |
| | `repr.query.local` | 查询本地摘要 | |
| 推理 | `reason.llm` | 提示 + 结构化约束 → 候选结构 | 可选；输出须再经 L5 |
| | `reason.rules` | 事实集 → 结论 | 确定性优先 |
| 通信 | `comm.send` | 目标 `unit_id` + L3 消息 | |
| | `comm.broadcast` | 域内广播（受 L4 限制） | |
| 世界 | `world.propose` | WM-IR 补丁 + 证据 + 前置版本 | 唯一写共享图通道 |
| | `world.query` | 子图规范 → 只读视图 | |
| 行动 | `act.tool` | 工具调用描述 → 结果/错误 | 可对接真实 API |
| 协调 | `coord.delegate` | 子任务描述 + SLA → 接受/拒绝 | 合同网原语 |
| 元 | `meta.capabilities` | 返回 L1 manifest | |
| 适应 | `adapt.bandit_select` | 同能力 Agent 集合 → 选择一个 | 多臂赌博机路由 |
| | `adapt.report_reward` | 任务完成信号 → reward 更新 | |
| 经济 | `econ.query_balance` | 查询 credit 余额与 reputation | |
| | `econ.ledger_update` | 记录 credit 变动 | |

### 5.2 能力组合约束

见 §2.3。关键规则：`reason.llm` 的输出不能直接作为 `world.propose` 的输入，必须经过 `reason.rules` 校验或人工审批。

### 5.3 与 UACA 的对应（追溯语义）

| UACA 1.0 | 能力映射 |
|---------|---------|
| 感知接入 | `sense.*` |
| 表征 | `repr.*`、`world.query` |
| 推理 | `reason.*` |
| 执行 | `act.*`、`coord.*` |
| 监控 | 策略钩子 + `repr.patch.local` 中的误差字段 |
| 演化 | `world.propose`（经批准）、配置热更新 |
| 适应 | `adapt.*` |
| 经济 | `econ.*` |

---

## 六、L0 完整规范：身份与生命周期

### 6.1 Agent 注册记录

```json
{
  "unit_id": "agent-03",
  "proto_version": "1.0",
  "schema_version": "1.2",
  "created_at": "2026-03-25T08:00:00Z",

  "lifecycle_state": "healthy",
  "lifecycle_allowed_transitions": {
    "starting": ["healthy", "quarantined"],
    "healthy": ["degraded", "quarantined", "stopping"],
    "degraded": ["healthy", "quarantined", "stopping"],
    "quarantined": ["probation", "stopping"],
    "probation": ["healthy", "quarantined", "stopping"],
    "stopping": ["terminated"]
  },

  "clock_mode": "hybrid",
  "physical_clock_sync": "ntp_required",
  "logical_clock_type": "vector_clock",
  "max_clock_skew_ms": 100,

  "trust_level": "standard",
  "heartbeat": {
    "interval_ms": 5000,
    "timeout_ms": 15000,
    "lease_duration_ms": 30000
  },

  "shadows": {
    "enabled": true,
    "agents": ["agent-07", "agent-12"],
    "failover_policy": "automatic",
    "state_sync_interval_ms": 10000
  }
}
```

### 6.2 生命周期状态机

```
                  ┌──────────────┐
                  │   starting   │
                  └──────┬───────┘
                         │ 成功注册 + 首次心跳
                         ▼
                  ┌──────────────┐
          ┌──────│   healthy    │──────┐
          │      └──────┬───────┘      │
          │             │              │
    性能下降│            │ 隔离          │ 停止
          │             │              │
          ▼             ▼              ▼
   ┌───────────┐ ┌────────────┐ ┌──────────┐
   │ degraded  │ │quarantined │ │ stopping │
   └─────┬─────┘ └─────┬──────┘ └────┬─────┘
         │             │              │
    恢复正常    人工/策略批准     清理完成
         │             │              │
         │             ▼              ▼
         │      ┌──────────┐   ┌───────────┐
         └─────→│probation │   │ terminated│
                └────┬─────┘   └───────────┘
                     │ 通过观察期
                     ▼
                ┌──────────┐
                │ healthy  │
                └──────────┘
```

---

## 七、L1 完整规范：能力清单

### 7.1 Capability Manifest Schema

```json
{
  "unit_id": "agent-03",
  "manifest_version": "1.2",
  "updated_at": "2026-03-25T09:00:00Z",

  "capabilities": [
    {
      "id": "sense.stream",
      "version": "1.0",
      "input_schema": "sense_stream_input.json",
      "output_schema": "observation_record.json",
      "sla": {
        "max_latency_ms": 500,
        "min_quality": 0.8
      }
    },
    {
      "id": "reason.llm",
      "version": "1.0",
      "input_schema": "reason_llm_input.json",
      "output_schema": "candidate_structure.json",
      "constraints": {
        "require_post_validation": "reason.rules",
        "max_output_tokens": 4096
      }
    },
    {
      "id": "world.propose",
      "version": "1.0",
      "input_schema": "world_propose_input.json",
      "output_schema": "proposal_result.json"
    }
  ],

  "capability_pipeline": {
    "allowed_chains": [
      ["sense.stream", "repr.patch.local", "world.propose"],
      ["sense.poll", "reason.rules", "world.propose"],
      ["sense.poll", "reason.llm", "reason.rules", "world.propose"]
    ],
    "require_validation_before_world_commit": true
  },

  "adaptation_policy": {
    "type": "bandit",
    "algorithm": "thompson_sampling",
    "exploration_floor": 0.05,
    "reward_function": "latency_quality_composite"
  },

  "economics": {
    "credit_balance": 1000,
    "reputation_score": 0.85,
    "min_task_reward": 10,
    "acceptance_policy": "threshold"
  }
}
```

### 7.2 能力声明的约束

- 每个能力 ID 必须在注册版本命名空间内唯一
- 能力声明的 `version` 支持语义化版本（MAJOR.MINOR）
- 新增能力需要 bump manifest_version，旧版本的 manifest 在超时后失效
- `capability_pipeline` 中的链条必须所有节点都在 `capabilities` 列表中

---

## 八、L2 完整规范：状态包络

### 8.1 State Envelope Schema

```json
{
  "unit_id": "agent-03",
  "envelope_version": "v42",
  "timestamp": "2026-03-25T10:00:00Z",

  "summary": {
    "current_task": "analyze-sensor-stream-01",
    "load_factor": 0.72,
    "error_rate_5m": 0.02,
    "belief_snapshot": {
      "domain": "object_detection",
      "entities_count": 15,
      "avg_confidence": 0.91
    }
  },

  "metadata": {
    "size_bytes": 2048,
    "max_size_bytes": 8192,
    "information_value": 0.65,
    "staleness_score": 0.12,
    "last_confirmed_by": "sense.stream:camera-01",
    "last_confirmed_at": "2026-03-25T09:59:30Z"
  },

  "vector_clock": {
    "agent-03": 42,
    "agent-07": 38,
    "agent-12": 15
  }
}
```

### 8.2 信息价值计算

`information_value` 衡量该摘要相对于接收方已知状态包含多少新信息：

```
information_value = 1 - (已知字段重叠数 / 总字段数)
                  × confidence_decay(age)
```

其中 `confidence_decay(age) = exp(-λ × age_seconds)`，λ 可配置。

`staleness_score` 衡量数据新鲜度：

```
staleness_score = min(1.0, age_seconds / staleness_threshold_seconds)
```

### 8.3 约束

- `size_bytes` 不得超过 `max_size_bytes`，超限拒绝而非截断
- 不包含私有 LLM 全上下文、提示词历史、原始观测流
- 序列化格式必须支持 round-trip（JSON 或 Protobuf）

---

## 九、L3 完整规范：交互原语

### 9.1 消息类型（完整闭集）

| 类型 | 语义 | 幂等 | 超时后行为 |
|------|------|------|-----------|
| `DIRECT` | 点对点请求/响应 | `idempotency_key` | 返回可判定错误，禁止静默丢 |
| `GOSSIP` | 带 TTL/hop_limit 的流言 | 去重表（窗口内） | 丢弃 |
| `PROPOSAL` | 对世界模型的修改提案 | `proposal_id` | 明确 `expired` / `superseded` |
| `TASK_OFFER` | 合同网：任务描述 + 约束 + 经济参数 | `offer_id` | 超时释放 |
| `TASK_ACK` | 接受/拒绝 + 理由 | 绑定 `offer_id` | — |
| `REWARD` | 任务完成信号，携带 reward_signal | `task_id` | 超时不再计入 |
| `LEDGER_UPDATE` | Credit 变动记录 | `transaction_id` | 重试，需幂等保证 |
| `BACKPRESSURE` | 显式反压信号 | — | 发送方降速 |
| `HEARTBEAT` | 存活探测 | 去重 | 触发 suspected 状态 |
| `RECONCILE` | 分区恢复后的状态对账请求 | `reconcile_id` | 重试 |

### 9.2 通用消息信封

```json
{
  "type": "DIRECT",
  "msg_id": "msg-abc-123",
  "proto_version": "1.0",
  "sender": "agent-03",
  "receiver": "agent-07",
  "timestamp": "2026-03-25T10:00:00Z",
  "vector_clock": {"agent-03": 43},
  "ttl_ms": 30000,
  "idempotency_key": "ik-xyz-789",

  "payload": { ... },

  "routing": {
    "hop_limit": 3,
    "path": ["agent-03"],
    "priority": "normal"
  },

  "economics": {
    "credit_cost": 5,
    "reward_if_completed": 50
  }
}
```

### 9.3 载荷上限

- 单消息字节上限与嵌套深度在 L4 配置
- 超限拒绝而非截断

### 9.4 背压与流控

```
每边：令牌桶（token bucket）
  - rate: 每秒 N 条
  - burst: 最大突发 M 条
  - 桶满 → 返回 BACKPRESSURE 错误码

全局：每域 QPS 上限
GOSSIP：fan-out 上限（每节点最多转发给 K 个邻居）

语义对齐 actor mailbox：满则显式反压，禁止无限缓冲
```

---

## 十、L4 完整规范：网络策略

### 10.1 边策略记录

```json
{
  "edge": "agent-03 → agent-07",
  "state": "active",
  "allowed": true,

  "rate_limit": {
    "qps": 100,
    "burst": 200,
    "token_bucket_refill_rate": 100
  },

  "trust_constraints": {
    "min_trust_level": "standard",
    "required_capabilities": ["sense.stream"]
  },

  "circuit_breaker": {
    "state": "closed",
    "failure_count": 0,
    "failure_threshold": 3,
    "success_threshold_for_recovery": 2,
    "open_duration_ms": 30000,
    "last_state_change": "2026-03-25T09:00:00Z"
  },

  "information_routing": {
    "weight": 0.85,
    "mutual_information_rate": 0.72,
    "avg_aoi_ms": 1500
  },

  "audit": {
    "created_reason": "static_config",
    "policy_rule_id": "NG1-deploy-manifest-v3",
    "last_modified": "2026-03-25T08:00:00Z"
  }
}
```

### 10.2 断路器状态机

```
          连续 N 次失败
  CLOSED ──────────────→ OPEN
    ▲                      │
    │  成功 M 次           │ open_duration 到期
    │                      ▼
    └──────────── HALF_OPEN
                    │
              探测成功 → CLOSED
              探测失败 → OPEN
```

### 10.3 信任级别与权限矩阵

| 信任级别 | sense.* | reason.* | world.propose | coord.delegate | L4 变更 |
|---------|---------|----------|---------------|----------------|---------|
| probation | ✅ | ✅ (rules only) | ❌ | ❌ | ❌ |
| standard | ✅ | ✅ | ✅ | ✅ | ❌ |
| elevated | ✅ | ✅ | ✅ | ✅ | 部分 ✅ |
| critical | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 十一、L5 完整规范：世界提交

### 11.1 提交流程

```
Agent ──sense──→ 观测记录
  │                │
  │           reason (基于观测)
  │                │
  │         world.propose (补丁 + 证据链)
  │                │
  │         WM 验证器
  │           ├─ ① 语法校验
  │           ├─ ② 版本冲突检测
  │           ├─ ③ capability_pipeline 合法性
  │           ├─ ④ 接地一致性校验
  │           └─ ⑤ 权限与信任级别检查
  │                │
  │         committed / rejected / staged
  │                │
  └── feedback ────┘
       (consistency_score, drift_alert, rejection_reason)
```

### 11.2 Proposal 载荷

```json
{
  "proposal_id": "prop-001",
  "unit_id": "agent-03",
  "timestamp": "2026-03-25T10:00:00Z",

  "patch": {
    "op": "add_node",
    "target": "wm-graph",
    "node": {
      "id": "obj-vehicle-42",
      "type": "vehicle",
      "properties": {"speed_kmh": 65, "lane": 2}
    }
  },

  "evidence": {
    "source": "sense.stream:camera-01",
    "timestamp": "2026-03-25T09:59:58Z",
    "confidence": 0.87,
    "grounding_chain": [
      {"type": "raw_observation", "ref": "obs-12345"},
      {"type": "inference_step", "model": "reason.rules", "ref": "inf-67890"},
      {"type": "validation_step", "model": "reason.rules", "ref": "val-11111"}
    ]
  },

  "base_version": "v42",
  "vector_clock": {"agent-03": 43, "agent-07": 38},

  "staging": false,
  "auto_commit_if_no_conflict": true
}
```

### 11.3 冲突解决策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| `reject` | 版本冲突直接拒绝，返回当前版本 | 强一致要求 |
| `last_writer_wins` | 基于时间戳（需时钟同步） | 低冲突域 |
| `merge_rules` | 按预定义合并规则自动合并 | 属性级更新 |
| `human_arbitration` | 冲突提交给人工仲裁队列 | 高价值/高风险 |

### 11.4 接地一致性校验

- **证据时效性**：观测时间 vs 提交时间，超阈值标记 `stale`
- **置信度衰减**：长时间未被新观测确认的条目，自动降低置信度
- **反事实探测**：标记为 `uncertain` 的条目，触发 `sense.poll` 验证
- **consistency_score**：综合以上因素的 0–1 分数

### 11.5 预测与事实分离

- 推理结果（`reason.llm` 输出）进入 `staging: true`
- 不进入 committed 除非满足：证据置信度 ≥ 阈值 AND 经过 `reason.rules` 校验 AND 策略允许

---

## 十二、群体网络构建

网络是有向多重图 G = (U, E)，U 为 UniAgent 集合，E 为允许交互的边。

### 12.1 边的来源（必选一种或组合）

| 规则 ID | 构造方式 | 用途 |
|---------|---------|------|
| NG1 | 静态配置（部署清单） | 冷启动、强合规 |
| NG2 | 世界模型边投影 | Role → 命令/汇报边；Adjacent → P2P 邻接；IsPartOf → 树内仅父子通信 |
| NG3 | 任务图派生 | 任务分解产生临时边（TTL、自动回收） |
| NG4 | 引入/发现 | 注册中心 + 受控邀请（签名 token），防任意全网互联 |
| NG5 | 适应引擎重连 | `adaptation_engine` 基于 regret 或 bandit 信号动态增删边 |

**禁止**：默认「全连接」或「任意 Agent 可连任意 Agent」——无法做 L4 策略与测试。

### 12.2 拓扑模式

| 模式 | 结构 | 典型算法/机制 | 适用 |
|------|------|-------------|------|
| 层级树 | Role 生成有向树 | 上游汇总/下游广播；超时与替身 | 组织、流水线 |
| 局域邻域 | Adjacent k-hop 子图 | DeGroot 加权平均、gossip | 共识、态势对齐 |
| 星型协调 | 协调器（可为无智能的队列） | 合同网、任务队列、背压 | 资源分配 |
| 共享介质 | 少边、多写日志/图 | OCC + 版本向量 / CRDT | stigmergy，强一致写 |
| **自适应混合** | **以上组合，由适应引擎动态切换** | **Bandit 选择拓扑模式 + regret 触发重配** | **复杂场景** |

### 12.3 动态变更

- 边增删必须产生审计事件：`{unit_id, edge, reason, policy_rule_id, triggered_by}`
- 任务边必须带 `expires_at`
- 分区检测：心跳与租约；失效边进入 `suspected` 状态，消息路由降级
- 适应引擎触发的边变更须记录 `adaptation_context`（regret 值、bandit 统计）

### 12.4 信息流度量（每条边维护）

```
① Mutual Information Rate: I(观测; 接收)
   该边传递的信息量 vs 噪声
   低 I → 该边价值低，考虑移除

② Age of Information (AoI)
   AoI(t) = t - timestamp(最新接收的状态)
   用于决定是否需要同步

③ Information Distortion
   经过 k-hop 后，消息与原始的语义距离
   用 embedding cosine similarity 近似
```

---

## 十三、交互机制设计

### 13.1 任务分配

**合同网（Contract Net）**：标准交互

```
协调器                    接受者
  │                         │
  │──── TASK_OFFER ────────→│
  │     (任务+约束+reward)   │
  │                         │
  │←─── TASK_ACK ──────────│
  │     (accept/reject)     │
  │                         │
  │     ... 执行 ...        │
  │                         │
  │←─── REWARD ────────────│
  │     (task_id, score)    │
```

**带信誉的竞价**：报价不只看价格，还看 reputation

```
effective_bid = base_bid × (1 / reputation_score)
协调器选择 effective_bid 最低的接受者
```

**队列竞争**：多个 worker 抢同一队列

- 可见性：消息对 N 个 worker 可见
- 公平性：采用加权轮询或最短队列优先，避免饥饿

### 13.2 共识机制

| 场景 | 算法 | 工程落地 |
|------|------|---------|
| 意见收敛 | DeGroot 加权平均 | GOSSIP + 收敛轮次上限 + 停机条件 |
| 配置一致性 | Raft / Membership | 仅用于全局配置，不用于业务数据 |
| 共享记忆一致 | OCC + MVCC | L5 `world.propose` |
| 冲突合并 | CRDT（按需） | 适用于可交换操作的属性更新 |

### 13.3 分布式探索

| 策略 | 说明 | 配置位置 |
|------|------|---------|
| ε-greedy | 以 ε 概率随机选择，1-ε 概率选最优 | L1 `adaptation_policy` |
| UCB1 | 基于置信上界的探索-利用平衡 | L1 `adaptation_policy` |
| Thompson Sampling | 贝叶斯采样，自适应探索率 | L1 `adaptation_policy` |
| 轮询 | 简单轮转，无学习 | L1 `adaptation_policy: static` |

### 13.4 分区恢复

```
1. 检测到分区恢复（心跳恢复）
2. 双方交换 vector_clock
3. 计算 delta（各自持有但对方没有的变更）
4. 按 L5 冲突解决策略合并
5. 生成 RECONCILE 完成事件
6. 边状态从 suspected → active
```

---

## 十四、适应引擎（Adaptation Engine）

### 14.1 定位

横切层，贯穿 L0–L5。不改变协议本身，而是**动态调整协议参数和网络拓扑**。

### 14.2 三层时间尺度

| 层级 | 时间尺度 | 机制 | 输出 |
|------|---------|------|------|
| 短期 | 分钟级 | 在线 bandit（UCB1 / Thompson） | 边权重、能力路由选择 |
| 中期 | 小时级 | 离线策略评估 + regret 计算 | 拓扑变更（加边/切边） |
| 长期 | 天级 | 版本演进、manifest 更新 | 新能力声明、旧能力废弃 |

### 14.3 边 Bandit

每条边 e 被视为一个臂：

```
对于边 e (sender → receiver, capability c):
  - 维护：尝试次数 n_e, 累积 reward R_e
  - reward = α × quality + β × (1 - normalized_latency) + γ × (1 - cost)
  - 选择策略：Thompson Sampling
    采样 θ_e ~ Beta(α_e, β_e)
    选择 argmax_e θ_e
  - 探索下限：exploration_floor = 0.05（即使 regret 高也保留 5% 概率尝试）
```

### 14.4 协调器策略梯度

协调器学习任务分配策略 π(s) → a：

```
状态 s = (可用 Agent 能力集, 各 Agent 负载, 历史成功率, 信誉分布)
动作 a = 选择哪个 Agent 接受任务
奖励 r = 任务完成质量 × 速度 × 成本效率

策略更新：∇J(θ) = E[∇log π(a|s;θ) × (r - baseline)]
baseline = 移动平均奖励
```

### 14.5 Regret Tracking 与拓扑触发

```
对于每条边 e:
  cumulative_regret_e = Σ_t (optimal_reward_t - actual_reward_t)
  
  规则：
  - cumulative_regret_e > threshold_high → 触发切边评估
  - cumulative_regret_e < threshold_low  for sustained period → 触发加边评估
  
  拓扑变更需经 L4 策略引擎批准
```

### 14.6 接口

```
L1 manifest:
  "adaptation_policy": {
    "type": "bandit",
    "algorithm": "thompson_sampling",
    "exploration_floor": 0.05,
    "reward_function": "latency_quality_composite",
    "reward_weights": {"quality": 0.5, "latency": 0.3, "cost": 0.2}
  }

L3 消息:
  REWARD {
    "task_id": "task-xyz",
    "reward_signal": 0.85,
    "latency_ms": 1200,
    "quality_score": 0.92,
    "cost_credits": 50
  }
```

---

## 十五、经济引擎（Economics Engine）

### 15.1 定位

横切层。提供激励兼容性，防止搭便车和资源滥用。

### 15.2 Credit Ledger

```
分布式账本（可简化为 append-only 日志）

每条记录：
{
  "transaction_id": "tx-001",
  "timestamp": "2026-03-25T10:05:00Z",
  "entries": [
    {"agent": "agent-03", "delta": +50, "reason": "task-complete:offer-xyz"},
    {"agent": "agent-07", "delta": -10, "reason": "request-served:direct-abc"}
  ],
  "vector_clock": {"ledger-node-1": 100}
}
```

### 15.3 任务定价

```
reward = base_reward × urgency_multiplier × scarcity_multiplier

其中：
  base_reward = f(任务复杂度)
  urgency_multiplier = f(剩余时间 / deadline)
  scarcity_multiplier = 1 / (能完成该任务的 Agent 数量)

协调器在 TASK_OFFER 中附带 reward
接受者用 credit_balance 约束决策（余额 < 阈值 → 只能接受高回报任务）
```

### 15.4 信誉系统

```
reputation = α × 完成率 + β × 响应速度归一化 + γ × 结果质量

参数：
  α = 0.4, β = 0.3, γ = 0.3（可配置）

更新规则：
  每次任务完成后，用指数移动平均更新
  reputation_new = decay × reputation_old + (1 - decay) × task_score

高 reputation → 优先获得高价值任务
```

### 15.5 防搭便车

```
在时间窗口 W 内（如 24 小时）：
  如果 Agent 完成的任务数 < K_min → 降级到 degraded
  如果连续 3 个窗口 < K_min → 降级到 quarantined
  
例外：manifest 声明 role 为 "observer" 的 Agent 免除此规则
```

### 15.6 通胀控制

```
全局 credit 池有上限 max_credits
当总流通 credit 接近上限时：
  reward 衰减 = max_credits / current_total_credits
  新任务 reward = base_reward × decay_factor
```

---

## 十六、韧性机制（Resilience）

### 16.1 Capability Shadowing

```
L0 manifest:
  "shadows": {
    "enabled": true,
    "agents": ["agent-07", "agent-12"],
    "failover_policy": "automatic",
    "state_sync_interval_ms": 10000
  }

行为：
  - shadow Agent 定期同步主 Agent 的 L2 State Envelope
  - 主 Agent 失效 → 注册中心自动将流量路由到 shadow
  - shadow 接管后，状态从最近的同步点恢复
```

### 16.2 优雅降级阶梯

```
Level 0 (full)        → 所有能力正常
Level 1 (reduced)     → 降低非关键能力的 SLA（如 sense.stream 降帧率）
Level 2 (minimal)     → 仅保留核心能力（sense.poll + reason.rules）
Level 3 (offline)     → 停止接受新任务，仅完成已承诺任务

降级触发条件：
  - error_rate_5m > threshold
  - load_factor > threshold
  - credit_balance < minimum
  
降级路径由 manifest 声明，策略引擎执行
```

### 16.3 隔离协议

```
检测到异常行为（如疯狂 propose、异常高的错误率）→
  1. trust_level 降为 quarantine
  2. L4 权限收紧：仅允许 comm.send 到指定管理节点
  3. 生成 quarantine 审计事件
  4. 需要人工或策略引擎批准才能恢复

恢复路径：quarantine → probation → standard
```

### 16.4 状态对账

```
分区恢复后：
  1. 双方交换 vector_clock
  2. 计算 delta（各自独有变更集）
  3. 按 L5 冲突解决策略合并
  4. 生成 RECONCILE 完成事件
  5. 边状态从 suspected → active
  6. credit ledger 做对账，确保无双花
```

---

## 十七、可观测指标（完整 SLO 集）

### 17.1 原有指标

| 指标 | 定义 | 用途 |
|------|------|------|
| `proposal_reject_rate` | 非法补丁占比 | 数据质量、提示词、模型漂移 |
| `proposal_conflict_rate` | 版本冲突率 | 并发设计、拓扑过密 |
| `msg_latency_p99` | 按边类型分位延迟 | 容量规划 |
| `backpressure_rate` | 反压触发频率 | 过载检测 |
| `task_offer_timeout_rate` | 合同网超时 | 能力不匹配 |
| `edge_churn` | 单位时间边增删 | 稳定性 |

### 17.2 新增指标

| 指标 | 定义 | 用途 |
|------|------|------|
| `information_freshness_aoi` | 按边 Age of Information 分位数 | 同步需求 |
| `grounding_consistency_score` | L5 提交的平均接地一致性 | 推理漂移检测 |
| `reputation_gini` | 信誉分布的基尼系数 | 搭便车/垄断检测 |
| `circuit_breaker_triggers` | 断路器触发次数/频率 | 边健康 |
| `adaptation_regret_cumulative` | 各边累积 regret | 适应引擎效果 |
| `credit_velocity` | 单位时间 credit 流转量 | 经济系统活性 |
| `degradation_events` | 降级事件次数 | 韧性健康 |
| `quarantine_events` | 隔离事件次数 | 安全健康 |
| `shadow_takeover_count` | shadow 接管次数 | 可用性 |
| `mutual_information_per_edge` | 各边互信息率 | 拓扑效率 |

### 17.3 告警规则

| 告警 | 条件 | 响应 |
|------|------|------|
| `drift_alert` | `grounding_consistency_score < 0.5` 持续 5 分钟 | 触发 `sense.poll` 验证 + 通知协调器 |
| `quarantine_spike` | `quarantine_events > 10` / 小时 | 检查网络攻击或模型异常 |
| `credit_deflation` | `credit_velocity < threshold` 持续 1 小时 | 调整 reward 参数 |
| `regret_explosion` | 任意边 `cumulative_regret > 3σ` | 触发拓扑重评估 |

---

## 十八、算法-机制-工程映射（完整表）

| 群体现象需求 | 指名原理/构件 | 工程落地 | 对应层级 |
|---|---|---|---|
| 意见收敛 | DeGroot 加权平均 | GOSSIP + 收敛轮次上限 + 停机条件 | L3 + §12.2 |
| 配置一致性 | Raft / Membership | 仅用于全局配置 | L4 |
| 共享记忆一致 | OCC + MVCC + CRDT | L5 `world.propose` | L5 |
| 任务分配 | 合同网 + 信誉加权竞价 | `TASK_OFFER` / `TASK_ACK` | L3 + §15 |
| 能力路由 | Multi-armed bandit (UCB1 / Thompson) | `adapt.bandit_select` | ★ Adaptation |
| 拓扑自适应 | Regret-based edge pruning/rewiring | Adaptation Engine → L4 | ★ Adaptation + L4 |
| 信息传播保真度 | Information bottleneck | 汇总节点有损压缩 | L2 + §12.4 |
| 异常检测 | CUSUM / Change-point detection | 行为分布突变告警 | ★ Observability |
| 资源公平分配 | Proportional fairness + max-min | 带权分配 vs 最弱者优先 | L4 + ★ Economics |
| 稳定性 | 负反馈控制 | 错误率↑ → 降耦合/降速 | L4 + L3 |
| 因果归因 | 事件溯源 + 有向影响边 | WM Event + Affect / 审计日志 | L5 + ★ Observability |
| 激励兼容 | 机制设计（VCG 简化） | Credit ledger + 定价 + reputation | ★ Economics |
| 韧性 | 冗余 + 断路器 + 优雅降级 | Shadow + Circuit breaker + Degradation ladder | L0 + L4 |
| 接地 | 证据链 + 时效性衰减 | Grounding chain + consistency score | L5 |

**不声称**：「本网络自动 AGI」。

**声称**：在给定拓扑与策略下，可证明/可测量的行为界：

- gossip 在连通图上的传播轮次上界
- 合同网在超时下的任务重分配保证
- bandit 算法的 regret 上界 O(√(T log T))
- 信用系统在通胀控制下的均衡存在性

---

## 十九、参考实现骨架

### 19.1 最小 SDK 功能清单

```
1. 注册与心跳
   - register(unit_id, manifest) → 注册中心
   - heartbeat(unit_id) → 周期性

2. 消息发送/接收
   - send(DIRECT, receiver, payload)
   - broadcast(GOSSIP, domain, payload, ttl)
   - on_receive(callback)

3. 世界模型交互
   - propose(patch, evidence, base_version) → result
   - query(subgraph_spec) → view

4. 合同网
   - offer(task, reward, constraints) → ack_list
   - accept/reject(offer_id, reason)

5. 经济
   - query_balance() → {credit, reputation}
   - ledger_update(transaction)

6. 适应
   - report_reward(task_id, reward)
   - get_routing_recommendation(capability) → agent_id
```

### 19.2 一致性测试场景

```
1. 双写冲突：两个 Agent 同时 propose 同一节点的不同属性
2. 乱序投递：消息 B 先于消息 A 到达
3. 重复投递：同一消息投递两次，验证幂等
4. 超时：TASK_OFFER 超时后资源释放
5. 分区恢复：模拟网络分区后恢复，验证状态对账
6. 接地验证：提交无 grounding_chain 的 proposal，验证拒绝
7. 断路器：连续失败触发 OPEN，恢复后 HALF_OPEN → CLOSED
8. 信用双花：分区期间尝试双花 credit，恢复后验证对账
9. 搭便车检测：Agent 长期不贡献，验证降级
10. 适应收敛：多 Agent 场景下 bandit 路由收敛到最优
```

---

## 二十、版本与演进

| 版本 | 内容 | 向后兼容 |
|------|------|---------|
| 1.0 | L0–L5 基础协议 + 适应/经济/韧性框架 | — |
| 1.1 | 增加新的能力命名空间 | ✅（新能力，旧 Agent 忽略） |
| 1.2 | 增加新的消息类型 | ✅（旧 Agent 收到未知类型返回 UNSUPPORTED） |
| 2.0 | 改变 L5 冲突解决语义 | ❌（需要迁移） |

**升级流程**：
1. 新版本规范发布
2. 参考实现更新
3. 一致性测试套件更新
4. 灰度：新旧版本共存，通过 `proto_version` 握手协商
5. 全量：旧版本 Agent 在 grace period 后被标记为 `deprecated`