# LifeWake Beta：Ritual Shell 信息架构与礼物能力规格

> 版本：v0.2 Beta 规格基线 · 2026-09-14  
> 上游：[PRODUCT_ESSENCE_CARRIER_AND_TECH](./PRODUCT_ESSENCE_CARRIER_AND_TECH.md) · [PRODUCT_EXPERIENCE_DESIGN](./PRODUCT_EXPERIENCE_DESIGN.md) · [PRODUCT_CHARTER](./PRODUCT_CHARTER.md)  
> 下游：[CAPABILITY_CONTRACTS](./CAPABILITY_CONTRACTS.md) · [DOMAIN_MODEL](./DOMAIN_MODEL.md) · [MVP_ACCEPTANCE_CASES](./MVP_ACCEPTANCE_CASES.md) CASE-015～017  
> 目标：把「仪式壳 + 主权核 + 礼物病毒」落成可设计、可实现、可验收的 Beta 规格。

---

## 0. Beta 范围

### 0.1 做

| 项 | 说明 |
|---|---|
| Ritual Shell 客户端 IA | 首路径单点击穿，无功能宫格 |
| 单人击穿闭环 | 材料 →（可 defer）→ 揭晓 → 反馈 → 可选保存 |
| 双人击穿闭环 | 邀请 → 双方同意 → 共同仪式 → 共享撤回 |
| Gift Edge | 可过期、无原料、可撤销的仪式礼物令牌与落地体验 |
| 主权稳定层 | Consent / 撤回 / 导出入口始终可达 |

### 0.2 不做（Beta）

- 无限 Ritual 流、推荐、签到、XP、亲密分、排行
- 站外原料预览、自动代发到社媒
- 真实医疗级设备 SDK 与生产级多模态 SLA（可用高质量 mock / 有限真实生成）
- Studio 完整创作者市场（保留内测策展）
- 小程序作为主壳（仅允许作为礼物落地的可选通道，须同契约）

---

## 1. Ritual Shell 信息架构

### 1.1 空间模型（用户感知）

```text
┌──────────────────────────────────────────────┐
│                 LifeWake Home                 │
│         （安静态 / 一件待揭晓 / 入口）            │
└───────────┬──────────────┬───────────┬────────┘
            │              │           │
            ▼              ▼           ▼
     「为此刻做一件事」  「送给 TA」   次要：Vault / 同意 / Bond
            │              │
            ▼              ▼
        RitualView      Gift Compose
            │              │
            ▼              ▼
     Feedback / Save   过期链接落地页
```

**硬规则：**

1. Home **不是**功能宫格；主视觉只有：安静说明、或一件可揭晓仪式、或两个主入口。
2. Consent Center、Vault、Bond Rights 从稳定控制区进入，不抢首屏叙事。
3. 同时最多 **一个** `ready` 仪式占据主焦点（TS-P2 / TS-U1）。

### 1.2 导航与深度

| 表面 | 深度 | 进入方式 | 退出 |
|---|---|---|---|
| Home | 0 | 冷启动 | — |
| Create Moment | 1 | 主 CTA | 取消回 Home 安静态 |
| Source Picker | 2 | Create 内 | 跳过单项 / 返回 |
| Weaving / Deferred | 1–2 | 系统态 | 取消；无倒计时 |
| RitualView | 1 | 揭晓 | 保存/删除/稍后 → Home 或 Vault |
| Gift Compose | 1 | 仪式后 CTA 或 Home「送给 TA」 | 取消；令牌未 mint 则无外链 |
| Gift Landing | 外部 | 令牌 URL | 体验后「我也做一个」或离开 |
| Duet Invite / Bond Space | 1–2 | 邀请或次要入口 | 拒绝私密；暂停不惩罚 |
| Consent Center | 1 | 稳定层 | 撤回即时生效 |
| Keepsake Vault | 1 | 稳定层 / 保存后 | 导出删除对等 |
| Feedback Sheet | modal | 揭晓后 | 负反馈一步完成 |

### 1.3 Home 三态

| 态 | 用户看见 | 主动作 | 禁止 |
|---|---|---|---|
| `empty_calm` | 「准备好时，为此刻做一件事」 | Create / 可选 Gift | 推荐填充、红点 |
| `ready_focus` | 一件仪式封面：标题、模态、为何现在、稍后 | 揭晓 / 稍后 | 第二件并排强推 |
| `deferred_quiet` | 「已安静放回灵感池」+ 可理解原因 | 查看原因 / 取消 | 倒计时、羞耻召回 |

