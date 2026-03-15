# 模板与项目的关系：从运行逻辑推导的最佳设计

> 从实际运行逻辑和应用创建过程出发，整理推导模板（Template）与项目（Project/Sub App）的关系，并给出最佳设计实现。

---

## 一、实际运行逻辑梳理

### 1.1 应用创建过程（Creation）

```
create_sub_uas_app.py [app_name] --target-root [target] --template [template_id]
        │
        ├─ project_path = workspace_root / target_root / app_name
        │   例: /workspace/projects/ai-recruitment
        │
        └─ run_init(project_path, template, force)
                │
                ├─ template_content = get_template(template)
                │   → 返回 dict: { "CLAUDE.md": "...", "configs/workflow_config.json": "...", ... }
                │
                └─ for (file_path, content) in template_content:
                        target = project_path / file_path
                        target.write_text(content)   # 逐文件写入磁盘
```

**结论**：模板 = 内存中的「路径→内容」映射；创建 = 将该映射逐文件写入目标目录。

### 1.2 应用发现与运行（Runtime）

```
run_uas_runtime_service.py [command] --projects-root [root] --app-id [id]
        │
        ├─ UASRuntimeService(workspace_root, projects_root)
        │
        ├─ discover_apps():
        │   glob(projects_root / "*/configs/platform_manifest.json")
        │   → 每个匹配的目录 = 一个 sub app
        │   → app_id = 目录名, app_root = 目录路径
        │
        ├─ get_runtime(app_id) → RuntimeManager(app_root)
        │
        └─ runtime.run(topic):
                context = context_injector.inject(app_root, topic)
                → 从 app_root 读取: configs/*.json, .claude/skills/*.md, docs/*.md
                workflow = context["configs"]["workflow_config"]
                for step in workflow["steps"]:
                    execute(step)  # llm 或 script，script 路径相对于 app_root
```

**结论**：运行时只依赖 `app_root` 下的文件；**不读取模板**，**不感知模板存在**。

### 1.3 关键发现

| 维度 | 创建阶段 | 运行阶段 |
|------|----------|----------|
| 输入 | template_id, app_name, target_root | app_id, projects_root |
| 数据来源 | 模板（内存 dict） | 项目目录（磁盘） |
| 模板作用 | 提供初始文件集 | **无** |
| 项目作用 | 写入目标 | 唯一数据源 |
| target_root / projects_root | 同一概念：sub app 的父目录 | 同一概念 |

---

## 二、关系推导

### 2.1 形式化定义

```
Template  := dict[RelativePath, Content]   # 路径→内容的映射
Project   := Directory                    # 满足 UAS 标准结构的目录
Creation  := (Template × ProjectPath) → Project
Runtime   := Project → Execution
```

### 2.2 关系图

```
                    ┌─────────────────────────────────────┐
                    │  Template（模板）                     │
                    │  - 存在于 asui-cli 代码中            │
                    │  - 无持久化，仅创建时使用             │
                    │  - 例: uas-subapp, selfpaw-swarm     │
                    └─────────────────────────────────────┘
                                        │
                                        │ Creation（创建）
                                        │ run_init(project_path, template)
                                        │ 逐文件写入
                                        ▼
                    ┌─────────────────────────────────────┐
                    │  Project（项目 / Sub App）            │
                    │  - 磁盘目录，如 projects/xxx/         │
                    │  - 含 platform_manifest.json 等      │
                    │  - 创建后与模板无链接                │
                    └─────────────────────────────────────┘
                                        │
                                        │ Runtime（运行）
                                        │ discover → RuntimeManager
                                        │ 只读 project，不读 template
                                        ▼
                    ┌─────────────────────────────────────┐
                    │  Execution（执行）                   │
                    │  - workflow_config 驱动              │
                    │  - 脚本、LLM 调用                    │
                    └─────────────────────────────────────┘
```

### 2.3 核心关系

| 关系 | 说明 |
|------|------|
| **Template → Project** | 一对多。一个模板可创建多个项目。 |
| **Project → Template** | 创建时多对一；创建后**无持久关联**。项目不存储「来自哪个模板」。 |
| **Runtime ↔ Template** | **无直接关系**。运行时只依赖项目目录。 |
| **target_root ≡ projects_root** | 同一概念：sub app 的父目录。创建时叫 target_root，运行时叫 projects_root。 |

