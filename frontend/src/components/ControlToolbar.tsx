import React from 'react';
import type { GripType } from '../types';

interface ControlToolbarProps {
  activeGrip: string;
  isDemoRunning: boolean;
  onStartDemo: () => void;
  onStopDemo: () => void;
  onSelectGrip: (grip: GripType) => void;
  onCalibrate: () => void;
  onSimulateSlip: () => void;
  onReset: () => void;
}

export const ControlToolbar: React.FC<ControlToolbarProps> = ({
  activeGrip,
  isDemoRunning,
  onStartDemo,
  onStopDemo,
  onSelectGrip,
  onCalibrate,
  onSimulateSlip,
  onReset,
}) => {
  const currentKey = activeGrip.toUpperCase().replace(' ', '_');

  return (
    <div className="bg-background-surface border border-border rounded-md p-4">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Primary Demo Controls */}
        <div className="flex items-center space-x-2">
          {!isDemoRunning ? (
            <button
              onClick={onStartDemo}
              className="px-4 py-2 bg-foreground text-background font-mono font-semibold text-xs uppercase tracking-wider rounded border border-foreground hover:bg-[#d8dce2] active:bg-[#b0b5be] transition-colors shadow-sm"
            >
              Start Demo
            </button>
          ) : (
            <button
              onClick={onStopDemo}
              className="px-4 py-2 bg-technical-red text-foreground font-mono font-semibold text-xs uppercase tracking-wider rounded border border-technical-red hover:bg-technical-red/80 active:bg-technical-red/90 transition-colors shadow-sm"
            >
              Stop Demo
            </button>
          )}

          <button
            onClick={onCalibrate}
            disabled={isDemoRunning}
            className="px-3.5 py-2 bg-background-elevated text-foreground-secondary hover:text-foreground font-mono text-xs uppercase tracking-wider rounded border border-border hover:bg-border/60 active:bg-border transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Calibrate
          </button>

          <button
            onClick={onReset}
            className="px-3 py-2 bg-background-elevated text-foreground-secondary hover:text-foreground font-mono text-xs uppercase tracking-wider rounded border border-border hover:bg-border/60 active:bg-border transition-colors"
          >
            Reset
          </button>
        </div>

        {/* Individual Grip Selectors */}
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-[11px] font-mono text-foreground-muted mr-1 uppercase">
            Manual Intent:
          </span>

          <button
            onClick={() => onSelectGrip('OPEN')}
            disabled={isDemoRunning}
            className={`px-3 py-1.5 font-mono text-xs uppercase tracking-wider rounded border transition-colors ${
              currentKey === 'OPEN'
                ? 'bg-foreground text-background font-semibold border-foreground'
                : 'bg-background-subtle text-foreground-secondary border-border hover:text-foreground hover:bg-background-elevated'
            } disabled:opacity-40 disabled:cursor-not-allowed`}
          >
            Open Hand
          </button>

          <button
            onClick={() => onSelectGrip('POWER_GRIP')}
            disabled={isDemoRunning}
            className={`px-3 py-1.5 font-mono text-xs uppercase tracking-wider rounded border transition-colors ${
              currentKey === 'POWER_GRIP'
                ? 'bg-foreground text-background font-semibold border-foreground'
                : 'bg-background-subtle text-foreground-secondary border-border hover:text-foreground hover:bg-background-elevated'
            } disabled:opacity-40 disabled:cursor-not-allowed`}
          >
            Power Grip
          </button>

          <button
            onClick={() => onSelectGrip('PINCH_GRIP')}
            disabled={isDemoRunning}
            className={`px-3 py-1.5 font-mono text-xs uppercase tracking-wider rounded border transition-colors ${
              currentKey === 'PINCH_GRIP'
                ? 'bg-foreground text-background font-semibold border-foreground'
                : 'bg-background-subtle text-foreground-secondary border-border hover:text-foreground hover:bg-background-elevated'
            } disabled:opacity-40 disabled:cursor-not-allowed`}
          >
            Pinch Grip
          </button>

          <button
            onClick={() => onSelectGrip('RELEASE')}
            disabled={isDemoRunning}
            className={`px-3 py-1.5 font-mono text-xs uppercase tracking-wider rounded border transition-colors ${
              currentKey === 'RELEASE'
                ? 'bg-foreground text-background font-semibold border-foreground'
                : 'bg-background-subtle text-foreground-secondary border-border hover:text-foreground hover:bg-background-elevated'
            } disabled:opacity-40 disabled:cursor-not-allowed`}
          >
            Release
          </button>

          <button
            onClick={onSimulateSlip}
            disabled={isDemoRunning}
            className="px-3 py-1.5 font-mono text-xs uppercase tracking-wider rounded border border-border bg-background-elevated text-foreground-secondary hover:text-technical-amber hover:border-technical-amber/40 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Simulate Slip
          </button>
        </div>
      </div>
    </div>
  );
};
