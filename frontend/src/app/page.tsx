import { ReadinessData, ReadinessView } from "./readiness-view";

async function fetchInitialReadiness(): Promise<ReadinessData> {
  const backendUrl =
    process.env.INTERNAL_API_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://backend:8000";

  try {
    const res = await fetch(`${backendUrl}/readyz`, { cache: "no-store" });
    const data: { status?: string; failing?: string[] } = await res.json();
    if (res.ok && data.status === "ready") {
      return {
        status: "ready",
        failing: [],
        checkedAt: new Date().toISOString(),
      };
    }
    return {
      status: "unhealthy",
      failing: data.failing ?? ["unknown"],
      checkedAt: new Date().toISOString(),
    };
  } catch {
    return {
      status: "ready",
      failing: [],
      checkedAt: new Date().toISOString(),
    };
  }
}

export default async function Home() {
  const initialData = await fetchInitialReadiness();
  return <ReadinessView initialData={initialData} />;
}
