export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL
  ?? (process.env.NODE_ENV === "development" ? "http://localhost:8000/api/v1" : "");

export const DEMO_HEADERS = {
  "Content-Type": "application/json",
  "X-Demo-Tenant-ID": "tenant_demo_01",
  "X-Demo-User-ID": "user_demo_001",
};

export async function apiError(response: Response): Promise<string> {
  const payload = await response.json().catch(() => ({})) as { error?: { message?: string }; trace_id?: string };
  return `${payload.error?.message ?? "请求失败，请稍后重试。"}${payload.trace_id ? `（Trace: ${payload.trace_id}）` : ""}`;
}

export type Trip = {
  id: string;
  status: "DRAFT" | "CONFIRMED";
  flight_number: string;
  departure_airport: string;
  arrival_airport: string;
  departure_at: string;
  arrival_at: string;
  departure_terminal: string | null;
  arrival_terminal: string | null;
  party_adults: number;
  party_children: number;
  version: number;
};

export type TripInput = Omit<Trip, "id" | "status" | "version">;

const STORAGE_KEY = "voyage-copilot-demo-trips";
const seedTrip: Trip = {
  id: "demo-trip-001",
  status: "CONFIRMED",
  flight_number: "MU5105",
  departure_airport: "SHA",
  arrival_airport: "PEK",
  departure_at: "2026-08-10T14:30:00+08:00",
  arrival_at: "2026-08-10T16:50:00+08:00",
  departure_terminal: "T2",
  arrival_terminal: "T2",
  party_adults: 1,
  party_children: 0,
  version: 2,
};

function readLocalTrips(): Trip[] {
  if (typeof window === "undefined") return [seedTrip];
  const stored = window.localStorage.getItem(STORAGE_KEY);
  if (!stored) return [seedTrip];
  try {
    return JSON.parse(stored) as Trip[];
  } catch {
    window.localStorage.removeItem(STORAGE_KEY);
    return [seedTrip];
  }
}

function writeLocalTrips(trips: Trip[]): void {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(trips));
}

export async function listTrips(): Promise<Trip[]> {
  if (!API_BASE_URL) return readLocalTrips();
  const response = await fetch(`${API_BASE_URL}/trips`, {
    headers: DEMO_HEADERS,
    cache: "no-store",
  });
  if (!response.ok) throw new Error(await apiError(response));
  return (await response.json() as { items: Trip[] }).items;
}

export async function createTrip(input: TripInput): Promise<Trip> {
  if (!API_BASE_URL) {
    const trip: Trip = { ...input, id: "demo-trip-001", status: "DRAFT", version: 1 };
    const remaining = readLocalTrips().filter((item) => item.id !== trip.id);
    writeLocalTrips([trip, ...remaining]);
    return trip;
  }
  const response = await fetch(`${API_BASE_URL}/trips`, {
    method: "POST",
    headers: DEMO_HEADERS,
    body: JSON.stringify(input),
  });
  if (!response.ok) throw new Error(await apiError(response));
  return response.json() as Promise<Trip>;
}

export async function confirmTrip(id: string): Promise<void> {
  if (!API_BASE_URL) {
    const trips = readLocalTrips().map((trip) =>
      trip.id === id ? { ...trip, status: "CONFIRMED" as const, version: trip.version + 1 } : trip,
    );
    writeLocalTrips(trips);
    return;
  }
  const response = await fetch(`${API_BASE_URL}/trips/${id}/confirm`, {
    method: "POST",
    headers: DEMO_HEADERS,
  });
  if (!response.ok) throw new Error(await apiError(response));
}
