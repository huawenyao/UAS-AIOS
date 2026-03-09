# 工单规则

## 分类标准

| 意图 | 分配组 | 优先级 |
|------|--------|--------|
| technical | 技术组 | P1 |
| refund | 客服主管 | P0 |
| complaint | 升级处理 | P0 |
| product_inquiry | 客服组 | P2 |

## 响应时效

- P0: 15 分钟
- P1: 1 小时
- P2: 4 小时

## 工单字段

- ticket_id
- user_input
- intent
- assigned_to
- priority
- created_at
