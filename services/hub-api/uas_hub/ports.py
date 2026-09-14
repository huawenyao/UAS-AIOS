"""全局 Port SPI。Hub 只经这些端口访问零件；零件可换，方法名不换。"""

from __future__ import annotations

from typing import Any, Protocol


class CubePort(Protocol):
    """M15 口径。失败必须 stale=True，不得假装实时，不得签发。"""

    def query(
        self,
        kpi_id: str,
        *,
        grain: str = "",
        start: str = "",
        end: str = "",
        dimensions: dict[str, Any] | None = None,
        available: bool = True,
    ) -> dict[str, Any]: ...


class KgPort(Protocol):
    """M16 时态知识。节点 ID 禁止 an-*；ingest ≠ cs 写。"""

    def search(
        self,
        *,
        object_ref: str | None = None,
        query: str | None = None,
        valid_at: str | None = None,
        as_of: str | None = None,
    ) -> list[dict[str, Any]]: ...

    def ingest_episode(self, episode: dict[str, Any]) -> dict[str, Any]: ...


class MemoryPort(Protocol):
    """M17 个人记忆。库隔离由实现保证；轨道禁令由 Hub 先判。"""

    def add(self, actor_id: str, text: str) -> dict[str, Any]: ...

    def search(self, actor_id: str, query: str) -> list[dict[str, Any]]: ...

    def forget(self, actor_id: str, memory_id: str) -> dict[str, Any]: ...


class InnerLoopPort(Protocol):
    """M19 内环。工具只回调 Hub；禁止出站 SoR。"""

    def start_thread(self, profile: str, tool_allowlist: list[str], track: str) -> str: ...

    def turn(self, thread_id: str, payload: dict[str, Any]) -> dict[str, Any]: ...

    def interrupt(self, thread_id: str) -> dict[str, Any]: ...

    def resume(self, thread_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]: ...

    def compact(self, thread_id: str) -> dict[str, Any]: ...


class McpPort(Protocol):
    """M13 MCP 壳。list 过滤；call 必须重走 PolicyChain。"""

    def list_tools(self, env: Any) -> list[dict[str, Any]]: ...

    def call_tool(self, env: Any, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]: ...


class SkillPort(Protocol):
    """M9 状态机：discovered → previewed → cited → installed → enabled → executed。"""

    def transition(self, skill_id: str, to_state: str, profile: str) -> dict[str, Any]: ...

    def state_of(self, skill_id: str) -> str: ...


class LawPort(Protocol):
    """M4 法则编译。未审批 ChangeSet 不得进入 compiled。"""

    def compile(self, pack_id: str, changeset_approved: bool) -> dict[str, Any]: ...


class ArtifactPort(Protocol):
    """M10 制品。kind=file 不能作为 pack.open 状态源。"""

    def put(self, kind: str, body: bytes | dict[str, Any]) -> dict[str, Any]: ...

    def get(self, artifact_id: str) -> dict[str, Any]: ...

    def usable_as_pack_state(self, artifact_id: str) -> bool: ...


class BrokerPort(Protocol):
    """M24 模型路由。换提供商不得改 hub.*。"""

    def complete(self, route_id: str, messages: list[dict[str, Any]]) -> dict[str, Any]: ...


class ConnectorPort(Protocol):
    """M14/M23 系统适配。密钥不得出现在返回或 tool description。"""

    id: str

    def invoke(
        self,
        operation: str,
        payload: dict[str, Any],
        scope: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]: ...

    def health(self) -> dict[str, Any]: ...


class EvolutionPort(Protocol):
    """M12 演化。auto_apply 永远为 false。"""

    auto_apply: bool

    def draft(self, signal: dict[str, Any]) -> dict[str, Any]: ...

    def apply(self, changeset_id: str, approved: bool) -> dict[str, Any]: ...


class IamPort(Protocol):
    """M8 岗位绑定。无岗位则切片拒绝。"""

    def bind(self, actor_id: str, tenant_id: str, position_id: str) -> dict[str, Any]: ...

    def position_of(self, actor_id: str, tenant_id: str) -> str | None: ...


class ReviewPort(Protocol):
    """M22 Utopia Spike。只读导出，禁止写路径。"""

    def export_candidates(self, query: str) -> dict[str, Any]: ...


from uas_hub.outer_loop import OuterLoopPort as OuterLoopPort
