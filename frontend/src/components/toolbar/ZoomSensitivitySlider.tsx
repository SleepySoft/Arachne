interface ZoomSensitivitySliderProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
}

export function ZoomSensitivitySlider({
  value,
  onChange,
  min = 0.01,
  max = 0.3,
  step = 0.01,
}: ZoomSensitivitySliderProps) {
  return (
    <div className="flex items-center gap-2 px-2">
      <span className="whitespace-nowrap text-[10px] text-slate-400">缩放粒度</span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="h-1 w-20 cursor-pointer appearance-none rounded bg-slate-700 accent-cyan-500 hover:bg-slate-600"
        title={`滚轮缩放灵敏度: ${value.toFixed(1)}`}
      />
      <span className="w-6 text-right text-[10px] tabular-nums text-slate-300">
        {value.toFixed(1)}
      </span>
    </div>
  );
}
