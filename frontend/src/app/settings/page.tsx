"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast";
import {
  api,
  ReminderRuleResponse,
  QuietHoursResponse,
} from "@/lib/api-client";
import { subscribeToPush, checkPushSubscription } from "@/lib/pwa";
import {
  Bell,
  Moon,
  Calendar,
  Copy,
  RotateCcw,
  Check,
  Send,
  Smartphone,
  ShieldCheck,
} from "lucide-react";

export default function SettingsPage() {
  const router = useRouter();
  const { user, profile, isLoading, refreshMe } = useAuth();
  const { toast } = useToast();

  const [rules, setRules] = React.useState<ReminderRuleResponse[]>([]);
  const [quietHours, setQuietHours] = React.useState<QuietHoursResponse | null>(null);
  const [pushEnabled, setPushEnabled] = React.useState(false);
  const [pushLoading, setPushLoading] = React.useState(false);
  const [copiedIcs, setCopiedIcs] = React.useState(false);
  const [rotatingToken, setRotatingToken] = React.useState(false);
  const [savingQuietHours, setSavingQuietHours] = React.useState(false);
  const [loading, setLoading] = React.useState(true);

  const [qhStart, setQhStart] = React.useState("22:00");
  const [qhEnd, setQhEnd] = React.useState("07:00");

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [isLoading, user, router]);

  const loadSettings = React.useCallback(async () => {
    try {
      setLoading(true);
      const [rulesData, qhData, isPushActive] = await Promise.all([
        api.reminders.getRules().catch(() => []),
        api.reminders.getQuietHours().catch(() => null),
        checkPushSubscription(),
      ]);

      setRules(rulesData);
      setQuietHours(qhData);
      setPushEnabled(isPushActive);

      if (qhData?.start_time) setQhStart(qhData.start_time.slice(0, 5));
      if (qhData?.end_time) setQhEnd(qhData.end_time.slice(0, 5));
    } catch (err) {
      console.error("Failed to load settings:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    if (user) {
      loadSettings();
    }
  }, [user, loadSettings]);

  const handleTogglePush = async () => {
    setPushLoading(true);
    try {
      const res = await subscribeToPush();
      if (res.success) {
        setPushEnabled(true);
        toast(res.message, "success");
      } else {
        toast(res.message, "error");
      }
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to toggle push notifications", "error");
    } finally {
      setPushLoading(false);
    }
  };

  const handleSaveQuietHours = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingQuietHours(true);
    try {
      await api.reminders.updateQuietHours({
        start_time: qhStart.length === 5 ? `${qhStart}:00` : qhStart,
        end_time: qhEnd.length === 5 ? `${qhEnd}:00` : qhEnd,
      });
      toast("Quiet hours updated. Non-emergency reminders will be deferred.", "success");
      loadSettings();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to update quiet hours", "error");
    } finally {
      setSavingQuietHours(false);
    }
  };

  const [icsFeedUrl, setIcsFeedUrl] = React.useState<string>("");

  const handleCopyIcsLink = () => {
    if (!icsFeedUrl) {
      toast("Click 'Generate / Rotate Secret Token' to obtain your personal ICS URL", "info");
      return;
    }
    navigator.clipboard.writeText(icsFeedUrl);
    setCopiedIcs(true);
    toast("Calendar feed URL copied to clipboard!", "success");
    setTimeout(() => setCopiedIcs(false), 3000);
  };

  const handleRotateIcsToken = async () => {
    setRotatingToken(true);
    try {
      const res = await api.calendar.rotateIcsToken();
      if (res.feed_url) {
        setIcsFeedUrl(`${window.location.origin}${res.feed_url}`);
      }
      toast("ICS token generated/rotated! Use this link in your calendar app.", "success");
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to rotate token", "error");
    } finally {
      setRotatingToken(false);
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-xl font-bold text-slate-900">Preferences & Reminders</h1>
          <p className="text-xs text-slate-500">
            Configure multi-channel notifications, quiet hours shift, and external iCalendar feed
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Web Push Notification Section */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center space-x-2">
                <Smartphone className="w-4 h-4 text-[#1e3a8a]" />
                <span>Web Push Notifications</span>
              </CardTitle>
              <CardDescription>
                Receive instant mobile alerts for upcoming classes and circular meetings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-3.5 bg-slate-50 border border-slate-200 rounded-lg">
                <div className="space-y-0.5">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-semibold text-slate-900">Push Status</span>
                    <Badge variant={pushEnabled ? "success" : "default"}>
                      {pushEnabled ? "ACTIVE" : "DISABLED"}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-500">
                    {pushEnabled
                      ? "Device registered with VAPID subscription keys"
                      : "Click below to grant notification permission"}
                  </p>
                </div>

                <Button
                  size="sm"
                  variant={pushEnabled ? "outline" : "primary"}
                  onClick={handleTogglePush}
                  disabled={pushLoading}
                >
                  {pushLoading ? "Registering..." : pushEnabled ? "Re-subscribe" : "Enable Push"}
                </Button>
              </div>

              <div className="text-[11px] text-slate-500 space-y-1">
                <div className="flex items-center space-x-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>VAPID cryptographic handshake with zero external tracking</span>
                </div>
                <div className="flex items-center space-x-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Automatic pruning of stale browser endpoints (HTTP 410 Gone)</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quiet Hours Section */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center space-x-2">
                <Moon className="w-4 h-4 text-[#1e3a8a]" />
                <span>Quiet Hours Preferences</span>
              </CardTitle>
              <CardDescription>
                Defer notifications across midnight window; morning class exemption applies
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSaveQuietHours} className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Start Time (IST)
                    </label>
                    <input
                      type="time"
                      value={qhStart}
                      onChange={(e) => setQhStart(e.target.value)}
                      className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      End Time (IST)
                    </label>
                    <input
                      type="time"
                      value={qhEnd}
                      onChange={(e) => setQhEnd(e.target.value)}
                      className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                    />
                  </div>
                </div>

                <div className="flex justify-end">
                  <Button type="submit" size="sm" disabled={savingQuietHours}>
                    {savingQuietHours ? "Saving..." : "Save Quiet Hours"}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* ICS External Calendar Feed */}
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="text-base flex items-center space-x-2">
                <Calendar className="w-4 h-4 text-[#1e3a8a]" />
                <span>RFC 5545 iCalendar Subscription Feed</span>
              </CardTitle>
              <CardDescription>
                Sync your classes, meetings, and deadlines to Google Calendar, Apple Calendar, or Outlook
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg space-y-2">
                <span className="block text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Secret WebCal Subscription URL
                </span>
                <div className="flex items-center space-x-2">
                  <input
                    type="text"
                    readOnly
                    value={
                      icsFeedUrl || "Click 'Generate / Rotate Secret Token' below to obtain your personal URL"
                    }
                    className="flex-1 px-3 py-2 border border-slate-300 rounded-md text-xs font-mono bg-white text-slate-700 select-all"
                  />
                  <Button size="sm" variant="outline" onClick={handleCopyIcsLink}>
                    {copiedIcs ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
                    <span className="ml-1.5">{copiedIcs ? "Copied" : "Copy Link"}</span>
                  </Button>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2">
                <p className="text-xs text-slate-500">
                  If your link was exposed, rotate your token immediately to invalidate past subscriptions.
                </p>
                <Button
                  size="sm"
                  variant="danger"
                  onClick={handleRotateIcsToken}
                  disabled={rotatingToken}
                >
                  <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
                  {rotatingToken ? "Rotating..." : "Rotate Secret Token"}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Active Reminder Rules Table */}
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="text-base flex items-center space-x-2">
                <Bell className="w-4 h-4 text-[#1e3a8a]" />
                <span>Configured Reminder Rules</span>
              </CardTitle>
              <CardDescription>
                Active notification lead times dispatched with exactly-once delivery guarantees
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="py-6 text-center text-xs text-slate-400">Loading rules...</div>
              ) : rules.length === 0 ? (
                <div className="py-6 text-center text-xs text-slate-400">
                  Default rules active: Classes at 15m; Meetings at 24h, 1h, and 10m.
                </div>
              ) : (
                <div className="border border-slate-200 rounded-lg overflow-x-auto">
                  <table className="w-full text-xs text-left">
                    <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                      <tr>
                        <th className="px-4 py-2.5">Event Kind</th>
                        <th className="px-4 py-2.5">Offsets (Minutes Before)</th>
                        <th className="px-4 py-2.5">Channels</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 font-mono">
                      {rules.map((rule) => (
                        <tr key={rule.id}>
                          <td className="px-4 py-2.5 font-sans font-semibold text-slate-800">
                            <Badge variant={rule.event_kind === "CLASS" ? "blue" : "purple"}>
                              {rule.event_kind}
                            </Badge>
                          </td>
                          <td className="px-4 py-2.5 text-slate-700">
                            {rule.offsets_minutes.join("m, ")}m
                          </td>
                          <td className="px-4 py-2.5">
                            <div className="flex space-x-1.5">
                              {rule.channels.map((ch) => (
                                <Badge key={ch} variant="outline">
                                  {ch}
                                </Badge>
                              ))}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
