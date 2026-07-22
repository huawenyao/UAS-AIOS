#!/usr/bin/env python3
"""Dependency-free structural smoke checks for the LifeWake prototype."""

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).parent


class PrototypeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.objects = set()
        self.scripts = []
        self.stylesheets = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        if attributes.get("data-object"):
            self.objects.add(attributes["data-object"])
        if tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"])
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href"))


def main():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    parser = PrototypeParser()
    parser.feed(html)

    required_ids = {
        "room",
        "desk",
        "subject-switcher-trigger",
        "scene-switcher-trigger",
        "sovereignty-trigger",
        "rehearse-trigger",
        "detail-drawer",
        "gift-dialog",
        "rehearsal-dialog",
        "sovereignty-dialog",
        "toast-region",
    }
    required_objects = {
        "portrait",
        "music",
        "gift",
        "photos",
        "clock",
        "envelope",
        "lamp",
        "notebook",
    }
    required_copy = {
        "妻子 · 林妍",
        "今晚，给她一个惊喜",
        "主权与边界",
        "预演惊喜",
        "策展低语",
    }
    required_bindings = {
        "toggleMusic",
        "openGift",
        "openRehearsal",
        "revokeMaterials",
        "onPointerMove",
        "sessionStorage",
    }

    assert required_ids <= parser.ids, f"missing DOM ids: {required_ids - parser.ids}"
    assert parser.objects == required_objects, f"unexpected object set: {parser.objects}"
    assert parser.scripts == ["app.js?v=2"], f"unexpected scripts: {parser.scripts}"
    assert parser.stylesheets == ["styles.css?v=2"], f"unexpected stylesheets: {parser.stylesheets}"
    assert all(copy in html for copy in required_copy), "required product copy missing"
    assert all(binding in js for binding in required_bindings), "core interaction binding missing"
    assert "@media (max-width: 760px)" in css, "mobile layout missing"
    assert "@media (prefers-reduced-motion: reduce)" in css, "reduced motion support missing"
    assert "http://" not in html + css + js and "https://" not in html + css + js, "external dependency found"

    print(
        "LifeWake smoke test passed: "
        f"{len(parser.ids)} ids, {len(parser.objects)} interactive objects, "
        "local assets only, responsive and reduced-motion rules present."
    )


if __name__ == "__main__":
    main()
