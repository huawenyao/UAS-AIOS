# Projects

本目录用于承载所有按 UAS-Platform 标准生成的业务子应用（sub uas app）。

## 生成方式

### 方式一：直接使用 asui-cli

```bash
asui init projects/<business-app> -t uas-subapp
```

### 方式二：使用元项目生成脚本

```bash
python3 scripts/create_sub_uas_app.py <business-app>
```

### 方式三：使用共享 Runtime Service 运行

```bash
python3 scripts/run_uas_runtime_service.py list
python3 scripts/run_uas_runtime_service.py registry
python3 scripts/run_uas_runtime_service.py health --app-id <business-app>
python3 scripts/run_uas_runtime_service.py validate --app-id <business-app>
python3 scripts/run_uas_runtime_service.py run --app-id <business-app> --topic "<业务议题>" --evaluate
python3 scripts/run_uas_runtime_service.py state --app-id <business-app> --topic-slug "<topic-slug>"
python3 scripts/run_uas_runtime_service.py enqueue --app-id <business-app> --topic "<业务议题>" --evaluate
python3 scripts/run_uas_runtime_service.py process
python3 scripts/run_uas_runtime_service.py queue
```

## 标准约束

所有 `projects/<business-app>/` 都必须：

- 产品架构遵循 `UAS-Platform = (I, K, R, A, S, G, E, Π)`
- 技术架构默认采用 `ASUI`
- 运行架构默认采用 `autonomous_agent runtime`
- 具备目标守恒、治理审计与演化回路
