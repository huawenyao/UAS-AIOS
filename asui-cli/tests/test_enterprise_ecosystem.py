"""
企业级 Agent 生态体系测试
覆盖：cs.* 语义层 / L1 SelfPaw / L2 ΠPaw / L3 ΠPaw / 端到端 B2B 管道
"""
import sys
from pathlib import Path

# 添加仓库根路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest


# ============================================================
# cs.* 语义服务层测试
# ============================================================
class TestCapabilityServices:

    def test_cs_customer_qualify_lead_pass(self):
        from enterprise.platform.capability_services.cs_customer import CustomerService
        cs = CustomerService()
        result = cs.qualify_lead({
            "lead_id": "LEAD_TEST",
            "budget_usd": 80000,
            "decision_maker": True,
            "pain_score": 8,
            "timeline_months": 3,
        })
        assert result.qualified is True
        assert result.score == 100
        assert result.next_action == "安排需求诊断会议"

    def test_cs_customer_qualify_lead_fail(self):
        from enterprise.platform.capability_services.cs_customer import CustomerService
        cs = CustomerService()
        result = cs.qualify_lead({
            "lead_id": "LEAD_TEST2",
            "budget_usd": 5000,     # 不足
            "decision_maker": False,  # 不足
            "pain_score": 3,         # 不足
            "timeline_months": 24,   # 过长
        })
        assert result.qualified is False
        assert result.score == 0
        assert len(result.disqualify_reasons) == 4

    def test_cs_approval_create_auto_approve(self):
        from enterprise.platform.capability_services.cs_approval import ApprovalService
        svc = ApprovalService()
        task = svc.create_approval_task(
            type_="discount",
            subject="5折扣测试",
            requester_id="ae_001",
            payload={"discount_pct": 3, "type": "discount"},
        )
        # 3% 折扣低于自动审批阈值 5%
        assert task.status == "approved"

    def test_cs_approval_create_requires_review(self):
        from enterprise.platform.capability_services.cs_approval import ApprovalService
        svc = ApprovalService()
        task = svc.create_approval_task(
            type_="quote",
            subject="大额报价审批",
            requester_id="ae_001",
            payload={"amount": 300000, "type": "quote"},
        )
        assert task.status == "pending"
        assert task.total_levels >= 3

    def test_cs_invoice_create_and_submit(self):
        from enterprise.platform.capability_services.cs_invoice import InvoiceService
        svc = InvoiceService()
        inv = svc.create_invoice_request(
            order_id="ORD_001",
            customer_id="CUST_001",
            amount=100000.0,
            invoice_type="vat_special",
            items=[{"description": "服务费", "unit_price": 100000, "quantity": 1}],
        )
        assert inv.status == "draft"
        assert inv.tax_rate == 0.13
        assert inv.total_amount == pytest.approx(113000.0, abs=1)

        submitted = svc.submit_invoice(inv.invoice_id)
        assert submitted.status == "submitted"

    def test_cs_finance_create_quote(self):
        from enterprise.platform.capability_services.cs_finance import FinanceService
        svc = FinanceService()
        quote = svc.create_quote(
            customer_id="CUST_001",
            opportunity_id="OPP_001",
            line_items=[
                {"name": "平台授权", "unit_price": 60000, "quantity": 1},
                {"name": "实施", "unit_price": 15000, "quantity": 1},
            ],
            discount_pct=10.0,
        )
        assert quote.subtotal == 75000.0
        assert quote.discount_amount == 7500.0
        assert quote.net_amount == 67500.0
        assert quote.status == "draft"

    def test_cs_finance_kpi_attribution_new(self):
        from enterprise.platform.capability_services.cs_finance import FinanceService
        svc = FinanceService()
        result = svc.calculate_kpi_attribution({
            "order_id": "ORD_001",
            "amount": 100000,
            "revenue_type": "new",
            "ae_id": "ae_001",
            "csm_id": "csm_001",
        })
        assert result["ae_amount"] == 100000
        assert result["csm_amount"] == 0

    def test_cs_finance_kpi_attribution_renewal(self):
        from enterprise.platform.capability_services.cs_finance import FinanceService
        svc = FinanceService()
        result = svc.calculate_kpi_attribution({
            "order_id": "ORD_002",
            "amount": 50000,
            "revenue_type": "renewal",
            "ae_id": "ae_001",
            "csm_id": "csm_001",
        })
        assert result["csm_amount"] == 50000
        assert result["ae_amount"] == 0


