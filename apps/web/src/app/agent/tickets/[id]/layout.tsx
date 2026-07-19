import type { ReactNode } from "react";

export const dynamicParams = false;
export function generateStaticParams(){return [{id:"demo-ticket-001"}]}

export default function TicketLayout({children}:{children:ReactNode}){return children}
