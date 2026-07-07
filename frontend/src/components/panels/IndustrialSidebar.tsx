import { CollapsibleSection } from "@/components/CollapsibleSection";
import { CompanyMultiSelector } from "@/components/CompanyMultiSelector";
import { FilterPanel } from "@/components/FilterPanel";
import { IndustryMultiSelector } from "@/components/IndustryMultiSelector";
import { Company, Industry } from "@/types";
import { IndustrialFiltersState } from "@/types/view";

interface IndustrialSidebarProps {
  selectedIndustries: Industry[];
  selectedCompanies: Company[];
  activeFilters: IndustrialFiltersState;
  onToggleIndustry: (industry: Industry) => void;
  onSelectIndustry: (industry: Industry) => void;
  onToggleCompany: (company: Company) => void;
  onSelectCompany: (company: Company) => void;
  onCreateIndustry: () => void;
  onCreateCompany: () => void;
  onChangeFilters: (filters: IndustrialFiltersState) => void;
}

export function IndustrialSidebar({
  selectedIndustries,
  selectedCompanies,
  activeFilters,
  onToggleIndustry,
  onSelectIndustry,
  onToggleCompany,
  onSelectCompany,
  onCreateIndustry,
  onCreateCompany,
  onChangeFilters,
}: IndustrialSidebarProps) {
  return (
    <div className="flex h-full flex-col overflow-hidden">
      {/* Active selection chips */}
      {(selectedIndustries.length > 0 || selectedCompanies.length > 0) && (
        <div className="border-b border-slate-800 p-2">
          <div className="mb-1.5 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            当前选择
          </div>
          <div className="flex flex-wrap gap-1">
            {selectedIndustries.map((ind) => (
              <span
                key={ind.industry_id}
                className="flex items-center gap-1 rounded bg-cyan-900/30 px-1.5 py-0.5 text-[10px] text-cyan-300"
              >
                {ind.name_zh}
                <button
                  onClick={() => onToggleIndustry(ind)}
                  className="text-cyan-500 hover:text-cyan-200"
                  title="移除"
                >
                  ×
                </button>
              </span>
            ))}
            {selectedCompanies.map((co) => (
              <span
                key={co.company_id}
                className="flex items-center gap-1 rounded bg-amber-900/30 px-1.5 py-0.5 text-[10px] text-amber-300"
              >
                {co.name_zh}
                <button
                  onClick={() => onToggleCompany(co)}
                  className="text-amber-500 hover:text-amber-200"
                  title="移除"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
        <CollapsibleSection title="行业" badge={selectedIndustries.length}>
          <IndustryMultiSelector
            selectedIds={selectedIndustries.map((i) => i.industry_id)}
            onToggle={onToggleIndustry}
            onSelect={onSelectIndustry}
            onCreate={onCreateIndustry}
          />
        </CollapsibleSection>

        <CollapsibleSection title="公司" badge={selectedCompanies.length}>
          <CompanyMultiSelector
            selectedIds={selectedCompanies.map((c) => c.company_id)}
            onToggle={onToggleCompany}
            onSelect={onSelectCompany}
            onCreate={onCreateCompany}
          />
        </CollapsibleSection>

        <CollapsibleSection title="过滤">
          <FilterPanel filters={activeFilters} onChange={onChangeFilters} />
        </CollapsibleSection>
      </div>
    </div>
  );
}
