"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

const groups = [
  {
    label: "会员端",
    items: [
      ["首页", "/"],
      ["我的行程", "/trips"],
      ["导入行程", "/trips/import"],
      ["AI管家", "/copilot"],
      ["权益中心", "/benefits"],
      ["服务推荐", "/recommendations"],
      ["旅程时间线", "/timeline"],
      ["模拟订单", "/orders/demo-order-001"],
      ["异常处理", "/disruptions/demo-event-001"],
    ],
  },
  {
    label: "客服端",
    items: [
      ["会话队列", "/agent/conversations"],
      ["会话摘要", "/agent/conversations/demo-conversation-001"],
      ["工单处理", "/agent/tickets/demo-ticket-001"],
    ],
  },
  {
    label: "运营端",
    items: [
      ["业务看板", "/admin/dashboard"],
      ["知识管理", "/admin/knowledge"],
      ["规则管理", "/admin/rules"],
      ["服务管理", "/admin/services"],
      ["AI质量", "/admin/quality"],
    ],
  },
] as const;

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="sidebar-brand" href="/">
          <span>V</span><div><strong>Voyage Copilot</strong><small>AI全旅程权益管家</small></div>
        </Link>
        <nav aria-label="主导航">
          {groups.map((group) => (
            <div className="nav-group" key={group.label}>
              <p>{group.label}</p>
              {group.items.map(([label, href]) => {
                const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
                return <Link className={active ? "active" : ""} href={href} key={href}>{label}</Link>;
              })}
            </div>
          ))}
        </nav>
        <div className="simulation-note">演示环境：全部权益、库存、点数和订单均为虚拟数据。</div>
      </aside>
      <div className="app-main">
        <header className="app-topbar">
          <div><span className="environment-dot" />MVP Demo</div>
          <div className="top-identity"><span>臻享计划</span><strong>林晨</strong><b>林</b></div>
        </header>
        <main className="page-container">{children}</main>
      </div>
    </div>
  );
}

