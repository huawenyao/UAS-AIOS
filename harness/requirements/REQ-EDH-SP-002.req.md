# Requirement: REQ-EDH-SP-002 - 岗位 Domain 自动绑定

## Status: completed (prototype)

## 需求层级: 产品

## 优先级: P0

## Acceptance Criteria

- [x] HR 岗位→Domain 映射配置格式
- [x] 预置岗位包：销售、客服、研发、HR（各含 cs 白名单）
- [x] Runner 启动时加载岗位 Domain 片段进 Prompt
- [x] 与 UAS Domain Builder 技能输出格式对齐

## 映射能力

SP-02 · PL-03

## 验证

`python scripts/validate_domain_binding.py`
