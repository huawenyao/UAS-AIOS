# ACA-protocol / UAS-AIOS

APP AGENT contract，build by tech protocol

## 架构范式：ASUI

**ASUI**（AI-System-UI Integration）以显式知识驱动 AI 与系统执行深度融合：

- **知识驱动**：`CLAUDE.md` + `configs/` 定义业务规则，修改即生效
- **构建即运行**：知识更新后立即可用，无需重型编译部署
- **增量演化**：通过 skills、evolution 回路与 `/evolveApply` 持续扩展

完整理论体系与索引见 [CLAUDE.md](./CLAUDE.md)。

## 项目结构

```
├── CLAUDE.md              # 系统操作手册（AI 自动加载）
├── .claude/               # skills · agents · commands
├── configs/               # 平台级业务规则
├── scripts/               # 校验与运行时工具
├── asui-cli/              # asui init 脚手架
├── projects/              # UAS subapp（标准八元组）
│   ├── ai-recruitment-os/
│   └── enterprise-sales-os/
├── examples/              # ASUI 领域验证（轻量，非全部 subapp）
│   ├── ai-recruitment/
│   ├── selfpaw-cognitive-swarm/
│   └── triadic-ideal-reality-swarm/
├── docs/                  # 理论、企业蓝图、MVP 规约
├── harness/               # reqharness 需求与 invariant
└── database/              # 平台级持久化
```

> 智能客服模板：`asui init <name> -t customer-service`（生成到目标目录，非 `examples/customer-service`）。

## 快速开始

### 1. 安装 asui CLI

```bash
cd asui-cli && pip install -e ".[dev]"
```

### 2. 初始化项目

```bash
asui init my-project
asui init recruitment-demo -t recruitment
asui init cs-demo -t customer-service
```

### 3. 运行验证

```bash
# 平台 invariant
python harness/invariants/run-all.py

# 列出可运行 subapp
python scripts/run_uas_runtime_service.py list

# Enterprise Sales MVP 验收（v0.2 原型）
python projects/enterprise-sales-os/scripts/evaluate_sales_mvp.py
```

### 4. 领域示例

在 Cursor 中打开 `examples/ai-recruitment` 或 `projects/ai-recruitment-os`，按各自 README 执行。

## 文档

| 主题 | 路径 |
|------|------|
| ASUI 架构 | [docs/ASUI_ARCHITECTURE.md](./docs/ASUI_ARCHITECTURE.md) |
| 企业产品蓝图 | [docs/UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md](./docs/UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md) |
| Sales OS MVP 规约 | [docs/enterprise-sales-os/README.md](./docs/enterprise-sales-os/README.md) |
| 治理未闭环追踪 | [docs/GOVERNANCE_REGISTRY.md](./docs/GOVERNANCE_REGISTRY.md) |
| 白皮书 | [whitepaper/ASUI_WHITEPAPER_CN.md](./whitepaper/ASUI_WHITEPAPER_CN.md) |