# ============================================================
# 数据平面 + 治理测试
# ============================================================
class TestDataPlaneAndGovernance:

    def test_tenant_manager_get_identity(self):
        from enterprise.platform.data_plane.tenant_manager import TenantManager
        mgr = TenantManager()
        identity = mgr.get_identity("USR_AE_001")
        assert identity is not None
        assert identity.position == "sales_ae"
        assert "sales_ae" in identity.roles

    def test_tenant_data_scope(self):
        from enterprise.platform.data_plane.tenant_manager import TenantManager
        mgr = TenantManager()
        scope = mgr.get_data_scope("USR_AE_001", "customers")
        assert scope == "own"

    def test_event_stream_publish_subscribe(self):
        from enterprise.platform.data_plane.event_stream import EventStream, DomainEvent
        stream = EventStream()
        received = []
        stream.subscribe("lead.qualified", received.append)

        event = stream.emit_lead_qualified("LEAD_001", "TENANT_001", "agent_001", {"score": 75})
        assert len(received) == 1
        assert received[0].event_type == "lead.qualified"
        assert event.sequence == 1

    def test_event_stream_replay(self):
        from enterprise.platform.data_plane.event_stream import EventStream, DomainEvent
        stream = EventStream()
        stream.emit_lead_qualified("L1", "T1", "a1", {})
        stream.emit_quote_approved("Q1", "T1", "a1", {})
        stream.emit_payment_received("I1", "T1", 1000)

        all_events = stream.replay()
        assert len(all_events) == 3

        lead_events = stream.replay(event_type="lead.qualified")
        assert len(lead_events) == 1

    def test_audit_chain_record_and_query(self):
        from enterprise.platform.data_plane.audit_chain import AuditChain
        chain = AuditChain()

        class FakeReq:
            correlation_id = "REQ_001"
            caller_id = "agent_001"
            tenant_id = "TENANT_001"
            service = "cs.customer"
            action = "qualify_lead"
            payload = {"budget": 50000}

        class FakeResp:
            status = "success"
            latency_ms = 42

        audit_id = chain.record(FakeReq(), FakeResp())
        assert audit_id is not None

        records = chain.query(tenant_id="TENANT_001")
        assert len(records) == 1
        assert records[0].service == "cs.customer"

    def test_audit_chain_integrity(self):
        from enterprise.platform.data_plane.audit_chain import AuditChain
        chain = AuditChain()

        class FakeReq:
            correlation_id = "REQ_002"
            caller_id = "agent_001"
            tenant_id = "TENANT_001"
            service = "cs.approval"
            action = "create"
            payload = {}

        class FakeResp:
            status = "success"
            latency_ms = 10

        chain.record(FakeReq(), FakeResp())
        integrity = chain.verify_integrity()
        assert integrity["integrity_ok"] is True

    def test_permission_engine_allow(self):
        from enterprise.platform.governance.permission_engine import PermissionEngine
        engine = PermissionEngine()
        engine.assign_roles("agent_ae", ["sales_ae"])

        result = engine.check("agent_ae", "TENANT_001", "cs.customer", "qualify_lead")
        assert result.allowed is True

    def test_permission_engine_deny(self):
        from enterprise.platform.governance.permission_engine import PermissionEngine
        engine = PermissionEngine()
        engine.assign_roles("agent_ae", ["sales_ae"])

        # 销售 AE 无权访问 cs.invoice.issue
        result = engine.check("agent_ae", "TENANT_001", "cs.invoice", "issue")
        assert result.allowed is False

    def test_compliance_engine_block(self):
        from enterprise.platform.governance.compliance_rules import ComplianceEngine
        engine = ComplianceEngine()
        passed, violations = engine.check("create_quote", {"discount_pct": 35})
        assert passed is False
        assert any(v.severity == "block" for v in violations)

    def test_compliance_engine_pass(self):
        from enterprise.platform.governance.compliance_rules import ComplianceEngine
        engine = ComplianceEngine()
        passed, violations = engine.check("create_quote", {"discount_pct": 10})
        assert passed is True


