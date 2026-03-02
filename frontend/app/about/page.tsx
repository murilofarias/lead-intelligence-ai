import { GlassCard } from "@/components/GlassCard";

export default function AboutPage() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold">
          About <span className="text-gradient">Lead Intelligence AI</span>
        </h1>
        <p className="mt-2 max-w-2xl text-white/60">
          A portfolio project demonstrating production-grade full-stack
          engineering: FastAPI, Pydantic v2, Claude with prompt caching, SSE
          streaming, Salesforce integration, Next.js 14 App Router, Framer
          Motion, and a design system rooted in glassmorphism.
        </p>
      </header>

      <GlassCard>
        <h2 className="mb-2 text-lg font-semibold">Why hybrid scoring?</h2>
        <p className="text-white/75">
          Deterministic rules answer "does this lead fit our ICP?" with
          auditable, unchanging math. Claude answers "is this lead actually
          ready?" by reading the prospect's own words. Weighting both gives
          sales teams a score they can trust and explain to leadership.
        </p>
      </GlassCard>

      <GlassCard>
        <h2 className="mb-2 text-lg font-semibold">Engineering highlights</h2>
        <ul className="list-disc space-y-2 pl-5 text-white/75">
          <li>
            Prompt caching on the Anthropic system prompt using{" "}
            <code className="font-mono text-brand-cyan">
              cache_control: ephemeral
            </code>{" "}
            — shaves latency and cost from every request.
          </li>
          <li>
            SSE streaming pipes Claude's reasoning to the browser token by
            token; the UI renders it in a monospace console with a blinking
            cursor.
          </li>
          <li>
            Prompt-injection defense: lead content is wrapped in{" "}
            <code className="font-mono">&lt;lead&gt;</code> tags, sanitized,
            and the system prompt explicitly instructs the model to treat it
            as data.
          </li>
          <li>
            Rate limiting via slowapi, CORS allow-list, structured JSON
            logging with PII redaction.
          </li>
          <li>
            Fixture mode lets reviewers explore the full product without any
            API keys.
          </li>
        </ul>
      </GlassCard>

      <GlassCard>
        <h2 className="mb-2 text-lg font-semibold">Target role</h2>
        <p className="text-white/75">
          Built as a demonstration for a{" "}
          <span className="text-gradient">Senior Full Stack</span> role at
          Euler — emphasis on product polish, AI integration, and revenue
          tooling.
        </p>
      </GlassCard>
    </div>
  );
}
