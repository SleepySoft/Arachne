import { useCallback, useMemo, useState } from "react";
import {
  Company,
  CompanyNetworkEdge,
  GraphEdge,
  IndustrialNode,
  Industry,
  PanelType,
} from "@/types";

export interface PanelState {
  panel: PanelType;
  selectedNode: IndustrialNode | null;
  selectedEdge: GraphEdge | null;
  selectedIndustry: Industry | null;
  selectedCompany: Company | null;
  selectedRelation: CompanyNetworkEdge | null;
  contextMenuNode: IndustrialNode | null;
}

const EMPTY_PANEL: PanelState = {
  panel: "none",
  selectedNode: null,
  selectedEdge: null,
  selectedIndustry: null,
  selectedCompany: null,
  selectedRelation: null,
  contextMenuNode: null,
};

export function usePanelStack() {
  const [stack, setStack] = useState<PanelState[]>([]);

  const top = useMemo<PanelState>(
    () => stack[stack.length - 1] ?? EMPTY_PANEL,
    [stack]
  );

  const push = useCallback((patch: Partial<PanelState>) => {
    setStack((prev) => [...prev, { ...EMPTY_PANEL, ...patch }]);
  }, []);

  const replace = useCallback((patch: Partial<PanelState>) => {
    setStack((prev) => {
      if (prev.length === 0) {
        return [{ ...EMPTY_PANEL, ...patch }];
      }
      const next = [...prev];
      next[next.length - 1] = { ...next[next.length - 1], ...patch };
      return next;
    });
  }, []);

  const pop = useCallback(() => {
    setStack((prev) => prev.slice(0, -1));
  }, []);

  const clear = useCallback(() => {
    setStack([]);
  }, []);

  const setSelectedNode = useCallback(
    (node: IndustrialNode | null) => replace({ selectedNode: node }),
    [replace]
  );

  const setSelectedEdge = useCallback(
    (edge: GraphEdge | null) => replace({ selectedEdge: edge }),
    [replace]
  );

  const setSelectedIndustry = useCallback(
    (industry: Industry | null) => replace({ selectedIndustry: industry }),
    [replace]
  );

  const setSelectedCompany = useCallback(
    (company: Company | null) => replace({ selectedCompany: company }),
    [replace]
  );

  const setSelectedRelation = useCallback(
    (relation: CompanyNetworkEdge | null) =>
      replace({ selectedRelation: relation }),
    [replace]
  );

  return {
    stack,
    top,
    panel: top.panel,
    selectedNode: top.selectedNode,
    selectedEdge: top.selectedEdge,
    selectedIndustry: top.selectedIndustry,
    selectedCompany: top.selectedCompany,
    selectedRelation: top.selectedRelation,
    contextMenuNode: top.contextMenuNode,
    canGoBack: stack.length > 1,
    push,
    replace,
    pop,
    clear,
    setSelectedNode,
    setSelectedEdge,
    setSelectedIndustry,
    setSelectedCompany,
    setSelectedRelation,
  };
}
