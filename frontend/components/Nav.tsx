"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/cn";

const links = [
  { href: "/", label: "Leads" },
  { href: "/score", label: "Score" },
  { href: "/about", label: "About" },
];

export function Nav() {
  const path = usePathname();
  return (
    <nav className="sticky top-0 z-20 border-b border-white/5 bg-black/30 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-lg bg-gradient-brand shadow-glow" />
          <span className="font-mono text-sm uppercase tracking-[0.2em]">
            lead<span className="text-gradient">.intel</span>
          </span>
        </Link>
        <div className="flex items-center gap-1">
          {links.map((l) => {
            const active = path === l.href || (l.href !== "/" && path.startsWith(l.href));
            return (
              <Link
                key={l.href}
                href={l.href}
                className={cn(
                  "rounded-full px-4 py-1.5 text-sm transition",
                  active
                    ? "bg-white/10 text-white"
                    : "text-white/60 hover:text-white hover:bg-white/5"
                )}
              >
                {l.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
