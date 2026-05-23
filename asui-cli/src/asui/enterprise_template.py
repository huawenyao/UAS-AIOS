"""
UAS-AIOS 企业级 Agent 生态体系模板
包含完整的 L1/L2/L3 数字人体系 + cs.* 服务层 + 数据平面 + 产品化封装
"""

ENTERPRISE_TEMPLATE = {
    "CLAUDE.md": """# UAS-AIOS 企业级 Agent 生态体系

## 系统定位

本项目是基于 UAS-AIOS 体系的**企业级 Agent 生态**，覆盖 L1（个人数字分身）→ L2（职能数字人）→ L3（经营数字人）三层架构。

## 第一性方法论：道德势术器

| 层次 | 映射 | 工程实现 |
|------|------|----------|
| 道（Tao）| 企业主权数据平面 | data_plane/ |
| 德（De） | 业务能力服务化 cs.* | platform/capability_services/ |
| 势（Shi）| 双轨 AGI（SelfPaw × ΠPaw）| agents/l1_selfpaw + l2/l3_pipaw |
| 术（Shu）| 三层数字人架构 | agents/ |
| 器（Qi） | 产品化封装 | domain_packages/ + workflow_templates/ |

## 三层数字人体系

```
L3 经营数字人（对外）
  → 销售顾问 · 客服 · 投标 · 渠道
  → ΠPaw：获 · 转 · 服 · 续

L2 职能数字人（对内跨部门）
  → 招聘 · 财务 · 合规 · 调度
  → ΠPaw 工作台

L1 个人数字分身（对内个人）
  → 第二大脑 · 任务代理 · 向上汇总
  → SelfPaw 企业版
```

## 平台 + 模型分层

```
模型层：通用 LLM + 领域模型
    ↓
平台层（UAS）：
  · Agent 平台（cs.* 语义服务 · 审批 · 治理 · 演化）
  · 数字基础能力（流程 · 表单 · 权限 · 数据）
  · 业务连接器 S-Grid（CRM / BPM / 财务 / ERP）
    ↓
数据平面：租户 · 主数据 · 事件流 · 审计链
```

## 核心原则

- **Agent 不直连 CRM/BPM**，只调用语义能力服务 cs.*
- **平台负责**：权限校验 + 语义翻译 + 审计记录 + 重试
- **模型负责**：理解与生成；**确定性引擎**负责：执行与合规

## 目录结构

```
.
├── configs/
│   ├── platform_manifest.json    # UAS Platform 八元组
│   ├── tenant_config.json        # 租户配置
│   └── agent_positions.json      # 数字岗位编制
├── platform/
│   ├── capability_services/      # cs.* 语义服务层
│   ├── data_plane/               # 数据平面
│   └── governance/               # 治理层
├── agents/
│   ├── l1_selfpaw/               # 个人数字分身
│   ├── l2_pipaw/                 # 职能数字人
│   └── l3_pipaw/                 # 经营数字人
├── domain_packages/              # 行业 Domain 包
├── workflow_templates/           # 流程模板
├── scripts/
│   ├── run_enterprise_platform.py  # 平台启动
│   └── demo_b2b_pipeline.py       # B2B 端到端演示
└── docs/
    └── ENTERPRISE_ARCHITECTURE.md  # 架构文档
```

## 快速启动

```bash
# 运行 B2B 端到端演示
python3 scripts/demo_b2b_pipeline.py

# 启动企业平台
python3 scripts/run_enterprise_platform.py
```

## 核心命令

- `/start_pipeline` — 启动 B2B 销售管道
- `/deploy_agent <l1|l2|l3> <position>` — 部署数字人
- `/cs_call <service> <action>` — 测试 cs.* 服务调用
- `/audit_report` — 生成合规审计报告
- `/evolve_apply` — 应用 ChangeSet 演化
""",

    "configs/platform_manifest.json": """{
  "name": "enterprise-uas-platform",
  "version": "1.0.0",
  "description": "企业级 UAS-AIOS Agent 生态平台",
  "uas_definition": {
    "I": "企业经营意图驱动（获客 · 转化 · 履约 · 续费）",
    "K": "行业 Domain 包 + 业务规则 + 审批矩阵",
    "R": "cs.* 语义服务运行时 + 确定性流程引擎",
    "A": "三层数字人（L1 SelfPaw + L2/L3 ΠPaw）",
    "S": "S-Grid 业务连接器（CRM / BPM / 财务 / ERP）",
    "G": "权限引擎 + 合规规则 + 审计链 + SLA 监控",
    "E": "ChangeSet 演化 + KPI 归因反馈回路",
    "Pi": "cs.* 语义协议栈 + 事件流协议"
  },
  "digital_positions": {
    "l1": ["sales_ae", "csm", "hr_bp", "finance", "developer"],
    "l2": ["hr_agent", "finance_agent", "compliance_agent", "ops_agent"],
    "l3": ["sales_agent", "customer_service_agent", "bidding_agent"]
  },
  "capability_services": [
    "cs.customer", "cs.approval", "cs.invoice", "cs.finance", "cs.bpm"
  ],
  "enabled_modules": ["l1_selfpaw", "l2_pipaw", "l3_pipaw", "audit", "governance", "evolution"]
}
""",

    "configs/tenant_config.json": """{
  "tenant_id": "TENANT_001",
  "name": "示例企业",
  "industry": "B2B SaaS",
  "tier": "enterprise",
  "data_region": "cn-north",
  "sso_provider": "azure_ad",
  "enabled_domain_packages": ["b2b_saas"],
  "custom_approval_matrix": {
    "quote_auto_approve_under": 10000,
    "discount_auto_approve_under_pct": 5
  }
}
""",

    "configs/agent_positions.json": """{
  "l1_positions": [
    {"position": "sales_ae", "domain_packages": ["sales_ontology", "b2b_saas"], "cs_whitelist": ["cs.customer.qualify_lead", "cs.finance.create_quote"]},
    {"position": "csm", "domain_packages": ["customer_success_ontology", "b2b_saas"], "cs_whitelist": ["cs.customer.health_score", "cs.invoice.ar_summary"]},
    {"position": "hr_bp", "domain_packages": ["hr_ontology"], "cs_whitelist": ["cs.bpm.start", "cs.approval.create"]},
    {"position": "finance", "domain_packages": ["finance_ontology"], "cs_whitelist": ["cs.invoice.*", "cs.finance.*"]}
  ],
  "l2_positions": [
    {"agent_id": "l2_hr_agent", "type": "hr", "kpi": ["time_to_hire", "headcount"], "sla_hours": 4},
    {"agent_id": "l2_finance_agent", "type": "finance", "kpi": ["dso", "invoice_accuracy"], "sla_hours": 2},
    {"agent_id": "l2_compliance_agent", "type": "compliance", "kpi": ["compliance_pass_rate"], "sla_hours": 2}
  ],
  "l3_positions": [
    {"agent_id": "l3_sales_agent", "type": "sales", "kpi": ["arr_new", "win_rate", "sales_cycle"], "sla_hours": 72},
    {"agent_id": "l3_cs_agent", "type": "customer_service", "kpi": ["nrr", "nps", "churn_rate"], "sla_hours": 4},
    {"agent_id": "l3_bidding_agent", "type": "bidding", "kpi": ["bid_win_rate", "compliance_rate"], "sla_hours": 48}
  ]
}
""",

    "scripts/run_enterprise_platform.py": """#!/usr/bin/env python3
\"\"\"企业平台启动脚本\"\"\"
import sys
import json
from pathlib import Path

def main():
    print("UAS-AIOS 企业级 Agent 平台")
    print("="*40)

    # 加载配置
    manifest_path = Path("configs/platform_manifest.json")
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"平台: {manifest.get('name', 'N/A')} v{manifest.get('version', 'N/A')}")
        print(f"描述: {manifest.get('description', '')}")

        positions = manifest.get("digital_positions", {})
        print(f"\\n数字岗位编制:")
        for level, pos_list in positions.items():
            print(f"  {level.upper()}: {', '.join(pos_list)}")

        services = manifest.get("capability_services", [])
        print(f"\\n能力服务层 (cs.*):")
        for svc in services:
            print(f"  ✓ {svc}")

    print("\\n平台已就绪。运行 demo_b2b_pipeline.py 查看端到端演示。")

if __name__ == "__main__":
    main()
""",

    "scripts/demo_b2b_pipeline.py": """#!/usr/bin/env python3
\"\"\"B2B 端到端管道演示（从企业项目根目录运行）\"\"\"
import subprocess
import sys
from pathlib import Path

# 寻找 enterprise 模块路径
enterprise_root = Path(__file__).parent.parent

if (enterprise_root / "enterprise" / "__init__.py").exists():
    sys.path.insert(0, str(enterprise_root))
    from enterprise.examples.b2b_lead_to_payment.scripts.b2b_pipeline import run_b2b_pipeline
    run_b2b_pipeline()
else:
    print("提示：将此脚本复制到 UAS-AIOS 仓库根目录后运行")
    print("或参考：enterprise/examples/b2b_lead_to_payment/scripts/b2b_pipeline.py")
""",

    "docs/ENTERPRISE_ARCHITECTURE.md": """# 企业级 Agent 生态架构

## 1. 总体架构

### 1.1 三层数字人体系

```
┌─────────────────────────────────────────────────────────────────┐
│  L3 经营数字人（ΠPaw 对外）                                      │
│  销售顾问 · 客服/履约 · 投标/合规 · 渠道伙伴                      │
│  经营向外：获（Acquire）· 转（Convert）· 服（Serve）· 续（Retain）│
└─────────────────────────────────────────────────────────────────┘
                            ↑ 调度与资源分配
┌─────────────────────────────────────────────────────────────────┐
│  L2 职能数字人（ΠPaw 工作台）                                    │
│  HR · 财务 · 合规 · 调度                                         │
│  接收 L1 升级 + 向 L3 提供支撑                                   │
└─────────────────────────────────────────────────────────────────┘
                            ↑ 意图单 + Evidence
┌─────────────────────────────────────────────────────────────────┐
│  L1 个人数字分身（SelfPaw 企业版）                               │
│  第二大脑 · 任务代理 · 向上汇总                                   │
│  对内：写 · 查 · 办 · 汇                                         │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 cs.* 语义服务层

```
Agent 调用（语义接口）
         ↓
cs.* 语义能力服务网关
  ├── 权限校验（RBAC + ABAC）
  ├── 语义翻译
  ├── 审计记录
  └── 自动重试
         ↓
后端适配器
  ├── cs.customer → CRM（Salesforce / HubSpot / 自研）
  ├── cs.approval → BPM 审批引擎
  ├── cs.invoice  → 财务系统
  ├── cs.finance  → 报价/收入确认
  └── cs.bpm      → 流程引擎（Camunda / Activiti）
```

### 1.3 数据平面

```
租户管理 → 数据隔离 → 岗位绑定 → SSO 会话
                    ↓
事件流（DomainEvent）
  lead.qualified → quote.approved → payment.received → ...
                    ↓
审计链（不可篡改）
  所有 cs.* 调用 → SHA-256 校验 → 合规报告
```

## 2. 端到端 B2B 示例

```
官网留资
  → L3 销售顾问.handle_inbound()
  → cs.customer.qualify_lead（BANT+ICP）
  → L1 SelfPaw.process_intent（意图识别）
  → L3 销售顾问.diagnose_needs（需求诊断）
  → L3 销售顾问.create_quote（报价生成）
  → L2 合规数字人.compliance_check（G6 合规审查）
  → cs.approval.create（审批路由）
  → cs.approval.approve（L3 审批）
  → L3 销售顾问.close_won（赢单+触发履约）
  → L2 财务数字人.process_invoice（开票）
  → L2 财务数字人.collect_payment（回款）
  → cs.finance.kpi_attribution（KPI归因）
  → ChangeSet 演化（业务进化）
```

## 3. SelfPaw 企业版六大能力

| # | 能力 | 实现 |
|---|------|------|
| 1 | 组织身份绑定 | SSO + 租户 + 岗位 + 数据 scope |
| 2 | Intent Hub | 意图识别；经营类升级 ΠPaw |
| 3 | 岗位 Domain 包 | Ontology + 可用 cs.* 白名单 |
| 4 | 授权内执行 | 填表 / 发起流程 / 代拟邮件 |
| 5 | 个人蜂群决策 | 五视角 → 可审计决策备忘录 |
| 6 | 向上汇总 | 周报摘要 / SLA 异常 → ΠPaw Task |

## 4. 产品化封装单元

| 封装单元 | 适配方式 |
|---------|---------|
| 行业 Domain 包 | 切换行业 = 切换 Ontology + 合规 + 话术 |
| 流程模板包 | 参数化 BPM + Agent 绑定 + SLA |
| 能力连接器包 | CRM/BPM/财务 endpoint + 字段映射 |
| 法则包 | 定价/信用/审批矩阵热更新 |
| 岗位 Agent 包 | Prompt + 工具白名单 + KPI |
""",

    "domain_packages/README.md": """# 行业 Domain 包

行业 Domain 包是 UAS-AIOS 灵活适配的核心机制。
**切换行业 = 切换 Ontology + 合规规则 + 业务话术**

## 已有包

- `b2b_saas/` — B2B SaaS 行业（实体 + 合规 + 审批矩阵 + KPI）

## 创建新包

1. 复制 `b2b_saas/` 目录结构
2. 修改 `domain_config.json`：实体定义 / 合规规则 / 审批矩阵
3. 在 `tenant_config.json` 的 `enabled_domain_packages` 中引用
""",
}
