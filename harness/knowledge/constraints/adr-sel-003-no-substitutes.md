# ADR-SEL-003：禁替代清单

## Status
Accepted · 2026-09-09 · harness 回写 2026-09-10

## Context
实施压力会推动「客户已买某套件，用它当中枢」。

## Decision
禁止用下列替代 L0 或 Hub：Palantir AIP、Fabric IQ、Agentforce、Copilot Studio、Dify/Coze/FastGPT 当 OS。  
禁止口径层或知识图谱签发生产写。  
禁止第三套 Agent 循环。  
禁止聊天历史、Lethe、Graphiti 充当经营状态。  
G 层否决权高于「客户已买某套件」；套件只进 S 层 Connector。

## Consequences
- 评审检查清单写入每张 REQ-UAS-M* 的 DoR
- 争议：德压过术