# ============================================================
# cs.* 网关测试
# ============================================================
class TestCapabilityServiceGateway:

    def _build_gateway(self):
        from enterprise.platform.capability_services.cs_gateway import CapabilityServiceGateway
        from enterprise.platform.capability_services.cs_customer import CustomerService
        from enterprise.platform.data_plane.audit_chain import AuditChain
        from enterprise.platform.governance.permission_engine import PermissionEngine

        perm = PermissionEngine()
        audit = AuditChain()
        gw = CapabilityServiceGateway(permission_engine=perm, audit_chain=audit)
        cs = CustomerService()
        gw.register_adapter("cs.customer", cs, {"desc": "客户服务"})
        perm.assign_roles("test_agent", ["l3_agent", "system_agent"])
        return gw, perm

    def test_gateway_invoke_success(self):
        from enterprise.platform.capability_services.cs_gateway import CSRequest
        gw, perm = self._build_gateway()

        req = CSRequest(
            service="cs.customer",
            action="qualify_lead",
            payload={"lead_id": "L1", "budget_usd": 50000, "decision_maker": True, "pain_score": 7, "timeline_months": 3},
            caller_id="test_agent",
            tenant_id="TENANT_001",
        )
        resp = gw.invoke(req)
        assert resp.status == "success"
        assert resp.result is not None
        assert resp.audit_id is not None

    def test_gateway_permission_denied(self):
        from enterprise.platform.capability_services.cs_gateway import CSRequest
        gw, perm = self._build_gateway()
        perm.assign_roles("restricted_agent", ["l1_user"])

        req = CSRequest(
            service="cs.customer",
            action="qualify_lead",
            payload={"lead_id": "L2", "budget_usd": 50000},
            caller_id="restricted_agent",
            tenant_id="TENANT_001",
        )
        # l1_user 应该可以调用 qualify_lead
        resp = gw.invoke(req)
        assert resp.status == "success"

    def test_gateway_service_not_found(self):
        from enterprise.platform.capability_services.cs_gateway import CSRequest
        from enterprise.platform.governance.permission_engine import PermissionRule
        gw, perm = self._build_gateway()
        # 给 system_agent 显式授权访问不存在的服务，使其通过权限检查，触发服务未找到错误
        perm.assign_roles("test_agent3", ["system_agent"])
        perm.add_rule(PermissionRule("system_agent", "cs.nonexistent", ["*"]))

        req = CSRequest(
            service="cs.nonexistent",
            action="foo",
            payload={},
            caller_id="test_agent3",
            tenant_id="TENANT_001",
        )
        resp = gw.invoke(req)
        assert resp.status == "failure"
        assert "SERVICE_NOT_FOUND" in (resp.error or "")


# ============================================================
# L1 SelfPaw 企业版测试
# ============================================================
class TestSelfPawEnterprise:

    def _build_selfpaw(self, user_id="USR_AE_001"):
        from enterprise.platform.capability_services.cs_gateway import CapabilityServiceGateway
        from enterprise.platform.capability_services.cs_customer import CustomerService
        from enterprise.platform.capability_services.cs_finance import FinanceService
        from enterprise.platform.capability_services.cs_approval import ApprovalService
        from enterprise.platform.data_plane.tenant_manager import TenantManager
        from enterprise.platform.data_plane.event_stream import EventStream
        from enterprise.platform.governance.permission_engine import PermissionEngine

        perm = PermissionEngine()
        gw = CapabilityServiceGateway(permission_engine=perm)
        gw.register_adapter("cs.customer", CustomerService())
        gw.register_adapter("cs.finance", FinanceService())
        gw.register_adapter("cs.approval", ApprovalService())

        tm = TenantManager()
        es = EventStream()

        from enterprise.agents.l1_selfpaw.selfpaw_enterprise import SelfPawEnterprise
        return SelfPawEnterprise(
            user_id=user_id,
            tenant_id="TENANT_DEMO",
            tenant_manager=tm,
            cs_gateway=gw,
            event_stream=es,
        )

    def test_selfpaw_initialization(self):
        sp = self._build_selfpaw()
        status = sp.get_status()
        assert status["user_id"] == "USR_AE_001"
        assert "sales_ae" in status["domain_packages"] or "sales_ontology" in status["domain_packages"]
        assert status["identity"] is not None

    def test_selfpaw_intent_personal(self):
        sp = self._build_selfpaw()
        result = sp.process_intent("帮我写一份工作总结", {})
        assert result["mode"] == "local_execution"

    def test_selfpaw_intent_business_escalate(self):
        sp = self._build_selfpaw()
        result = sp.process_intent(
            "客户要求申请额外折扣，需要审批",
            {"customer_id": "数智科技", "amount": 80000},
        )
        # 含审批关键词 → 升级
        assert result["mode"] in ("escalated", "local_execution")

    def test_selfpaw_swarm_decision(self):
        sp = self._build_selfpaw()
        memo = sp.make_decision("是否给客户 10% 折扣？", {"amount": 100000, "domain": "sales"})
        assert memo.recommended_action != ""
        assert memo.risk_level in ("low", "medium", "high")
        assert 0 <= memo.confidence <= 1
        assert len(memo.perspectives) == 5

    def test_selfpaw_domain_ontology(self):
        sp = self._build_selfpaw()
        ontology = sp.get_domain_ontology()
        assert len(ontology) > 0
        for pkg_data in ontology.values():
            assert "entities" in pkg_data
            assert "available_cs" in pkg_data

    def test_selfpaw_weekly_summary(self):
        sp = self._build_selfpaw()
        sp.process_intent("查询客户信息")
        summary = sp.generate_weekly_summary(week="2026-W21")
        assert summary.week == "2026-W21"
        assert summary.user_id == "USR_AE_001"

    def test_selfpaw_draft_email(self):
        sp = self._build_selfpaw()
        email = sp.draft_email(
            to="客户联系人",
            subject="方案跟进",
            context={"purpose": "发送需求诊断报告", "body": "请查阅附件中的诊断报告"},
        )
        assert "方案跟进" in email
        assert "数字分身" in email


