# Enterprise Sales OS

## 概述

UAS subapp：B2B 线索资格判断、报价草案、折扣审批与审计链。规约包在 `docs/enterprise-sales-os/`。

## 命令

- `/intent [线索议题]` — 归一化销售意图
- `python scripts/run_subapp.py "B2B线索报价" --evaluate --sales-case-id CASE-001` — UAS runtime 端到端
- `python scripts/evaluate_sales_mvp.py` — MVP 验收 CASE-001～008（离线脚本）

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/platform_manifest.json` | UAS 八元组清单 |
| `configs/workflow_config.json` | 销售闭环工作流 |
| `configs/governance_policy.json` | G1–G7 治理 |
| `configs/evolution_policy.json` | 演化与 ChangeSet 策略 |
| `configs/system_registry.json` | cs.* 能力依赖 |
| `configs/world_model.json` | 企业 WM 五维 + 镜像/透镜/熔炉 |

## 产物

- `database/audit/` — 审计事件
- `reports/` — 验收与运行报告
