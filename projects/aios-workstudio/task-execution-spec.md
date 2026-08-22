# 任务执行规格 · WorkStudio × Capability Hub 详细设计

> Phase 0 · loop-thinking-enhanced · 2026-08-22  
> 项目：`projects/aios-workstudio`  
> 模式：A · SIO-MMOS 深度分析（用户已调用 `/loop-thinking-enhanced`）

---

## 任务

把 T0 的「用户前台 / 能力后台」展开为可执行详细设计：WorkStudio 三种产品场景 + Capability Hub 中枢，并与 spec harness / 宪章 / ADR 对齐。

## 场景

- **类型**：系统设计（战略规划 × 软件架构）
- **载体**：Markdown 设计文档（本目录）
- **领域**：software_architecture + strategic_planning + competitive_analysis
- **受益者**：岗位主体、员工 Copilot、平台构建者
- **成功标准**：三场景有对象、门禁、输入输出契约；Hub 有策略剖面；与 ADR-001/002、reqharness、subapp 生产协议无断裂；T0 不变式不被违反

## 清晰度

约 82%。三场景由用户给定。未签字项：T0 价值流仍默认招聘短名单（作 Runtime 首个 App，不阻塞三场景设计）。

## 工具链

1. 读取 T0 / 宪章 / ADR / subapp 协议 / RBAC / cs.* 目录（已完成）
2. SIO-MMOS 五维分析 → `deep-analysis.md`
3. 事实清单 → `information-collected.md`
4. 详细设计 → `T1-WorkStudio详细设计.md` · `T1-CapabilityHub详细设计.md`
5. 回写 T0 产品结构

## 下钻点

| ID | 点 | 优先级 | 处理 |
|----|----|--------|------|
| D1 | 三场景与价值闭环 7 步的映射 | CRITICAL | 设计主轴 |
| D2 | Explore 如何「不限已有 Skill」仍可治理 | CRITICAL | Hub 策略剖面 + 产物契约 |
| D3 | Builder 与 reqharness / subapp 协议对齐 | CRITICAL | 阶段门禁表 |
| D4 | Runtime 与租户/RBAC/cs.* 对齐 | CRITICAL | 复用已有规格，不另起权限模型 |
| D5 | 三场景对象如何流转 | HIGH | ThemePack → Blueprint → Instance |
| D6 | 与 WorkBuddy 工作台差异 | HIGH | 品类句落地为场景结构 |

## 质量标准

- 准确性：引用仓库已有协议，禁止平行发明权限/能力模型
- 完整性：每场景有入口、对象、禁止项、产出、Hub 依赖
- 可执行：72 小时可开始做的接口与目录约定
- 宪章：过得了道-1…6 与 T0 八条不变式
