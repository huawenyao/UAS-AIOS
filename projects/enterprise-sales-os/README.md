# Enterprise Sales OS（UAS SubApp v0.2）

B2B 线索 → 报价 → 审批 MVP 可运行原型。开发规约见 [docs/enterprise-sales-os/README.md](../../docs/enterprise-sales-os/README.md)。

## 验证

```bash
python scripts/evaluate_sales_mvp.py
python scripts/run_subapp.py "B2B线索报价" --evaluate --sales-case-id CASE-001
python ../../scripts/run_uas_runtime_service.py run --app-id enterprise-sales-os --topic "B2B线索" --evaluate
```

## 状态

- **v0.3**：CASE-001～008 脚本验收（`evaluate_sales_mvp.py`）
- **open**：runtime 端到端 + 真 CRM 连接器