### 1.4 稳定控制层（所有仪式态可见）

固定可达（不随 `visual_theme` 消失）：

- 返回 / 关闭  
- 暂停（会话中）  
- 来源 / 同意摘要  
- 撤回相关入口（个人删除 / 共享撤回）  
- 字幕 / 减少动态  

---

## 2. 单点击穿路径规格

### 2.1 单人：`create_for_moment`

```yaml
flow_id: beta.solo.pierce
entry_cta: "为此刻做一件事"
steps:
  - id: purpose_glance
    ui: 一屏说明用途=为你创作；可跳过长文
    gate: 未授权前无材料预览诱导
  - id: source_pick
    ui: 可选哼唱/照片/想念/会话 pulse（均可跳过单项）
    min: 至少一项有效材料，否则 CONSENT/材料不足引导
  - id: consent_receipt
    ui: scope × purpose × 期限 × 处理者
    capability: lw.consent.check
  - id: weave
    ui: 可离开的安静态；无倒计时
  - id: timing
    capability: 内部 TimingDecision
    outcomes: [DELIVER_NOW, SLOW_INSPIRATION_DEFERRED, CANCELLED]
  - id: reveal
    ui: RitualView；先内容后 trace
    capability: lw.ritual.render
  - id: feedback
    ui: 有触动 / 不对 / 不舒服
    capability: lw.feedback.capture → lw.impact.evaluate
  - id: after
    ui: 保存 | 删除 | 「做成礼物送给 TA」（可选）
```

**体验验收：** UX-01、UX-02、UX-03、UX-10、UX-11；工程 CASE-001/002/003/008/009。

### 2.2 双人：`invite_duet_moment`

```yaml
flow_id: beta.duet.pierce
entry_cta: "和 TA 一起留下这一刻"
steps:
  - id: invite_compose
    ui: 目的、本次 scope、期限；不上传对方数据
  - id: partner_resolve
    ui_B: 独立同意或拒绝
    ui_A: 仅 ready / not_ready（无拒绝理由）
  - id: session_consents
    both: 本次会话授权
  - id: bond_gate
    capability: Bond Guardian + lw.pulse.duet（或共创 compose）
  - id: shared_reveal
    ui: 双方 RitualView；贡献可见不可比
  - id: share_rights
    ui: 共同归属、撤回入口对等
```

**体验验收：** UX-05、UX-06、UX-07；工程 CASE-005/006/010/012。

### 2.3 礼物：`gift_from_ritual`（Beta 增长主杠杆）

```yaml
flow_id: beta.gift.pierce
entry: 单人/共同仪式反馈为 meaningful 或用户主动「送给 TA」
steps:
  - id: gift_intent
    ui: 选择收件人通道（链接/邀请码）；说明「对方看不到你的原料」
  - id: owners_confirm
    if_shared: 每位共同权利人确认外发（逐方）
    if_solo: 仅本人确认
  - id: mint
    capability: lw.gift.token.mint
  - id: deliver_out
    ui: 复制链接 / 系统分享表（用户手动发出；禁止静默代发）
  - id: landing
    surface: Gift Landing（Web）
    capability: lw.gift.token.resolve
  - id: recipient_choice
    ui: 体验摘要 → 「我也做一个」| 「一起做一个」| 离开
  - id: revoke
    any_owner: lw.gift.token.revoke → 链接立即失效
```

---

## 3. Gift Edge：礼物对象与状态

