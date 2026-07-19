import type { Metadata } from "next";
import type { ReactNode } from "react";

import "./styles.css";
import { AppShell } from "@/components/app-shell";

export const metadata: Metadata = {
  title: "Voyage Copilot",
  description: "AI全旅程权益管家",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body><AppShell>{children}</AppShell></body>
    </html>
  );
}
