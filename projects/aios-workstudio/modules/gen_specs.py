#!/usr/bin/env python3
"""从 catalog.json 生成每模块 SPEC.md 与目录索引。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))

KIND_ZH = {
    "implement": "本产品实现",
    "compose": "本产品组合（UI 在此，内核在 Hub）",
    "consume": "本产品只经 hub.* 消费",
    "shell": "Console 可视化壳（不当内核）",
    "platform": "平台零件 · 不在本产品实现",
    "external": "外部系统 · 只连接",
    "optional": "默认不部署",
}


def render(mod: dict) -> str:
    veto = "\n".join(f"- {x}" for x in mod.get("veto") or [])
    accept = "\n".join(f"- {x}" for x in mod.get("accept") or [])
    slice_l = mod.get("slice") or "—"
    req_l = mod.get("req") or "—"
    return f"""# {mod["t"]}

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `{mod["id"]}`

| 项 | 值 |
|----|----|
| **ID** | `{mod["id"]}` |
| **平面** | {mod["plane"]} |
| **决策** | {mod["decision"]} |
| **本仓库角色** | {KIND_ZH.get(mod["kind"], mod["kind"])} |
| **代码落点** | `{mod["owner"]}` |
| **运行时** | {mod["runtime"]} |
| **切片** | `{slice_l}` |
| **需求** | `{req_l}` |

## 定位

{mod["d"]}

## 非职责

{mod["non"]}

## 设计方案

{mod["design"]}

## 技术选型

{mod["stack"]}

## 接口

```
{mod["api"]}
```

## 否决

{veto}

## 验收

{accept}

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 {mod["id"]} 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
"""


def main() -> None:
    rows = []
    for mod in CATALOG["modules"]:
        dest = ROOT / mod["dir"]
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "SPEC.md").write_text(render(mod), encoding="utf-8")
        rows.append(
            f"| `{mod['id']}` | [{mod['t']}](./{mod['dir']}/SPEC.md) | {mod['plane']} | {KIND_ZH.get(mod['kind'], mod['kind'])} | `{mod['owner']}` |"
        )
    index = f"""# aios-workstudio 模块目录

来源：`docs/strategic/design/uas-aios-cluster.html`  
规则：{CATALOG["rule"]}  
Hub：`{CATALOG["hub"]}`

| ID | 模块 | 平面 | 本仓库角色 | 代码落点 |
|----|------|------|------------|----------|
{chr(10).join(rows)}

重新生成：`python projects/aios-workstudio/modules/gen_specs.py`
"""
    (ROOT / "README.md").write_text(index, encoding="utf-8")
    print(f"wrote {len(CATALOG['modules'])} SPECs")


if __name__ == "__main__":
    main()
