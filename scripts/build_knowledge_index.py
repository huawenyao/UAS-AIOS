#!/usr/bin/env python3
"""
UAS-AIOS 知识索引构建脚本

扫描 .claude、configs、docs、schemas 等目录，构建实体-关系索引，
输出到 database/knowledge_index.json。

用法：
  python scripts/build_knowledge_index.py

索引结构：
  - entities: [{id, type, path, attributes, cognition_layer}]
  - relations: [{subject, predicate, object}]
"""
import json
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent.parent
INDEX_PATH = WORKSPACE / "database" / "knowledge_index.json"

# 实体类型与认知层映射
ENTITY_TYPES = {
    "Document": "S",
    "Skill": "S",
    "Agent": "A",
    "Command": "S",
    "Workflow": "S",
    "Step": "S",
    "Schema": "S",
    "Concept": "S",
}

# 关系类型
RELATIONS = ["references", "depends_on", "implements", "opponent_of", "validates", "defines", "extends"]


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """解析 YAML frontmatter，返回 (attrs, body)"""
    attrs = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                attrs = yaml.safe_load(parts[1]) or {}
            except Exception:
                # 简单 key: value 解析
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        k, v = k.strip(), v.strip().strip("[]'\"")
                        if v.startswith("["):
                            attrs[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",")]
                        else:
                            attrs[k] = v
            return attrs, parts[2].strip()
    return attrs, content


def extract_refs_from_content(content: str, base_path: str) -> list[str]:
    """从内容中提取引用路径（.claude/、configs/、docs/、schemas/）"""
    refs = []
    patterns = [
        r"\.claude/skills/([a-zA-Z0-9_]+\.md)",
        r"\.claude/agents/([a-zA-Z0-9_]+\.md)",
        r"configs/([a-zA-Z0-9_]+\.json)",
        r"docs/([a-zA-Z0-9_/]+\.md)",
        r"schemas/([a-zA-Z0-9_]+\.json)",
        r"([a-zA-Z0-9_]+\.md)",  # 相对引用
    ]
    for p in patterns:
        for m in re.finditer(p, content):
            refs.append(m.group(0))
    return list(set(refs))


def scan_skills(workspace: Path) -> tuple[list[dict], list[tuple]]:
    """扫描 .claude/skills"""
    entities = []
    relations = []
    skills_dir = workspace / ".claude" / "skills"
    if not skills_dir.exists():
        return entities, relations

    for f in skills_dir.glob("*.md"):
        if f.name.startswith("."):
            continue
        content = f.read_text(encoding="utf-8")
        attrs, _ = parse_frontmatter(content)
        refs = extract_refs_from_content(content, str(f))
        eid = f"skill:{f.stem}"
        entities.append({
            "id": eid,
            "type": "Skill",
            "path": str(f.relative_to(workspace)),
            "name": attrs.get("name", f.stem),
            "cognition_layer": "S",
        })
        for ref in refs:
            relations.append((eid, "references", ref))
    return entities, relations


def scan_agents(workspace: Path) -> tuple[list[dict], list[tuple]]:
    """扫描 .claude/agents"""
    entities = []
    relations = []
    agents_dir = workspace / ".claude" / "agents"
    if not agents_dir.exists():
        return entities, relations

    for f in agents_dir.glob("*.md"):
        if f.name in ("README.md", ".gitkeep"):
            continue
        content = f.read_text(encoding="utf-8")
        attrs, _ = parse_frontmatter(content)
        agent_id = attrs.get("agent_id", f"swarm_{f.stem}")
        opponents = attrs.get("opponent_agents", [])
        eid = f"agent:{agent_id}"
        entities.append({
            "id": eid,
            "type": "Agent",
            "path": str(f.relative_to(workspace)),
            "name": attrs.get("agent_name", f.stem),
            "stance": attrs.get("stance", ""),
            "cognition_layer": "A",
        })
        for opp in opponents:
            relations.append((eid, "opponent_of", f"agent:{opp}"))
    return entities, relations


def scan_commands(workspace: Path) -> tuple[list[dict], list[tuple]]:
    """扫描 .claude/commands"""
    entities = []
    relations = []
    commands_dir = workspace / ".claude" / "commands"
    if not commands_dir.exists():
        return entities, relations

    for f in commands_dir.glob("*.md"):
        if f.name.startswith("."):
            continue
        content = f.read_text(encoding="utf-8")
        refs = extract_refs_from_content(content, str(f))
        name = f.stem.replace("_", "").lower()
        eid = f"command:{name}"
        entities.append({
            "id": eid,
            "type": "Command",
            "path": str(f.relative_to(workspace)),
            "name": f"/{name}",
            "cognition_layer": "S",
        })
        for ref in refs:
            relations.append((eid, "references", ref))
    return entities, relations


