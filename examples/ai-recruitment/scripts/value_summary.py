"""招聘批次价值摘要 — 可机器校验、可嵌入 HTML/CLI 的统一契约。"""
from __future__ import annotations

INTERVIEW_READY_DECISIONS = frozenset({"strong_recommend", "recommend", "borderline"})


def build_value_summary(
    results: list[dict],
    *,
    total_files: int | None = None,
    valid_count: int | None = None,
    elapsed_seconds: float | None = None,
    minutes_per_resume_manual: float = 25.0,
) -> dict:
    """
    从候选人结果列表构建价值摘要（P0 契约）。

    Args:
        results: workflow 产出的候选人记录（含 decision、scores、evidence 等）
        total_files: 扫描到的简历文件总数（可选）
        valid_count: 有效解析的简历数（默认 len(results)）
        elapsed_seconds: 本批处理耗时（可选，用于 P2 效率展示）
        minutes_per_resume_manual: 人工单份阅读估算分钟数
    """
    valid = valid_count if valid_count is not None else len(results)
    total = total_files if total_files is not None else valid

    decisions: dict[str, int] = {}
    with_evidence = 0
    for r in results:
        dec = r.get("decision") or "unknown"
        decisions[dec] = decisions.get(dec, 0) + 1
        if r.get("evidence"):
            with_evidence += 1

    interview_ready = sum(
        decisions.get(d, 0) for d in INTERVIEW_READY_DECISIONS
    )
    explainability_rate = round(with_evidence / valid, 4) if valid else 0.0
    estimated_saved_minutes = int(valid * minutes_per_resume_manual)

    headline = (
        f"已为本次 {valid} 份有效简历生成可解释推荐名单，"
        f"推荐/待定共 {interview_ready} 人，可直接用于面试名单决策。"
    )

    summary = {
        "total_files": total,
        "valid_count": valid,
        "decisions": decisions,
        "interview_ready_count": interview_ready,
        "explainability_rate": explainability_rate,
        "estimated_saved_minutes": estimated_saved_minutes,
        "headline": headline,
        "minutes_per_resume_manual": minutes_per_resume_manual,
    }
    if elapsed_seconds is not None:
        summary["elapsed_seconds"] = round(elapsed_seconds, 2)
    if valid:
        scores = [r.get("scores", {}).get("total_score", 0) for r in results]
        summary["average_total_score"] = round(sum(scores) / len(scores), 2)
    return summary


def format_value_summary_console(summary: dict) -> str:
    """将价值摘要格式化为终端输出块。"""
    lines = [
        "",
        "=" * 60,
        "执行完成 · 价值摘要",
        "=" * 60,
        f"简历文件数: {summary.get('total_files', 0)}",
        f"有效简历数: {summary.get('valid_count', 0)}",
    ]
    if "average_total_score" in summary:
        lines.append(f"平均分: {summary['average_total_score']}")
    lines.append("")
    lines.append("决策分布:")
    icons = {
        "strong_recommend": "强推",
        "recommend": "推荐",
        "borderline": "待定",
        "not_recommend": "不推荐",
    }
    for key, count in summary.get("decisions", {}).items():
        label = icons.get(key, key)
        lines.append(f"  {label}: {count} 人")
    lines.append("")
    lines.append(f"预估节省: 约 {summary.get('estimated_saved_minutes', 0)} 分钟")
    lines.append(f"  (按每份简历人工阅读 {summary.get('minutes_per_resume_manual', 25)} 分钟计)")
    if summary.get("elapsed_seconds") is not None:
        lines.append(f"本批耗时: {summary['elapsed_seconds']} 秒")
    rate = summary.get("explainability_rate", 0)
    lines.append(f"可解释覆盖率: {rate * 100:.0f}% (含证据链)")
    lines.append("")
    lines.append(summary.get("headline", ""))
    lines.append("=" * 60)
    return "\n".join(lines)


def render_value_banner_html(summary: dict) -> str:
    """推荐名单页首屏价值摘要条（HTML 片段）。"""
    valid = summary.get("valid_count", 0)
    ready = summary.get("interview_ready_count", 0)
    saved = summary.get("estimated_saved_minutes", 0)
    rate = summary.get("explainability_rate", 0)
    headline = summary.get("headline", "")
    return f"""
    <section class="value-banner" role="status">
      <p class="value-headline">{headline}</p>
      <div class="value-metrics">
        <span>有效简历 <strong>{valid}</strong></span>
        <span>可进面试名单 <strong>{ready}</strong></span>
        <span>预估节省 <strong>{saved}</strong> 分钟</span>
        <span>证据链覆盖 <strong>{rate * 100:.0f}%</strong></span>
      </div>
    </section>
    """


__all__ = [
    "INTERVIEW_READY_DECISIONS",
    "build_value_summary",
    "format_value_summary_console",
    "render_value_banner_html",
]
