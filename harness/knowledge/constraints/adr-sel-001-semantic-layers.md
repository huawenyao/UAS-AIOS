# ADR-SEL-001：语义分层

## Status
Accepted · 2026-09-09 · harness 回写 2026-09-10

## Context
市场把口径语义层、经营本体、时态图谱、Agent 控制面说成同一件事。选错层会买成别人的 OS。

## Decision
1. **L0 自有**：责任图 + 五维 WM + Law Pack（永不外包）  
2. **L1 采购**：Cube Core + OSI/MetricFlow YAML  
3. **L2 采购**：Graphiti（时态运行时）；Utopia 仅 Spike，默认不进写路径  
4. **L3 采购**：Lethe / pylethe，分库  
5. 禁止 Palantir / Fabric IQ / 仓 Semantic View 当经营内核；禁止 Dify 知识库当 L2

## Consequences
- Hub 经 `cs.metric.query` / `hub.kg.*` / `hub.memory.self.*` 访问零件
- 零件可换，一线名词不换
- 落地：`docs/strategic/design/SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md`
