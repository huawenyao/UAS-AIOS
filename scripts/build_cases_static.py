#!/usr/bin/env python3
"""构建 cases-static StaticMCP 站点，将 HTML 部署为 MCP 资源。"""
import json
import os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CASES_STATIC = WORKSPACE / "cases-static"
RESOURCES = CASES_STATIC / "resources"

FILES = [
    ("uas_aios_pitch.html", "UAS-AIOS 战略简报", "file://uas_aios_pitch.html"),
    ("aios_business_plan.html", "UAS-AIOS 商业计划书", "file://aios_business_plan.html"),
]


def main():
    CASES_STATIC.mkdir(exist_ok=True)
    RESOURCES.mkdir(exist_ok=True)

    resources_manifest = []
    for filename, name, uri in FILES:
        src = WORKSPACE / filename
        if not src.exists():
            print(f"跳过不存在的文件: {src}")
            continue

        html_content = src.read_text(encoding="utf-8")
        resource_response = {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "text/html",
                    "text": html_content,
                }
            ]
        }

        # URI file://path -> resources/path.json (StaticMCP Bridge 映射规则)
        resource_path = uri.replace("file://", "")
        out_file = RESOURCES / f"{resource_path}.json"
        out_file.write_text(json.dumps(resource_response, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"已生成: {out_file}")

        resources_manifest.append({
            "uri": uri,
            "name": name,
            "mimeType": "text/html",
        })

    # mcp.json 清单 - StaticMCP 标准格式
    mcp_manifest = {
        "name": "cases-static",
        "version": "1.0.0",
        "description": "UAS-AIOS 案例展示：战略简报与商业计划书",
        "resources": resources_manifest,
    }
    (CASES_STATIC / "mcp.json").write_text(
        json.dumps(mcp_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"已生成: {CASES_STATIC / 'mcp.json'}")
    print("cases-static StaticMCP 站点构建完成！")


if __name__ == "__main__":
    main()
