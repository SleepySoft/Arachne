import type { ReactNode } from "react";

interface GraphToolbarProps {
  // 重排/连线功能暂不启用：
  // - 重排会强制全局重新布局，破坏用户已调整好的节点位置与视角
  // - 连线模式在复杂图上容易误触，后续再考虑更稳妥的入口
  // onRelayout?: () => void;
  // editMode?: "default" | "connect";
  // onToggleEditMode?: () => void;
  variant?: "boxed" | "inline";
}

export function GraphToolbar({
  // onRelayout,
  // editMode = "default",
  // onToggleEditMode,
  variant = "boxed",
}: GraphToolbarProps) {
  // 当前所有工具按钮均已注释掉，保留组件作为未来扩展的插槽。
  // 如需恢复，取消下面 JSX 中的注释，并恢复对应 props / imports。
  const buttons: ReactNode[] = [];
  /*
  if (onRelayout) {
    buttons.push(
      <button key="relayout" onClick={onRelayout} title="重新布局" ...>
        <RefreshCw className="h-3.5 w-3.5" />
        <span>重排</span>
      </button>
    );
  }
  if (onToggleEditMode) {
    buttons.push(...);
  }
  */

  if (buttons.length === 0) return null;

  if (variant === "inline") {
    return <>{buttons}</>;
  }

  return (
    <div className="absolute left-3 top-3 z-10 flex items-center gap-2 rounded-lg border border-slate-700 bg-slate-900/90 p-1.5 shadow-lg backdrop-blur">
      {buttons}
    </div>
  );
}
