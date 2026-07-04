# SelfPaw Enterprise（User AGI · L1）

员工数字分身原型：组织身份 → 岗位 Domain → 可选升级 ΠPaw。

## 运行

```bash
python scripts/run_uas_runtime_service.py run --app-id selfpaw-enterprise --topic "Q2 大客户攻坚"
python ../../scripts/run_edh_dual_track_loop.py
```

## 能力

- SP-001 组织身份：`org_identity` + `tenant_catalog`
- SP-002 岗位 Domain：`role_domain_bindings.json`
- SP-003 升级 ΠPaw：见仓库根 `intent_hub`
