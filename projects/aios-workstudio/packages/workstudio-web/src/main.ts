import { HubClient, HUB_DEFAULT, createSceneClient } from "../../hub-client/src/index.ts";

const app = document.getElementById("app")!;
const hub = new HubClient(import.meta.env.VITE_HUB ?? HUB_DEFAULT, {
  tenantId: "t-hengchuan",
  actorId: "cowen.hua",
  track: "pipaw",
});
const scene = createSceneClient(hub);

async function boot() {
  try {
    const pack = (await scene.packOpen("pos-cm")) as {
      nodes?: { node_id: string; kpi?: { name?: string; is?: unknown; stale?: boolean } }[];
    };
    const gates = (pack.nodes || [])
      .map((n) => `<li>${n.node_id} · ${n.kpi?.name ?? ""} ${n.kpi?.stale ? "(口径延迟)" : ""}</li>`)
      .join("");
    app.innerHTML = `<h1>今日必办</h1><ul>${gates || "<li>无切片</li>"}</ul><p>P0 完整壳仍在 /demo</p>`;
  } catch (err) {
    const body = err as { error?: { message?: string; next?: string } };
    app.innerHTML = `<h1>作战台暂不可用</h1><p>${body.error?.message ?? "请稍后重试"}</p><p>${body.error?.next ?? ""}</p>`;
  }
}

boot();
