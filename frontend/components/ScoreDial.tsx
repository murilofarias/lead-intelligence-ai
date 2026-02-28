"use client";

import { motion } from "framer-motion";
import { tierColor, type Tier } from "@/lib/api";

type Props = {
  score: number;
  tier: Tier;
  size?: number;
  label?: string;
};

export function ScoreDial({ score, tier, size = 140, label }: Props) {
  const stroke = 10;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(100, score)) / 100;
  const color = tierColor(tier);

  return (
    <div className="relative flex flex-col items-center" style={{ width: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <defs>
          <linearGradient id={`grad-${tier}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#8b5cf6" />
            <stop offset="100%" stopColor={color} />
          </linearGradient>
        </defs>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke="rgba(255,255,255,0.08)"
          strokeWidth={stroke}
          fill="none"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke={`url(#grad-${tier})`}
          strokeWidth={stroke}
          strokeLinecap="round"
          fill="none"
          initial={{ strokeDasharray: `0 ${c}` }}
          animate={{ strokeDasharray: `${c * pct} ${c}` }}
          transition={{ duration: 1.1, ease: "easeOut" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          className="font-mono text-3xl font-semibold text-white"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          {Math.round(score)}
        </motion.span>
        <span
          className="mt-1 text-[10px] font-mono uppercase tracking-[0.2em]"
          style={{ color }}
        >
          {tier}
        </span>
      </div>
      {label && (
        <span className="mt-2 text-xs text-white/60 font-mono">{label}</span>
      )}
    </div>
  );
}