---

## 三、当前实现的缺口

### 3.1 命名不一致

- 创建脚本：`--target-root`（目标根目录）
- 运行脚本：`--projects-root`（项目根目录）
- 语义相同，命名不同，易混淆。

### 3.2 无模板溯源

- 项目创建后，无法得知来自哪个模板。
- 影响：升级、迁移、调试时难以判断应参考哪类模板。

### 3.3 发现路径与创建路径需手动对齐

- 创建到 `examples/xxx` 时，运行需 `--projects-root examples`。
- 若创建用 `projects`、运行用 `examples`，则发现不到。

---

## 四、最佳设计实现

### 4.1 统一命名：subapp_root

**建议**：将 `target_root` 与 `projects_root` 统一为 `subapp_root`。

| 场景 | 当前 | 建议 |
|------|------|------|
| create_sub_uas_app.py | --target-root | --subapp-root |
| run_uas_runtime_service.py | --projects-root | --subapp-root |
| platform_manifest.json | subapp_root | 已存在，保持 |

**理由**：同一概念，单一命名，减少认知负担。

### 4.2 可选：模板溯源字段

在 `configs/platform_manifest.json` 中增加可选字段：

```json
{
  "platform": { ... },
  "provenance": {
    "template_id": "uas-subapp",
    "created_at": "2025-03-15T12:00:00Z"
  }
}
```

- **template_id**：创建时使用的模板 ID，便于溯源与升级。
- **created_at**：创建时间，便于审计。

**实现**：`run_init` 或 `create_sub_uas_app.py` 在写入时注入；模板需在 platform_manifest 中预留或合并该字段。

### 4.3 创建与发现的路径一致性

**规则**：创建时使用的 `subapp_root` 必须与运行时的 `subapp_root` 一致，否则无法发现。

**建议**：
1. 在 `createSubApp` 命令文档中明确：`--target projects` 创建的项目，需用 `--subapp-root projects` 运行。
2. 可选：创建完成后打印提示，如：
   ```
   运行: python3 scripts/run_uas_runtime_service.py list --subapp-root projects
   ```

### 4.4 模板与项目的职责边界（总结）

| 职责 | 模板 | 项目 |
|------|------|------|
| 定义初始结构 | ✓ | - |
| 定义工作流步骤 | ✓（写入项目后） | ✓（运行时读取） |
| 定义 Agent 配置 | ✓（写入项目后） | ✓（运行时读取） |
| 运行时数据源 | - | ✓ |
| 持久化 | 否（代码中） | 是（磁盘） |
| 可修改性 | 需改代码 | 直接改文件 |

**一句话**：模板是「工厂」，项目是「产品」；工厂只在生产时用，产品在生命周期内独立存在。

---

## 五、实现建议（按优先级）

### P1：文档与命名统一（低侵入）

1. 在 `docs/TEMPLATE_PROJECT_RELATIONSHIP.md`（本文档）中明确关系与命名建议。
2. 在 `create_sub_uas_app.py` 和 `run_uas_runtime_service.py` 中，为 `--target-root` / `--projects-root` 添加 `--subapp-root` 作为别名（兼容旧参数）。
3. 更新 `createSubApp` 命令与 `subapp_producer_protocol` 中的参数说明。

### P2：模板溯源（可选）

1. 在 `UAS_SUBAPP_TEMPLATE` 的 `platform_manifest.json` 中预留 `provenance` 结构。
2. 在 `run_init` 中增加可选参数 `template_id`，写入时注入 `provenance.template_id` 和 `provenance.created_at`。
3. `create_sub_uas_app.py` 调用时传入 `template` 作为 `template_id`。

### P3：创建后提示（可选）

在 `run_init` 或 `create_sub_uas_app.py` 结束时打印：

```
运行: python3 scripts/run_uas_runtime_service.py list --subapp-root projects
```

---

## 六、总结

| 问题 | 结论 |
|------|------|
| 模板和项目是什么关系？ | 模板是创建时的「文件蓝图」，项目是创建后的「运行实例」；创建后二者无持久链接。 |
| 运行逻辑依赖谁？ | 仅依赖项目目录；不依赖模板。 |
| 最佳设计？ | 统一 subapp_root 命名；可选增加 template 溯源；明确创建与发现的路径一致性。 |
