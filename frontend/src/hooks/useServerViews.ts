import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createServerView,
  deleteServerView,
  listServerViews,
  setDefaultServerView,
  updateServerView,
} from "@/services/api";
import type { SavedView, WorkspaceType } from "@/types/view";

export function useServerViews(workspace: WorkspaceType) {
  const queryClient = useQueryClient();
  const queryKey = ["server-views", workspace] as const;
  const query = useQuery({
    queryKey,
    queryFn: () => listServerViews(workspace),
    retry: false,
  });

  const refresh = () => {
    queryClient.invalidateQueries({ queryKey });
    queryClient.invalidateQueries({ queryKey: ["server-view-default", workspace] });
  };

  const createMutation = useMutation({
    mutationFn: (view: SavedView) =>
      createServerView({ name: view.name, workspace, view }),
    onSuccess: refresh,
  });
  const updateMutation = useMutation({
    mutationFn: ({ viewId, name }: { viewId: string; name: string }) =>
      updateServerView(viewId, { name }),
    onSuccess: refresh,
  });
  const deleteMutation = useMutation({
    mutationFn: deleteServerView,
    onSuccess: refresh,
  });
  const defaultMutation = useMutation({
    mutationFn: setDefaultServerView,
    onSuccess: refresh,
  });

  return {
    ...query,
    createView: createMutation.mutateAsync,
    renameView: (viewId: string, name: string) =>
      updateMutation.mutateAsync({ viewId, name }),
    deleteView: deleteMutation.mutateAsync,
    setDefaultView: defaultMutation.mutateAsync,
    isMutating:
      createMutation.isPending ||
      updateMutation.isPending ||
      deleteMutation.isPending ||
      defaultMutation.isPending,
  };
}
