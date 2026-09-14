/** 套件 B · Console 壳。只调 hub.ops.*，禁止 invoke_cs / kg ingest。 */

import { HubClient } from "./http.js";

export function createOpsClient(hub: HubClient) {
  return {
    tenantGet: () => hub.get("/hub/v1/ops/tenant/get"),
    healthSummary: () => hub.get("/hub/v1/ops/health/summary"),
    matrix: () => hub.get("/hub/v1/ops/profile/matrix"),
    policyExplain: (body: unknown) => hub.post("/hub/v1/ops/policy/explain", body),
    protocolRegistry: () => hub.get("/hub/v1/ops/protocol/registry"),
    protocolContracts: () => hub.get("/hub/v1/ops/protocol/contracts"),
    policySimulate: (body: unknown) => hub.post("/hub/v1/ops/policy/simulate", body),
    graphGet: (body: unknown) => hub.post("/hub/v1/ops/graph/get", body),
    graphValidate: (body: unknown) => hub.post("/hub/v1/ops/graph/validate", body),
    graphPublish: (body: unknown) => hub.post("/hub/v1/ops/graph/publish", body),
    wmGet: (body: unknown) => hub.post("/hub/v1/ops/wm/get", body),
    lawDiff: (body: unknown) => hub.post("/hub/v1/ops/law/diff", body),
    registryList: () => hub.get("/hub/v1/ops/registry/list"),
    registryPatch: (body: unknown) => hub.post("/hub/v1/ops/registry/patch", body),
    mcpPreview: (profile: string) =>
      hub.get(`/hub/v1/ops/mcp/preview?profile=${encodeURIComponent(profile)}`),
    connectorList: () => hub.get("/hub/v1/ops/connector/list"),
    connectorRotate: (body: unknown) => hub.post("/hub/v1/ops/connector/rotate", body),
    schemaDrift: () => hub.get("/hub/v1/ops/schema/drift"),
    iamBindings: () => hub.get("/hub/v1/ops/iam/bindings"),
    skillList: () => hub.get("/hub/v1/ops/skill/list"),
    artifactList: () => hub.get("/hub/v1/ops/artifact/list"),
    caliberStatus: () => hub.get("/hub/v1/ops/caliber/status"),
    kgSearch: (body: unknown) => hub.post("/hub/v1/ops/kg/search", body),
    kgIngestStatus: () => hub.get("/hub/v1/ops/kg/ingest_status"),
    memoryReceipt: (q = "") =>
      hub.get(`/hub/v1/ops/memory/receipt?q=${encodeURIComponent(q)}`),
    runtimeTask: (q = "") =>
      hub.get(`/hub/v1/ops/runtime/task?q=${encodeURIComponent(q)}`),
    runtimeRetry: (body: unknown) => hub.post("/hub/v1/ops/runtime/retry", body),
    modelRoute: () => hub.get("/hub/v1/ops/model/route"),
    changesetList: () => hub.get("/hub/v1/ops/changeset/list"),
    changesetSubmit: (body: unknown) => hub.post("/hub/v1/ops/changeset/submit", body),
    changesetDecide: (body: unknown) => hub.post("/hub/v1/ops/changeset/decide", body),
    auditSearch: (q = "") =>
      hub.get(`/hub/v1/ops/audit/search?q=${encodeURIComponent(q)}`),
    auditExport: (q = "") =>
      hub.get(`/hub/v1/ops/audit/export?q=${encodeURIComponent(q)}`),
  };
}
