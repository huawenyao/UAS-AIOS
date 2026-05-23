"""
cs.crm — CRM 连接器（后端适配器）
支持 Salesforce / HubSpot / 自研 CRM 多后端适配
Agent 调用 cs.customer，cs.customer 再调用 CRMConnector
"""
from __future__ import annotations
from typing import Dict, Optional


class CRMConnector:
    """
    CRM 适配器基类
    实现 Salesforce / HubSpot 等具体后端时继承此类
    """

    def __init__(self, backend: str = "mock", config: Dict = None):
        self.backend = backend
        self.config = config or {}
        self._mock_data: Dict[str, Dict] = {}
        self._setup()

    def _setup(self):
        # 预置 mock 数据
        self._mock_data = {
            "CUST_001": {
                "id": "CUST_001",
                "name": "云智科技",
                "industry": "SaaS",
                "company_size": "MID",
                "health_score": 78,
                "stage": "customer",
                "arr": 120000.0,
                "owner": "csm_zhang",
                "tags": ["high_value", "expansion_potential"],
            },
            "LEAD_001": {
                "id": "LEAD_001",
                "name": "数链网络",
                "industry": "FinTech",
                "company_size": "SMB",
                "health_score": 0,
                "stage": "lead",
                "arr": 0.0,
                "owner": "ae_li",
                "tags": ["inbound"],
            },
        }

    def get_customer(self, customer_id: str) -> Optional[Dict]:
        if self.backend == "mock":
            return self._mock_data.get(customer_id)
        raise NotImplementedError(f"CRM backend {self.backend} not implemented")

    def create_opportunity(self, data: Dict) -> Dict:
        if self.backend == "mock":
            opp_id = f"OPP_{len(self._mock_data) + 1:04d}"
            self._mock_data[opp_id] = {"id": opp_id, **data, "stage": "qualification"}
            return self._mock_data[opp_id]
        raise NotImplementedError

    def update_opportunity(self, opp_id: str, updates: Dict) -> Dict:
        if self.backend == "mock":
            if opp_id in self._mock_data:
                self._mock_data[opp_id].update(updates)
                return self._mock_data[opp_id]
            raise ValueError(f"Opportunity not found: {opp_id}")
        raise NotImplementedError

    def create_activity(self, activity: Dict) -> Dict:
        """记录销售活动（拜访/通话/邮件）"""
        if self.backend == "mock":
            act_id = f"ACT_{len(self._mock_data) + 1:04d}"
            self._mock_data[act_id] = {"id": act_id, **activity}
            return self._mock_data[act_id]
        raise NotImplementedError


class BPMConnector:
    """
    BPM 流程引擎适配器
    支持 Activiti / Camunda / 自研 BPM
    """

    def __init__(self, backend: str = "mock", config: Dict = None):
        self.backend = backend
        self.config = config or {}
        self._processes: Dict[str, Dict] = {}
        self._tasks: Dict[str, Dict] = {}

    def start_process(self, process_key: str, variables: Dict) -> Dict:
        """启动流程实例"""
        if self.backend == "mock":
            instance_id = f"PROC_{len(self._processes) + 1:04d}"
            instance = {
                "instance_id": instance_id,
                "process_key": process_key,
                "variables": variables,
                "status": "running",
                "current_task": self._get_first_task(process_key),
            }
            self._processes[instance_id] = instance
            return instance
        raise NotImplementedError

    def complete_task(self, task_id: str, variables: Dict = None) -> Dict:
        """完成流程任务"""
        if self.backend == "mock":
            task = self._tasks.get(task_id, {"task_id": task_id})
            task["status"] = "completed"
            task["output"] = variables or {}
            return task
        raise NotImplementedError

    def get_process_status(self, instance_id: str) -> Dict:
        return self._processes.get(instance_id, {"instance_id": instance_id, "status": "unknown"})

    def _get_first_task(self, process_key: str) -> str:
        task_map = {
            "lead_qualification": "qualify_lead",
            "quote_approval": "review_quote",
            "contract_signing": "legal_review",
            "invoice_process": "create_invoice",
            "onboarding": "account_setup",
        }
        return task_map.get(process_key, "manual_task")
