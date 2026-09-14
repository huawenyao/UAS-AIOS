# M6 Capability Hub · 本产品门面

完整定位见 [`../modules/control/M06-capability-hub/SPEC.md`](../modules/control/M06-capability-hub/SPEC.md)。

本目录是 WorkStudio 的 Hub 进程入口，内核复用 `services/hub-api`，禁止再写一套 PolicyChain。

```bash
python projects/aios-workstudio/CapabilityHub/run.py
python -m unittest discover -s projects/aios-workstudio/CapabilityHub/tests -v
```
