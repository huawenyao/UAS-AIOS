# 语义操作层参考场景

库存补货 Agent 的 SIO-MMOS/DIKW 最小闭环：

- 规格：`replenishment_sio.json`
- 编译器：`../../scripts/semantic_operation_layer.py`
- 契约：`../../schemas/semantic_operation.schema.json`
- 调研：`../../docs/strategic/SIO_MMOS_DIKW_Agent_World_Model_And_Semantic_Operation_Layer.md`

```bash
python3 scripts/awm_demo_loop.py
python3 scripts/semantic_operation_layer.py
python3 scripts/awm_scenario_matcher.py --brief examples/semantic-operation-layer/briefs/replenishment_brief.json
python3 -m pytest examples/semantic-operation-layer -v
# Demo UI: cd website && python3 -m http.server 8080  → http://127.0.0.1:8080/awm-demo/
```
