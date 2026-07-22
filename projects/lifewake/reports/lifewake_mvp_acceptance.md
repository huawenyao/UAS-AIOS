# LifeWake MVP 14 CASE 验收报告

- 通过: 14/14
- 失败: 无

- `CASE-001` 正常惊喜: PASS → `delivered`
- `CASE-002` 无同意: PASS → `consent_required`
- `CASE-003` 撤回: PASS → `consent_revoked`
- `CASE-004` solo: PASS → `delivered`
- `CASE-005` duet: PASS → `delivered`
- `CASE-006` 非双向: PASS → `bond_blocked`
- `CASE-007` connector recovery: PASS → `delivered`
- `CASE-008` 低 wow: PASS → `emotion_impact_failed`
- `CASE-009` 慢灵感 defer: PASS → `deferred`
- `CASE-010` 共享撤回: PASS → `delivered`
- `CASE-011` 交付→反馈→changeset 串联: PASS → `delivered`
- `CASE-012` 未成年人: PASS → `minor_blocked`
- `CASE-013` 设备断连: PASS → `device_not_linked`
- `CASE-014` 违规 purpose: PASS → `policy_denied`
