# Requirement: REQ-EDH-PP-001 - World Model Studio 最小闭环

## Status: completed

## 需求层级: 产品

## 优先级: P0

## 废止说明

原验收「客服岗位 Agent 标杆 / Task Panel / ΠPaw Demo」已废止。见 `docs/WORLD_MODEL_PRODUCT.md` §废止。

## Acceptance Criteria

- [x] 五维世界模型结构化知识文件（招聘短名单情景）
- [x] 7 步状态机每步读写世界模型
- [x] UI 可见对冲、门禁、证据、ChangeSet
- [x] `python scripts/run_cognitive_cycle.py` 落盘审计
- [x] 对照宪章 §7 书面检核

## 映射能力

PP-01 · 器层从数字人改为世界模型 OS

## 交付物

| 类型 | 路径 |
|------|------|
| 产品定义 | `docs/WORLD_MODEL_PRODUCT.md` |
| 原型 | `examples/world-model-studio/` |
| 脚本 | `scripts/run_cognitive_cycle.py` |

## 验证

```bash
python scripts/run_cognitive_cycle.py
python harness/invariants/run-all.py
```
