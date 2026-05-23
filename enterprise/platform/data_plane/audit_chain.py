"""
审计链
职责：所有 cs.* 调用的不可篡改审计记录
支持：调用溯源 / 合规报告 / 异常检测 / 链路追踪
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid
import hashlib


@dataclass
class AuditRecord:
    """审计记录（不可变）"""
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = ""
    caller_id: str = ""
    tenant_id: str = ""
    service: str = ""
    action: str = ""
    request_summary: str = ""
    response_status: str = ""
    latency_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    checksum: str = ""  # SHA-256 防篡改

    def compute_checksum(self) -> str:
        data = f"{self.audit_id}:{self.caller_id}:{self.service}:{self.action}:{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


class AuditChain:
    """
    不可变审计链
    生产环境可替换为 Elasticsearch / 区块链审计
    """

    def __init__(self, storage_path: Optional[str] = None):
        self._records: List[AuditRecord] = []
        self._storage_path = Path(storage_path) if storage_path else None

    def record(self, request: Any, response: Any) -> str:
        """记录 cs.* 调用审计"""
        # 提取关键信息（避免敏感数据全量记录）
        request_summary = self._summarize_request(request)

        audit = AuditRecord(
            request_id=getattr(request, "correlation_id", str(uuid.uuid4())),
            caller_id=getattr(request, "caller_id", "unknown"),
            tenant_id=getattr(request, "tenant_id", "unknown"),
            service=getattr(request, "service", ""),
            action=getattr(request, "action", ""),
            request_summary=request_summary,
            response_status=getattr(response, "status", "unknown"),
            latency_ms=getattr(response, "latency_ms", 0),
        )
        audit.checksum = audit.compute_checksum()
        self._records.append(audit)

        if self._storage_path:
            self._persist(audit)

        return audit.audit_id

    def query(
        self,
        caller_id: Optional[str] = None,
        service: Optional[str] = None,
        tenant_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[AuditRecord]:
        """查询审计记录"""
        results = list(self._records)
        if caller_id:
            results = [r for r in results if r.caller_id == caller_id]
        if service:
            results = [r for r in results if r.service == service]
        if tenant_id:
            results = [r for r in results if r.tenant_id == tenant_id]
        if start_time:
            results = [r for r in results if r.timestamp >= start_time]
        if end_time:
            results = [r for r in results if r.timestamp <= end_time]
        return results

    def compliance_report(self, tenant_id: str, period: str = "today") -> Dict:
        """合规报告"""
        records = self.query(tenant_id=tenant_id)
        service_counts: Dict[str, int] = {}
        failure_counts: Dict[str, int] = {}

        for r in records:
            service_counts[r.service] = service_counts.get(r.service, 0) + 1
            if r.response_status != "success":
                failure_counts[r.service] = failure_counts.get(r.service, 0) + 1

        return {
            "tenant_id": tenant_id,
            "period": period,
            "total_calls": len(records),
            "service_breakdown": service_counts,
            "failure_breakdown": failure_counts,
            "failure_rate": round(
                sum(failure_counts.values()) / max(len(records), 1) * 100, 2
            ),
            "unique_callers": len({r.caller_id for r in records}),
        }

    def verify_integrity(self) -> Dict:
        """验证审计链完整性（防篡改）"""
        violations = []
        for record in self._records:
            expected = record.compute_checksum()
            if record.checksum != expected:
                violations.append(record.audit_id)
        return {
            "total_records": len(self._records),
            "violations": violations,
            "integrity_ok": len(violations) == 0,
        }

    def _summarize_request(self, request: Any) -> str:
        """提取请求摘要（去除敏感字段）"""
        sensitive_keys = {"password", "token", "secret", "card_number", "id_number"}
        payload = getattr(request, "payload", {})
        safe_payload = {
            k: "***" if k.lower() in sensitive_keys else v
            for k, v in (payload.items() if isinstance(payload, dict) else {})
        }
        return json.dumps(safe_payload, ensure_ascii=False)[:200]

    def _persist(self, record: AuditRecord):
        """持久化审计记录（追加模式）"""
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._storage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "audit_id": record.audit_id,
                "request_id": record.request_id,
                "caller_id": record.caller_id,
                "tenant_id": record.tenant_id,
                "service": record.service,
                "action": record.action,
                "status": record.response_status,
                "timestamp": record.timestamp,
                "checksum": record.checksum,
            }, ensure_ascii=False) + "\n")
