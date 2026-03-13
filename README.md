# ACA-protocol / UAS-AIOS

APP AGENT contract，build by tech protocol

## 架构范式：ASUI × UAS-AIOS

本项目采用 **ASUI**（AI-System-UI Integration）架构范式，并扩展为 **UAS-AIOS** 完整体系：

- **知识驱动**：CLAUDE.md + configs 定义业务规则，修改即生效
- **构建即运行**：无需编译/部署，知识更新后立即可用
- **增量演化**：通过添加知识文件持续扩展系统能力

## 项目结构

```
├── CLAUDE.md          # 系统操作手册（AI 自动加载）
├── .claude/
│   ├── skills/        # 功能模块知识
│   ├── agents/        # 场景化 Agent 配置
│   └── commands/      # 交互命令定义
├── configs/           # 业务规则配置
├── scripts/           # 执行工具脚本
├── database/          # 数据持久化（含 knowledge_index.json）
├── docs/              # 统一文档中心
│   ├── architecture/  # 架构文档
│   ├── strategy/      # 战略与范式
│   └── whitepaper/    # 白皮书
├── assets/            # 产品与对外材料
├── schemas/           # JSON Schema 定义
├── asui-cli/          # asui init 脚手架
└── examples/          # 领域验证项目
```

## 文档索引

- [文档中心](docs/README.md) - 完整文档索引
- [UAS-AIOS 架构](docs/architecture/UAS_AIOS_ARCHITECTURE.md)
- [ASUI 架构理论](docs/architecture/ASUI_ARCHITECTURE.md)
- [认知空间定义](docs/COGNITIVE_SPACE.md)
- [ASUI 白皮书](docs/whitepaper/ASUI_WHITEPAPER_CN.md)

## 认知空间与索引

- **认知空间**：用户认知、系统认知、Agent 认知、协议认知（见 [docs/COGNITIVE_SPACE.md](docs/COGNITIVE_SPACE.md)）
- **知识索引**：`python scripts/build_knowledge_index.py` 构建
- **索引查询**：`python scripts/query_index.py [--entity TYPE | --refs ID | --deps ID]`

## 快速开始

### 1. 安装 asui 脚手架

```bash
cd asui-cli && pip install -e .
```

### 2. 初始化项目

```bash
asui init my-project
asui init customer-service-demo -t customer-service
asui init recruitment-demo -t recruitment
```

### 3. 蜂群决策

```
/swarmDecision [决策议题]
```

### 4. 构建知识索引

```bash
python scripts/build_knowledge_index.py
```
