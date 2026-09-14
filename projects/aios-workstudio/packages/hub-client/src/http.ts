/** WorkStudio 一线只走北向 hub.scene.* 与进度 SSE。禁止零件 SDK。 */

export type HubErrorBody = {
  error: { code: string; message: string; next?: string; explain_ref?: string };
};

export type EnvelopeHeaders = {
  tenantId: string;
  actorId: string;
  track: string;
  threadId?: string;
};

export class HubClient {
  constructor(
    readonly baseUrl: string,
    readonly headers: EnvelopeHeaders,
  ) {}

  private hdr(): Record<string, string> {
    const h: Record<string, string> = {
      "Content-Type": "application/json",
      "X-Tenant-Id": this.headers.tenantId,
      "X-Actor-Id": this.headers.actorId,
      "X-Track": this.headers.track,
    };
    if (this.headers.threadId) h["X-Thread-Id"] = this.headers.threadId;
    return h;
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    const res = await fetch(this.baseUrl + path, {
      method: "POST",
      headers: this.hdr(),
      body: JSON.stringify(body ?? {}),
    });
    const json = await res.json();
    if (!res.ok) throw json as HubErrorBody;
    return json as T;
  }

  async get<T>(path: string): Promise<T> {
    const res = await fetch(this.baseUrl + path, { headers: this.hdr() });
    const json = await res.json();
    if (!res.ok) throw json as HubErrorBody;
    return json as T;
  }
}

export const HUB_DEFAULT = "http://127.0.0.1:18088";