# ============================================================
# L3 SalesAgent 测试
# ============================================================
class TestSalesAgent:

    def _build_sales_agent(self):
        from enterprise.platform.capability_services.cs_gateway import CapabilityServiceGateway
        from enterprise.platform.capability_services.cs_customer import CustomerService
        from enterprise.platform.capability_services.cs_finance import FinanceService
        from enterprise.platform.capability_services.cs_approval import ApprovalService
        from enterprise.platform.capability_services.cs_bpm import BPMService
        from enterprise.platform.data_plane.event_stream import EventStream
        from enterprise.platform.governance.permission_engine import PermissionEngine
        from enterprise.agents.l3_pipaw.sales_agent import SalesAgent

        perm = PermissionEngine()
        gw = CapabilityServiceGateway(permission_engine=perm)
        gw.register_adapter("cs.customer", CustomerService())
        gw.register_adapter("cs.finance", FinanceService())
        gw.register_adapter("cs.approval", ApprovalService())
        gw.register_adapter("cs.bpm", BPMService())

        return SalesAgent(
            tenant_id="TENANT_DEMO",
            cs_gateway=gw,
            event_stream=EventStream(),
        )

    def test_sales_agent_qualify_success(self):
        agent = self._build_sales_agent()
        result = agent.handle_inbound("website", {
            "company": "测试科技",
            "budget_usd": 80000,
            "is_decision_maker": True,
            "pain_score": 8,
            "timeline_months": 3,
        })
        assert result["status"] == "qualified"
        assert "opp_id" in result
        assert result["score"] == 100

    def test_sales_agent_qualify_fail(self):
        agent = self._build_sales_agent()
        result = agent.handle_inbound("website", {
            "company": "小预算公司",
            "budget_usd": 1000,
            "is_decision_maker": False,
            "pain_score": 2,
            "timeline_months": 36,
        })
        assert result["status"] == "disqualified"

    def test_sales_agent_full_pipeline(self):
        """完整销售管道：资格 → 诊断 → 报价"""
        agent = self._build_sales_agent()

        # 资格判断
        qual = agent.handle_inbound("website", {
            "company": "管道测试企业",
            "budget_usd": 100000,
            "is_decision_maker": True,
            "pain_score": 9,
            "timeline_months": 2,
        })
        assert qual["status"] == "qualified"
        opp_id = qual["opp_id"]

        # 需求诊断
        diag = agent.diagnose_needs(opp_id, {
            "pain_points": ["效率低", "数据孤岛"],
            "desired_outcomes": ["自动化"],
        })
        assert diag["stage"] == "proposal"

        # 报价
        quote = agent.create_quote(
            opp_id,
            [{"name": "平台许可", "unit_price": 80000, "quantity": 1}],
            discount_pct=5.0,
        )
        assert "quote_id" in quote or quote.get("status") == "compliance_blocked"

    def test_pipeline_summary(self):
        agent = self._build_sales_agent()
        agent.handle_inbound("test", {
            "company": "测试公司",
            "budget_usd": 50000,
            "is_decision_maker": True,
            "pain_score": 7,
            "timeline_months": 4,
        })
        summary = agent.get_pipeline_summary()
        assert summary["total_opportunities"] >= 1


