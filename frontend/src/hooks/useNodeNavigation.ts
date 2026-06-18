import { useCallback, useEffect, useState } from "react";
import { IndustrialNode } from "@/types";

const STORAGE_KEY = "arachne-node-navigation-enabled";

interface NavigationState {
  history: IndustrialNode[];
  index: number;
}

export function useNodeNavigation() {
  const [enabled, setEnabled] = useState<boolean>(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw === null ? true : JSON.parse(raw);
    } catch {
      return true;
    }
  });

  const [state, setState] = useState<NavigationState>({ history: [], index: -1 });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(enabled));
    } catch {
      // ignore
    }
  }, [enabled]);

  const push = useCallback(
    (node: IndustrialNode) => {
      if (!enabled) return;
      setState((prev) => {
        const nextHistory = prev.history.slice(0, prev.index + 1);
        if (nextHistory.length > 0 && nextHistory[nextHistory.length - 1].node_id === node.node_id) {
          return prev;
        }
        const newHistory = [...nextHistory, node];
        return { history: newHistory, index: newHistory.length - 1 };
      });
    },
    [enabled]
  );

  const back = useCallback((): IndustrialNode | null => {
    let result: IndustrialNode | null = null;
    setState((prev) => {
      if (prev.index <= 0) return prev;
      const newIndex = prev.index - 1;
      result = prev.history[newIndex];
      return { ...prev, index: newIndex };
    });
    return result;
  }, []);

  const forward = useCallback((): IndustrialNode | null => {
    let result: IndustrialNode | null = null;
    setState((prev) => {
      if (prev.index < 0 || prev.index >= prev.history.length - 1) return prev;
      const newIndex = prev.index + 1;
      result = prev.history[newIndex];
      return { ...prev, index: newIndex };
    });
    return result;
  }, []);

  const goto = useCallback((targetIndex: number): IndustrialNode | null => {
    let result: IndustrialNode | null = null;
    setState((prev) => {
      if (targetIndex < 0 || targetIndex >= prev.history.length) return prev;
      result = prev.history[targetIndex];
      return { ...prev, index: targetIndex };
    });
    return result;
  }, []);

  const clear = useCallback(() => {
    setState({ history: [], index: -1 });
  }, []);

  const toggleEnabled = useCallback(() => {
    setEnabled((v) => !v);
  }, []);

  return {
    enabled,
    setEnabled,
    toggleEnabled,
    history: state.history,
    index: state.index,
    currentNode: state.index >= 0 ? state.history[state.index] : null,
    canGoBack: state.index > 0,
    canGoForward: state.index >= 0 && state.index < state.history.length - 1,
    push,
    back,
    forward,
    goto,
    clear,
  };
}
