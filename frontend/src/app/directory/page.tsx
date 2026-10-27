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
  FacultyResponse,
  BulkImportReportResponse,
  AcademicTermResponse,
  HolidayResponse,
} from "@/lib/api-client";
import {
  Users,
  Upload,
  Calendar,
  CheckCircle2,
  AlertCircle,
  FileSpreadsheet,
  Building,
  Mail,
  Shield,
} from "lucide-react";

export default function DirectoryPage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();
  const { toast } = useToast();

  const [activeTab, setActiveTab] = React.useState<"faculty" | "terms-holidays">("faculty");
  const [faculty, setFaculty] = React.useState<FacultyResponse[]>([]);
  const [terms, setTerms] = React.useState<AcademicTermResponse[]>([]);
  const [holidays, setHolidays] = React.useState<HolidayResponse[]>([]);
  const [loading, setLoading] = React.useState(true);

  const [importModalOpen, setImportModalOpen] = React.useState(false);
  const [importFile, setImportFile] = React.useState<File | null>(null);
  const [importing, setImporting] = React.useState(false);
  const [importReport, setImportReport] = React.useState<BulkImportReportResponse | null>(null);

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
      return;
    }
    if (!isLoading && user && user.role === "FACULTY") {
      router.push("/today");
    }
  }, [isLoading, user, router]);

  const loadDirectoryData = React.useCallback(async () => {
    try {
      setLoading(true);
      const [facData, termsData, holidaysData] = await Promise.all([
        api.directory.listFaculty().catch(() => []),
        api.directory.listTerms().catch(() => []),
        api.directory.listHolidays().catch(() => []),
      ]);

      setFaculty(facData);
      setTerms(termsData);
      setHolidays(holidaysData);
    } catch (err) {
      console.error("Failed to load directory data:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    if (user && (user.role === "ADMIN" || user.role === "HOD")) {
      loadDirectoryData();
    }
  }, [user, loadDirectoryData]);

  const handleBulkImport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!importFile) return;
    setImporting(true);
    try {
      const report = await api.directory.bulkImport(importFile);
      setImportReport(report);
      toast(
        `Import completed: ${report.created_count} created, ${report.updated_count} updated, ${report.rejected_count} rejected.`,
        report.rejected_count > 0 ? "info" : "success"
      );
      loadDirectoryData();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Bulk import failed", "error");
    } finally {
      setImporting(false);
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-lg border border-slate-200">
          <div>
            <h1 className="text-xl font-bold text-slate-900">Department Administration</h1>
            <p className="text-xs text-slate-500">
              Manage faculty accounts, bulk roster import, academic terms, and gazetted holidays
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <div className="inline-flex rounded-md border border-slate-200 p-0.5 bg-slate-50 text-xs">
              <button
                onClick={() => setActiveTab("faculty")}
                className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                  activeTab === "faculty"
                    ? "bg-white shadow-xs text-slate-900 font-semibold"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Faculty Directory
              </button>
              <button
                onClick={() => setActiveTab("terms-holidays")}
                className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                  activeTab === "terms-holidays"
                    ? "bg-white shadow-xs text-slate-900 font-semibold"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Terms & Holidays
              </button>
            </div>

            <Button
              size="sm"
              onClick={() => {
                setImportReport(null);
                setImportFile(null);
                setImportModalOpen(true);
              }}
              className="text-xs"
            >
              <Upload className="w-3.5 h-3.5 mr-1" />
              Bulk Import CSV
            </Button>
          </div>
        </div>

        {/* Tab 1: Faculty Directory */}
        {activeTab === "faculty" && (
          <Card>
            <CardHeader className="py-3 px-4 border-b border-slate-100 flex flex-row items-center justify-between">
              <CardTitle className="text-sm font-semibold">Department Roster</CardTitle>
              <Badge variant="outline">{faculty.length} Members</Badge>
            </CardHeader>
            <CardContent className="p-0">
              {loading ? (
                <div className="py-12 text-center text-xs text-slate-400">Loading faculty...</div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left">
                    <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                      <tr>
                        <th className="px-4 py-3">Initials</th>
                        <th className="px-4 py-3">Full Name</th>
                        <th className="px-4 py-3">Institutional Email</th>
                        <th className="px-4 py-3">Aliases</th>
                        <th className="px-4 py-3">Role</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {faculty.map((f) => (
                        <tr key={f.id} className="hover:bg-slate-50/50">
                          <td className="px-4 py-3">
                            <Badge variant="blue" className="font-mono">
                              {f.initials}
                            </Badge>
                          </td>
                          <td className="px-4 py-3 font-medium text-slate-900">{f.full_name}</td>
                          <td className="px-4 py-3 text-slate-600 font-mono">{f.email}</td>
                          <td className="px-4 py-3 text-slate-500 font-mono">
                            {f.aliases && f.aliases.length > 0 ? f.aliases.join(", ") : "—"}
                          </td>
                          <td className="px-4 py-3">
                            <Badge variant="default">
                              Faculty Member
                            </Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Tab 2: Terms and Holidays */}
        {activeTab === "terms-holidays" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Academic Terms */}
            <Card>
              <CardHeader className="py-3 px-4 border-b border-slate-100">
                <CardTitle className="text-sm font-semibold flex items-center space-x-2">
                  <Building className="w-4 h-4 text-[#1e3a8a]" />
                  <span>Academic Terms</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4 space-y-3">
                {terms.map((term) => (
                  <div key={term.id} className="p-3 rounded-lg border border-slate-200 bg-white space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold text-slate-900">{term.name}</span>
                      <Badge variant="success">ACTIVE</Badge>
                    </div>
                    <div className="text-[11px] text-slate-500 font-mono">
                      {new Date(term.start_date).toLocaleDateString()} to{" "}
                      {new Date(term.end_date).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Holidays List */}
            <Card>
              <CardHeader className="py-3 px-4 border-b border-slate-100">
                <CardTitle className="text-sm font-semibold flex items-center space-x-2">
                  <Calendar className="w-4 h-4 text-emerald-600" />
                  <span>Gazetted Holidays (Recurrence Skipped)</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4 space-y-2">
                {holidays.map((h) => (
                  <div
                    key={h.id}
                    className="p-2.5 rounded border border-emerald-100 bg-emerald-50/40 flex items-center justify-between text-xs"
                  >
                    <span className="font-medium text-slate-900">{h.label}</span>
                    <Badge variant="outline" className="font-mono text-emerald-800">
                      {h.date}
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Bulk Import Modal */}
        <Dialog
          open={importModalOpen}
          onOpenChange={setImportModalOpen}
          title="Bulk Import Faculty Roster"
          description="Upload a CSV file containing email, full_name, initials, and optional aliases"
          maxWidth="xl"
        >
          <form onSubmit={handleBulkImport} className="space-y-4">
            <div className="p-4 border-2 border-dashed border-slate-300 rounded-lg text-center bg-slate-50">
              <FileSpreadsheet className="w-8 h-8 text-slate-400 mx-auto mb-1.5" />
              <p className="text-xs font-medium text-slate-700">
                {importFile ? importFile.name : "Select CSV faculty roster"}
              </p>
              <input
                type="file"
                accept=".csv"
                required
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    setImportFile(e.target.files[0]);
                  }
                }}
                className="mt-2 text-xs"
              />
            </div>

            {importReport && (
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-2">
                <div className="flex items-center justify-between text-xs font-semibold text-slate-800">
                  <span>Import Report Summary</span>
                  <span>{importReport.total_rows} Total Rows Processed</span>
                </div>
                <div className="flex space-x-2 text-xs">
                  <Badge variant="success">{importReport.created_count} Created</Badge>
                  <Badge variant="blue">{importReport.updated_count} Updated</Badge>
                  <Badge variant="danger">{importReport.rejected_count} Rejected</Badge>
                </div>
                <div className="max-h-36 overflow-y-auto space-y-1 pt-1 divide-y divide-slate-100">
                  {importReport.rows.map((row, idx) => (
                    <div key={idx} className="pt-1 text-[11px] font-mono flex items-center justify-between">
                      <span>Row {row.row_number}: {row.initials || "—"} ({row.email || "—"})</span>
                      <span className={row.status === "CREATED" || row.status === "UPDATED" ? "text-emerald-700 font-semibold" : "text-red-700"}>
                        {row.message}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex justify-end space-x-2 pt-3 border-t border-slate-100">
              <Button type="button" variant="outline" size="sm" onClick={() => setImportModalOpen(false)}>
                Close
              </Button>
              <Button type="submit" size="sm" disabled={!importFile || importing}>
                {importing ? "Importing Roster..." : "Execute Bulk Import"}
              </Button>
            </div>
          </form>
        </Dialog>
      </div>
    </AppShell>
  );
}
