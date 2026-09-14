/** 套件 A · 使用平面。只消费 hub.scene.* / exec SSE / policy.explain。 */

import { HubClient } from "./http.js";

export function createSceneClient(hub: HubClient) {
  return {
    packList: () => hub.get<{ packs: unknown[] }>("/hub/v1/scene/pack/list"),
    packOpen: (position_id: string, period?: unknown) =>
      hub.post("/hub/v1/scene/pack/open", { position_id, period }),
    insightList: () => hub.get("/hub/v1/scene/insight/list"),
    insightDrill: (source_node_id: string, evidence_refs?: unknown[]) =>
      hub.post("/hub/v1/scene/insight/drill", { source_node_id, evidence_refs }),
    taskIssue: (body: Record<string, unknown>) => hub.post("/hub/v1/scene/task/issue", body),
    taskReturn: (body: Record<string, unknown>) => hub.post("/hub/v1/scene/task/return", body),
    execOpen: (task_id: string) => hub.post("/hub/v1/exec/open", { task_id }),
    cycleStep: (task_id: string, signal: string) =>
      hub.post("/hub/v1/instance/cycle_step", { task_id, signal }),
    explain: (code: string) => hub.get(`/hub/v1/policy/explain?code=${encodeURIComponent(code)}`),
    eventsUrl: (task_id: string) => `${hub.baseUrl}/hub/v1/exec/${task_id}/events`,
  };
}
