# Hub

```
python scripts/validate_uas_aios_phase_a.py
python scripts/run_hub_api.py
```

HTTP 只暴露 `/hub/v1`（另有 `/health`）。剖面由路径强制，body.profile 作废。包同一 `Hub.from_repo()`。

`POST /hub/v1/exec/open` 启动外环（实验室 `InMemoryOuterLoop`，Workflow 名 `RuntimeCycleWorkflow`）。一线 Demo 不展示 workflow_id。

作战台 Demo 默认打 `http://127.0.0.1:18088`；Hub 未起时回退夹具。8088 已被本机其他控制台占用，故不用。
