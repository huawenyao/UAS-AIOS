window.HUB_PACK = {
  "envelope": {
    "tenant_id": "t-hengchuan",
    "actor_id": "cowen.hua",
    "profile": "scene",
    "track": "pipaw",
    "position_id": "pos-cm"
  },
  "pack": {
    "graph_id": "ag-hengchuan-ltc",
    "tenant_id": "t-hengchuan",
    "nodes": [
      {
        "node_id": "an-stage-visit",
        "parent_id": null,
        "goal": {
          "statement": "把衡川客户经理的阶段拜访停留压回 SLA 以内",
          "horizon": "2026-Q3",
          "success_criteria": "an-stage-visit 的 kpi.is <= 14"
        },
        "org": {
          "unit_id": "org.team-ltc",
          "position_id": "pos-cm",
          "owner_id": "cowen.hua",
          "raci": "A"
        },
        "kpi": {
          "kpi_id": "kpi-visit-dwell",
          "name": "阶段停留天数",
          "unit": "day",
          "caliber": "now - stage_entered_at",
          "ought": 14,
          "is": 28,
          "status": "gate",
          "as_of": "2026-09-12T12:04:29Z",
          "stale": false,
          "caliber_id": "now - stage_entered_at"
        },
        "process": {
          "value_stream": "LTC 线索到回款",
          "stage": "qualify",
          "cs_read": [
            "cs.visit.list",
            "cs.metric.query"
          ],
          "cs_write": [
            "cs.visit.schedule"
          ],
          "system_of_record": "crm"
        },
        "wm": {
          "space": "cn.east.ltc",
          "time": "2026-08",
          "subject": "cowen.hua",
          "object": "UEC-10293",
          "feedback": "visit.scheduled -> kpi.is"
        },
        "object_refs": [
          "UEC-10293"
        ],
        "_incomplete": null
      }
    ],
    "insights_open_count": 0,
    "tasks_open_count": 0
  },
  "tools_scene": [
    "cs.customer.get_profile",
    "cs.customer.query",
    "cs.lead.list",
    "cs.metric.query",
    "cs.notify.send_email",
    "cs.process.advance",
    "cs.visit.list"
  ],
  "tools_runtime": [
    "cs.approval.submit",
    "cs.customer.get_profile",
    "cs.customer.query",
    "cs.lead.list",
    "cs.lead.qualify_lead",
    "cs.metric.query",
    "cs.notify.send_email",
    "cs.notify.send_im",
    "cs.process.advance",
    "cs.process.start",
    "cs.ticket.create",
    "cs.ticket.escalate",
    "cs.visit.list",
    "cs.visit.schedule"
  ],
  "write_blocked": {
    "error": {
      "code": "PROFILE_FORBIDS_SIDE_EFFECT",
      "message": "现在是作战台，不能改 CRM。请签发任务后进入运行。",
      "explain_ref": "hub.policy.explain",
      "next": "hub.scene.task.issue",
      "retryable": false,
      "detail": ""
    }
  },
  "issued_task": {
    "task_id": "tsk-an-stage-visit-001",
    "tenant_id": "t-hengchuan",
    "source_node_id": "an-stage-visit",
    "insight_id": "ins-an-stage-visit-drill",
    "assignee": {
      "owner_id": "zhangsan",
      "position_id": "pos-bd"
    },
    "due": null,
    "cs_write": [
      "cs.visit.schedule"
    ],
    "evidence_refs": [
      "ep-visit-20260715"
    ],
    "status": "issued",
    "track": "pipaw",
    "workflow_id": null,
    "issued_at": "2026-09-12T12:04:29Z"
  },
  "explain": {
    "PROFILE_FORBIDS_SIDE_EFFECT": {
      "message": "现在是作战台，不能改 CRM。请签发任务后进入运行。",
      "next": "hub.scene.task.issue"
    },
    "TASK_SOURCE_REQUIRED": {
      "message": "经营任务必须带责任图源节点。",
      "next": "从今日必办选择节点再签发"
    },
    "UNGROUNDED_INSIGHT": {
      "message": "建议还没有证据，不能派活。",
      "next": "补时间线或口径证据后再 drill"
    },
    "WM_INCOMPLETE": {
      "message": "这个位置还没建模完整（缺五维），不能签发。",
      "next": "请知识管理员补世界模型投影"
    },
    "TENANT_MISMATCH": {
      "message": "当前账号不属于这张经营图的租户。",
      "next": "联系平台管理员开通岗位"
    },
    "MEMORY_TRACK_FORBIDDEN": {
      "message": "经营轨道不能读个人记忆。",
      "next": "使用岗位上下文而不是个人备忘"
    },
    "TRACK_ESCALATION_REQUIRED": {
      "message": "个人轨道不能直接写经营系统，需要带证据升级。",
      "next": "提交升级工单"
    },
    "THREAD_PROFILE_IMMUTABLE": {
      "message": "同一会话不能改剖面，请新开执行。",
      "next": "新开 Thread"
    },
    "CALIBER_MISSING": {
      "message": "这个指标还没有口径，数字不能当经营事实。",
      "next": "配置 caliber 后再打开作战台"
    },
    "OPERATION_NOT_FOUND": {
      "message": "能力目录里没有这个动作，或本租户未启用。",
      "next": "在能力网格启用 operation"
    },
    "GATE_BLOCKED": {
      "message": "治理门禁拒绝了这次调用。",
      "next": "查看审计与门禁说明"
    },
    "SCOPE_DENIED": {
      "message": "当前范围看不到这些客户或数据。",
      "next": "申请更大 scope 或换岗位"
    },
    "INVARIANT_FAILED": {
      "message": "发布前检查没过，不能进入运行。",
      "next": "修复 invariant 后再 release"
    },
    "SKILL_NOT_EXECUTABLE_IN_PROFILE": {
      "message": "现在只能引用技能，不能执行。",
      "next": "安装并在运行态启用后再用"
    },
    "TASK_NOT_ISSUED": {
      "message": "还没有签发的经营任务，不能进入运行。",
      "next": "hub.scene.task.issue"
    }
  }
};
