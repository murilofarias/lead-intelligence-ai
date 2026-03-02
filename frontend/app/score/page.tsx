"use client";

import { useState } from "react";
import { toast } from "sonner";
import { GlassCard } from "@/components/GlassCard";
import { ScoreDial } from "@/components/ScoreDial";
import { scoreProfile, type ScoreBreakdown } from "@/lib/api";

const INITIAL = {
  full_name: "Dana Alvarez",
  email: "dana@examplecorp.com",
  title: "VP Revenue Ops",
  company: "ExampleCorp",
  industry: "saas",
  company_size: 1200,
  annual_revenue_usd: 200_000_000,
  country: "US",
  source: "referral",
  message: "Evaluating scoring platforms. Budget approved, want to start pilot next month.",
};

export default function ScorePage() {
  const [form, setForm] = useState(INITIAL);
  const [result, setResult] = useState<ScoreBreakdown | null>(null);
  const [loading, setLoading] = useState(false);

  const update = (k: keyof typeof form, v: string | number) =>
    setForm((f) => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const r = await scoreProfile(form as any);
      setResult(r);
    } catch (err) {
      toast.error("Scoring failed", { description: String(err) });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold">
          Score a lead <span className="text-gradient">in real time</span>
        </h1>
        <p className="mt-2 text-white/60">
          Paste a lead profile, get a hybrid rules + Claude score with full
          breakdown.
        </p>
      </header>

      <div className="grid gap-6 md:grid-cols-[1.3fr_1fr]">
        <GlassCard>
          <form onSubmit={submit} className="grid grid-cols-2 gap-4">
            <Field label="Full name" value={form.full_name} onChange={(v) => update("full_name", v)} />
            <Field label="Email" value={form.email} onChange={(v) => update("email", v)} />
            <Field label="Title" value={form.title} onChange={(v) => update("title", v)} />
            <Field label="Company" value={form.company} onChange={(v) => update("company", v)} />
            <Select
              label="Industry"
              value={form.industry}
              onChange={(v) => update("industry", v)}
              options={["saas", "fintech", "healthtech", "ecommerce", "manufacturing", "media", "education", "logistics", "government", "other"]}
            />
            <Field label="Country (ISO2)" value={form.country} onChange={(v) => update("country", v.toUpperCase().slice(0, 2))} />
            <Field label="Employees" type="number" value={String(form.company_size)} onChange={(v) => update("company_size", Number(v))} />
            <Field label="Annual revenue (USD)" type="number" value={String(form.annual_revenue_usd)} onChange={(v) => update("annual_revenue_usd", Number(v))} />
            <Select
              label="Source"
              value={form.source}
              onChange={(v) => update("source", v)}
              options={["referral", "event", "partner", "webinar", "content", "g2", "outbound", "website", "linkedin"]}
            />
            <div className="col-span-2">
              <Label>Message</Label>
              <textarea
                value={form.message}
                onChange={(e) => update("message", e.target.value)}
                rows={4}
                className="w-full rounded-lg bg-black/30 p-3 text-sm outline-none focus:ring-1 focus:ring-brand-purple"
              />
            </div>
            <div className="col-span-2 flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="rounded-full bg-gradient-brand px-6 py-2 text-sm font-medium text-white shadow-glow disabled:opacity-50"
              >
                {loading ? "Scoring…" : "Score lead"}
              </button>
            </div>
          </form>
        </GlassCard>

        <GlassCard className="flex flex-col items-center justify-center text-center">
          {result ? (
            <>
              <ScoreDial
                score={result.final_score}
                tier={result.tier}
                size={180}
                label="final score"
              />
              <div className="mt-6 w-full space-y-2 text-left">
                {[...result.rule_signals, ...result.llm_signals].map((s) => (
                  <div
                    key={s.name}
                    className="flex items-center justify-between rounded bg-white/[0.03] px-3 py-2 text-xs"
                  >
                    <span className="text-white/80">{s.name}</span>
                    <span className="font-mono text-brand-cyan">+{s.points}</span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p className="text-white/40">
              Submit the form to see the breakdown here.
            </p>
          )}
        </GlassCard>
      </div>
    </div>
  );
}

function Label({ children }: { children: React.ReactNode }) {
  return (
    <div className="mb-1 text-[10px] font-mono uppercase tracking-widest text-white/50">
      {children}
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
}) {
  return (
    <div>
      <Label>{label}</Label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg bg-black/30 px-3 py-2 text-sm outline-none focus:ring-1 focus:ring-brand-purple"
      />
    </div>
  );
}

function Select({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
}) {
  return (
    <div>
      <Label>{label}</Label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg bg-black/30 px-3 py-2 text-sm outline-none focus:ring-1 focus:ring-brand-purple"
      >
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </div>
  );
}
