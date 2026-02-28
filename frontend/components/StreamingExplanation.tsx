"use client";

import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { explainStreamUrl, type Explanation } from "@/lib/api";

export function StreamingExplanation({ leadId }: { leadId: string }) {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState<Explanation | null>(null);
  const [status, setStatus] = useState<"idle" | "streaming" | "done" | "error">(
    "idle"
  );
  const esRef = useRef<EventSource | null>(null);

  const start = () => {
    setText("");
    setSummary(null);
    setStatus("streaming");
    const es = new EventSource(explainStreamUrl(leadId));
    esRef.current = es;
    es.addEventListener("chunk", (e) => {
      try {
        const { text: t } = JSON.parse((e as MessageEvent).data);
        setText((prev) => prev + t);
      } catch {}
    });
    es.addEventListener("done", (e) => {
      try {
        setSummary(JSON.parse((e as MessageEvent).data));
      } catch {}
      setStatus("done");
      es.close();
    });
    es.onerror = () => {
      setStatus("error");
      es.close();
    };
  };

  useEffect(() => () => esRef.current?.close(), []);

  return (
    <div className="glass p-5">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-mono uppercase tracking-widest text-white/70">
          Claude reasoning
        </h3>
        <button
          onClick={start}
          disabled={status === "streaming"}
          className="rounded-full bg-gradient-brand px-4 py-1.5 text-xs font-medium text-white shadow-glow disabled:opacity-50"
        >
          {status === "streaming" ? "Streaming…" : "Run analysis"}
        </button>
      </div>

      <motion.pre
        key={text.length}
        className="min-h-[180px] whitespace-pre-wrap rounded-lg bg-black/40 p-4 font-mono text-sm leading-relaxed text-white/85"
      >
        {text || (
          <span className="text-white/40">
            Press "Run analysis" to stream Claude's reasoning over SSE.
          </span>
        )}
        {status === "streaming" && (
          <span className="ml-1 inline-block h-4 w-2 animate-pulse bg-brand-cyan align-middle" />
        )}
      </motion.pre>

      {summary && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 space-y-3 text-sm"
        >
          <div>
            <div className="mb-1 text-[10px] font-mono uppercase tracking-widest text-brand-cyan">
              Summary
            </div>
            <p className="text-white/80">{summary.summary}</p>
          </div>
          <div>
            <div className="mb-1 text-[10px] font-mono uppercase tracking-widest text-brand-purple">
              Recommended action
            </div>
            <p className="text-white/80">{summary.recommended_action}</p>
          </div>
          <div>
            <div className="mb-1 text-[10px] font-mono uppercase tracking-widest text-white/60">
              Talking points
            </div>
            <ul className="list-disc space-y-1 pl-5 text-white/75">
              {summary.talking_points.map((p, i) => (
                <li key={i}>{p}</li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}
    </div>
  );
}
