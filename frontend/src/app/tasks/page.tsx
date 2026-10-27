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
  TaskResponse,
  TaskTemplateResponse,
  HodDashboardResponse,
  FacultyResponse,
} from "@/lib/api-client";
import {
  CheckSquare,
  Plus,
  Filter,
  CheckCircle2,
  Clock,
  RotateCcw,
  Trash2,
  Users,
  BarChart3,
  Calendar,
  AlertCircle,
  FileCheck,
} from "lucide-react";

export default function TasksPage() {
  const router = useRouter();
  const { user, profile, isLoading } = useAuth();
  const { toast } = useToast();

  const [activeTab, setActiveTab] = React.useState<"my-tasks" | "hod-assign" | "hod-dashboard">("my-tasks");
  const [tasks, setTasks] = React.useState<TaskResponse[]>([]);
  const [templates, setTemplates] = React.useState<TaskTemplateResponse[]>([]);
  const [facultyList, setFacultyList] = React.useState<FacultyResponse[]>([]);
  const [hodDashboard, setHodDashboard] = React.useState<HodDashboardResponse | null>(null);
  const [loading, setLoading] = React.useState(true);

  const [selectedCategory, setSelectedCategory] = React.useState<string>("");
  const [selectedStatus, setSelectedStatus] = React.useState<string>("TODO");
  const [overdueOnly, setOverdueOnly] = React.useState<boolean>(false);

  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [newTitle, setNewTitle] = React.useState("");
  const [newDesc, setNewDesc] = React.useState("");
  const [newCategory, setNewCategory] = React.useState<
    "Academic documentation" | "Exam work" | "Accreditation" | "Administrative" | "Personal"
  >("Academic documentation");
  const [newDeadline, setNewDeadline] = React.useState("");
  const [newImportance, setNewImportance] = React.useState<number>(3);
  const [submittingTask, setSubmittingTask] = React.useState(false);

  const [assignTitle, setAssignTitle] = React.useState("");
  const [assignDesc, setAssignDesc] = React.useState("");
  const [assignCategory, setAssignCategory] = React.useState<
    "Academic documentation" | "Exam work" | "Accreditation" | "Administrative" | "Personal"
  >("Academic documentation");
  const [assignDeadline, setAssignDeadline] = React.useState("");
  const [assignImportance, setAssignImportance] = React.useState<number>(3);
  const [assignees, setAssignees] = React.useState<string[]>([]);
  const [submittingAssign, setSubmittingAssign] = React.useState(false);

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [isLoading, user, router]);

  const loadTasksData = React.useCallback(async () => {
    try {
      setLoading(true);
      const [tasksData, templatesData, facultyData, dashboardData] = await Promise.all([
        api.tasks.list({
          category: selectedCategory || undefined,
          status: selectedStatus || undefined,
          overdue_only: overdueOnly ? true : undefined,
        }),
        api.tasks.getTemplates().catch(() => []),
        api.directory.listFaculty().catch(() => []),
        user?.role === "HOD" || user?.role === "ADMIN" ? api.tasks.getHodDashboard().catch(() => null) : Promise.resolve(null),
      ]);

      setTasks(tasksData.sort((a, b) => b.priority_score - a.priority_score));
      setTemplates(templatesData);
      setFacultyList(facultyData);
      setHodDashboard(dashboardData);
    } catch (err) {
      console.error("Failed to load tasks data:", err);
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, selectedStatus, overdueOnly, user]);

  React.useEffect(() => {
    if (user) {
      loadTasksData();
    }
  }, [user, loadTasksData]);

  const handleCreatePersonalTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittingTask(true);
    try {
      await api.tasks.create({
        title: newTitle,
        description: newDesc,
        category: newCategory,
        deadline: new Date(newDeadline).toISOString(),
        importance: newImportance,
      });

      toast("Task created and scheduled on calendar", "success");
      setCreateModalOpen(false);
      setNewTitle("");
      setNewDesc("");
      loadTasksData();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to create task", "error");
    } finally {
      setSubmittingTask(false);
    }
  };

  const handleApplyTemplate = (tpl: TaskTemplateResponse) => {
    setAssignTitle(tpl.title);
    setAssignDesc(tpl.description);
    setAssignCategory(tpl.category as "Academic documentation" | "Exam work" | "Accreditation" | "Administrative" | "Personal");
    setAssignImportance(tpl.default_importance);

    const d = new Date();
    d.setDate(d.getDate() + tpl.default_lead_days);
    d.setHours(17, 0, 0, 0);
    const dStr = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    setAssignDeadline(dStr);
  };

  const handleAssignBulkTasks = async (e: React.FormEvent) => {
    e.preventDefault();
    if (assignees.length === 0) {
      toast("Please select at least one faculty member to assign", "error");
      return;
    }
    setSubmittingAssign(true);
    try {
      const res = await api.tasks.assign({
        title: assignTitle,
        description: assignDesc,
        category: assignCategory,
        deadline: new Date(assignDeadline).toISOString(),
        importance: assignImportance,
        assignee_ids: assignees,
      });

      toast(`Assigned task cohort to ${res.length} faculty members!`, "success");
      setAssignTitle("");
      setAssignDesc("");
      setAssignees([]);
      setActiveTab("hod-dashboard");
      loadTasksData();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Assignment failed", "error");
    } finally {
      setSubmittingAssign(false);
    }
  };

  const handleToggleComplete = async (task: TaskResponse) => {
    try {
      if (task.status === "DONE") {
        await api.tasks.reopen(task.id);
        toast("Task reopened", "info");
      } else {
        await api.tasks.complete(task.id);
        toast("Task completed", "success");
      }
      loadTasksData();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to update task", "error");
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    try {
      await api.tasks.delete(taskId);
      toast("Task deleted", "info");
      loadTasksData();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to delete task", "error");
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Top Header and Tab Controls */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-lg border border-slate-200">
          <div>
            <h1 className="text-xl font-bold text-slate-900">Documentation & Tasks</h1>
            <p className="text-xs text-slate-500">
              CO-PO mapping, IA marks upload, lab manuals with continuous priority scoring
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <div className="inline-flex rounded-md border border-slate-200 p-0.5 bg-slate-50 text-xs">
              <button
                onClick={() => setActiveTab("my-tasks")}
                className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                  activeTab === "my-tasks"
                    ? "bg-white shadow-xs text-slate-900 font-semibold"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Tasks List
              </button>
              {(user?.role === "HOD" || user?.role === "ADMIN") && (
                <>
                  <button
                    onClick={() => setActiveTab("hod-assign")}
                    className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                      activeTab === "hod-assign"
                        ? "bg-white shadow-xs text-slate-900 font-semibold"
                        : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    HOD Assignment
                  </button>
                  <button
                    onClick={() => setActiveTab("hod-dashboard")}
                    className={`px-3 py-1.5 rounded font-medium cursor-pointer ${
                      activeTab === "hod-dashboard"
                        ? "bg-white shadow-xs text-slate-900 font-semibold"
                        : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    Department Progress
                  </button>
                </>
              )}
            </div>

            <Button
              size="sm"
              onClick={() => {
                const now = new Date();
                now.setDate(now.getDate() + 3);
                now.setHours(17, 0, 0, 0);
                const defaultDl = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
                  .toISOString()
                  .slice(0, 16);
                setNewDeadline(defaultDl);
                setCreateModalOpen(true);
              }}
              className="text-xs"
            >
              <Plus className="w-3.5 h-3.5 mr-1" />
              New Task
            </Button>
          </div>
        </div>

        {/* Tab 1: Task List */}
        {activeTab === "my-tasks" && (
          <div className="space-y-4">
            {/* Filter Bar */}
            <div className="flex flex-wrap items-center gap-3 p-3 bg-white rounded-lg border border-slate-200 text-xs">
              <div className="flex items-center space-x-1.5 text-slate-500 font-semibold">
                <Filter className="w-3.5 h-3.5" />
                <span>Filters:</span>
              </div>

              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-2 py-1 border border-slate-300 rounded text-xs text-slate-800 bg-white"
              >
                <option value="">All Statuses</option>
                <option value="TODO">To Do</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="DONE">Completed</option>
              </select>

              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-2 py-1 border border-slate-300 rounded text-xs text-slate-800 bg-white"
              >
                <option value="">All Categories</option>
                <option value="Academic documentation">Academic documentation</option>
                <option value="Exam work">Exam work</option>
                <option value="Accreditation">Accreditation</option>
                <option value="Administrative">Administrative</option>
                <option value="Personal">Personal</option>
              </select>

              <label className="flex items-center space-x-1.5 cursor-pointer ml-auto">
                <input
                  type="checkbox"
                  checked={overdueOnly}
                  onChange={(e) => setOverdueOnly(e.target.checked)}
                  className="rounded border-slate-300 text-[#1e3a8a] focus:ring-[#1e3a8a]"
                />
                <span className="font-semibold text-red-700">Overdue Only (P &gt; 1.0)</span>
              </label>
            </div>

            {/* Tasks Cards */}
            <Card>
              <CardHeader className="py-3 px-4 border-b border-slate-100 flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-semibold">Ranked Documentation Tasks</CardTitle>
                <Badge variant="outline">{tasks.length} tasks</Badge>
              </CardHeader>
              <CardContent className="p-4">
                {loading ? (
                  <div className="py-12 text-center text-xs text-slate-400">Loading tasks...</div>
                ) : tasks.length === 0 ? (
                  <div className="py-12 text-center space-y-2">
                    <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
                    <p className="text-xs text-slate-500">No tasks matching selected filter criteria.</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {tasks.map((task) => {
                      const isOverdue = task.priority_score > 1.0;
                      const isDone = task.status === "DONE";

                      return (
                        <div
                          key={task.id}
                          className={`p-3.5 rounded-lg border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                            isDone
                              ? "border-slate-100 bg-slate-50/60 opacity-60"
                              : isOverdue
                              ? "border-red-300 bg-red-50/40 hover:border-red-400"
                              : "border-slate-200 bg-white hover:border-slate-300"
                          }`}
                        >
                          <div className="flex items-start space-x-3">
                            <button
                              onClick={() => handleToggleComplete(task)}
                              className={`w-5 h-5 rounded border mt-0.5 flex items-center justify-center transition-colors cursor-pointer ${
                                isDone
                                  ? "bg-emerald-600 border-emerald-600 text-white"
                                  : "border-slate-300 hover:border-emerald-500 bg-white"
                              }`}
                              title={isDone ? "Reopen task" : "Mark done"}
                              aria-label={isDone ? "Reopen task" : "Mark done"}
                            >
                              {isDone && <CheckCircle2 className="w-3.5 h-3.5" />}
                            </button>

                            <div>
                              <div className="flex items-center space-x-2">
                                <h4
                                  className={`text-sm font-semibold ${
                                    isDone ? "line-through text-slate-500" : "text-slate-900"
                                  }`}
                                >
                                  {task.title}
                                </h4>
                                <Badge
                                  variant={
                                    isDone ? "default" : isOverdue ? "danger" : "blue"
                                  }
                                >
                                  P: {task.priority_score.toFixed(2)}
                                </Badge>
                                <Badge variant="outline">{task.category}</Badge>
                                {task.parent_assignment_id && (
                                  <Badge variant="purple" className="text-[10px]">
                                    HOD ASSIGNED
                                  </Badge>
                                )}
                              </div>

                              {task.description && (
                                <p className="text-xs text-slate-600 mt-1 line-clamp-1">
                                  {task.description}
                                </p>
                              )}

                              <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-500 font-mono mt-1">
                                <span className="flex items-center space-x-1">
                                  <Clock className="w-3.5 h-3.5" />
                                  <span>
                                    Due{" "}
                                    {new Intl.DateTimeFormat("en-IN", {
                                      weekday: "short",
                                      day: "numeric",
                                      month: "short",
                                      hour: "2-digit",
                                      minute: "2-digit",
                                      timeZone: "Asia/Kolkata",
                                    }).format(new Date(task.deadline_utc))}
                                  </span>
                                </span>
                                <span>•</span>
                                <span>Importance: {task.importance} / 5</span>
                                {task.recurrence && <span>• {task.recurrence}</span>}
                              </div>
                            </div>
                          </div>

                          <div className="flex items-center space-x-2 self-end sm:self-center">
                            {isDone ? (
                              <button
                                onClick={() => handleToggleComplete(task)}
                                className="text-xs text-slate-500 hover:text-slate-800 flex items-center space-x-1 cursor-pointer"
                              >
                                <RotateCcw className="w-3.5 h-3.5" />
                                <span>Reopen</span>
                              </button>
                            ) : null}
                            <button
                              onClick={() => handleDeleteTask(task.id)}
                              className="p-1 rounded text-slate-400 hover:text-red-600 transition-colors cursor-pointer"
                              title="Delete task"
                              aria-label="Delete task"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Tab 2: HOD Bulk Assignment */}
        {activeTab === "hod-assign" && (
          <div className="space-y-6">
            {/* Template Selector Cards */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Standard Academic Documentation Templates</CardTitle>
                <CardDescription>
                  Pre-filled templates for CO-PO mapping, IA marks upload, and accreditation compliance
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {templates.map((tpl) => (
                    <div
                      key={tpl.id}
                      onClick={() => handleApplyTemplate(tpl)}
                      className="p-3.5 rounded-lg border border-slate-200 hover:border-[#1e3a8a] bg-white hover:bg-blue-50/20 cursor-pointer transition-all space-y-1.5"
                    >
                      <div className="flex items-center justify-between">
                        <Badge variant="blue">{tpl.category}</Badge>
                        <span className="text-[11px] font-mono text-slate-400">
                          {tpl.default_lead_days}d lead
                        </span>
                      </div>
                      <h4 className="text-sm font-semibold text-slate-900">{tpl.title}</h4>
                      <p className="text-xs text-slate-500 line-clamp-2">{tpl.description}</p>
                      <div className="text-[11px] text-[#1e3a8a] font-semibold pt-1">
                        Use Template →
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Assignment Form */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Assign Cohort Documentation Task</CardTitle>
                <CardDescription>
                  Creates tracked clones for each selected faculty member with escalating alerts
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleAssignBulkTasks} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Task Title
                    </label>
                    <input
                      type="text"
                      required
                      value={assignTitle}
                      onChange={(e) => setAssignTitle(e.target.value)}
                      placeholder="Upload Module 1 IA Marks"
                      className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Description & Instructions
                    </label>
                    <textarea
                      rows={2}
                      value={assignDesc}
                      onChange={(e) => setAssignDesc(e.target.value)}
                      placeholder="Ensure all scheme papers are mapped to CO-1 and uploaded in ERP"
                      className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        Category
                      </label>
                      <select
                        value={assignCategory}
                        onChange={(e) => setAssignCategory(e.target.value as "Academic documentation" | "Exam work" | "Accreditation" | "Administrative" | "Personal")}
                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                      >
                        <option value="Academic documentation">Academic documentation</option>
                        <option value="Exam work">Exam work</option>
                        <option value="Accreditation">Accreditation</option>
                        <option value="Administrative">Administrative</option>
                        <option value="Personal">Personal</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        Common Deadline (IST)
                      </label>
                      <input
                        type="datetime-local"
                        required
                        value={assignDeadline}
                        onChange={(e) => setAssignDeadline(e.target.value)}
                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        Importance (1-5)
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="5"
                        required
                        value={assignImportance}
                        onChange={(e) => setAssignImportance(Number(e.target.value))}
                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider">
                        Select Faculty Assignees ({assignees.length} selected)
                      </label>
                      <button
                        type="button"
                        onClick={() => {
                          if (assignees.length === facultyList.length) {
                            setAssignees([]);
                          } else {
                            setAssignees(facultyList.map((f) => f.id));
                          }
                        }}
                        className="text-xs text-[#1e3a8a] font-semibold hover:underline"
                      >
                        {assignees.length === facultyList.length ? "Deselect All" : "Select All Department"}
                      </button>
                    </div>
                    <div className="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto p-2 border border-slate-200 rounded-md">
                      {facultyList.map((f) => {
                        const selected = assignees.includes(f.id);
                        return (
                          <button
                            key={f.id}
                            type="button"
                            onClick={() => {
                              if (selected) {
                                setAssignees(assignees.filter((id) => id !== f.id));
                              } else {
                                setAssignees([...assignees, f.id]);
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

                  <div className="flex justify-end pt-3">
                    <Button type="submit" disabled={submittingAssign}>
                      {submittingAssign ? "Assigning Cohort..." : "Dispatch Assignment to Faculty"}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Tab 3: HOD Analytics Dashboard */}
        {activeTab === "hod-dashboard" && hodDashboard && (
          <div className="space-y-6">
            {/* Top Stat Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs">
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Total Assigned
                </span>
                <span className="text-2xl font-bold text-slate-900 font-mono mt-1 block">
                  {hodDashboard.total_assigned}
                </span>
              </div>

              <div className="p-4 bg-emerald-50 rounded-lg border border-emerald-200 shadow-xs">
                <span className="block text-xs font-semibold text-emerald-700 uppercase tracking-wider">
                  Completed
                </span>
                <span className="text-2xl font-bold text-emerald-800 font-mono mt-1 block">
                  {hodDashboard.total_completed}
                </span>
              </div>

              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200 shadow-xs">
                <span className="block text-xs font-semibold text-blue-700 uppercase tracking-wider">
                  Completion Rate
                </span>
                <span className="text-2xl font-bold text-blue-800 font-mono mt-1 block">
                  {hodDashboard.overall_completion_rate.toFixed(1)}%
                </span>
              </div>

              <div className="p-4 bg-red-50 rounded-lg border border-red-200 shadow-xs">
                <span className="block text-xs font-semibold text-red-700 uppercase tracking-wider">
                  Overdue Tasks
                </span>
                <span className="text-2xl font-bold text-red-800 font-mono mt-1 block">
                  {hodDashboard.total_overdue}
                </span>
              </div>
            </div>

            {/* Assignment Cohorts Progress Table */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Assigned Task Cohorts Progress</CardTitle>
                <CardDescription>
                  Tracking documentation completion across department-wide assignments
                </CardDescription>
              </CardHeader>
              <CardContent>
                {hodDashboard.assignments.length === 0 ? (
                  <div className="py-8 text-center text-xs text-slate-400">
                    No active bulk cohort assignments. Use the HOD Assignment tab to assign tasks.
                  </div>
                ) : (
                  <div className="border border-slate-200 rounded-lg overflow-x-auto">
                    <table className="w-full text-xs text-left">
                      <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                        <tr>
                          <th className="px-4 py-3">Assignment Cohort</th>
                          <th className="px-4 py-3">Category</th>
                          <th className="px-4 py-3">Assigned</th>
                          <th className="px-4 py-3">Completed</th>
                          <th className="px-4 py-3 w-48">Progress</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100 font-mono">
                        {hodDashboard.assignments.map((a) => (
                          <tr key={a.assignment_id} className="hover:bg-slate-50/50">
                            <td className="px-4 py-3 font-sans font-semibold text-slate-900">
                              {a.title}
                            </td>
                            <td className="px-4 py-3">
                              <Badge variant="blue">{a.category}</Badge>
                            </td>
                            <td className="px-4 py-3 text-slate-700">{a.total_count}</td>
                            <td className="px-4 py-3 text-emerald-700 font-semibold">{a.completed_count}</td>
                            <td className="px-4 py-3">
                              <div className="flex items-center space-x-2">
                                <div className="flex-1 bg-slate-200 h-2 rounded-full overflow-hidden">
                                  <div
                                    className="bg-emerald-600 h-full rounded-full transition-all"
                                    style={{ width: `${Math.min(100, a.completion_rate)}%` }}
                                  />
                                </div>
                                <span className="text-[11px] font-semibold text-slate-600 w-10 text-right">
                                  {a.completion_rate.toFixed(0)}%
                                </span>
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

            {/* Overdue Faculty Alerts Table */}
            {hodDashboard.faculty_overdue.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base text-red-900 flex items-center space-x-2">
                    <AlertCircle className="w-4 h-4 text-red-600" />
                    <span>Faculty with Overdue Documentation</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="border border-red-200 rounded-lg overflow-x-auto bg-red-50/20">
                    <table className="w-full text-xs text-left">
                      <thead className="bg-red-50 text-red-900 border-b border-red-200">
                        <tr>
                          <th className="px-4 py-2.5">Faculty Name</th>
                          <th className="px-4 py-2.5">Institutional Email</th>
                          <th className="px-4 py-2.5">Overdue Count</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-red-100 font-mono">
                        {hodDashboard.faculty_overdue.map((f, i) => (
                          <tr key={i}>
                            <td className="px-4 py-2.5 font-sans font-medium text-slate-900">
                              {f.faculty_name}
                            </td>
                            <td className="px-4 py-2.5 text-slate-600">{f.email}</td>
                            <td className="px-4 py-2.5">
                              <Badge variant="danger">{f.overdue_count} Overdue</Badge>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* New Personal Task Modal */}
        <Dialog
          open={createModalOpen}
          onOpenChange={setCreateModalOpen}
          title="Create Documentation Task"
          description="Track course files, evaluation deadlines, and accreditation submissions"
        >
          <form onSubmit={handleCreatePersonalTask} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Title
              </label>
              <input
                type="text"
                required
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="Finalize Lab Manual for CS301"
                className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Description
              </label>
              <textarea
                rows={2}
                value={newDesc}
                onChange={(e) => setNewDesc(e.target.value)}
                placeholder="Update experiment 7 to include Python socket programming"
                className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Category
                </label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value as "Academic documentation" | "Exam work" | "Accreditation" | "Administrative" | "Personal")}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                >
                  <option value="Academic documentation">Academic documentation</option>
                  <option value="Exam work">Exam work</option>
                  <option value="Accreditation">Accreditation</option>
                  <option value="Administrative">Administrative</option>
                  <option value="Personal">Personal</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Importance (1-5)
                </label>
                <input
                  type="number"
                  min="1"
                  max="5"
                  required
                  value={newImportance}
                  onChange={(e) => setNewImportance(Number(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Deadline (Local IST)
              </label>
              <input
                type="datetime-local"
                required
                value={newDeadline}
                onChange={(e) => setNewDeadline(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#1e3a8a]"
              />
            </div>

            <div className="flex justify-end space-x-2 pt-3 border-t border-slate-100">
              <Button type="button" variant="outline" onClick={() => setCreateModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={submittingTask}>
                {submittingTask ? "Saving..." : "Create Task"}
              </Button>
            </div>
          </form>
        </Dialog>
      </div>
    </AppShell>
  );
}
