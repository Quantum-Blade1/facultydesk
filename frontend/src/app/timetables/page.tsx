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
  AcademicTermResponse,
  TimetableUploadDetailResponse,
} from "@/lib/api-client";
import {
  UploadCloud,
  FileSpreadsheet,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Users,
  RefreshCw,
  FileText,
} from "lucide-react";

export default function TimetablesPage() {
  const router = useRouter();
  const { user, profile, isLoading } = useAuth();
  const { toast } = useToast();

  const [terms, setTerms] = React.useState<AcademicTermResponse[]>([]);
  const [selectedTermId, setSelectedTermId] = React.useState<string>("");
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const [dragActive, setDragActive] = React.useState(false);
  const [uploading, setUploading] = React.useState(false);
  const [currentUploadId, setCurrentUploadId] = React.useState<string | null>(null);
  const [uploadDetail, setUploadDetail] = React.useState<TimetableUploadDetailResponse | null>(null);
  const [confirming, setConfirming] = React.useState(false);

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
      return;
    }
    if (!isLoading && user && user.role === "FACULTY") {
      router.push("/today");
    }
  }, [isLoading, user, router]);

  React.useEffect(() => {
    async function loadTerms() {
      try {
        const termsData = await api.directory.listTerms();
        setTerms(termsData);
        if (termsData.length > 0 && termsData[0]?.id) {
          setSelectedTermId(termsData[0].id);
        }
      } catch (err) {
        console.error("Failed to load academic terms:", err);
      }
    }
    if (user && (user.role === "ADMIN" || user.role === "HOD")) {
      loadTerms();
    }
  }, [user]);

  React.useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    if (currentUploadId && uploadDetail?.status !== "PREVIEW_READY" && uploadDetail?.status !== "CONFIRMED" && uploadDetail?.status !== "FAILED") {
      interval = setInterval(async () => {
        try {
          const detail = await api.timetables.get(currentUploadId);
          setUploadDetail(detail);
          if (detail.status === "PREVIEW_READY") {
            toast("Timetable parsed successfully! Ready for preview.", "success");
          } else if (detail.status === "FAILED") {
            toast("Timetable parsing failed. Check report.", "error");
          }
        } catch {
        }
      }, 1500);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [currentUploadId, uploadDetail?.status, toast]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !selectedTermId) {
      toast("Please select a file and an academic term", "error");
      return;
    }
    setUploading(true);
    try {
      const res = await api.timetables.upload(selectedFile, selectedTermId, profile?.department_id);
      setCurrentUploadId(res.upload_id);
      toast("Timetable uploaded. Processing in background...", "info");
      const detail = await api.timetables.get(res.upload_id);
      setUploadDetail(detail);
    } catch (err) {
      toast(err instanceof Error ? err.message : "Upload failed", "error");
    } finally {
      setUploading(false);
    }
  };

  const handleConfirm = async () => {
    if (!currentUploadId) return;
    setConfirming(true);
    try {
      const res = await api.timetables.confirm(currentUploadId);
      toast(`Confirmed! Created ${res.slots_created} slots across faculty schedules.`, "success");
      const detail = await api.timetables.get(currentUploadId);
      setUploadDetail(detail);
    } catch (err) {
      toast(err instanceof Error ? err.message : "Confirmation failed", "error");
    } finally {
      setConfirming(false);
    }
  };

  const report = uploadDetail?.parse_report as {
    total_slots?: number;
    resolved_slots?: number;
    unresolved_count?: number;
    unresolved_tokens?: Array<{ cell: string; token: string; reason: string }>;
    co_teacher_cells?: Array<{ cell: string; text: string; resolved_faculty: string[] }>;
    sample_slots?: Array<{
      weekday: number;
      start_time: string;
      end_time: string;
      course_id: string;
      faculty_initials: string;
      room: string;
    }>;
  } | undefined;

  const weekdayNames = ["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-xl font-bold text-slate-900">Upload Department Timetable</h1>
          <p className="text-xs text-slate-500">
            Ingest master schedules (XLSX, CSV, PDF), resolve faculty initials, and expand co-teacher lab periods
          </p>
        </div>

        {/* Upload Zone */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Upload Schedule File</CardTitle>
            <CardDescription>
              Supported formats: Native Excel (.xlsx), Comma-Separated Values (.csv), or digital PDF with text layer
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Academic Term
                </label>
                <select
                  value={selectedTermId}
                  onChange={(e) => setSelectedTermId(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                >
                  {terms.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.name} ({new Date(t.start_date).toLocaleDateString()} -{" "}
                      {new Date(t.end_date).toLocaleDateString()})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
                dragActive ? "border-[#1e3a8a] bg-blue-50/50" : "border-slate-300 bg-slate-50/50"
              }`}
            >
              <FileSpreadsheet className="w-10 h-10 text-slate-400 mx-auto mb-2" />
              <p className="text-sm font-medium text-slate-700">
                {selectedFile ? selectedFile.name : "Drag and drop department timetable here"}
              </p>
              <p className="text-xs text-slate-500 mt-1">Maximum file size: 15 MB</p>
              <div className="mt-3">
                <label className="inline-flex items-center justify-center px-4 py-2 border border-slate-300 rounded-md text-xs font-semibold bg-white text-slate-700 hover:bg-slate-50 cursor-pointer shadow-xs">
                  <span>Browse File</span>
                  <input
                    type="file"
                    accept=".xlsx,.csv,.pdf"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                </label>
              </div>
            </div>

            <div className="flex justify-end">
              <Button
                onClick={handleUpload}
                disabled={!selectedFile || !selectedTermId || uploading}
                className="w-full sm:w-auto"
              >
                {uploading ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <UploadCloud className="w-4 h-4 mr-2" />
                    Parse Timetable
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Live Parsing Status & Preview Report */}
        {uploadDetail && (
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-3">
              <div>
                <div className="flex items-center space-x-2">
                  <CardTitle className="text-base">Parsing & Resolution Report</CardTitle>
                  <Badge
                    variant={
                      uploadDetail.status === "CONFIRMED"
                        ? "success"
                        : uploadDetail.status === "PREVIEW_READY"
                        ? "blue"
                        : uploadDetail.status === "FAILED"
                        ? "danger"
                        : "warning"
                    }
                  >
                    {uploadDetail.status}
                  </Badge>
                </div>
                <p className="text-xs text-slate-500 mt-0.5">
                  Uploaded at {new Date(uploadDetail.uploaded_at_utc).toLocaleTimeString()}
                </p>
              </div>

              {uploadDetail.status === "PREVIEW_READY" && (
                <Button onClick={handleConfirm} disabled={confirming} className="bg-emerald-600 hover:bg-emerald-700">
                  {confirming ? "Confirming..." : "Confirm & Save Timetable"}
                </Button>
              )}
            </CardHeader>
            <CardContent className="space-y-6">
              {report && (
                <>
                  {/* Summary Metric Counters */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                      <span className="block text-[11px] font-semibold text-slate-400 uppercase">
                        Total Slots
                      </span>
                      <span className="text-xl font-bold text-slate-900 font-mono">
                        {report.total_slots ?? 0}
                      </span>
                    </div>
                    <div className="p-3 bg-emerald-50 rounded-lg border border-emerald-200">
                      <span className="block text-[11px] font-semibold text-emerald-700 uppercase">
                        Resolved Slots
                      </span>
                      <span className="text-xl font-bold text-emerald-800 font-mono">
                        {report.resolved_slots ?? 0}
                      </span>
                    </div>
                    <div className="p-3 bg-amber-50 rounded-lg border border-amber-200">
                      <span className="block text-[11px] font-semibold text-amber-700 uppercase">
                        Unresolved
                      </span>
                      <span className="text-xl font-bold text-amber-800 font-mono">
                        {report.unresolved_count ?? 0}
                      </span>
                    </div>
                    <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                      <span className="block text-[11px] font-semibold text-purple-700 uppercase">
                        Co-Teacher Cells
                      </span>
                      <span className="text-xl font-bold text-purple-800 font-mono">
                        {report.co_teacher_cells?.length ?? 0}
                      </span>
                    </div>
                  </div>

                  {/* Unresolved Tokens Warning if any */}
                  {report.unresolved_tokens && report.unresolved_tokens.length > 0 && (
                    <div className="p-4 rounded-lg bg-amber-50 border border-amber-200 space-y-2">
                      <div className="flex items-center space-x-2 text-xs font-semibold text-amber-900">
                        <AlertTriangle className="w-4 h-4 text-amber-600" />
                        <span>Unresolved Initials / Cell Tokens (Require Manual Verification):</span>
                      </div>
                      <div className="space-y-1">
                        {report.unresolved_tokens.map((u, i) => (
                          <div key={i} className="text-xs text-amber-800 font-mono flex items-center space-x-2">
                            <span className="font-bold">[{u.cell}]</span>
                            <span>{u.token}</span>
                            <span className="text-slate-500">• {u.reason}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Co-Teacher Lab Splits if any */}
                  {report.co_teacher_cells && report.co_teacher_cells.length > 0 && (
                    <div className="p-4 rounded-lg bg-purple-50 border border-purple-200 space-y-2">
                      <div className="flex items-center space-x-2 text-xs font-semibold text-purple-900">
                        <Users className="w-4 h-4 text-purple-600" />
                        <span>Co-Teacher Multi-Faculty Labs Expanded:</span>
                      </div>
                      <div className="space-y-1">
                        {report.co_teacher_cells.map((c, i) => (
                          <div key={i} className="text-xs text-purple-800 font-mono flex items-center space-x-2">
                            <span className="font-bold">[{c.cell}]</span>
                            <span>{c.text}</span>
                            <span className="text-slate-500">
                              → Split to {c.resolved_faculty.join(", ")}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Preview Table of Extracted Slots */}
                  {report.sample_slots && report.sample_slots.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
                        Sample Extracted Slots
                      </h4>
                      <div className="border border-slate-200 rounded-lg overflow-x-auto">
                        <table className="w-full text-xs text-left">
                          <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                            <tr>
                              <th className="px-3 py-2">Day</th>
                              <th className="px-3 py-2">Time Interval</th>
                              <th className="px-3 py-2">Course</th>
                              <th className="px-3 py-2">Faculty</th>
                              <th className="px-3 py-2">Room</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100 font-mono">
                            {report.sample_slots.map((slot, i) => (
                              <tr key={i} className="hover:bg-slate-50/50">
                                <td className="px-3 py-2 font-semibold text-slate-800">
                                  {weekdayNames[slot.weekday] || `Day ${slot.weekday}`}
                                </td>
                                <td className="px-3 py-2 text-slate-600">
                                  {slot.start_time} - {slot.end_time}
                                </td>
                                <td className="px-3 py-2 text-slate-900 font-sans font-medium">
                                  {slot.course_id}
                                </td>
                                <td className="px-3 py-2">
                                  <Badge variant="blue">{slot.faculty_initials}</Badge>
                                </td>
                                <td className="px-3 py-2 text-slate-500">{slot.room}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </AppShell>
  );
}
