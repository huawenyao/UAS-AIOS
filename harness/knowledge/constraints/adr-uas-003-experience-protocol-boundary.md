# ADR-UAS-003：体验域通用机制上收 G/E/Π

## Status

Accepted · 2026-07-22

## Context

LifeWake 在 SelfPaw 的生命体验场景中需要灵魂数据主权、关系共创、仪式交付和情感价值反馈。它们既不只是某个体验配方的内部字段，也不属于企业系统执行入口 `cs.*`。

若全部留在 `lw.*`：

- 其他个人体验域会重复实现授权、多人共创和影响反馈；
- SelfPaw Core 无法统一执行撤回、审计和演化门禁；
- 仪式及影响记录无法跨 Domain Pack 互操作。

若全部上收平台：

- Kernel 会耦合具体体验、文案、媒介和领域法则；
- LifeWake 与企业 SelfPaw / ΠPaw 的能力命名空间会相互污染；
- 平台协议演进会被单一产品节奏绑架。

## Decision

1. **G 层**上收主体同意与关系共创的治理语义：
   - `schemas/consent_record.schema.json`
   - `schemas/bond_cocreation.schema.json`
2. **E 层**上收情感影响的证据记录，使体验价值能进入反馈—反身—ChangeSet 回路：
   - `schemas/emotion_impact.schema.json`
3. **Π 层**上收仪式协议信封，使参与者、目的、步骤、授权引用和交付状态可互操作：
   - `schemas/ritual_envelope.schema.json`
4. 具体体验能力、类型、连接器、素材和策略继续保留在 LifeWake Domain Pack 的 **`lw.*`** 命名空间。
5. LifeWake 注册为 `selfpaw` 产品轨道下的 `experience_domain`，不新增与 User AGI / Business AGI 并列的轨道，不引入额外层级。

## Boundary

| 平台 G/E/Π | LifeWake Domain Pack |
|-------------|----------------------|
| 同意记录、撤回状态、目的与 scope | 哪些 `lw.*` 操作需要哪些 scope |
| 参与者、贡献、互惠和归属记录 | 关系体验配方及领域失衡判断 |
| 仪式生命周期和通用步骤信封 | 具体文案、媒介、节奏和呈现 |
| 情感影响维度、证据与演化候选引用 | 领域阈值、推荐策略和人工策展 |

## Compatibility

- 四个 schema 是可选增量契约，不修改现有 manifest、审计或 `cs.*` schema 的必填字段。
- 企业 SelfPaw / ΠPaw 不使用体验协议时行为不变；既有 L1/L2/L3 治理继续有效。
- `cs.*` 保持企业 Capability Service 语义；禁止把 `lw.*` 填入 `capability_service.schema.json` 以规避命名规则。
- 消费体验域可以使用 `lw.*`，其他领域使用各自命名空间，并通过 adapter 映射通用协议。
- schema 采用 Draft-07 和版本字段/扩展容器；向后兼容演进只增加可选字段或新版本，不重定义既有字段。

## Consequences

- SelfPaw Core 需逐步实现同意撤回、导出/删除和多人争议处理。
- LifeWake 需增加 `lw.*` 输出到四类通用记录的 adapter。
- 情感影响生成的 ChangeSet 默认不得自动应用，仍需 G 层门禁。
- 仓库提供独立 schema 校验脚本；LifeWake MVP 验收作为体验域场景接入生态 runner。

