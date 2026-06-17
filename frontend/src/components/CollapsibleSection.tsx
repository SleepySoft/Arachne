import { ChevronDown, ChevronUp } from "lucide-react";
import { ReactNode, useState } from "react";

interface CollapsibleSectionProps {
  title: string;
  badge?: number;
  children: ReactNode;
  defaultOpen?: boolean;
}

export function CollapsibleSection({
  title,
  badge,
  children,
  defaultOpen = true,
}: CollapsibleSectionProps) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="border-b border-slate-800 last:border-b-0">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400 hover:bg-slate-800"
      >
        <span className="flex items-center gap-1.5">
          {title}
          {badge ? (
            <span className="rounded-full bg-cyan-900/40 px-1.5 py-0 text-[9px] text-cyan-400">
              {badge}
            </span>
          ) : null}
        </span>
        {open ? (
          <ChevronUp className="h-3 w-3" />
        ) : (
          <ChevronDown className="h-3 w-3" />
        )}
      </button>
      {open && <div className="pb-2">{children}</div>}
    </div>
  );
}
