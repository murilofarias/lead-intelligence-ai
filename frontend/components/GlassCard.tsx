"use client";

import { cn } from "@/lib/cn";
import { motion, type HTMLMotionProps } from "framer-motion";
import type { PropsWithChildren } from "react";

type Props = PropsWithChildren<{
  className?: string;
  hover?: boolean;
}> & HTMLMotionProps<"div">;

export function GlassCard({
  children,
  className,
  hover = true,
  ...rest
}: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={cn("glass p-5", hover && "glass-hover", className)}
      {...rest}
    >
      {children}
    </motion.div>
  );
}
