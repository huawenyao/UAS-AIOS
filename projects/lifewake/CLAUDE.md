# 生命回响（LifeWake）

## 概述

UAS subapp：将「惊喜盲盒」与「心跳音乐」收敛为可审计、可撤回、可演化的情感共创闭环。规约包在仓库根目录 `docs/lifewake/`。

## 命令

- `/intent [情感议题]` — 归一化惊喜或心跳共鸣意图
- `python scripts/evaluate_lifewake_mvp.py` — MVP 验收 CASE-001～008
- `python scripts/run_subapp.py "生命回响" --evaluate` — 经 UAS runtime 工作流（若环境支持 LLM 步）

离线流水线单步：

```bash
echo '{"topic":"惊喜盲盒","lifewake_case_id":"CASE-001"}' | python3 scripts/run_lifewake_pipeline.py
```

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/platform_manifest.json` | UAS 八元组 + `spec_root: docs/lifewake` |
| `configs/workflow_config.json` | 同意 → 创作 → 仪式报告 |
| `configs/governance_policy.json` | 隐私用途、wow 门禁、双向关系 |
| `configs/swarm_agents.json` | 情感炼金 Agent 编织 |
| `configs/system_registry.json` | `lw.*` 能力与 mock connector |
| `configs/world_model.json` | 情感世界模型五维 |
| `configs/entity_schemas.json` | Person/Consent/Surprise/Pulse 等 |

## 产物

- `database/audit/` — 同意与创作审计
- `reports/` — 仪式报告与验收摘要

## 原则

1. 数据只用于「为用户创作」，绝不用于「定义用户」
2. 关系功能必须双向
3. 每次交付必须可解释（inspiration_trace）
4. 慢灵感：拒绝刷屏式推送
