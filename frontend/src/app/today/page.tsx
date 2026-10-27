"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast";
import { api, CalendarEventResponse, TaskResponse, ScheduledNotificationResponse } from "@/lib/api-client";
import { Clock, Calendar, CheckSquare, Bell, ArrowRight, CheckCircle2, AlertTriangle, BookOpen } from "lucide-react";
import Link from "next/link";

export default function TodayPage() {
  const router = useRouter();
  const { user, profile, isLoading } = useAuth();
  const { toast } = useToast();

  const [events, setEvents] = React.useState<CalendarEventResponse[]>([]);
  const [tasks, setTasks] = React.useState<TaskResponse[]>([]);
  const [alerts, setAlerts] = React.useState<ScheduledNotificationResponse[]>([]);
  const [loadingData, setLoadingData] = React.useState(true);
  const [currentTime, setCurrentTime] = React.useState(new Date());

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [isLoading, user, router]);

  React.useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const loadDashboardData = React.useCallback(async () => {
    if (!user) return;
    try {
      setLoadingData(true);
      const startOfDay = new Date();
      startOfDay.setHours(0, 0, 0, 0);
      const endOfDay = new Date();
      endOfDay.setHours(23, 59, 59, 999);

      const [eventsData, tasksData, alertsData] = await Promise.all([
        api.calendar.getEvents({
          start: startOfDay.toISOString(),
          end: endOfDay.toISOString(),
        }),
        api.tasks.list({ status: "TODO" }),
        api.reminders.getUpcomingNotifications(10),
      ]);

      setEvents(eventsData.sort((a, b) => new Date(a.start_utc).getTime() - new Date(b.start_utc).getTime()));
      setTasks(tasksData.sort((a, b) => b.priority_score - a.priority_score).slice(0, 5));
      setAlerts(alertsData);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    } finally {
      setLoadingData(false);
    }
  }, [user]);

  React.useEffect(() => {
    if (user) {
      loadDashboardData();
    }
  }, [user, loadDashboardData]);

  const handleCompleteTask = async (taskId: string) => {
    try {
      await api.tasks.complete(taskId);
      toast("Task completed", "success");
      loadDashboardData();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to complete task", "error");
    }
  };

  const nextEvent = events.find((e) => new Date(e.end_utc).getTime() > currentTime.getTime());

  let countdownText = "No more events today";
  let countdownDiffMinutes = 0;
  if (nextEvent) {
    const startMs = new Date(nextEvent.start_utc).getTime();
    const nowMs = currentTime.getTime();
    if (nowMs < startMs) {
      const diffSec = Math.floor((startMs - nowMs) / 1000);
      const mins = Math.floor(diffSec / 60);
      const secs = diffSec % 60;
      countdownDiffMinutes = mins;
      countdownText = `Starts in ${mins}m ${secs}s`;
    } else {
      countdownText = "Happening now";
    }
  }

  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-sm font-medium text-slate-500 animate-pulse">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Welcome & Next Event Hero */}
        <div className="bg-[#1e3a8a] text-white rounded-xl p-5 sm:p-6 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <span className="text-xs uppercase font-semibold text-blue-200 tracking-wider">
                Daily Briefing
              </span>
              <h1 className="text-xl sm:text-2xl font-bold mt-0.5">
                Welcome back, {profile ? profile.full_name : user.email}
              </h1>
              <p className="text-xs sm:text-sm text-blue-100 mt-1">
                {events.length} schedule items and {tasks.length} pending tasks today.
              </p>
            </div>

            {nextEvent ? (
              <div className="bg-white/10 backdrop-blur-xs rounded-lg p-3.5 border border-white/20 min-w-[220px]">
                <div className="flex items-center space-x-1.5 text-xs text-blue-200 font-medium">
                  <Clock className="w-3.5 h-3.5" />
                  <span>Next: {nextEvent.kind}</span>
                </div>
                <div className="text-base font-bold mt-1 truncate">{nextEvent.title}</div>
                <div className="flex items-center justify-between text-xs text-blue-100 mt-1 font-mono">
                  <span>
                    {new Intl.DateTimeFormat("en-IN", {
                      hour: "2-digit",
                      minute: "2-digit",
                      timeZone: "Asia/Kolkata",
                    }).format(new Date(nextEvent.start_utc))}
                    {nextEvent.location ? ` • ${nextEvent.location}` : ""}
                  </span>
                  <span className="font-semibold text-amber-300">{countdownText}</span>
                </div>
              </div>
            ) : (
              <div className="bg-white/10 backdrop-blur-xs rounded-lg p-3.5 border border-white/20 text-xs text-blue-100">
                All classes and meetings for today are finished.
              </div>
            )}
          </div>
        </div>

        {/* Unread Alerts Banner if any */}
        {alerts.length > 0 && (
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-3.5 text-xs text-amber-900 flex items-start space-x-3">
            <Bell className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div className="flex-1">
              <span className="font-semibold">Upcoming Delivery: </span>
              {alerts.length} notifications scheduled ({alerts[0]?.channel} alert at{" "}
              {new Intl.DateTimeFormat("en-IN", {
                hour: "2-digit",
                minute: "2-digit",
                timeZone: "Asia/Kolkata",
              }).format(new Date(alerts[0]?.fire_at_utc || new Date()))}
              ).
            </div>
            <Link href="/settings" className="font-semibold text-amber-800 underline hover:text-amber-950">
              Manage
            </Link>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Today's Schedule Timeline */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-3">
              <div>
                <CardTitle className="text-base">Today&apos;s Schedule</CardTitle>
                <p className="text-xs text-slate-500">Classes, meetings, and deadlines</p>
              </div>
              <Link href="/calendar" className="text-xs font-semibold text-[#1e3a8a] hover:underline flex items-center">
                Calendar <ArrowRight className="w-3 h-3 ml-1" />
              </Link>
            </CardHeader>
            <CardContent>
              {loadingData ? (
                <div className="py-8 text-center text-xs text-slate-400">Loading schedule...</div>
              ) : events.length === 0 ? (
                <div className="py-8 text-center space-y-2">
                  <Calendar className="w-8 h-8 text-slate-300 mx-auto" />
                  <p className="text-xs text-slate-500">No events scheduled for today.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {events.map((event) => {
                    const isPast = new Date(event.end_utc).getTime() < currentTime.getTime();
                    const isNow =
                      new Date(event.start_utc).getTime() <= currentTime.getTime() &&
                      new Date(event.end_utc).getTime() >= currentTime.getTime();

                    return (
                      <div
                        key={event.id}
                        className={`p-3 rounded-md border transition-colors flex items-center justify-between ${
                          isNow
                            ? "border-blue-400 bg-blue-50/50"
                            : isPast
                            ? "border-slate-100 bg-slate-50 opacity-60"
                            : "border-slate-200 bg-white"
                        }`}
                      >
                        <div className="flex items-start space-x-3">
                          <div className="w-1.5 h-10 rounded-full bg-[#1e3a8a] shrink-0 mt-0.5" />
                          <div>
                            <div className="flex items-center space-x-2">
                              <span className="text-xs font-semibold text-slate-900">{event.title}</span>
                              <Badge
                                variant={
                                  event.kind === "CLASS"
                                    ? "blue"
                                    : event.kind === "MEETING"
                                    ? "purple"
                                    : "danger"
                                }
                              >
                                {event.kind}
                              </Badge>
                              {isNow && (
                                <Badge variant="success" className="animate-pulse">
                                  LIVE
                                </Badge>
                              )}
                            </div>
                            <div className="text-[11px] text-slate-500 font-mono mt-0.5">
                              {new Intl.DateTimeFormat("en-IN", {
                                hour: "2-digit",
                                minute: "2-digit",
                                timeZone: "Asia/Kolkata",
                              }).format(new Date(event.start_utc))}{" "}
                              -{" "}
                              {new Intl.DateTimeFormat("en-IN", {
                                hour: "2-digit",
                                minute: "2-digit",
                                timeZone: "Asia/Kolkata",
                              }).format(new Date(event.end_utc))}
                              {event.location ? ` • ${event.location}` : ""}
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Top Priority Tasks */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-3">
              <div>
                <CardTitle className="text-base">High-Priority Tasks</CardTitle>
                <p className="text-xs text-slate-500">Sorted by mathematical priority P</p>
              </div>
              <Link href="/tasks" className="text-xs font-semibold text-[#1e3a8a] hover:underline flex items-center">
                All Tasks <ArrowRight className="w-3 h-3 ml-1" />
              </Link>
            </CardHeader>
            <CardContent>
              {loadingData ? (
                <div className="py-8 text-center text-xs text-slate-400">Loading tasks...</div>
              ) : tasks.length === 0 ? (
                <div className="py-8 text-center space-y-2">
                  <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
                  <p className="text-xs text-slate-500">All documentation tasks are complete!</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {tasks.map((task) => {
                    const isOverdue = task.priority_score > 1.0;
                    return (
                      <div
                        key={task.id}
                        className={`p-3 rounded-md border flex items-center justify-between transition-colors ${
                          isOverdue ? "border-red-200 bg-red-50/40" : "border-slate-200 bg-white"
                        }`}
                      >
                        <div className="flex-1 pr-3">
                          <div className="flex items-center space-x-2">
                            <span className="text-xs font-semibold text-slate-900 line-clamp-1">
                              {task.title}
                            </span>
                            <Badge variant={isOverdue ? "danger" : "default"}>
                              P: {task.priority_score.toFixed(2)}
                            </Badge>
                          </div>
                          <div className="flex items-center space-x-2 text-[11px] text-slate-500 mt-1">
                            <span className="font-medium text-slate-600">{task.category}</span>
                            <span>•</span>
                            <span>
                              Due{" "}
                              {new Intl.DateTimeFormat("en-IN", {
                                day: "numeric",
                                month: "short",
                                hour: "2-digit",
                                minute: "2-digit",
                                timeZone: "Asia/Kolkata",
                              }).format(new Date(task.deadline_utc))}
                            </span>
                          </div>
                        </div>

                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleCompleteTask(task.id)}
                          className="shrink-0 text-emerald-700 hover:bg-emerald-50 hover:border-emerald-300"
                          title="Mark complete"
                          aria-label={`Complete task ${task.title}`}
                        >
                          <CheckCircle2 className="w-4 h-4" />
                        </Button>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
