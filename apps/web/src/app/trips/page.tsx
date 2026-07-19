"use client";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { Badge, EmptyState, PageHeader } from "@/components/ui";
import { API_BASE_URL, DEMO_HEADERS, apiError } from "@/lib/api";

type Trip = { id:string; status:"DRAFT"|"CONFIRMED"; flight_number:string; departure_airport:string; arrival_airport:string; departure_at:string; departure_terminal:string|null; party_adults:number; party_children:number; version:number };

export default function TripsPage() {
  const [trips,setTrips]=useState<Trip[]>([]); const [loading,setLoading]=useState(true); const [error,setError]=useState("");
  const load=useCallback(async()=>{setLoading(true);setError("");try{const response=await fetch(`${API_BASE_URL}/trips`,{headers:DEMO_HEADERS,cache:"no-store"});if(!response.ok)throw new Error(await apiError(response));setTrips((await response.json()).items)}catch(value){setError(value instanceof Error?value.message:"加载失败")}finally{setLoading(false)}},[]);
  useEffect(()=>{void load()},[load]);
  async function confirm(id:string){const response=await fetch(`${API_BASE_URL}/trips/${id}/confirm`,{method:"POST",headers:DEMO_HEADERS});if(!response.ok){setError(await apiError(response));return}await load()}
  return <><PageHeader eyebrow="行程中心" title="我的行程" description="查看已确认、待确认和发生变化的全部行程。" action={<Link className="button primary" href="/trips/import">导入行程</Link>} />{error&&<div className="alert danger">{error}</div>}{loading?<div className="card loading">正在加载行程…</div>:trips.length===0?<EmptyState title="还没有行程" description="上传行程单或手工录入第一段航班。"/>:<div className="stack">{trips.map(trip=><article className="card trip-list-card" key={trip.id}><div><Badge tone={trip.status==="CONFIRMED"?"success":"warning"}>{trip.status==="CONFIRMED"?"已确认":"待确认"}</Badge><h2>{trip.departure_airport} → {trip.arrival_airport}</h2><p>{trip.flight_number} · {new Intl.DateTimeFormat("zh-CN",{dateStyle:"long",timeStyle:"short"}).format(new Date(trip.departure_at))} · {trip.departure_terminal??"航站楼待确认"}</p><small>{trip.party_adults}名成人{trip.party_children?` · ${trip.party_children}名儿童`:""} · 数据版本v{trip.version}</small></div><div className="action-row">{trip.status==="DRAFT"&&<button className="button primary" onClick={()=>void confirm(trip.id)}>确认行程</button>}<Link className="button" href={`/trips/${trip.id}`}>查看详情</Link></div></article>)}</div>}</>;
}

