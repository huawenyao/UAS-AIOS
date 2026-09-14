"""M14 系统适配夹具。幂等；密钥不得出现在返回。"""

from __future__ import annotations

from typing import Any

_SECRET_TOKENS = ("token", "password", "secret", "api_key")


class FixtureConnector:
    id = "connector.crm.mock"

    def __init__(self) -> None:
        self._results: dict[str, dict[str, Any]] = {}
        self.write_count = 0
        self.call_count = 0

    def invoke(
        self,
        operation: str,
        payload: dict[str, Any],
        scope: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        _ = payload, scope
        self.call_count += 1
        cached = self._results.get(idempotency_key)
        if cached is not None:
            return dict(cached)
        self.write_count += 1
        result = {
            "result_code": "ok",
            "data": {
                "operation": operation,
                "accepted": True,
                "idempotency_key": idempotency_key,
            },
            "connector_id": self.id,
        }
        _reject_secrets(result)
        self._results[idempotency_key] = result
        return dict(result)

    def health(self) -> dict[str, Any]:
        return {"ok": True, "secrets_exposed": False}


def _reject_secrets(obj: Any) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            lowered = str(key).lower()
            if any(token in lowered for token in _SECRET_TOKENS):
                raise AssertionError(f"secret field leaked: {key}")
            _reject_secrets(value)
    elif isinstance(obj, list):
        for item in obj:
            _reject_secrets(item)
    elif isinstance(obj, str):
        lowered = obj.lower()
        if any(token == lowered for token in _SECRET_TOKENS):
            raise AssertionError("secret value leaked")
