"""正式项目层测试 — domain / schemas / capabilities / orchestrator / store / metrics / cli。

覆盖规约红线与状态机不变量。与既有 14 CASE 测试共存，确保回归。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# 让 tests/ 能 import 顶层 lifewake 包
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lifewake import (
    domain,
    schemas,
    capabilities,
    orchestrator,
    store,
    metrics,
    cli,
)  # noqa: E402

# === domain 不变量 ===


class TestDomainInvariants:
    def test_consent_must_be_create_for_user(self):
        with pytest.raises(domain.DomainError):
            domain.ConsentGrant(
                consent_id="c",
                person_id="p",
                scopes=("s",),
                purpose="ads",
                expires_at="2026-01-01",
            )

    def test_consent_must_be_withdrawable(self):
        with pytest.raises(domain.DomainError):
            domain.ConsentGrant(
                consent_id="c",
                person_id="p",
                scopes=("s",),
                withdrawable=False,
                expires_at="2026-01-01",
            )

    def test_consent_requires_expires_at(self):
        with pytest.raises(domain.DomainError):
            domain.ConsentGrant(consent_id="c", person_id="p", scopes=("s",))

    def test_surprise_requires_uniqueness_refs(self):
        with pytest.raises(domain.DomainError):
            domain.Surprise(
                surprise_id="s",
                kind="song",
                payload={},
                inspiration_trace=(),
                timing_window="e",
            )

    def test_bond_requires_two_members(self):
        with pytest.raises(domain.DomainError):
            domain.Bond(bond_id="b", members=("a",), needs={})

    def test_changeset_auto_apply_forbidden(self):
        with pytest.raises(domain.DomainError):
            domain.ChangeSet(
                changeset_id="cs",
                source="s",
                target_pack="surprise_policy",
                summary="x",
                auto_apply=True,
            )

    def test_envelope_requires_timing_and_impact_ref(self):
        with pytest.raises(domain.DomainError):
            domain.RitualEnvelope(
                envelope_id="e", ritual_id="r", intent_ref="i", artifact_ref="a"
            )

    def test_audit_rejects_forbidden_payload(self):
        with pytest.raises(domain.DomainError):
            domain.AuditEvent(
                audit_id="a",
                event="e",
                trace_id="t",
                payload={"raw_pulse_stream": "leaked"},
            )


# === schema 校验 ===


class TestSchemas:
    def test_validate_consent_ok(self):
        data = {
            "consent_id": "c",
            "person_id": "p",
            "scopes": ["s"],
            "purpose": "create_for_user",
            "expires_at": "2026-01-01",
            "withdrawable": True,
        }
        out = schemas.validate_entity("ConsentGrant", data)
        assert out["consent_id"] == "c"

    def test_validate_envelope_missing_ref_rejected(self):
        data = {
            "envelope_id": "e",
            "ritual_id": "r",
            "intent_ref": "i",
            "artifact_ref": "a",
        }
        with pytest.raises(schemas.ValidationError):
            schemas.validate_ritual_envelope(data)

    def test_validate_audit_sanitizes_forbidden(self):
        data = {
            "audit_id": "a",
            "event": "e",
            "trace_id": "t",
            "payload": {"exact_age": 17},
        }
        with pytest.raises(schemas.ValidationError):
            schemas.validate_audit_event(data)

    def test_validate_changeset_auto_apply_rejected(self):
        data = {
            "changeset_id": "cs",
            "target_pack": "surprise_policy",
            "auto_apply": True,
        }
        with pytest.raises(schemas.ValidationError):
            schemas.validate_entity("ChangeSet", data)


# === 能力契约 ===


class TestCapabilities:
    def test_registry_has_14_p0_capabilities(self):
        reg = capabilities.build_registry()
        names = reg.names()
        assert len(names) == 14
        for required in [
            "lw.consent.check",
            "lw.surprise.compose",
            "lw.ritual.render",
            "lw.changeset.draft",
        ]:
            assert required in names

    def test_reserved_capability_returns_feature_reserved(self):
        reg = capabilities.build_registry()
        resp = reg.invoke(
            capabilities.CapabilityCall(capability="lw.memory.weave", trace_id="t")
        )
        assert resp.status == "failed"
        assert resp.error["code"] == "FEATURE_RESERVED"

    def test_idempotency_returns_cached(self):
        reg = capabilities.build_registry()
        call = capabilities.CapabilityCall(
            capability="lw.consent.check",
            trace_id="idem",
            idempotency_key="k1",
            inputs={
                "consent": {
                    "consent_id": "c",
                    "person_id": "p",
                    "scopes": ["signals.low_sensitivity"],
                    "status": "granted",
                },
                "intent_type": "surprise_delivery",
            },
            policy={
                "required_scopes": ["signals.low_sensitivity"],
                "purpose": "create_for_user",
            },
        )
        r1 = reg.invoke(call)
        r2 = reg.invoke(call)
        assert r1.status == "success"
        assert r2.status == "success"
        # 同 idempotency_key 应命中缓存（audit 不再增长）
        before = len(capabilities.audit_log())
        reg.invoke(call)
        after = len(capabilities.audit_log())
        assert after == before

    def test_audit_log_sanitized(self):
        capabilities.reset_audit()
        capabilities.append_audit("test", "t", {"ok": True})
        log = capabilities.audit_log()
        assert log[0]["payload"] == {"ok": True}
        with pytest.raises(schemas.ValidationError):
            capabilities.append_audit("bad", "t", {"diagnostic_inference": "x"})


# === 状态机编排 ===

GOOD_CONSENT = {
    "consent_id": "c1",
    "person_id": "p1",
    "scopes": ["signals.low_sensitivity"],
    "purpose": "create_for_user",
    "status": "granted",
    "withdrawable": True,
    "expires_at": "2026-12-31",
}


class TestOrchestrator:
    def test_happy_path_order_invariant(self):
        orch = orchestrator.Orchestrator(
            governance={"wow_score_threshold": 0.7, "delivery_count_today": 0}
        )
        run = orchestrator.IntentRun(
            intent_id="happy", intent_type="surprise_delivery", trace_id="happy"
        )
        orch.run_surprise(
            run,
            consent=GOOD_CONSENT,
            raw_signals=[{"kind": "hum_melody", "value": "rain"}],
            user_feedback=0.85,
        )
        assert run.state == "closed"
        assert orchestrator.verify_order_invariant(run.history) is True
        # impact 必须在 timing 之前
        assert run.history.index("impact_checking") < run.history.index(
            "timing_deciding"
        )
        assert run.history.index("timing_deciding") < run.history.index(
            "ritual_rendering"
        )

    def test_consent_required_when_missing(self):
        orch = orchestrator.Orchestrator(governance={"wow_score_threshold": 0.7})
        run = orchestrator.IntentRun(
            intent_id="noc", intent_type="surprise_delivery", trace_id="noc"
        )
        orch.run_surprise(
            run, consent=None, raw_signals=[{"kind": "hum_melody", "value": "x"}]
        )
        assert run.state == "consent_required"

    def test_safety_hold_preempts(self):
        orch = orchestrator.Orchestrator(governance={"wow_score_threshold": 0.7})
        run = orchestrator.IntentRun(
            intent_id="safe", intent_type="surprise_delivery", trace_id="safe"
        )
        orch.run_surprise(
            run,
            consent=GOOD_CONSENT,
            raw_signals=[{"kind": "hum_melody", "value": "x"}],
            safety_signal={"category": "possible_self_harm"},
        )
        assert run.state == "safety_hold"

    def test_slow_inspiration_deferred(self):
        orch = orchestrator.Orchestrator(
            governance={"wow_score_threshold": 0.7, "delivery_count_today": 2}
        )
        run = orchestrator.IntentRun(
            intent_id="slow", intent_type="surprise_delivery", trace_id="slow"
        )
        orch.run_surprise(
            run,
            consent=GOOD_CONSENT,
            raw_signals=[{"kind": "hum_melody", "value": "x"}],
        )
        assert run.state == "slow_inspiration_deferred"

    def test_revoke_blocks_post_revoke_processing(self):
        orch = orchestrator.Orchestrator(governance={"wow_score_threshold": 0.7})
        run = orchestrator.IntentRun(
            intent_id="rev", intent_type="surprise_delivery", trace_id="rev"
        )
        run.transition("consent_checking")
        run.transition("signal_weaving")
        orch.revoke_consent(run, consent_id="c1")
        assert run.state == "consent_revoked"
        with pytest.raises(orchestrator.StateMachineError):
            run.transition("composing")

    def test_low_impact_does_not_deliver(self):
        orch = orchestrator.Orchestrator(
            governance={"wow_score_threshold": 0.99}
        )  # 极高阈值 → impact 必失败
        run = orchestrator.IntentRun(
            intent_id="low", intent_type="surprise_delivery", trace_id="low"
        )
        orch.run_surprise(
            run,
            consent=GOOD_CONSENT,
            raw_signals=[{"kind": "hum_melody", "value": "x"}],
        )
        assert run.state == "emotion_impact_failed"


# === 存储 ===


class TestStore:
    def test_save_and_load_run(self, tmp_path):
        s = store.Store(root=tmp_path)
        s.save_run("r1", {"run_id": "r1", "state": {"final": "closed"}})
        loaded = s.runs.load("r1")
        assert loaded["run_id"] == "r1"
        assert "r1" in [r["_key"] for r in s.runs.list_all()]

    def test_save_envelope_validates(self, tmp_path):
        s = store.Store(root=tmp_path)
        with pytest.raises(schemas.ValidationError):
            s.save_envelope(
                {"envelope_id": "e", "ritual_id": "r"}
            )  # 缺 timing/impact ref

    def test_save_envelope_ok(self, tmp_path):
        s = store.Store(root=tmp_path)
        env = {
            "envelope_id": "e1",
            "ritual_id": "r1",
            "intent_ref": "i",
            "artifact_ref": "a",
            "timing_decision_ref": "t",
            "emotion_impact_ref": "ei",
        }
        s.save_envelope(env)
        assert s.keepsakes.load("e1")["envelope_id"] == "e1"

    def test_audit_jsonl_appends(self, tmp_path):
        s = store.Store(root=tmp_path)
        s.append_audit_jsonl(
            {"audit_id": "a1", "event": "e", "trace_id": "t", "payload": {}}
        )
        s.append_audit_jsonl(
            {"audit_id": "a2", "event": "e", "trace_id": "t", "payload": {}}
        )
        log = (tmp_path / "audit" / "execution_log.jsonl").read_text(encoding="utf-8")
        assert log.count("\n") == 2

    def test_save_consent_validates(self, tmp_path):
        s = store.Store(root=tmp_path)
        with pytest.raises(schemas.ValidationError):
            s.save_consent(
                "c",
                {
                    "consent_id": "c",
                    "person_id": "p",
                    "scopes": ["s"],
                    "purpose": "ads",
                    "expires_at": "x",
                },
            )


# === 指标 ===


class TestMetrics:
    def test_mrcr_computation(self):
        runs = [
            {
                "ritual_revealed": True,
                "consent_valid": True,
                "user_feedback_label": "meaningful",
            },
            {
                "ritual_revealed": True,
                "consent_valid": True,
                "user_feedback_label": "not_meaningful",
            },
            {
                "ritual_revealed": True,
                "consent_valid": False,
                "user_feedback_label": "meaningful",
            },  # 不计入分母
        ]
        out = metrics.compute_mrcr(runs)
        assert out["eligible_revealed_rituals"] == 2
        assert out["meaningful_rituals"] == 1
        assert out["mrcr"] == 0.5

    def test_guardrail_veto_on_post_revoke_processing(self, tmp_path):
        s = store.Store(root=tmp_path)
        s.save_run("r1", {"post_revoke_processing_count": 1})
        m = metrics.compute_metrics(s)
        assert "post_revoke_processing_gt_zero" in m["guardrail_veto"]

    def test_telemetry_sanitization_rejects_forbidden(self):
        with pytest.raises(metrics.MetricsError):
            metrics.sanitize_telemetry({"properties": {"raw_pulse_stream": "x"}})

    def test_telemetry_sanitization_ok(self):
        out = metrics.sanitize_telemetry({"properties": {"rating": 5}})
        assert out["properties"]["rating"] == 5


# === CLI 真实输入边界 ===


class TestCLI:
    def test_run_intent_real_input(self, tmp_path):
        payload = {
            "intent_type": "surprise_delivery",
            "consent": GOOD_CONSENT,
            "raw_signals": [
                {"kind": "hum_melody", "value": "rain"},
                {"kind": "favorite_artist_style", "value": "jazz"},
            ],
            "timing_window": "evening",
            "user_feedback": 0.85,
            "curator_score": 0.8,
            "delivery_date": "2026-07-25",
        }
        record = cli.run_intent(payload, store=store.Store(root=tmp_path))
        assert record["state"]["final"] == "closed"
        assert record["ritual_revealed"] is True
        assert record["consent_valid"] is True
        assert "envelope" in record["artifacts"]
        assert "keepsake" in record["artifacts"]
        assert orchestrator.verify_order_invariant(record["history"]) is True

    def test_cli_main_metrics_flag(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setattr(store, "DEFAULT_ROOT", tmp_path)
        rc = cli.main(["--metrics"])
        out = capsys.readouterr().out
        assert rc == 0
        data = json.loads(out)
        assert "M-01_mrcr" in data
        assert "guardrail_veto" in data

    def test_cli_main_invalid_json(self, capsys):
        rc = cli.main(["--intent", "{not json"])
        assert rc == 2
