(() => {
  "use strict";
  const DEFAULT = "http://127.0.0.1:18088";
  function headers() {
    const role = (window.CONSOLE_OPS_ROLE || "admin");
    return {
      "Content-Type": "application/json",
      "X-Tenant-Id": "t-hengchuan",
      "X-Actor-Id": "cowen.hua",
      "X-Track": "pipaw",
      "X-Ops-Role": role,
    };
  }
  async function req(method, path, body) {
    const res = await fetch((window.HUB_BASE || DEFAULT) + path, {
      method,
      headers: headers(),
      body: body == null ? undefined : JSON.stringify(body),
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
  }
  window.HubOps = {
    tenantGet: () => req("GET", "/hub/v1/ops/tenant/get"),
    healthSummary: () => req("GET", "/hub/v1/ops/health/summary"),
    schemaDrift: () => req("GET", "/hub/v1/ops/schema/drift"),
    matrix: () => req("GET", "/hub/v1/ops/profile/matrix"),
    policyExplain: (code) => req("POST", "/hub/v1/ops/policy/explain", { code }),
    protocolRegistry: () => req("GET", "/hub/v1/ops/protocol/registry"),
    protocolContracts: () => req("GET", "/hub/v1/ops/protocol/contracts"),
    policySimulate: (body) => req("POST", "/hub/v1/ops/policy/simulate", body),
    graphGet: (body) => req("POST", "/hub/v1/ops/graph/get", body || {}),
    graphValidate: (body) => req("POST", "/hub/v1/ops/graph/validate", body || {}),
    graphPublish: (body) => req("POST", "/hub/v1/ops/graph/publish", body || {}),
    wmGet: (body) => req("POST", "/hub/v1/ops/wm/get", body),
    lawDiff: (body) => req("POST", "/hub/v1/ops/law/diff", body || {}),
    registryList: () => req("GET", "/hub/v1/ops/registry/list"),
    registryPatch: (body) => req("POST", "/hub/v1/ops/registry/patch", body),
    mcpPreview: (profile) => req("GET", "/hub/v1/ops/mcp/preview?profile=" + encodeURIComponent(profile || "scene")),
    connectorList: () => req("GET", "/hub/v1/ops/connector/list"),
    connectorRotate: (body) => req("POST", "/hub/v1/ops/connector/rotate", body || {}),
    skillList: () => req("GET", "/hub/v1/ops/skill/list"),
    iamBindings: () => req("GET", "/hub/v1/ops/iam/bindings"),
    changesetList: () => req("GET", "/hub/v1/ops/changeset/list"),
    changesetSubmit: (body) => req("POST", "/hub/v1/ops/changeset/submit", body),
    changesetDecide: (body) => req("POST", "/hub/v1/ops/changeset/decide", body),
    auditSearch: (q) => req("GET", "/hub/v1/ops/audit/search?q=" + encodeURIComponent(q || "")),
    auditExport: (q) => req("GET", "/hub/v1/ops/audit/export?q=" + encodeURIComponent(q || "")),
    caliberStatus: () => req("GET", "/hub/v1/ops/caliber/status"),
    kgIngestStatus: () => req("GET", "/hub/v1/ops/kg/ingest_status"),
    kgSearch: (body) => req("POST", "/hub/v1/ops/kg/search", body || {}),
    runtimeTask: (q) => req("GET", "/hub/v1/ops/runtime/task?q=" + encodeURIComponent(q || "")),
    runtimeRetry: (body) => req("POST", "/hub/v1/ops/runtime/retry", body || {}),
    artifactList: () => req("GET", "/hub/v1/ops/artifact/list"),
    modelRoute: () => req("GET", "/hub/v1/ops/model/route"),
    memoryReceipt: (q) => req("GET", "/hub/v1/ops/memory/receipt?q=" + encodeURIComponent(q || "")),
    memoryForget: (body) => req("POST", "/hub/v1/ops/memory/forget", body || {}),
    automationJobs: () => req("GET", "/hub/v1/ops/automation/jobs"),
    automationRun: (body) => req("POST", "/hub/v1/ops/automation/run", body || {}),
    wmList: () => req("GET", "/hub/v1/ops/wm/list"),
  };
})();