def scan_workflows(workspace: Path) -> tuple[list[dict], list[tuple]]:
    """扫描 configs/*.json 工作流"""
    entities = []
    relations = []
    configs_dir = workspace / "configs"
    if not configs_dir.exists():
        return entities, relations

    for f in configs_dir.glob("*.json"):
        if f.name.startswith("_"):
            continue
        try:
            cfg = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if "steps" not in cfg:
            continue
        wf_id = cfg.get("name", f.stem)
        eid = f"workflow:{f.stem}"
        entities.append({
            "id": eid,
            "type": "Workflow",
            "path": str(f.relative_to(workspace)),
            "name": wf_id,
            "version": cfg.get("version", ""),
            "steps_count": len(cfg.get("steps", [])),
            "cognition_layer": "S",
        })
        # global_config 引用
        gc = cfg.get("global_config", {})
        for k, v in gc.items():
            if isinstance(v, str) and (".md" in v or ".json" in v):
                relations.append((eid, "references", v))
        # steps 依赖
        for step in cfg.get("steps", []):
            step_id = step.get("id")
            if step_id:
                relations.append((eid, "contains", f"step:{step_id}"))
            for dep in step.get("dependencies", []):
                relations.append((f"step:{step_id}", "depends_on", f"step:{dep}"))
    return entities, relations


def scan_documents(workspace: Path) -> list[dict]:
    """扫描 docs 下的文档"""
    entities = []
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return entities

    for f in docs_dir.rglob("*.md"):
        if f.name.startswith("."):
            continue
        rel = str(f.relative_to(workspace))
        eid = f"doc:{f.stem}"
        entities.append({
            "id": eid,
            "type": "Document",
            "path": rel,
            "name": f.stem,
            "cognition_layer": "S",
        })
    return entities


def scan_schemas(workspace: Path) -> list[dict]:
    """扫描 schemas"""
    entities = []
    schemas_dir = workspace / "schemas"
    if not schemas_dir.exists():
        return entities

    for f in schemas_dir.glob("*.json"):
        eid = f"schema:{f.stem}"
        entities.append({
            "id": eid,
            "type": "Schema",
            "path": str(f.relative_to(workspace)),
            "name": f.stem,
            "cognition_layer": "S",
        })
    return entities


def normalize_relations(relations: list[tuple], entities: list[dict]) -> list[dict]:
    """将关系转为标准格式"""
    entity_ids = {e["id"] for e in entities}
    entity_paths = {e["path"]: e["id"] for e in entities if "path" in e}
    result = []
    for subj, pred, obj in relations:
        # 尝试将 path 引用转为 entity id
        if obj not in entity_ids and obj in entity_paths:
            obj = entity_paths[obj]
        result.append({"subject": subj, "predicate": pred, "object": obj})
    return result


def main():
    workspace = WORKSPACE
    all_entities = []
    all_relations = []

    # 扫描各类型
    for entities, relations in [scan_skills(workspace), scan_agents(workspace), scan_commands(workspace), scan_workflows(workspace)]:
        all_entities.extend(entities)
        all_relations.extend(relations)
    all_entities.extend(scan_documents(workspace))
    all_entities.extend(scan_schemas(workspace))

    # 去重实体
    seen = set()
    unique_entities = []
    for e in all_entities:
        if e["id"] not in seen:
            seen.add(e["id"])
            unique_entities.append(e)

    # 规范化关系
    norm_relations = normalize_relations(all_relations, unique_entities)

    index = {
        "version": "1.0",
        "built_at": datetime.now().isoformat(),
        "cognition_space": "UAS-AIOS",
        "entities": unique_entities,
        "relations": norm_relations,
        "stats": {
            "entities_count": len(unique_entities),
            "relations_count": len(norm_relations),
            "by_type": {},
        },
    }

    for e in unique_entities:
        t = e["type"]
        index["stats"]["by_type"][t] = index["stats"]["by_type"].get(t, 0) + 1

    INDEX_PATH.parent.mkdir(exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Index built: {INDEX_PATH}")
    print(f"  Entities: {len(unique_entities)}, Relations: {len(norm_relations)}")
    print(f"  By type: {index['stats']['by_type']}")


if __name__ == "__main__":
    main()
