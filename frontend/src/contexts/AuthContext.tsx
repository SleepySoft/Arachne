import { createContext, useContext, type ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";
import { getAuthScope } from "@/services/api";

interface AuthContextValue {
  scope: string;
  isReadOnly: boolean;
}

const AuthContext = createContext<AuthContextValue>({
  scope: "read_write",
  isReadOnly: false,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data } = useQuery({
    queryKey: ["auth-scope"],
    queryFn: getAuthScope,
    staleTime: 30_000,
    refetchInterval: 60_000,
    retry: false,
  });
  const scope = data?.scope ?? "read_write";
  const isReadOnly = scope === "read_only";
  return (
    <AuthContext.Provider value={{ scope, isReadOnly }}>
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  return useContext(AuthContext);
}
