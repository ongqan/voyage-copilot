import type { ReactNode } from "react";

export function PageHeader({ eyebrow, title, description, action }: { eyebrow?: string; title: string; description: string; action?: ReactNode }) {
  return <div className="page-header"><div>{eyebrow && <p className="eyebrow">{eyebrow}</p>}<h1>{title}</h1><p>{description}</p></div>{action && <div className="page-action">{action}</div>}</div>;
}

export function Badge({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "success" | "warning" | "danger" | "info" }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}

export function StatCard({ label, value, detail, tone }: { label: string; value: string; detail: string; tone?: "success" | "warning" | "danger" }) {
  return <article className={`card stat-card ${tone ?? ""}`}><span>{label}</span><strong>{value}</strong><small>{detail}</small></article>;
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return <div className="empty-state"><strong>{title}</strong><p>{description}</p></div>;
}

export function SectionTitle({ title, detail }: { title: string; detail?: string }) {
  return <div className="section-heading"><h2>{title}</h2>{detail && <span>{detail}</span>}</div>;
}

