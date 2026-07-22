---
name: lifewake-output-contract
description: 生命回响运行输出契约，确保报告可审计、可验收
---

# LifeWake 输出契约

每次运行 JSON 至少包含：

```json
{
  "intent": {"intent_id": "", "intent_type": "", "risk_level": "", "actor": ""},
  "consent": {},
  "audit": [],
  "report": {"conclusion": "", "next_step": ""},
  "world_model_view": {
    "subjects": [],
    "objects": [],
    "drive": [],
    "blockers": [],
    "connectors": []
  },
  "state": {"final": ""},
  "errors": []
}
```

成功创作时额外包含 `artifact` 与 `ritual.emotion_impact`。  
反馈用例额外包含 `changeset.auto_apply = false`。