### 3.1 `GiftToken`（领域对象）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `gift_id` | string | 是 | 礼物 ID |
| `token_hash` | string | 是 | 仅存哈希；明文 token 只在 mint 时返回一次 |
| `ritual_ref` | string | 是 | 源 `ritual_id` / envelope |
| `keepsake_ref` | string | 否 | 若已保存 |
| `grantor_ids` | string[] | 是 | 外发授权人；共同作品须全体 |
| `beneficiary_hint` | enum | 是 | `open_link` / `named_invite`（具名不暴露站外 PII） |
| `surface` | enum | 是 | `expiring_link` |
| `payload_public` | object | 是 | 站外可见：标题、模态摘要、非原料封面、邀请文案 |
| `payload_forbidden` | — | — | **不得含** signals、pulse、trace 细节、consent 原文、诊断 |
| `expires_at` | string | 是 | 默认短过期（建议 ≤ 7d，可配置护栏上限） |
| `max_resolves` | int | 是 | 建议 1–3；防广播刮取 |
| `resolve_count` | int | 是 | 已解析次数 |
| `status` | enum | 是 | `active` / `expired` / `revoked` / `exhausted` |
| `share_grant_refs` | string[] | 是 | 关联 ShareGrant |
| `created_at` | string | 是 | mint 时间 |
| `revoked_at` | string | 否 | 撤回时间 |
| `revoked_by` | string | 否 | 撤回人 |

### 3.2 生命周期

```text
mint → active
  ├─ resolve（未超限）→ active | exhausted
  ├─ expires_at → expired
  └─ revoke → revoked

expired | revoked | exhausted → resolve 一律 GIFT_INVALID
```

事件：`gift.minted`、`gift.resolved`、`gift.revoked`、`gift.expired`、`gift.access_denied`。

### 3.3 Gift Landing 体验契约

| 要求 | 说明 |
|---|---|
| 先体验后转化 | 落地页可播放/展示 `payload_public`；不逼注册才能「看一眼」的羞辱墙可讨论，但 **完整共创必须进站内同意** |
| 无原料 | Network 与 DOM 不得出现 signal/pulse/原始资产 URL（仅公开派生媒体） |
| 撤回同步 | `revoked` 后落地页显示权利占位，与站内 `SHARE_REVOKED` 语义一致 |
| 转化 CTA | 「为此刻做一件事」「和赠予者一起做一个」；无「再看更多推荐」 |
| 遥测 | 仅聚合 resolve 成功/失败；无收件人通讯录上传 |

---

## 4. 客户端页面级验收清单

| ID | 页面/态 | 必过 |
|---|---|---|
| SHELL-01 | Home `empty_calm` | 无推荐流、无红点；双主 CTA 文案符合击穿 |
| SHELL-02 | Create Moment | 未授权无预览诱导；可跳过单项来源 |
| SHELL-03 | Weaving | 可杀进程再回；无倒计时 |
| SHELL-04 | Deferred | 文案尊重时机；可取消 |
| SHELL-05 | RitualView | 三步内 trace；控制层齐全 |
| SHELL-06 | Feedback | 负反馈一步；不强制原因 |
| SHELL-07 | Gift Compose | 明示无原料外发；共同作品需双确认 |
| SHELL-08 | Gift Landing | 无原料；revoke 后失效 |
| SHELL-09 | Duet invite | 拒绝不回传理由；不循环催促 |
| SHELL-10 | Consent/Vault | 撤回 ≥ 分享入口显著度 |

---

## 5. 与工程实现的边界

| Beta 规格 | v0.1 现态 (`projects/lifewake`) | Beta 增量 |
|---|---|---|
| 击穿路径语义 | pipeline + CASE-001～014 | 增加 gift intent 与 CASE-015～017 |
| RitualView | report/JSON | Web Ritual Shell 原型对齐本文 IA |
| Gift Edge | 仅有 share revoke 语义 | `lw.gift.token.*` + 落地页 mock |
| 真实推送/IM | 无 | 仍禁止静默代发；只提供用户可复制链接 |

实现顺序建议：

1. 领域实体 `GiftToken` + 能力合约 mock  
2. CASE-015～017 行为验收绿灯  
3. Web Shell：Home 三态 + RitualView + Gift Landing  
4. 再接有限真实生成 / 设备  

---

## 6. 守恒检查（Beta 专用）

1. 首路径是否仍是「为此刻做一件事」，而非设置页？  
2. 礼物是否做到无原料、可过期、可撤销、默认短寿命？  
3. 是否出现 XP/连胜/亲密分/无限流？  
4. 共同作品外发是否逐方确认？  
5. 转化是否指向再一次有意义仪式，而非停留时长？  

---

*本文是 Beta 体验与礼物能力的单一规格源；能力字段冲突时以 [CAPABILITY_CONTRACTS](./CAPABILITY_CONTRACTS.md) 与 [DOMAIN_MODEL](./DOMAIN_MODEL.md) 同步修订为准。*
