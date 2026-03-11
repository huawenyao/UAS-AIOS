#!/usr/bin/env python3
"""蜂群决策方案持久化 - SelfPaw 认知智能体蜂群"""
import json
import sys
from pathlib import Path
from datetime import datetime

DB_DIR = Path(__file__).parent.parent / "database"
SWARM_DB = DB_DIR / "swarm_decisions.json"


def main():
    """从 stdin 读取辩证融合结果，持久化到数据库"""
    data = json.load(sys.stdin)
    DB_DIR.mkdir(exist_ok=True)

    record = {
        "id": data.get("synthesis_version", datetime.now().strftime("%Y%m%d%H%M%S")),
        "created_at": datetime.now().isoformat(),
        "synthesis": data,
        "evidence_chain": data.get("evidence_chain", []),
    }

    decisions = []
    if SWARM_DB.exists():
        decisions = json.loads(SWARM_DB.read_text(encoding="utf-8"))

    decisions.append(record)
    SWARM_DB.write_text(
        json.dumps(decisions, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps({"status": "persisted", "db_path": str(SWARM_DB), "record_id": record["id"]}))


if __name__ == "__main__":
    main()
