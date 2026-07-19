export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const DEMO_HEADERS = {
  "Content-Type": "application/json",
  "X-Demo-Tenant-ID": "tenant_demo_01",
  "X-Demo-User-ID": "user_demo_001",
};

export async function apiError(response: Response): Promise<string> {
  const payload = await response.json().catch(() => ({})) as { error?: { message?: string }; trace_id?: string };
  return `${payload.error?.message ?? "请求失败，请稍后重试。"}${payload.trace_id ? `（Trace: ${payload.trace_id}）` : ""}`;
}

