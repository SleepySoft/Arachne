import type { ReactNode } from "react";

export function cn(...classes: (string | false | undefined)[]) {
  return classes.filter(Boolean).join(" ");
}

export function FormField({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="space-y-1">
      <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">{label}</label>
      {children}
    </div>
  );
}

export function Card({
  title,
  icon,
  children,
  className,
}: {
  title?: string;
  icon?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("rounded-lg border border-slate-800 bg-slate-900/60", className)}>
      {title && (
        <div className="flex items-center gap-2 border-b border-slate-800 px-4 py-3">
          {icon && <span className="text-slate-400">{icon}</span>}
          <h3 className="text-sm font-medium text-slate-200">{title}</h3>
        </div>
      )}
      <div className="p-4">{children}</div>
    </div>
  );
}

export function Badge({
  children,
  color = "slate",
}: {
  children: ReactNode;
  color?: "slate" | "cyan" | "amber" | "emerald" | "red";
}) {
  const map = {
    slate: "bg-slate-800 text-slate-300",
    cyan: "bg-cyan-900/40 text-cyan-300",
    amber: "bg-amber-900/40 text-amber-300",
    emerald: "bg-emerald-900/40 text-emerald-300",
    red: "bg-red-900/40 text-red-300",
  };
  return (
    <span className={cn("rounded px-1.5 py-0.5 text-[10px] font-medium", map[color])}>
      {children}
    </span>
  );
}
