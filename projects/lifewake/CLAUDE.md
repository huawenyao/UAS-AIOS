# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 生命回响（LifeWake）

UAS subapp：将「惊喜盲盒」与「心跳音乐」收敛为可审计、可撤回、可演化的情感共创闭环。

- 模块规约包（状态机/能力契约/领域模型/治理矩阵等）：`docs/lifewake/`（本项目内）
- 完整产品 BP：仓库根 `../../docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md`
- 可运行实现摘要：`docs/APP_BLUEPRINT.md`；开发计划：`docs/DEVELOPMENT_PLAN.md`

## 双层架构（最重要的全局图景）

```
docs/lifewake/*.md（规约）──落地为──▶ lifewake/（正式层，v0.3.x）
                                          │
                                          └─ importlib 动态加载 ─▶ scripts/lifewake_policy.py（治理引擎）
scripts/（原型/MVP 层）──行为验收──▶ CASE-001～014 + 价值闭环
prototype/（静态 Demo，无构建）
```

- **`lifewake/` 正式包**：类型化领域模型（`domain.py`，15 实体 + 6 不变量）→ jsonschema 校验（`schemas.py`）→ `lw.*` 能力注册表 + 调用/响应信封 + 幂等 + 审计（`capabilities.py`）→ 状态机编排 intent→closed（`orchestrator.py`）→ 仓储持久化（`store.py`）→ MRCR + M-01~M-18 指标 + 护栏否决（`metrics.py`）→ 真实输入边界（`cli.py`）。
- **关键耦合**：`lifewake/capabilities.py` 通过 importlib 按相对路径替换加载 `scripts/lifewake_policy.py`——两层共享同一治理实现，改治理逻辑只改 scripts 侧这一份。
- **规约即代码**：每个 `lifewake/` 模块 docstring 标注「规约来源：docs/lifewake/XXX.md」。修改行为时须同步对应规约文档。
- **`scripts/` 原型层**：`evaluate_lifewake_mvp.py`（14 CASE 行为验收，`run_lifewake_pipeline.py` 复用其 `run_case`）、`run_value_loop_prototype.py`（7 步价值闭环）、`run_emotion_kpi_snapshot.py`（从运行事实生成 KPI）。
- **`prototype/`**：无构建依赖静态三件套；`cd prototype && python3 -m http.server 8090` 后浏览器打开，默认情景「妻子 · 林妍」。

## 核心不变量（红线，测试会强制）

- 状态机顺序：compose → `impact_checking` → `timing_deciding` → `ritual_rendering`（`orchestrator.py` 的 `TRANSITIONS`/`ORDER`/`TERMINAL`）；consent 撤回可在任意执行态抢占；duet 断连不可静默降级为 solo（红线 17）。
- 数据用途仅 `create_for_user`；`profile_user`/`ads`/`score_user` 一律拒绝。精确 scope、撤回、未成年人监护授权检查在 `lifewake_policy.check_consent`。
- 关系功能必须双向：`pulse_duet` 需双方同意且 `needs_met` 覆盖全部参与者。
- 每次交付必须可解释（`inspiration_trace` + `uniqueness_refs`），wow_score 过门禁才交付。
- 演化反馈只生成 `auto_apply: false` 的 ChangeSet 草案，绝不自动写回。
- 慢灵感：遵守 `max_surprises_per_day`，拒绝刷屏式推送。
- 执行协议速查见 `.claude/skills/lifewake_protocol.md` 与 `output_contract.md`。

## 命令

依赖：Python ≥3.10 标准库 + pytest；`jsonschema` 可选（缺失时回退 `domain.py` dataclass `__post_init__` 不变量，且 dataclass 校验始终叠加执行）。无 pyproject/requirements 文件。测试通过 `sys.path` 注入导入顶层包，**必须从项目根目录运行 pytest**。

```bash
pytest -q                                    # 全部测试（正式层 + 14 CASE + 价值闭环 + 策略红线）
pytest tests/test_formal_layer.py -q         # 仅正式层
pytest tests/test_formal_layer.py -q -k orchestrator   # 跑单个测试

python scripts/evaluate_lifewake_mvp.py      # 行为验收 CASE-001～014
python scripts/run_value_loop_prototype.py --run-id walkthrough_value_loop  # 输入→体验→反馈→演化完整闭环
python scripts/run_emotion_kpi_snapshot.py   # 从运行事实生成情感 KPI

# 真实输入边界（非仅 CASE 夹具；也支持 stdin 管道）
python3 -m lifewake.cli --intent '{"intent_type":"surprise_delivery","consent":{...},"raw_signals":[...]}' --pretty
python3 -m lifewake.cli --metrics --pretty

# 离线流水线单步（UAS runtime 脚本步）
echo '{"topic":"惊喜盲盒","lifewake_case_id":"CASE-001"}' | python3 scripts/run_lifewake_pipeline.py

# 经 UAS runtime 工作流（需要 asui 包；脚本自动向上层目录 bootstrap 路径，环境不支持则跳过）
python scripts/run_subapp.py "生命回响" --evaluate
```

交互命令：`/intent [情感议题]`（归一化惊喜或心跳共鸣意图）、`/design`、`/validate`、`/evolve`（见 `.claude/commands/README.md`）。

意图类型仅接受：`surprise_delivery` / `pulse_solo` / `pulse_duet` / `feedback_review`。

## 知识层（configs/，修改即生效）

| 文件 | 用途 |
|------|------|
| `platform_manifest.json` | UAS 八元组 + `spec_root: docs/lifewake` + 能力依赖/预留清单 |
| `workflow_config.json` | UAS 九步执行链与 Agent 审计 |
| `governance_policy.json` | 隐私用途、wow 门禁、双向关系、consent scope 映射 |
| `swarm_agents.json` | 情感炼金 Agent 编织（Agent 注册表统一在此） |
| `system_registry.json` | `lw.*` 能力与 mock connector |
| `world_model.json` | 情感世界模型五维 |
| `entity_schemas.json` | Person/Consent/Surprise/Pulse 等实体 schema |

## 产物目录（运行事实，勿手工编辑）

- `database/audit/` — 同意与创作审计；`database/runs/` — 价值闭环运行事实
- `database/feedback/` — 与交付对象绑定的反馈；`database/cognitive_state/` — ChangeSet 与收益快照
- `reports/` — 仪式报告（HTML 可直接浏览器打开）与验收摘要

## 产品原则

1. 数据只用于「为用户创作」，绝不用于「定义用户」
2. 关系功能必须双向
3. 每次交付必须可解释（inspiration_trace）
4. 慢灵感：拒绝刷屏式推送
