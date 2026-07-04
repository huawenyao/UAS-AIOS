# SelfPaw（User AGI）参考实现锚点

> **权威实现仓库**（本机路径）：`C:\Users\ranwu\XiaomiCloud\aipos\copaw-src`  
> **相对路径**（自 UAS-AIOS 根目录）：`../aipos/copaw-src`  
> **last_review**: 2026-06-04

---

## 边界说明（必读）

| 范围 | 仓库 | 职责 |
|------|------|------|
| **SelfPaw 产品实现** | `aipos/copaw-src` | User AGI（UAS-U）：个人助理、记忆、Skills、Domain/Project、AEE、多端通道、Console |
| **UAS-AIOS 本仓库** | `UAS-AIOS` | UAS 内核、ΠPaw（Business AGI）、企业数据平面、`cs.*`、Intent 升级契约、subapp 样板 |
| **企业版桥接** | `projects/selfpaw-enterprise` + `asui-cli/.../org_identity.py` | 租户/岗位 Domain、升级 ΠPaw；**不重复实现** copaw-src 已有能力 |

**结论**：SelfPaw **已实现**，不在 UAS-AIOS 内从零建设 U 层；UAS-AIOS 负责与 ΠPaw 及企业治理的**集成与契约**。

---

## copaw-src 关键模块映射

| UAS 概念 | copaw-src 路径 |
|----------|----------------|
| AEE / RuntimeContext | `src/selfpaw/aee/`（含 `runtime_context.py`、`intent.py`） |
| Domain 认知包 | `src/selfpaw/domains/` |
| Project 容器 | `src/selfpaw/projects/` |
| 记忆服务 | `src/selfpaw/memory/` |
| 世界模型认知 | `src/selfpaw/world_model_cognition/` |
| Console / API | `src/selfpaw/app/`、`src/selfpaw/console/` |
| CLI | `src/selfpaw/cli/` |
| 架构权威说明 | `docs/SelfPaw-架构权威说明.md`（若存在） |

---

## 与 UAS-AIOS 的集成点

1. **Intent 升级 ΠPaw**：`asui-cli/src/asui/intent_hub.py` ← 企业员工从 SelfPaw 侧提交经营类意图  
2. **实体图谱**：`harness/entity-map.json` 中 `aipos_mapping` 指向 copaw-src  
3. **战略对齐**：`docs/strategic/UAS_AIPOS_SelfPaw_Integrated_Product_Tech_Architecture.md`  
4. **设计详设**：`docs/strategic/detailed-design/SelfPaw_Personal_Cognitive_OS_Detailed_Design.md`

---

## 开发时如何选用

- 改 **个人助理、记忆、Skills、通道** → 在 `copaw-src` 开发  
- 改 **企业租户、cs.\*、ΠPaw 岗位、销售/客服闭环** → 在 `UAS-AIOS` 开发  
- 改 **L1 企业身份 + 升级协议** → UAS-AIOS `org_identity` / `intent_hub` + copaw-src 会话上下文对齐

---

## 验证 copaw-src 可达

```powershell
Test-Path C:\Users\ranwu\XiaomiCloud\aipos\copaw-src\src\selfpaw\aee\runtime_context.py
```

Harness：`python harness/invariants/run-all.py` 含 `selfpaw_reference_repo` 检查。
