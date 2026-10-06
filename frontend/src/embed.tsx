import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { EmbedReasoningPage } from "@/pages/EmbedReasoningPage";
import { EmbedCompanyExposurePage } from "@/pages/EmbedCompanyExposurePage";
import { AuthProvider } from "@/contexts/AuthContext";
import "@/styles/index.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const companyId = new URLSearchParams(window.location.search).get("company")?.trim();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        {companyId ? (
          <EmbedCompanyExposurePage companyId={companyId} />
        ) : (
          <EmbedReasoningPage />
        )}
      </AuthProvider>
    </QueryClientProvider>
  </React.StrictMode>,
);
