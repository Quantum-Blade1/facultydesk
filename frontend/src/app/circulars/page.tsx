"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog } from "@/components/ui/dialog";
import { useToast } from "@/components/ui/toast";
import {
  api,
  CircularDetailResponse,
  FacultyResponse,
} from "@/lib/api-client";
import {
  FileText,
  Camera,
  Upload,
  AlertTriangle,
  CheckCircle2,
  Clock,
  MapPin,
  Users,
  Eye,
  Check,
  X,
  FileSearch,
  RefreshCw,
} from "lucide-react";

export default function CircularsPage() {
  const router = useRouter();
  const { user, profile, isLoading } = useAuth();
  const { toast } = useToast();

  const [circulars, setCirculars] = React.useState<CircularDetailResponse[]>([]);
  const [facultyList, setFacultyList] = React.useState<FacultyResponse[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [uploading, setUploading] = React.useState(false);

  const [reviewModalOpen, setReviewModalOpen] = React.useState(false);
  const [activeCircular, setActiveCircular] = React.useState<CircularDetailResponse | null>(null);
  const [editTitle, setEditTitle] = React.useState("");
  const [editDate, setEditDate] = React.useState("");
  const [editStartTime, setEditStartTime] = React.useState("");
  const [editEndTime, setEditEndTime] = React.useState("");
  const [editVenue, setEditVenue] = React.useState("");
  const [editAttendees, setEditAttendees] = React.useState<string[]>([]);
  const [confirming, setConfirming] = React.useState(false);
  const [rejectReason, setRejectReason] = React.useState("");
  const [showRejectInput, setShowRejectInput] = React.useState(false);

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [isLoading, user, router]);

  const loadCirculars = React.useCallback(async () => {
    try {
      setLoading(true);
      const [queue, faculty] = await Promise.all([
        api.circulars.listReviewQueue().catch(() => []),
        api.directory.listFaculty().catch(() => []),
      ]);
      setCirculars(queue);
      setFacultyList(faculty);
    } catch (err) {
      console.error("Failed to load circulars:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    if (user) {
      loadCirculars();
      const timer = setInterval(() => {
        loadCirculars();
      }, 3000);
      return () => clearInterval(timer);
    }
  }, [user, loadCirculars]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0]) return;
    const file = e.target.files[0];
    setUploading(true);
    try {
      const res = await api.circulars.upload(file, profile?.department_id);
      toast("Circular uploaded. Background OCR and extraction running...", "info");
      setTimeout(() => {
        loadCirculars();
      }, 2000);
    } catch (err) {
      toast(err instanceof Error ? err.message : "Upload failed", "error");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const openReviewModal = (circ: CircularDetailResponse) => {
    setActiveCircular(circ);
    const ext = circ.extracted_fields as {
      title?: string;
      date?: string;
      start_time?: string;
      end_time?: string;
      venue?: string;
      attendee_faculty_ids?: string[];
      confidence?: number;
      low_confidence_fields?: string[];
    } | null;

    setEditTitle(ext?.title || circ.file_key);
    setEditDate(ext?.date || "");
    setEditStartTime(ext?.start_time || "10:30");
    setEditEndTime(ext?.end_time || "11:30");
    setEditVenue(ext?.venue || "");
    setEditAttendees(ext?.attendee_faculty_ids || (profile ? [profile.id] : []));
    setShowRejectInput(false);
    setRejectReason("");
    setReviewModalOpen(true);
  };

  const handleConfirmCircular = async () => {
    if (!activeCircular) return;
    setConfirming(true);
    try {
      await api.circulars.confirm(activeCircular.id, {
        title: editTitle,
        meeting_date: editDate,
        start_time: editStartTime,
        end_time: editEndTime,
        venue: editVenue,
        attendee_ids: editAttendees,
      });

      toast("Meeting confirmed and scheduled across attendee calendars!", "success");
      setReviewModalOpen(false);
      loadCirculars();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Confirmation failed", "error");
    } finally {
      setConfirming(false);
    }
  };

  const handleRejectCircular = async () => {
    if (!activeCircular) return;
    if (!rejectReason) {
      toast("Please provide a rejection reason", "error");
      return;
    }
    setConfirming(true);
    try {
      await api.circulars.reject(activeCircular.id, {
        reason: rejectReason,
      });
      toast("Circular rejected", "info");
      setReviewModalOpen(false);
      loadCirculars();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Rejection failed", "error");
    } finally {
      setConfirming(false);
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold text-slate-900">Meeting Circulars</h1>
            <p className="text-xs text-slate-500">
              OCR scanning, formal meeting grammar extraction, and human review queue
            </p>
          </div>

          <div className="flex items-center space-x-2">
            {/* Camera Capture on Phone */}
            <label className="inline-flex items-center justify-center px-3 py-2 border border-slate-300 rounded-md text-xs font-semibold bg-white text-slate-700 hover:bg-slate-50 cursor-pointer shadow-xs">
              <Camera className="w-4 h-4 mr-1.5 text-slate-500" />
              <span>Camera</span>
              <input
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleFileUpload}
                disabled={uploading}
                className="hidden"
              />
            </label>

            {/* Document / PDF Upload */}
            <label className="inline-flex items-center justify-center px-3 py-2 border border-[#1e3a8a] rounded-md text-xs font-semibold bg-[#1e3a8a] text-white hover:bg-[#1e40af] cursor-pointer shadow-xs">
              <Upload className="w-4 h-4 mr-1.5" />
              <span>{uploading ? "Uploading..." : "Upload Circular"}</span>
              <input
                type="file"
                accept="application/pdf,image/png,image/jpeg"
                onChange={handleFileUpload}
                disabled={uploading}
                className="hidden"
              />
            </label>
          </div>
        </div>

        {/* Circulars List */}
        <Card>
          <CardHeader className="py-3 px-4 border-b border-slate-100 flex flex-row items-center justify-between">
            <CardTitle className="text-sm font-semibold">Review Queue & Extractions</CardTitle>
            <Badge variant="outline">{circulars.length} Documents</Badge>
          </CardHeader>
          <CardContent className="p-4">
            {loading ? (
              <div className="py-12 text-center text-xs text-slate-400">Loading circulars...</div>
            ) : circulars.length === 0 ? (
              <div className="py-12 text-center space-y-2">
                <FileSearch className="w-8 h-8 text-slate-300 mx-auto" />
                <p className="text-xs text-slate-500">No circulars in review queue.</p>
                <p className="text-[11px] text-slate-400">
                  Upload a photo or PDF notice above to extract meeting dates, times, and attendees.
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {circulars.map((circ) => {
                  const ext = circ.extracted_fields as {
                    title?: string;
                    date?: string;
                    start_time?: string;
                    venue?: string;
                    confidence?: number;
                  } | null;

                  const confidencePct = ext?.confidence ? Math.round(ext.confidence * 100) : 0;
                  const isNeedsReview = circ.status === "NEEDS_REVIEW";

                  return (
                    <div
                      key={circ.id}
                      className={`p-3.5 rounded-lg border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                        isNeedsReview
                          ? "border-amber-300 bg-amber-50/30 hover:border-amber-400"
                          : "border-slate-200 bg-white"
                      }`}
                    >
                      <div className="flex items-start space-x-3">
                        <div className="p-2 rounded-md bg-slate-100 text-slate-600 shrink-0 mt-0.5">
                          <FileText className="w-5 h-5 text-[#1e3a8a]" />
                        </div>
                        <div>
                          <div className="flex items-center space-x-2">
                            <h4 className="text-sm font-semibold text-slate-900">
                              {ext?.title || circ.file_key}
                            </h4>
                            <Badge
                              variant={
                                circ.status === "CONFIRMED"
                                  ? "success"
                                  : circ.status === "NEEDS_REVIEW"
                                  ? "warning"
                                  : circ.status === "REJECTED"
                                  ? "danger"
                                  : "default"
                              }
                            >
                              {circ.status}
                            </Badge>
                            {confidencePct > 0 && (
                              <Badge variant={confidencePct >= 70 ? "blue" : "warning"}>
                                OCR: {confidencePct}%
                              </Badge>
                            )}
                          </div>
                          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-500 font-mono mt-1">
                            {ext?.date && (
                              <span className="flex items-center space-x-1">
                                <Clock className="w-3.5 h-3.5" />
                                <span>
                                  {ext.date} {ext.start_time ? `at ${ext.start_time}` : ""}
                                </span>
                              </span>
                            )}
                            {ext?.venue && (
                              <span className="flex items-center space-x-1">
                                <MapPin className="w-3.5 h-3.5" />
                                <span>{ext.venue}</span>
                              </span>
                            )}
                            <span className="text-slate-400">
                              Status: {circ.status}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2 self-end sm:self-center">
                        <Button
                          size="sm"
                          variant={isNeedsReview ? "primary" : "outline"}
                          onClick={() => openReviewModal(circ)}
                          className="text-xs"
                        >
                          <Eye className="w-3.5 h-3.5 mr-1" />
                          {isNeedsReview ? "Review & Confirm" : "View Details"}
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Review & Edit Modal */}
        <Dialog
          open={reviewModalOpen}
          onOpenChange={setReviewModalOpen}
          title="Review Circular Extraction"
          description="Verify extracted fields before confirming meeting onto faculty calendars"
          maxWidth="2xl"
        >
          {activeCircular && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Document Information / Preview */}
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-2">
                  <span className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
                    Document Source
                  </span>
                  <div className="text-xs text-slate-600 font-mono space-y-1">
                    <div>
                      <span className="text-slate-400">File Key: </span>
                      <span className="truncate block">{activeCircular.file_key}</span>
                    </div>
                    <div>
                      <span className="text-slate-400">Confidence: </span>
                      <span>{Math.round(activeCircular.confidence * 100)}%</span>
                    </div>
                    <div>
                      <span className="text-slate-400">Status: </span>
                      <Badge variant="warning">{activeCircular.status}</Badge>
                    </div>
                  </div>

                  {/* OCR Review Reasons if any */}
                  {Array.isArray((activeCircular.extracted_fields as Record<string, unknown>)?.low_confidence_fields) &&
                    ((activeCircular.extracted_fields as Record<string, unknown>).low_confidence_fields as string[]).length > 0 && (
                    <div className="pt-2 border-t border-slate-200">
                      <span className="text-[11px] font-semibold text-amber-800 uppercase flex items-center space-x-1 mb-1">
                        <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                        <span>Flags Triggering Review:</span>
                      </span>
                      <ul className="text-xs text-amber-900 list-disc list-inside space-y-0.5">
                        {((activeCircular.extracted_fields as Record<string, unknown>).low_confidence_fields as string[]).map((r, i) => (
                          <li key={i}>{r}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Editable Fields Form */}
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Meeting Title
                    </label>
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="w-full px-3 py-1.5 border border-slate-300 rounded-md text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-2">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        Date
                      </label>
                      <input
                        type="date"
                        value={editDate}
                        onChange={(e) => setEditDate(e.target.value)}
                        className="w-full px-2 py-1.5 border border-slate-300 rounded-md text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        Start
                      </label>
                      <input
                        type="time"
                        value={editStartTime}
                        onChange={(e) => setEditStartTime(e.target.value)}
                        className="w-full px-2 py-1.5 border border-slate-300 rounded-md text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        End
                      </label>
                      <input
                        type="time"
                        value={editEndTime}
                        onChange={(e) => setEditEndTime(e.target.value)}
                        className="w-full px-2 py-1.5 border border-slate-300 rounded-md text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Venue / Room
                    </label>
                    <input
                      type="text"
                      value={editVenue}
                      onChange={(e) => setEditVenue(e.target.value)}
                      placeholder="Seminar Hall"
                      className="w-full px-3 py-1.5 border border-slate-300 rounded-md text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Resolved Attendees
                    </label>
                    <div className="flex flex-wrap gap-1 max-h-24 overflow-y-auto p-1.5 border border-slate-200 rounded-md">
                      {facultyList.map((f) => {
                        const selected = editAttendees.includes(f.id);
                        return (
                          <button
                            key={f.id}
                            type="button"
                            onClick={() => {
                              if (selected) {
                                setEditAttendees(editAttendees.filter((id) => id !== f.id));
                              } else {
                                setEditAttendees([...editAttendees, f.id]);
                              }
                            }}
                            className={`px-1.5 py-0.5 rounded text-[11px] font-medium border cursor-pointer ${
                              selected
                                ? "bg-[#1e3a8a] text-white border-[#1e3a8a]"
                                : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                            }`}
                          >
                            {f.initials}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>

              {/* Rejection Input */}
              {showRejectInput && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg space-y-2">
                  <label className="block text-xs font-semibold text-red-900">
                    Reason for Rejection:
                  </label>
                  <input
                    type="text"
                    value={rejectReason}
                    onChange={(e) => setRejectReason(e.target.value)}
                    placeholder="Illegible text / Corrupted scan / Duplicate meeting"
                    className="w-full px-3 py-1.5 border border-red-300 rounded-md text-xs text-red-900 focus:outline-none focus:ring-2 focus:ring-red-600 bg-white"
                  />
                  <div className="flex justify-end space-x-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setShowRejectInput(false)}
                      className="text-xs"
                    >
                      Cancel
                    </Button>
                    <Button
                      size="sm"
                      variant="danger"
                      onClick={handleRejectCircular}
                      disabled={confirming}
                      className="text-xs"
                    >
                      Confirm Rejection
                    </Button>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                {!showRejectInput && (
                  <Button
                    type="button"
                    variant="danger"
                    size="sm"
                    onClick={() => setShowRejectInput(true)}
                  >
                    Reject Circular
                  </Button>
                )}
                <div className="flex space-x-2 ml-auto">
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => setReviewModalOpen(false)}
                  >
                    Close
                  </Button>
                  <Button
                    type="button"
                    size="sm"
                    onClick={handleConfirmCircular}
                    disabled={confirming || !editDate || !editStartTime}
                    className="bg-emerald-600 hover:bg-emerald-700"
                  >
                    {confirming ? "Confirming..." : "Confirm & Schedule Meeting"}
                  </Button>
                </div>
              </div>
            </div>
          )}
        </Dialog>
      </div>
    </AppShell>
  );
}
