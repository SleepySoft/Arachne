import { CompanySidebar } from "@/components/CompanySidebar";
import { SubTab } from "./SubTab";
import { Company } from "@/types";

interface CompanySidebarPanelProps {
  selectedId?: string;
  companySubView: "company_list";
  setCompanySubView: (view: "company_list") => void;
  onSelectCompany: (company: Company) => void;
  onCreateCompany: () => void;
}

export function CompanySidebarPanel({
  selectedId,
  companySubView,
  setCompanySubView,
  onSelectCompany,
  onCreateCompany,
}: CompanySidebarPanelProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex border-b border-slate-700">
        <SubTab
          active={companySubView === "company_list"}
          onClick={() => setCompanySubView("company_list")}
          label="公司列表"
        />
      </div>
      <div className="flex-1 overflow-auto">
        {companySubView === "company_list" && (
          <CompanySidebar
            selectedId={selectedId}
            onSelect={onSelectCompany}
            onCreate={onCreateCompany}
          />
        )}
      </div>
    </div>
  );
}
