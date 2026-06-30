import { useCallback, useRef, useState } from "react";
import { IndustrialViewState, CompanyViewState, WorkspaceType } from "@/types/view";

const MAX_HISTORY_SIZE = 20;

type HistoryState = IndustrialViewState | CompanyViewState;

export interface ViewHistory {
  push(workspace: "industrial", state: IndustrialViewState): void;
  push(workspace: "company", state: CompanyViewState): void;
  undo(workspace: "industrial"): IndustrialViewState | undefined;
  undo(workspace: "company"): CompanyViewState | undefined;
  reset(workspace: WorkspaceType): void;
  canUndo(workspace: WorkspaceType): boolean;
}

export function useViewStateHistory(): ViewHistory {
  const industrialStackRef = useRef<IndustrialViewState[]>([]);
  const companyStackRef = useRef<CompanyViewState[]>([]);
  const [lengths, setLengths] = useState({ industrial: 0, company: 0 });

  const syncLengths = useCallback(() => {
    setLengths({
      industrial: industrialStackRef.current.length,
      company: companyStackRef.current.length,
    });
  }, []);

  const push = useCallback((workspace: WorkspaceType, state: HistoryState) => {
    if (workspace === "industrial") {
      industrialStackRef.current = [...industrialStackRef.current, state as IndustrialViewState];
      if (industrialStackRef.current.length > MAX_HISTORY_SIZE) {
        industrialStackRef.current.shift();
      }
    } else {
      companyStackRef.current = [...companyStackRef.current, state as CompanyViewState];
      if (companyStackRef.current.length > MAX_HISTORY_SIZE) {
        companyStackRef.current.shift();
      }
    }
    syncLengths();
  }, [syncLengths]);

  const undo = useCallback((workspace: WorkspaceType): HistoryState | undefined => {
    if (workspace === "industrial") {
      const stack = industrialStackRef.current;
      if (stack.length === 0) return undefined;
      const last = stack[stack.length - 1];
      industrialStackRef.current = stack.slice(0, -1);
      syncLengths();
      return last;
    } else {
      const stack = companyStackRef.current;
      if (stack.length === 0) return undefined;
      const last = stack[stack.length - 1];
      companyStackRef.current = stack.slice(0, -1);
      syncLengths();
      return last;
    }
  }, [syncLengths]);

  const reset = useCallback((workspace: WorkspaceType) => {
    if (workspace === "industrial") {
      industrialStackRef.current = [];
    } else {
      companyStackRef.current = [];
    }
    syncLengths();
  }, [syncLengths]);

  const canUndo = useCallback((workspace: WorkspaceType) => {
    return lengths[workspace] > 0;
  }, [lengths]);

  return {
    push: push as ViewHistory["push"],
    undo: undo as ViewHistory["undo"],
    reset,
    canUndo,
  };
}
