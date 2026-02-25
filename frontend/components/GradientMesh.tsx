"use client";

import { motion } from "framer-motion";

export function GradientMesh() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <motion.div
        className="absolute -top-40 -left-40 h-[520px] w-[520px] rounded-full blur-3xl"
        style={{ background: "radial-gradient(circle, #8b5cf6 0%, transparent 60%)", opacity: 0.35 }}
        animate={{ x: [0, 80, 0], y: [0, 40, 0] }}
        transition={{ duration: 18, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute -bottom-32 -right-32 h-[620px] w-[620px] rounded-full blur-3xl"
        style={{ background: "radial-gradient(circle, #22d3ee 0%, transparent 60%)", opacity: 0.25 }}
        animate={{ x: [0, -60, 0], y: [0, -30, 0] }}
        transition={{ duration: 22, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute top-1/3 left-1/2 h-[420px] w-[420px] rounded-full blur-3xl"
        style={{ background: "radial-gradient(circle, #ec4899 0%, transparent 60%)", opacity: 0.12 }}
        animate={{ x: [-120, 120, -120], y: [0, 60, 0] }}
        transition={{ duration: 28, repeat: Infinity, ease: "easeInOut" }}
      />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_transparent_0%,_rgba(7,7,17,0.85)_70%)]" />
    </div>
  );
}
