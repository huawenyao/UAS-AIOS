# SystemConnector 规格与密钥分区（Phase-0）

> 实现：`asui-cli/src/asui/connectors/` · 配置：`configs/connectors.json`

## 适配器接口

```python
class SystemConnector(ABC):
    def invoke(
        self,
        operation: str,       # 语义操作名，如 qualify_lead
        payload: dict,
        ctx: InvokeContext,   # tenant_id, user_id, role_ids, product_track
    ) -> InvokeResult:
        ...
```

统一入口：`CapabilityServiceRouter.invoke(operation_ref, payload, ctx)`  
其中 `operation_ref = cs.{service}.{operation}`。

## Phase-0 连接器

| connector_id | 类型 | 实现 | 服务 |
|--------------|------|------|------|
| connector.crm.sandbox | crm | mock | cs.customer, cs.lead |
| connector.oa.sandbox | oa | mock | cs.approval, cs.notify |
| connector.itsm.sandbox | itsm | mock | cs.ticket |
| connector.bpm.sandbox | bpm | mock | cs.process |

## 密钥分区

- 配置中 **仅** 使用 `secret_ref`，禁止明文密钥写入 git。  
- 约定前缀：  
  - `env:EDH_CRM_MOCK_KEY` — 进程环境变量  
  - `file:.secret/crm.json` — 工作区外或 gitignore 目录（Phase-1）  
- Mock 实现不读取真实密钥；HTTP/SDK 实现须从 `secret_ref` 解析。

## CLI

```bash
python scripts/validate_connectors.py validate
python scripts/invoke_capability.py cs.lead.qualify_lead --payload-json "{\"lead_id\":\"L-1001\"}"
cd asui-cli && python -m pytest tests/test_edh_connectors.py -v
```

## 调用链

```
Agent Tool (capability_invoke)
  → CapabilityServiceRouter
    → RBAC 校验（enterprise_rbac_template.json）
    → SystemConnector.invoke
      → mock_crm / mock_oa / ...
```
