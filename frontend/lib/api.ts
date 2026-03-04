export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export type Tier = "hot" | "warm" | "cool" | "cold";

export interface Lead {
  id: string;
  full_name: string;
  email: string;
  title: string;
  company: string;
  industry: string;
  company_size: number;
  annual_revenue_usd: number;
  country: string;
  source: string;
  message: string;
  created_at: string;
}

export interface Signal {
  name: string;
  points: number;
  detail: string;
}

export interface ScoreBreakdown {
  rules_score: number;
  llm_score: number;
  final_score: number;
  tier: Tier;
  rule_signals: Signal[];
  llm_signals: Signal[];
  rules_weight: number;
  llm_weight: number;
}

export interface ScoredLead {
  lead: Lead;
  breakdown: ScoreBreakdown;
}

export interface Explanation {
  lead_id: string;
  summary: string;
  recommended_action: string;
  talking_points: string[];
}

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return (await res.json()) as T;
}

export async function listLeads(): Promise<ScoredLead[]> {
  return json(await fetch(`${API_BASE}/api/leads`, { cache: "no-store" }));
}

export async function getLead(id: string): Promise<ScoredLead> {
  return json(await fetch(`${API_BASE}/api/leads/${id}`, { cache: "no-store" }));
}

export async function scoreProfile(
  profile: Omit<Lead, "id" | "created_at">
): Promise<ScoreBreakdown> {
  return json(
    await fetch(`${API_BASE}/api/score`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile),
    })
  );
}

export async function pushToSalesforce(id: string) {
  return json<{
    lead_id: string;
    salesforce_id: string;
    pushed_at: string;
    fixture: boolean;
  }>(
    await fetch(`${API_BASE}/api/leads/${id}/push-to-salesforce`, {
      method: "POST",
    })
  );
}

export function explainStreamUrl(id: string): string {
  return `${API_BASE}/api/leads/${id}/explain`;
}

export function tierColor(tier: Tier): string {
  switch (tier) {
    case "hot":
      return "#f43f5e";
    case "warm":
      return "#f59e0b";
    case "cool":
      return "#22d3ee";
    default:
      return "#64748b";
  }
}
