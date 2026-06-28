// 显示值到内部倍率的转换：显示 1.0 对应内部 0.1（标准速度）
// 左侧从 1.0 按 0.1 步进递减到 0.1；右侧从 1.0 按 0.2 步进递增到 3.0
const ZOOM_LEVELS = [
  0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0,
  2.2, 2.4, 2.6, 2.8, 3.0,
];

const MULTIPLIER = 0.1;

interface ZoomSensitivitySliderProps {
  value: number; // 内部倍率，如 0.1 表示标准速度
  onChange: (value: number) => void;
}

export function ZoomSensitivitySlider({ value, onChange }: ZoomSensitivitySliderProps) {
  const displayValue = Math.round(value / MULTIPLIER * 10) / 10;
  const index = ZOOM_LEVELS.findIndex((level) => Math.abs(level - displayValue) < 1e-9);
  const safeIndex = index === -1 ? 9 : index; // 找不到时默认标准速度 1.0

  return (
    <div className="flex items-center gap-2 px-2">
      <span className="whitespace-nowrap text-[10px] text-slate-400">缩放速度</span>
      <input
        type="range"
        min={0}
        max={ZOOM_LEVELS.length - 1}
        step={1}
        value={safeIndex}
        onChange={(e) => {
          const idx = parseInt(e.target.value, 10);
          onChange(ZOOM_LEVELS[idx] * MULTIPLIER);
        }}
        className="h-1 w-24 cursor-pointer appearance-none rounded bg-slate-700 accent-cyan-500 hover:bg-slate-600"
        title={`缩放速度: ${ZOOM_LEVELS[safeIndex].toFixed(1)}`}
      />
      <span className="w-6 text-right text-[10px] tabular-nums text-slate-300">
        {ZOOM_LEVELS[safeIndex].toFixed(1)}
      </span>
    </div>
  );
}
