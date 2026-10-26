import React, { useEffect, useRef, useCallback } from 'react';
import type { EMGSignalData, EMGFeatures } from '../types';

interface EmgChartProps {
  signalData: EMGSignalData | null;
  features: EMGFeatures | null;
  activeGrip: string;
}

export const EmgChart: React.FC<EmgChartProps> = ({
  signalData,
  features,
  activeGrip,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const stateKey = activeGrip.toUpperCase().replace(' ', '_');

  const getSignalDescription = () => {
    switch (stateKey) {
      case 'POWER_GRIP':
        return 'High Co-Contraction Burst (Both Channels Active)';
      case 'PINCH_GRIP':
        return 'Selective Precision Burst (Flexor Dominant)';
      case 'RELEASE':
        return 'Transient Motor Decay (Dropping to Baseline)';
      case 'OPEN':
      default:
        return 'Resting Baseline (Low Voltage Floor)';
    }
  };

  const drawChart = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // High-DPI responsive scaling
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width;
    const height = rect.height;

    // Clear background
    ctx.fillStyle = '#11141a';
    ctx.fillRect(0, 0, width, height);

    // Draw technical grid lines
    ctx.strokeStyle = '#1d222c';
    ctx.lineWidth = 1;

    // Horizontal grid
    const hSteps = 6;
    for (let i = 0; i <= hSteps; i++) {
      const y = (height / hSteps) * i;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Vertical grid
    const vSteps = 10;
    for (let i = 0; i <= vSteps; i++) {
      const x = (width / vSteps) * i;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    // Zero Baselines
    const midY1 = height * 0.28;
    const midY2 = height * 0.74;

    ctx.strokeStyle = '#2d3545';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(40, midY1);
    ctx.lineTo(width, midY1);
    ctx.moveTo(40, midY2);
    ctx.lineTo(width, midY2);
    ctx.stroke();
    ctx.setLineDash([]);

    // Voltage scale ticks on left margin
    ctx.fillStyle = '#64748b';
    ctx.font = '9px monospace';
    ctx.textAlign = 'right';

    // Channel 1 scale
    ctx.fillText('+1V', 35, midY1 - height * 0.18);
    ctx.fillText('0V', 35, midY1 + 3);
    ctx.fillText('-1V', 35, midY1 + height * 0.18);

    // Channel 2 scale
    ctx.fillText('+1V', 35, midY2 - height * 0.18);
    ctx.fillText('0V', 35, midY2 + 3);
    ctx.fillText('-1V', 35, midY2 + height * 0.18);

    // Channel baseline labels
    ctx.fillStyle = '#94a3b8';
    ctx.font = '10px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('CH1: FLEXOR', 45, midY1 - height * 0.19);
    ctx.fillText('CH2: EXTENSOR', 45, midY2 - height * 0.19);

    if (!signalData || !signalData.channel_1_flexor.length) {
      ctx.fillStyle = '#6f7682';
      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('Awaiting synthetic sEMG window stream...', width / 2, height / 2);
      return;
    }

    const ch1 = signalData.channel_1_flexor;
    const ch2 = signalData.channel_2_extensor;
    const n = ch1.length;
    const plotStartX = 42;
    const plotWidth = width - plotStartX;
    const stepX = plotWidth / (n - 1);
    const ampScale = height * 0.22;

    // Draw Channel 1: Flexor (High-contrast bright white)
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    for (let i = 0; i < n; i++) {
      const x = plotStartX + i * stepX;
      const y = midY1 - ch1[i] * ampScale;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Draw Channel 2: Extensor (Technical silver-grey)
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    for (let i = 0; i < n; i++) {
      const x = plotStartX + i * stepX;
      const y = midY2 - ch2[i] * ampScale;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }, [signalData]);

  useEffect(() => {
    drawChart();

    const container = containerRef.current;
    if (!container) return;

    const resizeObserver = new ResizeObserver(() => {
      drawChart();
    });
    resizeObserver.observe(container);

    return () => {
      resizeObserver.disconnect();
    };
  }, [drawChart]);

  return (
    <div className="bg-background-surface border border-border rounded-md p-4 flex flex-col justify-between h-full">
      {/* Chart Header */}
      <div className="flex items-center justify-between border-b border-border-subtle pb-2 mb-2">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono uppercase tracking-wider text-foreground font-semibold">
            Synthetic sEMG Waveform
          </span>
          <span className="text-[10px] bg-background-elevated border border-border-strong px-2 py-0.5 rounded text-foreground font-mono">
            200 ms Window · 1000 Hz
          </span>
        </div>
        <div className="flex items-center space-x-3 text-[11px] font-mono">
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-1 bg-[#ffffff] inline-block rounded-sm" />
            <span className="text-foreground font-medium">Ch1: Flexor</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-1 bg-[#94a3b8] inline-block rounded-sm" />
            <span className="text-foreground-secondary">Ch2: Extensor</span>
          </div>
        </div>
      </div>

      {/* Waveform Canvas */}
      <div ref={containerRef} className="relative w-full h-[155px] bg-background-subtle border border-border-subtle rounded overflow-hidden">
        <canvas ref={canvasRef} className="w-full h-full block" />
        <div className="absolute top-1.5 right-2 text-[10px] font-mono text-foreground font-semibold bg-background-surface/90 border border-border px-2 py-0.5 rounded">
          {getSignalDescription()}
        </div>
      </div>

      {/* Extracted Features Strip */}
      <div className="mt-3 pt-2 border-t border-border-subtle">
        <div className="text-[10px] font-mono uppercase tracking-wider text-foreground-muted mb-1.5 flex justify-between">
          <span>Time-Domain Statistical Features</span>
          <span className="text-foreground-secondary">Input Vector: 12-dim</span>
        </div>
        <div className="grid grid-cols-5 gap-2 font-mono">
          <div className="bg-background-subtle border border-border-subtle p-1.5 rounded text-center">
            <div className="text-[10px] text-foreground-muted">RMS</div>
            <div className="text-xs font-bold text-foreground mt-0.5">
              {features ? features.combined_rms.toFixed(3) : '--'}
            </div>
            <div className="text-[9px] text-foreground-muted">Volts</div>
          </div>

          <div className="bg-background-subtle border border-border-subtle p-1.5 rounded text-center">
            <div className="text-[10px] text-foreground-muted">MAV</div>
            <div className="text-xs font-bold text-foreground mt-0.5">
              {features ? features.combined_mav.toFixed(3) : '--'}
            </div>
            <div className="text-[9px] text-foreground-muted">Volts</div>
          </div>

          <div className="bg-background-subtle border border-border-subtle p-1.5 rounded text-center">
            <div className="text-[10px] text-foreground-muted">VAR</div>
            <div className="text-xs font-bold text-foreground mt-0.5">
              {features ? features.ch1_var.toFixed(4) : '--'}
            </div>
            <div className="text-[9px] text-foreground-muted">V²</div>
          </div>

          <div className="bg-background-subtle border border-border-subtle p-1.5 rounded text-center">
            <div className="text-[10px] text-foreground-muted">ENERGY</div>
            <div className="text-xs font-bold text-foreground mt-0.5">
              {features ? features.combined_energy.toFixed(1) : '--'}
            </div>
            <div className="text-[9px] text-foreground-muted">SSI</div>
          </div>

          <div className="bg-background-subtle border border-border-subtle p-1.5 rounded text-center">
            <div className="text-[10px] text-foreground-muted">ZCR</div>
            <div className="text-xs font-bold text-foreground mt-0.5">
              {features ? features.combined_zcr.toFixed(3) : '--'}
            </div>
            <div className="text-[9px] text-foreground-muted">rate</div>
          </div>
        </div>
      </div>
    </div>
  );
};
