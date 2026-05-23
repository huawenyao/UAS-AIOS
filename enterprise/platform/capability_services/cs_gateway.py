"""
cs.* 语义能力服务网关
职责：权限校验 → 语义翻译 → 后端适配器路由 → 审计记录 → 重试
Agent 调用唯一入口，屏蔽所有底层 CRM/BPM/ERP 差异。
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from ..data_plane.audit_chain import AuditChain
from ..governance.permission_engine import PermissionEngine


@dataclass
class CSRequest:
    """能力服务调用请求"""
    service: str          # cs.customer / cs.approval / cs.invoice ...
    action: str           # qualify_lead / create_quote / approve / ...
    payload: Dict[str, Any]
    caller_id: str        # Agent ID 或 User ID
    tenant_id: str
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_context: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CSResponse:
    """能力服务调用响应"""
    request_id: str
    service: str
    action: str
    status: str           # success / failure / pending
    result: Any
    error: Optional[str] = None
    audit_id: Optional[str] = None
    latency_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CapabilityServiceGateway:
    """
    平台级语义能力服务网关
    核心三原则：
    1. Agent 只调用语义接口，不直连业务系统
    2. 权限由平台统一校验，不由 Agent 自判
    3. 所有调用全量审计，支持回溯
    """

    def __init__(
        self,
        permission_engine: Optional[PermissionEngine] = None,
        audit_chain: Optional[AuditChain] = None,
        max_retries: int = 3,
        retry_delay_ms: int = 500,
    ):
        self._permission = permission_engine or PermissionEngine()
        self._audit = audit_chain or AuditChain()
        self._max_retries = max_retries
        self._retry_delay_ms = retry_delay_ms
        self._adapters: Dict[str, Callable] = {}
        self._service_registry: Dict[str, Dict] = {}

    # ------------------------------------------------------------------
    # 注册适配器
    # ------------------------------------------------------------------
    def register_adapter(self, service_name: str, adapter: Callable, metadata: Dict = None):
        """注册后端适配器（CRM / BPM / ERP 连接器）"""
        self._adapters[service_name] = adapter
        self._service_registry[service_name] = metadata or {}

    # ------------------------------------------------------------------
    # 核心调用链：权限 → 执行 → 审计
    # ------------------------------------------------------------------
    def invoke(self, request: CSRequest) -> CSResponse:
        """同步调用能力服务"""
        start_ms = int(time.time() * 1000)

        # 1. 权限校验
        perm_result = self._permission.check(
            caller_id=request.caller_id,
            tenant_id=request.tenant_id,
            service=request.service,
            action=request.action,
            context=request.payload,
        )
        if not perm_result.allowed:
            resp = CSResponse(
                request_id=request.correlation_id,
                service=request.service,
                action=request.action,
                status="failure",
                result=None,
                error=f"PERMISSION_DENIED: {perm_result.reason}",
            )
            self._audit.record(request, resp)
            return resp

        # 2. 查找适配器
        adapter = self._adapters.get(request.service)
        if not adapter:
            resp = CSResponse(
                request_id=request.correlation_id,
                service=request.service,
                action=request.action,
                status="failure",
                result=None,
                error=f"SERVICE_NOT_FOUND: {request.service}",
            )
            self._audit.record(request, resp)
            return resp

        # 3. 执行（带重试）
        last_error = None
        for attempt in range(1, self._max_retries + 1):
            try:
                result = adapter(action=request.action, payload=request.payload, context=request)
                latency = int(time.time() * 1000) - start_ms
                resp = CSResponse(
                    request_id=request.correlation_id,
                    service=request.service,
                    action=request.action,
                    status="success",
                    result=result,
                    latency_ms=latency,
                )
                audit_id = self._audit.record(request, resp)
                resp.audit_id = audit_id
                return resp
            except Exception as exc:
                last_error = str(exc)
                if attempt < self._max_retries:
                    time.sleep(self._retry_delay_ms / 1000 * attempt)

        # 所有重试失败
        latency = int(time.time() * 1000) - start_ms
        resp = CSResponse(
            request_id=request.correlation_id,
            service=request.service,
            action=request.action,
            status="failure",
            result=None,
            error=f"MAX_RETRIES_EXCEEDED: {last_error}",
            latency_ms=latency,
        )
        self._audit.record(request, resp)
        return resp

    def list_services(self) -> Dict[str, Dict]:
        """返回已注册的服务清单"""
        return dict(self._service_registry)
