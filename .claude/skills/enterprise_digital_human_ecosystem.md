# 企业数字人生态 L1–L3 构建技能

> 标准总纲：`docs/ENTERPRISE_PLATFORM_STANDARD.md`  
> 战略架构：`docs/ENTERPRISE_DIGITAL_HUMAN_L1_L3_ECOSYSTEM.md`  
> 产品规格：`docs/ENTERPRISE_PRODUCT_FUNCTIONAL_SPEC.md`  
> 技术模块：`docs/ENTERPRISE_TECHNICAL_MODULE_SPEC.md`  
> cs 协议：`docs/ENTERPRISE_CS_CAPABILITY_PROTOCOL.md`

## 何时使用

- 为企业场景设计/评估 UAS subapp 或 ΠPaw 岗位体系  
- 将业务议题映射到 DH-L1/L2/L3 与 SelfPaw/ΠPaw 双轨  
- 定义 `cs.*` 能力白名单与 S-Grid 适配器，**禁止** Agent 直连 CRM/BPM API  

## 构建流程（ASUI 标准 + 企业约束）

```
1. 主权与组织分析
   → 租户边界、岗位 scope、合规红线（法则包）
2. 世界模型五维（任务级）
   → 主体（员工/客户/岗位Agent）、客体（线索/订单/合同）、反馈（SLA/KPI）
3. DH 层级判定
   → 个人办事 DH-L1 | 跨部门 DH-L2 | 对外经营 DH-L3
4. cs.* 能力清单
   → 从 enterprise_cs_capability_registry 选取 + 岗位白名单
5. 双轨协同
   → Intent/Evidence 升级路径、Outward Gateway 是否需要
6. UAS 八元组资产
   → platform_manifest, workflow, swarm_agents, governance, evolution, system_registry
7. 商业封装
   → Domain 包 / 岗位包 / 连接器包 / 席位模型
```

## 评估维度（企业扩展）

| 维度 | 阈值 | 检查项 |
|------|------|--------|
| 主权 | 必须 | Agent 工具列表无 raw CRM API；审计链字段完整 |
| 分工 | ≥80% | 岗位 Agent 有 cs 白名单与 KPI |
| 确定性 | 资金/审批/合规 | execution_mode=deterministic |
| 双轨 | 有升级路径 | L1→L2/L3 Intent+Evidence 契约 |
| UAS 覆盖 | ≥80% | I,K,R,A,S,G,E,Π 各有配置或文档占位 |
| 经营闭环 | 场景相关 | 获转服续或对内履约至少一条端到端 |

## 反模式

- 把 DH-L3 销售顾问做成「仅 ChatGPT 套壳」无 cs 与审批  
- SelfPaw 直接调用 `backend_crm` 适配器  
- 省略 Evidence 包导致 ΠPaw 无法审计接力  
- 与 Cognitive Agent L1/L2/L3 混称（应使用 **DH-L1/L2/L3**）

## 配置模板

- `configs/enterprise_cs_capability_registry.example.json`  
- `configs/enterprise_digital_human_tiers.example.json`  
- `configs/enterprise_data_plane_manifest.example.json`  
- `configs/schemas/enterprise_*.schema.json`  

## 需求与模块编号

- 产品功能：`FR-<模块>-<序号>`（见 ENTERPRISE_PRODUCT_FUNCTIONAL_SPEC）  
- 技术模块：`TM-<Name>`（见 ENTERPRISE_TECHNICAL_MODULE_SPEC）  

## 命令衔接

- `/build_domain <业务议题>` — 见 `domain_builder.md`  
- `asui init <project> -t uas-subapp` — Business 轨 subapp  
- `python3 scripts/run_uas_runtime_service.py run --app-id <id> --topic "<议题>" --evaluate`
