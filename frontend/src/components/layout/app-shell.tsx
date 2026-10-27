"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import {
  Calendar,
  CheckSquare,
  FileText,
  Home,
  Settings,
  UploadCloud,
  Users,
  LogOut,
  GraduationCap,
  Menu,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  roles?: Array<"ADMIN" | "HOD" | "FACULTY">;
}

const NAV_ITEMS: NavItem[] = [
  { name: "Today", href: "/today", icon: Home },
  { name: "Calendar", href: "/calendar", icon: Calendar },
  { name: "Tasks", href: "/tasks", icon: CheckSquare },
  { name: "Circulars", href: "/circulars", icon: FileText },
  { name: "Timetable", href: "/timetables", icon: UploadCloud, roles: ["ADMIN", "HOD"] },
  { name: "Directory", href: "/directory", icon: Users, roles: ["ADMIN", "HOD"] },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user, profile, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const role = user?.role || "FACULTY";

  const allowedNav = NAV_ITEMS.filter(
    (item) => !item.roles || item.roles.includes(role as "ADMIN" | "HOD" | "FACULTY")
  );

  const formattedDate = new Intl.DateTimeFormat("en-IN", {
    weekday: "short",
    day: "numeric",
    month: "short",
  }).format(new Date());

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col pb-16 md:pb-0">
      {/* Top Header */}
      <header className="sticky top-0 z-40 bg-white border-b border-slate-200 px-4 sm:px-6 h-14 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Link href="/today" className="flex items-center space-x-2 text-[#1e3a8a] font-bold text-base tracking-tight">
            <div className="w-8 h-8 rounded-md bg-[#1e3a8a] text-white flex items-center justify-center">
              <GraduationCap className="w-5 h-5" />
            </div>
            <span>FacultyDesk</span>
          </Link>
          <span className="hidden sm:inline-block text-slate-300">|</span>
          <span className="hidden sm:inline-block text-xs font-medium text-slate-500 tabular-nums">
            {formattedDate}
          </span>
        </div>

        <div className="flex items-center space-x-2 sm:space-x-3">
          {profile && (
            <Badge variant="blue" className="hidden sm:inline-flex font-mono">
              {profile.initials}
            </Badge>
          )}
          <Badge
            variant={role === "ADMIN" ? "danger" : role === "HOD" ? "purple" : "default"}
            className="text-[10px] uppercase font-semibold"
          >
            {role}
          </Badge>
          <button
            onClick={() => logout()}
            className="p-1.5 rounded text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors cursor-pointer"
            title="Log out"
            aria-label="Log out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </header>

      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        {/* Desktop Sidebar */}
        <aside className="hidden md:flex flex-col w-56 bg-white border-r border-slate-200 p-3 space-y-1 shrink-0">
          <div className="px-3 py-2 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Workspace
          </div>
          {allowedNav.map((item) => {
            const active = pathname === item.href || (item.href === "/today" && pathname === "/");
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                  active
                    ? "bg-blue-50 text-[#1e3a8a] font-semibold"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                )}
              >
                <Icon className={cn("w-4 h-4", active ? "text-[#1e3a8a]" : "text-slate-400")} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-5xl w-full mx-auto overflow-y-auto">
          {children}
        </main>
      </div>

      {/* Mobile Bottom Navigation Bar (Phone < 768px) */}
      <nav
        aria-label="Mobile Navigation"
        className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-slate-200 h-14 flex items-center justify-around px-1"
      >
        <Link
          href="/today"
          className={cn(
            "flex flex-col items-center justify-center w-14 py-1 text-[10px] font-medium transition-colors",
            pathname === "/today" || pathname === "/" ? "text-[#1e3a8a] font-bold" : "text-slate-500 hover:text-slate-800"
          )}
        >
          <Home className="w-4 h-4 mb-0.5" />
          <span>Today</span>
        </Link>
        <Link
          href="/calendar"
          className={cn(
            "flex flex-col items-center justify-center w-14 py-1 text-[10px] font-medium transition-colors",
            pathname === "/calendar" ? "text-[#1e3a8a] font-bold" : "text-slate-500 hover:text-slate-800"
          )}
        >
          <Calendar className="w-4 h-4 mb-0.5" />
          <span>Calendar</span>
        </Link>
        <Link
          href="/tasks"
          className={cn(
            "flex flex-col items-center justify-center w-14 py-1 text-[10px] font-medium transition-colors",
            pathname === "/tasks" ? "text-[#1e3a8a] font-bold" : "text-slate-500 hover:text-slate-800"
          )}
        >
          <CheckSquare className="w-4 h-4 mb-0.5" />
          <span>Tasks</span>
        </Link>
        <Link
          href="/circulars"
          className={cn(
            "flex flex-col items-center justify-center w-14 py-1 text-[10px] font-medium transition-colors",
            pathname === "/circulars" ? "text-[#1e3a8a] font-bold" : "text-slate-500 hover:text-slate-800"
          )}
        >
          <FileText className="w-4 h-4 mb-0.5" />
          <span>Circulars</span>
        </Link>
        <button
          onClick={() => setMobileMenuOpen(true)}
          className={cn(
            "flex flex-col items-center justify-center w-14 py-1 text-[10px] font-medium text-slate-500 hover:text-slate-800 cursor-pointer",
            pathname === "/settings" || pathname === "/timetables" || pathname === "/directory"
              ? "text-[#1e3a8a] font-bold"
              : ""
          )}
          aria-label="More options"
        >
          <Menu className="w-4 h-4 mb-0.5" />
          <span>More</span>
        </button>
      </nav>

      {/* Mobile Drawer for More Items */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex flex-col justify-end bg-slate-900/50 backdrop-blur-xs">
          <div
            className="flex-1"
            onClick={() => setMobileMenuOpen(false)}
            aria-hidden="true"
          />
          <div className="bg-white rounded-t-xl border-t border-slate-200 p-4 space-y-2 animate-in slide-in-from-bottom-5 duration-150">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Additional Navigation
              </span>
              <button
                onClick={() => setMobileMenuOpen(false)}
                className="p-1 rounded text-slate-400 hover:text-slate-600"
                aria-label="Close menu"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            {allowedNav
              .filter((item) => !["/today", "/calendar", "/tasks", "/circulars"].includes(item.href))
              .map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center space-x-3 px-3 py-2.5 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-100"
                  >
                    <Icon className="w-4 h-4 text-slate-400" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            <div className="pt-2 border-t border-slate-100">
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  logout();
                }}
                className="w-full flex items-center space-x-3 px-3 py-2.5 rounded-md text-sm font-medium text-red-600 hover:bg-red-50"
              >
                <LogOut className="w-4 h-4" />
                <span>Log Out</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
