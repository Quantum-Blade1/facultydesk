"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog } from "@/components/ui/dialog";
import { useToast } from "@/components/ui/toast";
import {
  api,
  CalendarEventResponse,
  ClashReportResponse,
  FreeSlotResponse,
  FacultyResponse,
} from "@/lib/api-client";
import {
  Calendar as CalendarIcon,
  Plus,
  AlertTriangle,
  Clock,
  MapPin,
  Users,
  Search,
  Check,
} from "lucide-react";

export default function CalendarPage() {
  const router = useRouter();
  const { user, profile, isLoading } = useAuth();
  const { toast } = useToast();

  const [viewMode, setViewMode] = React.useState<"week" | "day" | "list">("week");
  const [currentDate, setCurrentDate] = React.useState(new Date());
  const [events, setEvents] = React.useState<CalendarEventResponse[]>([]);
  const [clashes, setClashes] = React.useState<ClashReportResponse>({ clashes: [], total_clashes: 0 });
  const [facultyList, setFacultyList] = React.useState<FacultyResponse[]>([]);
  const [loading, setLoading] = React.useState(true);

  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [newEventTitle, setNewEventTitle] = React.useState("");
  const [newEventKind, setNewEventKind] = React.useState<"CLASS" | "MEETING" | "DEADLINE" | "CUSTOM">("MEETING");
  const [newEventLocation, setNewEventLocation] = React.useState("");
  const [newEventStart, setNewEventStart] = React.useState("");
  const [newEventEnd, setNewEventEnd] = React.useState("");
  const [newEventAttendees, setNewEventAttendees] = React.useState<string[]>([]);
  const [overrideClashes, setOverrideClashes] = React.useState(false);
  const [submitting, setSubmitting] = React.useState(false);

  const [freeSlotModalOpen, setFreeSlotModalOpen] = React.useState(false);
  const [selectedFacultyForSlots, setSelectedFacultyForSlots] = React.useState<string[]>([]);
  const [slotDate, setSlotDate] = React.useState(new Date().toISOString().split("T")[0] || "");
  const [slotDuration, setSlotDuration] = React.useState(60);
  const [foundFreeSlots, setFoundFreeSlots] = React.useState<FreeSlotResponse[]>([]);
  const [searchingSlots, setSearchingSlots] = React.useState(false);

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [isLoading, user, router]);

  const loadCalendarData = React.useCallback(async () => {
    try {
      setLoading(true);
      const start = new Date(currentDate);
      start.setDate(start.getDate() - 7);
      start.setHours(0, 0, 0, 0);

      const end = new Date(currentDate);
      end.setDate(end.getDate() + 14);
      end.setHours(23, 59, 59, 999);

      const [eventsData, clashData, facultyData] = await Promise.all([
        api.calendar.getEvents({
          start: start.toISOString(),
          end: end.toISOString(),
        }),
        api.calendar.getClashes(start.toISOString(), end.toISOString()),
        api.directory.listFaculty().catch(() => []),
      ]);

      setEvents(eventsData);
      setClashes(clashData);
      setFacultyList(facultyData);
    } catch (err) {
      console.error("Failed to fetch calendar data:", err);
    } finally {
      setLoading(false);
    }
  }, [currentDate]);

  React.useEffect(() => {
    if (user) {
      loadCalendarData();
    }
  }, [user, loadCalendarData]);

  React.useEffect(() => {
    if (typeof window !== "undefined" && window.innerWidth < 640) {
      setViewMode("list");
    }
  }, []);

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const attendees = newEventAttendees.length > 0 ? newEventAttendees : (profile ? [profile.id] : []);
      await api.calendar.createEvent({
        title: newEventTitle,
        kind: newEventKind,
        start_utc: new Date(newEventStart).toISOString(),
        end_utc: new Date(newEventEnd).toISOString(),
        location: newEventLocation || "",
        attendee_ids: attendees,
        override_clashes: overrideClashes,
      });

      toast("Event created successfully", "success");
      setCreateModalOpen(false);
      setNewEventTitle("");
      setNewEventLocation("");
      setNewEventAttendees([]);
      setOverrideClashes(false);
      loadCalendarData();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to create event", "error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSearchFreeSlots = async () => {
    if (selectedFacultyForSlots.length === 0) {
      toast("Please select at least one faculty member", "error");
      return;
    }
    setSearchingSlots(true);
    try {
      const slots = await api.calendar.findFreeSlots({
        attendee_ids: selectedFacultyForSlots,
        start_date: slotDate,
        end_date: slotDate,
        duration_minutes: slotDuration,
        work_start_time: "08:00:00",
        work_end_time: "18:00:00",
      });
      setFoundFreeSlots(slots);
      if (slots.length === 0) {
        toast("No common free slots found for the chosen criteria", "info");
      }
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to find free slots", "error");
    } finally {
      setSearchingSlots(false);
    }
  };

  const isEventClashing = (eventId: string) => {
    return clashes.clashes.some((c) => c.event_1_id === eventId || c.event_2_id === eventId);
  };

  const getKindColorClass = (kind: string) => {
    switch (kind) {
      case "CLASS":
        return "bg-blue-800 text-white border-blue-900";
      case "MEETING":
        return "bg-purple-700 text-white border-purple-800";
      case "DEADLINE":
        return "bg-rose-700 text-white border-rose-800";
      case "PERSONAL":
        return "bg-emerald-700 text-white border-emerald-800";
      default:
        return "bg-slate-700 text-white border-slate-800";
    }
  };

  const sortedEvents = [...events].sort(
    (a, b) => new Date(a.start_utc).getTime() - new Date(b.start_utc).getTime()
  );

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Top Control Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-lg border border-slate-200">
          <div>
            <h1 className="text-xl font-bold text-slate-900">Academic Calendar</h1>
            <p className="text-xs text-slate-500">
              Timetable classes, circular meetings, and documentation deadlines
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <div className="inline-flex rounded-md border border-slate-200 p-0.5 bg-slate-50 text-xs">
              <button
                onClick={() => setViewMode("week")}
                className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                  viewMode === "week" ? "bg-white shadow-xs text-slate-900 font-semibold" : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Week
              </button>
              <button
                onClick={() => setViewMode("day")}
                className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                  viewMode === "day" ? "bg-white shadow-xs text-slate-900 font-semibold" : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Day
              </button>
              <button
                onClick={() => setViewMode("list")}
                className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                  viewMode === "list" ? "bg-white shadow-xs text-slate-900 font-semibold" : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Agenda List
              </button>
            </div>

            {user?.role === "HOD" && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setFreeSlotModalOpen(true)}
                className="text-xs"
              >
                <Search className="w-3.5 h-3.5 mr-1" />
                Find Free Slots
              </Button>
            )}

            <Button
              size="sm"
              onClick={() => {
                const now = new Date();
                const nowStr = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
                  .toISOString()
                  .slice(0, 16);
                const laterStr = new Date(now.getTime() + 60 * 60000 - now.getTimezoneOffset() * 60000)
                  .toISOString()
                  .slice(0, 16);
                setNewEventStart(nowStr);
                setNewEventEnd(laterStr);
                setCreateModalOpen(true);
              }}
              className="text-xs"
            >
              <Plus className="w-3.5 h-3.5 mr-1" />
              New Event
            </Button>
          </div>
        </div>

        {/* Clash Banner if clashes exist */}
        {clashes.total_clashes > 0 && (
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-3.5 text-xs text-amber-900 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
              <span>
                <strong>{clashes.total_clashes} schedule clash(es) detected</strong> across your timetable and meetings. Overlapping items are highlighted.
              </span>
            </div>
            <Badge variant="warning">{clashes.total_clashes} CLASHES</Badge>
          </div>
        )}

        {/* Calendar View Content */}
        {loading ? (
          <div className="py-16 text-center text-xs text-slate-400">Loading events...</div>
        ) : (
          <Card>
            <CardHeader className="py-3 px-4 border-b border-slate-100 flex flex-row items-center justify-between">
              <CardTitle className="text-sm font-semibold">
                {viewMode === "list" ? "Agenda Timeline" : "Schedule Grid"}
              </CardTitle>
              <div className="flex items-center space-x-2 text-xs">
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-blue-800" />
                  <span>Class</span>
                </span>
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-purple-700" />
                  <span>Meeting</span>
                </span>
                <span className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-700" />
                  <span>Deadline</span>
                </span>
              </div>
            </CardHeader>
            <CardContent className="p-4">
              {sortedEvents.length === 0 ? (
                <div className="py-12 text-center space-y-2">
                  <CalendarIcon className="w-8 h-8 text-slate-300 mx-auto" />
                  <p className="text-xs text-slate-500">No events found in this date range.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {sortedEvents.map((event) => {
                    const clashing = isEventClashing(event.id);
                    const startDate = new Date(event.start_utc);
                    const endDate = new Date(event.end_utc);

                    return (
                      <div
                        key={event.id}
                        className={`p-3.5 rounded-lg border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                          clashing
                            ? "border-amber-400 bg-amber-50/50"
                            : "border-slate-200 bg-white hover:border-slate-300"
                        }`}
                      >
                        <div className="flex items-start space-x-3">
                          <div
                            className={`px-2.5 py-1 rounded text-xs font-bold uppercase shrink-0 ${getKindColorClass(
                              event.kind
                            )}`}
                          >
                            {event.kind}
                          </div>
                          <div>
                            <div className="flex items-center space-x-2">
                              <h4 className="text-sm font-semibold text-slate-900">{event.title}</h4>
                              {clashing && (
                                <Badge variant="warning" className="flex items-center space-x-1">
                                  <AlertTriangle className="w-3 h-3 mr-0.5" />
                                  <span>CLASH</span>
                                </Badge>
                              )}
                            </div>
                            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-500 font-mono mt-1">
                              <span className="flex items-center space-x-1">
                                <Clock className="w-3.5 h-3.5" />
                                <span>
                                  {new Intl.DateTimeFormat("en-IN", {
                                    weekday: "short",
                                    day: "numeric",
                                    month: "short",
                                    hour: "2-digit",
                                    minute: "2-digit",
                                    timeZone: "Asia/Kolkata",
                                  }).format(startDate)}{" "}
                                  -{" "}
                                  {new Intl.DateTimeFormat("en-IN", {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                    timeZone: "Asia/Kolkata",
                                  }).format(endDate)}
                                </span>
                              </span>
                              {event.location && (
                                <span className="flex items-center space-x-1">
                                  <MapPin className="w-3.5 h-3.5" />
                                  <span>{event.location}</span>
                                </span>
                              )}
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center space-x-2 self-end sm:self-center">
                          <button
                            onClick={async () => {
                              if (confirm(`Cancel event "${event.title}"?`)) {
                                try {
                                  await api.calendar.cancelEvent(event.id);
                                  toast("Event cancelled", "success");
                                  loadCalendarData();
                                } catch (err) {
                                  toast(err instanceof Error ? err.message : "Failed to cancel", "error");
                                }
                              }
                            }}
                            className="text-xs text-red-600 hover:underline px-2 py-1 cursor-pointer"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Create Event Modal */}
        <Dialog
          open={createModalOpen}
          onOpenChange={setCreateModalOpen}
          title="Create Calendar Event"
          description="Schedule a class, meeting, or personal block with sweep-line clash detection"
        >
          <form onSubmit={handleCreateEvent} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Event Title
              </label>
              <input
                type="text"
                required
                value={newEventTitle}
                onChange={(e) => setNewEventTitle(e.target.value)}
                placeholder="Department Review Meeting"
                className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Kind
                </label>
                <select
                  value={newEventKind}
                  onChange={(e) => setNewEventKind(e.target.value as "CLASS" | "MEETING" | "DEADLINE" | "CUSTOM")}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                >
                  <option value="MEETING">Meeting</option>
                  <option value="CLASS">Class</option>
                  <option value="DEADLINE">Deadline</option>
                  <option value="CUSTOM">Custom / Personal</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Venue / Location
                </label>
                <input
                  type="text"
                  value={newEventLocation}
                  onChange={(e) => setNewEventLocation(e.target.value)}
                  placeholder="Seminar Hall / Room 302"
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Start (Local IST)
                </label>
                <input
                  type="datetime-local"
                  required
                  value={newEventStart}
                  onChange={(e) => setNewEventStart(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  End (Local IST)
                </label>
                <input
                  type="datetime-local"
                  required
                  value={newEventEnd}
                  onChange={(e) => setNewEventEnd(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                />
              </div>
            </div>

            {facultyList.length > 0 && (
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Attendees (Faculty Initials)
                </label>
                <div className="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto p-2 border border-slate-200 rounded-md">
                  {facultyList.map((f) => {
                    const selected = newEventAttendees.includes(f.id);
                    return (
                      <button
                        key={f.id}
                        type="button"
                        onClick={() => {
                          if (selected) {
                            setNewEventAttendees(newEventAttendees.filter((id) => id !== f.id));
                          } else {
                            setNewEventAttendees([...newEventAttendees, f.id]);
                          }
                        }}
                        className={`px-2 py-1 rounded text-xs font-medium border cursor-pointer ${
                          selected
                            ? "bg-[#1e3a8a] text-white border-[#1e3a8a]"
                            : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                        }`}
                      >
                        {f.initials} ({f.full_name})
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            <div className="pt-2">
              <label className="flex items-center space-x-2 text-xs text-slate-700 cursor-pointer">
                <input
                  type="checkbox"
                  checked={overrideClashes}
                  onChange={(e) => setOverrideClashes(e.target.checked)}
                  className="rounded border-slate-300 text-[#1e3a8a] focus:ring-[#1e3a8a]"
                />
                <span>Override timetable and meeting clashes if detected</span>
              </label>
            </div>

            <div className="flex justify-end space-x-2 pt-4 border-t border-slate-100">
              <Button type="button" variant="outline" onClick={() => setCreateModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={submitting}>
                {submitting ? "Saving..." : "Create Event"}
              </Button>
            </div>
          </form>
        </Dialog>

        {/* Free Slot Finder Modal (HOD) */}
        <Dialog
          open={freeSlotModalOpen}
          onOpenChange={setFreeSlotModalOpen}
          title="Common Free Slot Finder"
          description="Find non-overlapping available intervals across multiple faculty members"
        >
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Select Faculty
              </label>
              <div className="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto p-2 border border-slate-200 rounded-md">
                {facultyList.map((f) => {
                  const selected = selectedFacultyForSlots.includes(f.id);
                  return (
                    <button
                      key={f.id}
                      type="button"
                      onClick={() => {
                        if (selected) {
                          setSelectedFacultyForSlots(selectedFacultyForSlots.filter((id) => id !== f.id));
                        } else {
                          setSelectedFacultyForSlots([...selectedFacultyForSlots, f.id]);
                        }
                      }}
                      className={`px-2 py-1 rounded text-xs font-medium border cursor-pointer ${
                        selected
                          ? "bg-[#1e3a8a] text-white border-[#1e3a8a]"
                          : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                      }`}
                    >
                      {f.initials} ({f.full_name})
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Search Date
                </label>
                <input
                  type="date"
                  value={slotDate}
                  onChange={(e) => setSlotDate(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Min Duration (Mins)
                </label>
                <input
                  type="number"
                  min="15"
                  step="15"
                  value={slotDuration}
                  onChange={(e) => setSlotDuration(Number(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                />
              </div>
            </div>

            <Button
              type="button"
              onClick={handleSearchFreeSlots}
              disabled={searchingSlots}
              className="w-full"
            >
              {searchingSlots ? "Searching Intervals..." : "Find Available Slots"}
            </Button>

            {foundFreeSlots.length > 0 && (
              <div className="pt-2 space-y-2">
                <span className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Available Common Intervals:
                </span>
                <div className="space-y-1.5 max-h-40 overflow-y-auto">
                  {foundFreeSlots.map((slot, idx) => (
                    <div
                      key={idx}
                      className="p-2.5 rounded border border-emerald-200 bg-emerald-50/50 flex items-center justify-between text-xs"
                    >
                      <span className="font-mono font-medium text-emerald-900">
                        {new Intl.DateTimeFormat("en-IN", {
                          hour: "2-digit",
                          minute: "2-digit",
                          timeZone: "Asia/Kolkata",
                        }).format(new Date(slot.start_utc))}{" "}
                        -{" "}
                        {new Intl.DateTimeFormat("en-IN", {
                          hour: "2-digit",
                          minute: "2-digit",
                          timeZone: "Asia/Kolkata",
                        }).format(new Date(slot.end_utc))}
                      </span>
                      <Badge variant="success">
                        {Math.round(
                          (new Date(slot.end_utc).getTime() - new Date(slot.start_utc).getTime()) / 60000
                        )}{" "}
                        mins
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Dialog>
      </div>
    </AppShell>
  );
}
