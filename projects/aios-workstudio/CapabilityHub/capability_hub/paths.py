from __future__ import annotations

from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
REPO = PKG.parents[2]
HUB_API = REPO / "services" / "hub-api"
MATRIX = PKG / "configs" / "profile_matrix.json"
