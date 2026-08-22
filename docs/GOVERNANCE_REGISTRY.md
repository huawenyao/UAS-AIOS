# UAS-AIOS 治理与未闭环登记册

> **状态**：active · **last_review**：2026-07-22  
> **用途**：统一登记仓库内产品原型、验证型 subapp、治理证据和未闭环项；成熟度以 `ECOSYSTEM_IMPLEMENTATION_STATUS.md` 的 D1-D4 口径为准。

## 1. 登记规则

- `product_track` 只使用 `selfpaw`、`pipaw`、`dual_track` 或 `uas`；Domain Pack 不创建新 AGI 轨。
- `prototype` 表示有可运行证据但尚非生产就绪；`validation` 表示方法或架构验证样例。
- 每个未闭环项必须有稳定 ID、范围、验收证据和状态。
- `cs.*` 属于企业 Capability Service；消费体验域使用独立领域命名空间，并通过通用协议接入 G/E/Π。

## 2. 产品与 subapp 登记

| ID | 路径 | product_track / 分类 | 状态 | 主要证据 | 未闭环 |
|----|------|----------------------|------|----------|--------|
| selfpaw-enterprise | `projects/selfpaw-enterprise/` | selfpaw / 企业桥接 | prototype | `configs/platform_manifest.json`、`scripts/run_edh_dual_track_loop.py` | GOV-SELFPAW-01 |
| enterprise-sales-os | `projects/enterprise-sales-os/` | pipaw / 经营域 | prototype | `scripts/evaluate_sales_mvp.py`、销售 MVP CASE-001～008 | GOV-SALES-01 |
| ai-recruitment-os | `projects/ai-recruitment-os/` | pipaw / 职能域 | prototype | `configs/platform_manifest.json`、业务回路与审计产物 | GOV-RECRUIT-01 |
| lifewake | `projects/lifewake/` | selfpaw / experience_domain | prototype | `scripts/evaluate_lifewake_mvp.py`、仓库级 consent/ritual/emotion/bond 四项 schema | GOV-LW-01～03 |
| ai-recruitment-example | `examples/ai-recruitment/` | uas / 领域闭环验证 | validation | `scripts/run_entity_closed_loop.py`、实体事件模型 | GOV-EXAMPLE-01 |
| selfpaw-cognitive-swarm | `examples/selfpaw-cognitive-swarm/` | selfpaw / 蜂群验证 | validation | `configs/platform_manifest.json`、蜂群决策产物 | GOV-EXAMPLE-02 |
| triadic-ideal-reality-swarm | `examples/triadic-ideal-reality-swarm/` | uas / 推演验证 | validation | `configs/platform_manifest.json`、三维理念现实流程 | GOV-EXAMPLE-03 |

说明：LifeWake 是 SelfPaw 生命体验 Domain Pack，不计入企业数字人 L1-L3 完成率；边界见 `strategic/LIFEWAKE_USER_AGI_EXPERIENCE_DOMAIN.md`。

## 3. 平台治理基线

| 基线 | UAS 层 | 当前工件 | 状态 |
|------|--------|----------|------|
| 企业租户、RBAC/ABAC、审计 | G/S | `schemas/enterprise_*.schema.json`、`schemas/audit_record.schema.json`、企业校验脚本 | baseline |
| 企业能力服务 | S/G | `schemas/capability_service.schema.json`、`configs/capability_registry.json` | baseline |
| 跨轨意图升级 | I/G/Π | `schemas/intent_object.schema.json`、`schemas/working_task.schema.json` | prototype |
| 体验同意与数据主权 | G | `schemas/consent_record.schema.json` | baseline schema |
| 关系共创 | G/Π | `schemas/bond_cocreation.schema.json` | baseline schema |
| 仪式信封 | Π | `schemas/ritual_envelope.schema.json` | baseline schema |
| 情感影响闭环 | E | `schemas/emotion_impact.schema.json` | baseline schema |

## 4. 未闭环项

| ID | 范围 | 未闭环 | 验收证据 | 状态 |
|----|------|--------|----------|------|
| GOV-SELFPAW-01 | SelfPaw Enterprise | 与 SelfPaw 主实现的组织身份、记忆和权限一体化 | 跨仓集成测试覆盖身份、撤权和审计 | open |
| GOV-SALES-01 | Enterprise Sales OS | 沙箱连接器到真实 CRM/BPM 的生产门禁、密钥和回滚 | 生产等价沙箱 + L3 审批/回滚演练 | open |
| GOV-RECRUIT-01 | AI Recruitment OS | 招聘数据保留、偏差监测和人工申诉闭环 | 数据生命周期与公平性审计报告 | open |
| GOV-LW-01 | LifeWake | `lw.*` 输出尚未通过 adapter 形成四类通用 G/E/Π 记录 | adapter 契约测试 + schema 校验 | open |
| GOV-LW-02 | LifeWake / SelfPaw | 同意撤回、导出、删除及多人争议的持久化执行 | 撤回后禁止处理并完成删除/审计测试 | open |
| GOV-LW-03 | LifeWake / E | 情感影响目前是短周期原型，缺少长期负面影响与停止偏好评估 | 纵向反馈测试 + ChangeSet 人工门禁证据 | open |
| GOV-EXAMPLE-01 | Recruitment example | 验证型数据与生产隐私治理未对接 | 明确升级到项目或保持非生产声明 | tracked |
| GOV-EXAMPLE-02 | Cognitive swarm | 蜂群结论偏差与人工 override 尚无统一 Gate 契约 | Gate/override 自动化测试 | tracked |
| GOV-EXAMPLE-03 | Triadic swarm | 实例化结果到真实 System Grid 的执行与回滚未闭环 | 连接器沙箱执行/回滚证据 | tracked |

## 5. 验证入口

- 全生态原型：`python scripts/run_ecosystem_prototype.py`
- 企业与生态 invariants：`python harness/invariants/run-all.py`
- 体验协议 schema：`python scripts/validate_experience_protocol_schemas.py`

