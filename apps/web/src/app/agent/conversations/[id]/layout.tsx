import type { ReactNode } from "react";

export const dynamicParams = false;
export function generateStaticParams(){return [{id:"demo-conversation-001"}]}

export default function ConversationLayout({children}:{children:ReactNode}){return children}
