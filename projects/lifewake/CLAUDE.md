# 生命回响（LifeWake）

## 概述

UAS subapp：将「惊喜盲盒」与「心跳音乐」收敛为可审计、可撤回、可演化的情感共创闭环。规约包在仓库根目录 `docs/lifewake/`。

完整产品 BP：`../../docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md`；
本项目可运行实现摘要：`docs/APP_BLUEPRINT.md`。

## 命令

- `/intent [情感议题]` — 归一化惊喜或心跳共鸣意图
- `python scripts/evaluate_lifewake_mvp.py` — 行为验收 CASE-001～014
- `python scripts/run_value_loop_prototype.py` — 输入→体验→反馈→演化完整闭环
- `python scripts/run_emotion_kpi_snapshot.py` — 从运行事实生成情感 KPI
- `pytest -q` — 策略红线、14 CASE 与价值闭环测试
- `python scripts/run_subapp.py "生命回响" --evaluate` — 经 UAS runtime 工作流（若环境支持 LLM 步）

离线流水线单步：

```bash
echo '{"topic":"惊喜盲盒","lifewake_case_id":"CASE-001"}' | python3 scripts/run_lifewake_pipeline.py
```

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/platform_manifest.json` | UAS 八元组 + `spec_root: docs/lifewake` |
| `configs/workflow_config.json` | UAS 九步执行链与 Agent 审计 |
| `configs/governance_policy.json` | 隐私用途、wow 门禁、双向关系 |
| `configs/swarm_agents.json` | 情感炼金 Agent 编织 |
| `configs/system_registry.json` | `lw.*` 能力与 mock connector |
| `configs/world_model.json` | 情感世界模型五维 |
| `configs/entity_schemas.json` | Person/Consent/Surprise/Pulse 等 |

## 产物

- `database/audit/` — 同意与创作审计
- `database/runs/` — 价值闭环运行事实
- `database/feedback/` — 与交付对象绑定的反馈
- `database/cognitive_state/` — ChangeSet 与收益快照
- `reports/` — 仪式报告与验收摘要

## 原则

1. 数据只用于「为用户创作」，绝不用于「定义用户」
2. 关系功能必须双向
3. 每次交付必须可解释（inspiration_trace）
4. 慢灵感：拒绝刷屏式推送
