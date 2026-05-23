"""
企业租户管理
职责：租户隔离 / 主数据 scope / 岗位权限绑定 / SSO 会话
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TenantConfig:
    tenant_id: str
    name: str
    industry: str
    tier: str             # startup / growth / enterprise
    enabled_modules: List[str]
    data_region: str      # cn-north / cn-south / global
    sso_provider: Optional[str] = None
    max_agents: int = 100
    custom_domain_packages: List[str] = field(default_factory=list)


@dataclass
class OrgIdentity:
    """员工组织身份 — SelfPaw 企业版能力1"""
    user_id: str
    tenant_id: str
    employee_id: str
    name: str
    position: str         # 岗位：sales_ae / csm / hr / finance / dev
    department: str
    roles: List[str]      # RBAC 角色
    data_scope: Dict      # 可访问数据范围 {customers: "own", reports: "department"}
    l1_agent_id: Optional[str] = None  # 绑定的 SelfPaw Agent ID
    manager_id: Optional[str] = None


class TenantManager:
    """
    企业租户管理器
    核心原则：数据主权隔离，跨租户禁止直接访问
    """

    def __init__(self):
        self._tenants: Dict[str, TenantConfig] = {}
        self._identities: Dict[str, OrgIdentity] = {}
        self._sso_sessions: Dict[str, Dict] = {}
        self._setup_demo_tenant()

    def _setup_demo_tenant(self):
        """初始化演示租户"""
        demo_tenant = TenantConfig(
            tenant_id="TENANT_DEMO",
            name="演示企业",
            industry="SaaS",
            tier="enterprise",
            enabled_modules=["l1_selfpaw", "l2_pipaw", "l3_pipaw", "cs_customer", "cs_approval", "cs_finance"],
            data_region="cn-north",
            sso_provider="mock_sso",
        )
        self._tenants["TENANT_DEMO"] = demo_tenant

        # 演示员工
        employees = [
            OrgIdentity("USR_AE_001", "TENANT_DEMO", "EMP_001", "李明", "sales_ae", "销售部",
                        ["sales_ae", "l1_user"], {"customers": "own", "opportunities": "own"}),
            OrgIdentity("USR_CSM_001", "TENANT_DEMO", "EMP_002", "王芳", "csm", "客户成功部",
                        ["csm", "l1_user"], {"customers": "team", "health_scores": "all"}),
            OrgIdentity("USR_HR_001", "TENANT_DEMO", "EMP_003", "张伟", "hr_bp", "人力资源部",
                        ["hr", "l2_user"], {"employees": "all", "salaries": "restricted"}),
            OrgIdentity("USR_FIN_001", "TENANT_DEMO", "EMP_004", "陈丽", "finance", "财务部",
                        ["finance", "l2_user"], {"invoices": "all", "payments": "all"}),
            OrgIdentity("USR_MGR_001", "TENANT_DEMO", "EMP_005", "赵总", "sales_manager", "销售部",
                        ["sales_manager", "approver", "l2_user"],
                        {"customers": "department", "opportunities": "department", "quotes": "all"}),
        ]
        for emp in employees:
            self._identities[emp.user_id] = emp

    def register_tenant(self, config: TenantConfig) -> str:
        self._tenants[config.tenant_id] = config
        return config.tenant_id

    def get_tenant(self, tenant_id: str) -> Optional[TenantConfig]:
        return self._tenants.get(tenant_id)

    def bind_org_identity(self, identity: OrgIdentity) -> str:
        self._identities[identity.user_id] = identity
        return identity.user_id

    def get_identity(self, user_id: str) -> Optional[OrgIdentity]:
        return self._identities.get(user_id)

    def get_data_scope(self, user_id: str, resource_type: str) -> str:
        identity = self._identities.get(user_id)
        if not identity:
            return "none"
        return identity.data_scope.get(resource_type, "none")

    def validate_cross_tenant(self, user_id: str, target_tenant_id: str) -> bool:
        identity = self._identities.get(user_id)
        if not identity:
            return False
        return identity.tenant_id == target_tenant_id

    def list_positions(self, tenant_id: str) -> List[str]:
        return list({
            i.position for i in self._identities.values()
            if i.tenant_id == tenant_id
        })

    def get_domain_packages(self, user_id: str) -> List[str]:
        """获取用户岗位对应的 Domain 包"""
        identity = self._identities.get(user_id)
        if not identity:
            return []
        position_domain_map = {
            "sales_ae": ["sales_ontology", "b2b_saas"],
            "csm": ["customer_success_ontology", "b2b_saas"],
            "hr_bp": ["hr_ontology", "recruitment"],
            "finance": ["finance_ontology", "invoice_process"],
            "sales_manager": ["sales_ontology", "approval_matrix", "b2b_saas"],
        }
        return position_domain_map.get(identity.position, ["default_ontology"])
