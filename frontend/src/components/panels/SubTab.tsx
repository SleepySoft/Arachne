interface SubTabProps {
  active: boolean;
  onClick: () => void;
  label: string;
}

export function SubTab({ active, onClick, label }: SubTabProps) {
  return (
    <button
      onClick={onClick}
      className={`flex-1 px-2 py-2 text-[11px] font-medium transition-colors ${
        active
          ? "border-b-2 border-cyan-500 text-cyan-400"
          : "text-slate-500 hover:text-slate-300"
      }`}
    >
      {label}
    </button>
  );
}