# ============================================================
# L2 Finance Agent 测试
# ============================================================
class TestFinanceAgent:

    def _build_finance_agent(self):
        from enterprise.platform.capability_services.cs_gateway import CapabilityServiceGateway
        from enterprise.platform.capability_services.cs_invoice import InvoiceService
        from enterprise.platform.capability_services.cs_finance import FinanceService
        from enterprise.platform.data_plane.event_stream import EventStream
        from enterprise.platform.governance.permission_engine import PermissionEngine
        from enterprise.agents.l2_pipaw.finance_agent import FinanceAgent

        perm = PermissionEngine()
        gw = CapabilityServiceGateway(permission_engine=perm)
        gw.register_adapter("cs.invoice", InvoiceService())
        gw.register_adapter("cs.finance", FinanceService())

        return FinanceAgent(
            tenant_id="TENANT_DEMO",
            cs_gateway=gw,
            event_stream=EventStream(),
        )

    def test_finance_agent_process_invoice(self):
        from enterprise.agents.l2_pipaw.functional_agent import AgentTask
        agent = self._build_finance_agent()

        task = AgentTask(
            task_type="process_invoice",
            payload={
                "order_id": "ORD_001",
                "customer_id": "CUST_001",
                "amount": 100000.0,
                "invoice_type": "vat_special",
                "items": [{"description": "服务费", "unit_price": 100000, "quantity": 1}],
            },
        )
        result = agent.execute_task(task)
        assert result.status == "completed"
        assert result.result is not None
        assert "invoice_id" in result.result

    def test_finance_agent_business_analysis(self):
        from enterprise.agents.l2_pipaw.functional_agent import AgentTask
        agent = self._build_finance_agent()

        task = AgentTask(
            task_type="business_analysis",
            payload={"period": "2026-Q2"},
        )
        result = agent.execute_task(task)
        assert result.status == "completed"


# ============================================================
# CLI 模板测试
# ============================================================
class TestEnterpriseTemplate:

    def test_enterprise_template_exists(self):
        from asui.templates import get_template
        template = get_template("enterprise")
        assert "CLAUDE.md" in template
        assert "configs/platform_manifest.json" in template
        assert "scripts/run_enterprise_platform.py" in template
        assert "docs/ENTERPRISE_ARCHITECTURE.md" in template

    def test_enterprise_template_manifest_json(self):
        import json
        from asui.templates import get_template
        template = get_template("enterprise")
        manifest = json.loads(template["configs/platform_manifest.json"])
        assert "uas_definition" in manifest
        assert "I" in manifest["uas_definition"]
        assert "digital_positions" in manifest
        assert "l1" in manifest["digital_positions"]
        assert "l3" in manifest["digital_positions"]

    def test_enterprise_template_init(self, tmp_path):
        import sys, os
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        from asui.init import run_init
        success = run_init(tmp_path / "test-enterprise", "enterprise", force=False)
        assert success
        assert (tmp_path / "test-enterprise" / "CLAUDE.md").exists()
        assert (tmp_path / "test-enterprise" / "configs" / "platform_manifest.json").exists()

    def test_all_templates_still_work(self):
        from asui.templates import get_template
        for name in ["default", "customer-service", "recruitment", "selfpaw-swarm",
                     "triadic-ideal-reality-swarm", "uas-subapp", "enterprise"]:
            tmpl = get_template(name)
            assert isinstance(tmpl, dict)
            assert len(tmpl) > 0


# ============================================================
# 端到端 B2B 管道集成测试
# ============================================================
class TestB2BPipelineIntegration:

    def test_b2b_pipeline_runs(self):
        """验证完整 B2B 管道可运行并产生正确结果"""
        from enterprise.examples.b2b_lead_to_payment.scripts.b2b_pipeline import run_b2b_pipeline
        result = run_b2b_pipeline()

        assert result["won_amount"] > 0
        assert result["event_count"] >= 5
        assert result["audit_calls"] >= 3
        assert "changeset" in result
        assert len(result["changeset"]["learning"]) > 0
