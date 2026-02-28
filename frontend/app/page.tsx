"use client";

import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { LeadCard } from "@/components/LeadCard";
import { listLeads, type ScoredLead } from "@/lib/api";

type Range = "all" | "hot" | "warm" | "cool" | "cold";

export default function HomePage() {
  const [items, setItems] = useState<ScoredLead[] | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [filter, setFilter] = useState<Range>("all");
  const [query, setQuery] = useState("");

  useEffect(() => {
    listLeads()
      .then(setItems)
      .catch((e) => setErr(String(e)));
  }, []);

  const filtered = useMemo(() => {
    if (!items) return [];
    return items.filter((it) => {
      if (filter !== "all" && it.breakdown.tier !== filter) return false;
      if (query) {
        const q = query.toLowerCase();
        const hay = `${it.lead.full_name} ${it.lead.company} ${it.lead.industry} ${it.lead.title}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }, [items, filter, query]);

  return (
    <div className="space-y-10">
      <section className="relative">
        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-semibold tracking-tight md:text-5xl"
        >
          Lead Intelligence, <span className="text-gradient">explained.</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
          className="mt-3 max-w-2xl text-white/70"
        >
          Hybrid scoring combining a deterministic rules engine with Claude's
          qualitative reasoning. Every score is transparent, explainable, and
          one click away from Salesforce.
        </motion.p>
      </section>

      <section className="flex flex-wrap items-center gap-3">
        <div className="glass flex items-center gap-2 px-3 py-2">
          {(["all", "hot", "warm", "cool", "cold"] as Range[]).map((r) => (
            <button
              key={r}
              onClick={() => setFilter(r)}
              className={`rounded-full px-3 py-1 text-xs font-mono uppercase tracking-wider transition ${
                filter === r
                  ? "bg-white/10 text-white"
                  : "text-white/50 hover:text-white"
              }`}
            >
              {r}
            </button>
          ))}
        </div>
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search leads…"
          className="glass flex-1 bg-transparent px-4 py-2 text-sm outline-none placeholder:text-white/30 focus:border-brand-purple"
        />
      </section>

      {err && (
        <div className="glass p-4 text-sm text-rose-300">
          Couldn't load leads: {err}. Make sure the backend is running on{" "}
          <code>localhost:8000</code>.
        </div>
      )}

      {!items && !err && (
        <div className="grid gap-4 md:grid-cols-2">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="glass h-[140px] animate-pulse-slow opacity-50"
            />
          ))}
        </div>
      )}

      {items && (
        <section className="grid gap-4 md:grid-cols-2">
          {filtered.map((it) => (
            <LeadCard key={it.lead.id} item={it} />
          ))}
          {filtered.length === 0 && (
            <div className="glass col-span-full p-8 text-center text-white/50">
              No leads match this filter.
            </div>
          )}
        </section>
      )}
    </div>
  );
}
