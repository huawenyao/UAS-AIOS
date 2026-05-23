"""
企业语义能力服务层 cs.*
Agent 不直连 CRM/BPM，只调用语义能力服务，
由平台做权限、翻译、审计、重试。
"""
from .cs_gateway import CapabilityServiceGateway
from .cs_customer import CustomerService
from .cs_approval import ApprovalService
from .cs_invoice import InvoiceService
from .cs_crm import CRMConnector
from .cs_bpm import BPMConnector
from .cs_finance import FinanceService

__all__ = [
    "CapabilityServiceGateway",
    "CustomerService",
    "ApprovalService",
    "InvoiceService",
    "CRMConnector",
    "BPMConnector",
    "FinanceService",
]
