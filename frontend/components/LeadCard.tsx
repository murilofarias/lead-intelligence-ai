"use client";

import Link from "next/link";
import { ScoreDial } from "./ScoreDial";
import { GlassCard } from "./GlassCard";
import type { ScoredLead } from "@/lib/api";

export function LeadCard({ item }: { item: ScoredLead }) {
  const { lead, breakdown } = item;
  return (
    <Link href={`/leads/${lead.id}`} className="block">
      <GlassCard className="flex items-center gap-5">
        <ScoreDial score={breakdown.final_score} tier={breakdown.tier} size={110} />
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <h3 className="truncate text-lg font-semibold text-white">
              {lead.full_name}
            </h3>
            <span className="font-mono text-[10px] uppercase tracking-widest text-white/40">
              {lead.id}
            </span>
          </div>
          <p className="truncate text-sm text-white/70">
            {lead.title} · {lead.company}
          </p>
          <p className="mt-2 line-clamp-2 text-xs text-white/50">
            {lead.message || "—"}
          </p>
          <div className="mt-3 flex flex-wrap gap-2 text-[10px] font-mono uppercase tracking-wider text-white/60">
            <span className="rounded-full border border-white/10 px-2 py-0.5">
              {lead.industry}
            </span>
            <span className="rounded-full border border-white/10 px-2 py-0.5">
              {lead.company_size.toLocaleString()} emp
            </span>
            <span className="rounded-full border border-white/10 px-2 py-0.5">
              {lead.country}
            </span>
            <span className="rounded-full border border-white/10 px-2 py-0.5">
              {lead.source}
            </span>
          </div>
        </div>
      </GlassCard>
    </Link>
  );
}
