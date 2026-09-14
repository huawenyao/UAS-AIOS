(() => {
  "use strict";
  const DEFAULT = "http://127.0.0.1:18088";
  function headers() {
    return {
      "Content-Type": "application/json",
      "X-Tenant-Id": "t-hengchuan",
      "X-Actor-Id": "cowen.hua",
      "X-Track": "pipaw",
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
  window.HubScene = {
    packOpen: (position_id) => req("POST", "/hub/v1/scene/pack/open", { position_id }),
    insightDrill: (source_node_id, evidence_refs) =>
      req("POST", "/hub/v1/scene/insight/drill", { source_node_id, evidence_refs }),
    taskIssue: (body) => req("POST", "/hub/v1/scene/task/issue", body),
    explain: (code) => req("GET", "/hub/v1/policy/explain?code=" + encodeURIComponent(code)),
    invokeCs: (operation, input) =>
      req("POST", "/hub/v1/scene/invoke_cs", { operation, input }),
    execOpen: (task_id) => req("POST", "/hub/v1/exec/open", { task_id }),
    cycleStep: (task_id, signal) =>
      req("POST", "/hub/v1/instance/cycle_step", { task_id, signal }),
    eventsPoll: (task_id) =>
      req("GET", "/hub/v1/exec/" + encodeURIComponent(task_id) + "/events"),
  };
})();
