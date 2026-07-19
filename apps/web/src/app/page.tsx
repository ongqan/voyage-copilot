import Link from "next/link";
import { Badge, PageHeader, SectionTitle, StatCard } from "@/components/ui";
import { benefits, order, recommendations, timeline } from "@/lib/demo-data";

export default function HomePage() {
  return <>
    <PageHeader eyebrow="会员首页" title="下午好，林晨" description="你的上海虹桥至北京首都行程已确认，以下服务均已按资格和时间校验。" action={<Link className="button primary" href="/trips/import">导入新行程</Link>} />
    <div className="demo-banner"><b>演示环境</b><span>所有权益、点数、库存和订单均为虚拟数据，不产生真实交易。</span></div>
    <div className="stats-grid"><StatCard label="可用权益" value="6" detail="来自3个虚拟计划" /><StatCard label="推荐服务" value="3" detail="均匹配SHA T2" tone="success" /><StatCard label="待处理变化" value="1" detail="模拟航站楼变化" tone="warning" /><StatCard label="AI已解决" value="78%" detail="本月演示数据" /></div>
    <div className="dashboard-grid">
      <section className="card trip-hero"><div className="card-top"><div><Badge tone="success">行程已确认</Badge><h2>上海虹桥 → 北京首都</h2><p>MU5105 · 2026年8月10日 14:30 · T2</p></div><div className="route-code"><strong>SHA</strong><span>2h20m</span><strong>PEK</strong></div></div><div className="action-row"><Link className="button primary" href="/recommendations">查看3项推荐</Link><Link className="button" href="/timeline">查看时间线</Link><Link className="button ghost" href="/trips">管理行程</Link></div></section>
      <section className="card"><SectionTitle title="权益摘要" detail={`${benefits.length}项`} /><div className="compact-list">{benefits.slice(0,3).map(item => <div key={item.id}><span><b>{item.name}</b><small>{item.source}</small></span><strong>{item.balance}</strong></div>)}</div><Link className="text-link" href="/benefits">查看全部权益 →</Link></section>
    </div>
    <SectionTitle title="为本次行程推荐" detail="已检查资格、营业时间、航站楼和模拟库存" />
    <div className="recommend-grid">{recommendations.map((item, index) => <article className="card recommendation-card" key={item.id}><div><Badge tone={index === 0 ? "success" : "info"}>{index === 0 ? "最适合" : item.type}</Badge><h3>{item.name}</h3><p>{item.reason}</p></div><dl><div><dt>建议时间</dt><dd>{item.time}</dd></div><div><dt>使用成本</dt><dd>{item.cost}</dd></div></dl><Link className="button" href="/recommendations">查看详情</Link></article>)}</div>
    <div className="dashboard-grid lower"><section className="card"><SectionTitle title="今日旅程时间线" /><div className="mini-timeline">{timeline.slice(1,5).map(item => <div key={item.time}><time>{item.time}</time><span><b>{item.title}</b><small>{item.detail}</small></span></div>)}</div><Link className="text-link" href="/timeline">打开完整时间线 →</Link></section><section className="card"><SectionTitle title="最近模拟订单" /><Badge tone="success">{order.status}</Badge><h3>{order.service}</h3><p>{order.useAt}<br />{order.location}</p><Link className="button" href={`/orders/demo-order-001`}>查看订单与凭证</Link></section></div>
  </>;
}

