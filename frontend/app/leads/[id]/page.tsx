"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { ScoreDial } from "@/components/ScoreDial";
import { GlassCard } from "@/components/GlassCard";
import { StreamingExplanation } from "@/components/StreamingExplanation";
import { getLead, pushToSalesforce, type ScoredLead } from "@/lib/api";

export default function LeadDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<ScoredLead | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [pushing, setPushing] = useState(false);

  useEffect(() => {
    if (!id) return;
    getLead(id).then(setData).catch((e) => setErr(String(e)));
  }, [id]);

  const handlePush = async () => {
    if (!id) return;
    setPushing(true);
    try {
      const res = await pushToSalesforce(id);
      toast.success(
        `Pushed to Salesforce${res.fixture ? " (fixture mode)" : ""}`,
        { description: `Salesforce ID: ${res.salesforce_id}` }
      );
    } catch (e) {
      toast.error("Push failed", { description: String(e) });
    } finally {
      setPushing(false);
    }
  };

  if (err)
    return (
      <div className="glass p-6 text-rose-300">Couldn't load lead: {err}</div>
    );

  if (!data)
    return (
      <div className="glass h-64 animate-pulse-slow opacity-50" aria-label="loading" />
    );

  const { lead, breakdown } = data;

  return (
    <div className="space-y-8">
      <Link href="/" className="text-sm text-white/50 hover:text-white">
        ← All leads
      </Link>

      <section className="grid gap-6 md:grid-cols-[260px_1fr]">
        <GlassCard className="flex flex-col items-center justify-center">
          <ScoreDial
            score={breakdown.final_score}
            tier={breakdown.tier}
            size={180}
            label={`final · ${breakdown.tier}`}
          />
          <div className="mt-4 flex gap-6 text-center">
            <div>
              <div className="text-[10px] font-mono uppercase tracking-widest text-white/50">
                Rules
              </div>
              <div className="font-mono text-lg">{breakdown.rules_score}</div>
            </div>
            <div>
              <div className="text-[10px] font-mono uppercase tracking-widest text-white/50">
                LLM
              </div>
              <div className="font-mono text-lg">{breakdown.llm_score}</div>
            </div>
          </div>
        </GlassCard>

        <GlassCard>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-semibold text-white">
                {lead.full_name}
              </h1>
              <p className="text-white/60">
                {lead.title} · {lead.company}
              </p>
              <p className="mt-1 text-xs font-mono text-white/40">
                {lead.email} · {lead.country} · {lead.industry}
              </p>
            </div>
            <button
              onClick={handlePush}
              disabled={pushing}
              className="rounded-full bg-gradient-brand px-4 py-2 text-sm font-medium text-white shadow-glow disabled:opacity-50"
            >
              {pushing ? "Pushing…" : "Push to Salesforce"}
            </button>
          </div>
          <p className="mt-4 rounded-lg bg-black/30 p-4 text-sm italic text-white/75">
            “{lead.message || "No message provided."}”
          </p>
          <div className="mt-4 grid grid-cols-2 gap-4 text-sm md:grid-cols-4">
            <Fact label="Employees" value={lead.company_size.toLocaleString()} />
            <Fact
              label="Revenue"
              value={`$${(lead.annual_revenue_usd / 1_000_000).toLocaleString(
                undefined,
                { maximumFractionDigits: 0 }
              )}M`}
            />
            <Fact label="Source" value={lead.source} />
            <Fact label="Lead ID" value={lead.id} />
          </div>
        </GlassCard>
      </section>

      <section className="grid gap-6 md:grid-cols-2">
        <GlassCard>
          <h3 className="mb-3 text-sm font-mono uppercase tracking-widest text-white/70">
            Rules signals ({Math.round(breakdown.rules_weight * 100)}%)
          </h3>
          <ul className="space-y-2">
            {breakdown.rule_signals.map((s) => (
              <SignalRow key={s.name} {...s} />
            ))}
          </ul>
        </GlassCard>
        <GlassCard>
          <h3 className="mb-3 text-sm font-mono uppercase tracking-widest text-white/70">
            LLM signals ({Math.round(breakdown.llm_weight * 100)}%)
          </h3>
          <ul className="space-y-2">
            {breakdown.llm_signals.map((s) => (
              <SignalRow key={s.name} {...s} />
            ))}
          </ul>
        </GlassCard>
      </section>

      <StreamingExplanation leadId={lead.id} />
    </div>
  );
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-[10px] font-mono uppercase tracking-widest text-white/50">
        {label}
      </div>
      <div className="text-white/90">{value}</div>
    </div>
  );
}

function SignalRow({
  name,
  points,
  detail,
}: {
  name: string;
  points: number;
  detail: string;
}) {
  return (
    <li className="flex items-start justify-between gap-3 rounded-lg bg-white/[0.03] p-3">
      <div>
        <div className="text-sm text-white">{name}</div>
        <div className="text-xs text-white/50">{detail}</div>
      </div>
      <div className="font-mono text-sm text-brand-cyan">+{points}</div>
    </li>
  );
}
