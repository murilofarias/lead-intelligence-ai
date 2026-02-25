import "./globals.css";
import type { Metadata } from "next";
import { Toaster } from "sonner";
import { GradientMesh } from "@/components/GradientMesh";
import { CursorGlow } from "@/components/CursorGlow";
import { Nav } from "@/components/Nav";

export const metadata: Metadata = {
  title: "Lead Intelligence AI",
  description:
    "AI-powered lead scoring — hybrid rules engine + Claude qualitative analysis.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="relative min-h-screen text-white antialiased">
        <GradientMesh />
        <CursorGlow />
        <Nav />
        <main className="relative z-10 mx-auto max-w-6xl px-6 py-10">
          {children}
        </main>
        <Toaster theme="dark" position="bottom-right" richColors />
      </body>
    </html>
  );
}
