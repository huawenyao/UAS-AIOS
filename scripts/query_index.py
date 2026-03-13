#!/usr/bin/env python3
"""
知识索引查询工具

用法：
  python scripts/query_index.py                    # 输出索引摘要
  python scripts/query_index.py --entity agent      # 按类型筛选实体
  python scripts/query_index.py --refs swarm_methodology  # 谁引用了 X
  python scripts/query_index.py --deps agent:swarm_01    # X 依赖/关联什么
"""
import json
import sys
from pathlib import Path

INDEX_PATH = Path(__file__).parent.parent / "database" / "knowledge_index.json"


def load_index():
    if not INDEX_PATH.exists():
        print("Index not found. Run: python scripts/build_knowledge_index.py")
        sys.exit(1)
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def main():
    index = load_index()
    entities = {e["id"]: e for e in index["entities"]}
    relations = index["relations"]

    args = sys.argv[1:]
    if not args:
        print(f"Knowledge Index v{index['version']} | Built: {index['built_at']}")
        print(f"Entities: {index['stats']['entities_count']} | Relations: {index['stats']['relations_count']}")
        print("\nBy type:", index["stats"]["by_type"])
        return

    if args[0] == "--entity" and len(args) > 1:
        etype = args[1].lower()
        for e in index["entities"]:
            if e["type"].lower() == etype or etype in e["id"].lower():
                print(f"  {e['id']} | {e.get('name', e['path'])} | {e['path']}")
        return

    if args[0] == "--refs" and len(args) > 1:
        target = args[1]
        for r in relations:
            if r["object"] == target or target in r["object"] or target in r["subject"]:
                print(f"  {r['subject']} --[{r['predicate']}]--> {r['object']}")
        return

    if args[0] == "--deps" and len(args) > 1:
        target = args[1]
        for r in relations:
            if r["subject"] == target:
                print(f"  {r['subject']} --[{r['predicate']}]--> {r['object']}")
            elif r["object"] == target:
                print(f"  {r['subject']} --[{r['predicate']}]--> {r['object']}")
        return

    print("Usage: query_index.py [--entity TYPE | --refs ID | --deps ID]")


if __name__ == "__main__":
    main()
