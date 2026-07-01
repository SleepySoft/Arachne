import { useCallback, useRef, useState } from "react";
import { IndustrialViewState, CompanyViewState, WorkspaceType } from "@/types/view";

const MAX_HISTORY_SIZE = 20;

interface HistoryEntry<T> {
  state: T;
  layoutOnly: boolean;
}

type IndustrialHistoryEntry = HistoryEntry<IndustrialViewState>;
type CompanyHistoryEntry = HistoryEntry<CompanyViewState>;

export interface ViewHistory {
  push(workspace: "industrial", state: IndustrialViewState, layoutOnly?: boolean): void;
  push(workspace: "company", state: CompanyViewState, layoutOnly?: boolean): void;
  undo(workspace: "industrial"): { state: IndustrialViewState; layoutOnly: boolean } | undefined;
  undo(workspace: "company"): { state: CompanyViewState; layoutOnly: boolean } | undefined;
  reset(workspace: WorkspaceType): void;
  canUndo(workspace: WorkspaceType): boolean;
}

export function useViewStateHistory(): ViewHistory {
  const industrialStackRef = useRef<IndustrialHistoryEntry[]>([]);
  const companyStackRef = useRef<CompanyHistoryEntry[]>([]);
  const [lengths, setLengths] = useState({ industrial: 0, company: 0 });

  const syncLengths = useCallback(() => {
    setLengths({
      industrial: industrialStackRef.current.length,
      company: companyStackRef.current.length,
    });
  }, []);

  const push = useCallback(
    (workspace: WorkspaceType, state: IndustrialViewState | CompanyViewState, layoutOnly = false) => {
      if (workspace === "industrial") {
        industrialStackRef.current = [
          ...industrialStackRef.current,
          { state: state as IndustrialViewState, layoutOnly },
        ];
        if (industrialStackRef.current.length > MAX_HISTORY_SIZE) {
          industrialStackRef.current.shift();
        }
      } else {
        companyStackRef.current = [
          ...companyStackRef.current,
          { state: state as CompanyViewState, layoutOnly },
        ];
        if (companyStackRef.current.length > MAX_HISTORY_SIZE) {
          companyStackRef.current.shift();
        }
      }
      syncLengths();
    },
    [syncLengths]
  );

  const undo = useCallback(
    (workspace: WorkspaceType):
      | { state: IndustrialViewState | CompanyViewState; layoutOnly: boolean }
      | undefined => {
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
    },
    [syncLengths]
  );

  const reset = useCallback((workspace: WorkspaceType) => {
    if (workspace === "industrial") {
      industrialStackRef.current = [];
    } else {
      companyStackRef.current = [];
    }
    syncLengths();
  }, [syncLengths]);

  const canUndo = useCallback(
    (workspace: WorkspaceType) => {
      return lengths[workspace] > 0;
    },
    [lengths]
  );

  return {
    push: push as ViewHistory["push"],
    undo: undo as ViewHistory["undo"],
    reset,
    canUndo,
  };
}
