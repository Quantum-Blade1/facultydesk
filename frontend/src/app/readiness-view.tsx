"use client";

import { useEffect, useState } from "react";

export interface ReadinessData {
  status: "loading" | "ready" | "unhealthy" | "error";
  failing: string[];
  checkedAt: string;
}

export function ReadinessView({ initialData }: { initialData: ReadinessData }) {
  const [readiness, setReadiness] = useState<ReadinessData>(initialData);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    async function checkReadiness() {
      try {
        const res = await fetch(`${apiUrl}/readyz`, { cache: "no-store" });
        const data: { status?: string; failing?: string[] } = await res.json();
        if (res.ok && data.status === "ready") {
          setReadiness({
            status: "ready",
            failing: [],
            checkedAt: new Date().toISOString(),
          });
        } else {
          setReadiness({
            status: "unhealthy",
            failing: data.failing ?? ["unknown"],
            checkedAt: new Date().toISOString(),
          });
        }
      } catch {
        setReadiness((prev) => ({
          ...prev,
          status: prev.status === "ready" ? "ready" : "error",
          checkedAt: new Date().toISOString(),
        }));
      }
    }

    checkReadiness();
    const interval = setInterval(checkReadiness, 5000);
    return () => clearInterval(interval);
  }, [apiUrl]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 p-6 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <main className="w-full max-w-lg rounded-xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div className="mb-6 flex items-center justify-between border-b border-slate-100 pb-4 dark:border-slate-800">
          <div>
            <h1 className="text-xl font-bold tracking-tight">FacultyDesk</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Department Operations Platform
            </p>
          </div>
          <div
            id="readiness-badge"
            className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ${
              readiness.status === "ready"
                ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300"
                : readiness.status === "loading"
                  ? "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300"
                  : "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300"
            }`}
          >
            {readiness.status}
          </div>
        </div>

        <div className="space-y-4">
          <div className="rounded-lg bg-slate-50 p-4 dark:bg-slate-800/50">
            <div className="text-xs font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Backend Health
            </div>
            <div className="mt-1 flex items-center justify-between">
              <span className="text-sm font-medium">Readiness Probe</span>
              <span
                id="backend-status"
                className="font-mono text-sm font-semibold capitalize"
              >
                {readiness.status}
              </span>
            </div>
            {readiness.failing.length > 0 && (
              <div className="mt-2 text-xs text-rose-600 dark:text-rose-400">
                Failing: {readiness.failing.join(", ")}
              </div>
            )}
          </div>

          <div className="grid grid-cols-3 gap-3 text-center text-xs">
            <div className="rounded-md border border-slate-200 p-2.5 dark:border-slate-800">
              <div className="text-slate-500 dark:text-slate-400">Database</div>
              <div className="mt-1 font-semibold">PostgreSQL 16</div>
            </div>
            <div className="rounded-md border border-slate-200 p-2.5 dark:border-slate-800">
              <div className="text-slate-500 dark:text-slate-400">Queue &amp; Cache</div>
              <div className="mt-1 font-semibold">Redis 7</div>
            </div>
            <div className="rounded-md border border-slate-200 p-2.5 dark:border-slate-800">
              <div className="text-slate-500 dark:text-slate-400">Storage</div>
              <div className="mt-1 font-semibold">MinIO S3</div>
            </div>
          </div>
        </div>

        {readiness.checkedAt && (
          <div className="mt-6 text-center text-xs text-slate-400">
            Last checked: {readiness.checkedAt}
          </div>
        )}
      </main>
    </div>
  );
}
