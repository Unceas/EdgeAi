import React from 'react';
import type { ControllerState } from '../types';

interface GripControlPanelProps {
  controllerState: ControllerState;
  onSimulateSlip: () => void;
  onPressureOverrideChange?: (val: number | null) => void;
}

export const GripControlPanel: React.FC<GripControlPanelProps> = ({
  controllerState,
  onSimulateSlip,
}) => {
  const {
    current_pressure_n,
    target_pressure_n,
    max_safe_pressure_n,
    grip_force_percent,
    contact_detected,
    slip_detected,
    controller_action,
    stability_index,
  } = controllerState;

  // Pressure progress percentage relative to safety ceiling
  const pressurePct = Math.min(100, (current_pressure_n / max_safe_pressure_n) * 100);
  const targetPct = Math.min(100, (target_pressure_n / max_safe_pressure_n) * 100);

  // Closed-loop pipeline stages: IDLE -> CONTACT -> INCREASING -> DECREASING -> MAINTAINING -> SLIP DETECTED -> ANTI-SLIP -> STABILIZED
  type PipelineStage = 'IDLE' | 'CONTACT' | 'INCREASING' | 'DECREASING' | 'MAINTAINING' | 'SLIP DETECTED' | 'ANTI-SLIP' | 'STABILIZED';

  let currentStage: PipelineStage = 'IDLE';
  if (slip_detected) {
    currentStage = 'SLIP DETECTED';
  } else if (controller_action === 'SLIP_COMPENSATION') {
    currentStage = 'ANTI-SLIP';
  } else if (controller_action === 'MAINTAINING' && stability_index > 95) {
    currentStage = 'STABILIZED';
  } else if (controller_action === 'MAINTAINING') {
    currentStage = 'MAINTAINING';
  } else if (controller_action === 'DECREASING') {
    currentStage = 'DECREASING';
  } else if (controller_action === 'INCREASING') {
    currentStage = 'INCREASING';
  } else if (contact_detected) {
    currentStage = 'CONTACT';
  } else {
    currentStage = 'IDLE';
  }

  const STAGES: PipelineStage[] = [
    'IDLE',
    'CONTACT',
    'INCREASING',
    'DECREASING',
    'MAINTAINING',
    'SLIP DETECTED',
    'ANTI-SLIP',
    'STABILIZED',
  ];

  return (
    <div className="bg-background-surface border border-border rounded-md p-4 flex flex-col justify-between h-full">
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-border-subtle pb-2 mb-2">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono uppercase tracking-wider text-foreground font-semibold">
            Adaptive Closed-Loop Controller
          </span>
          <span className="text-[10px] bg-background-elevated border border-border-strong px-2 py-0.5 rounded text-foreground font-mono">
            Tactile FSR Reflex
          </span>
        </div>
        <span
          className={`text-[11px] font-mono font-bold px-2 py-0.5 rounded border ${
            slip_detected || controller_action === 'SLIP_COMPENSATION'
              ? 'text-foreground bg-technical-red border-technical-red animate-pulse'
              : controller_action === 'MAINTAINING'
              ? 'text-foreground bg-technical-green/30 border-technical-green'
              : controller_action === 'INCREASING'
              ? 'text-foreground bg-technical-amber/30 border-technical-amber'
              : controller_action === 'DECREASING'
              ? 'text-foreground bg-technical-cyan/30 border-technical-cyan'
              : 'text-foreground-secondary bg-background-elevated border-border'
          }`}
        >
          {controller_action.replace('_', ' ')}
        </span>
      </div>

      {/* Controller State Pipeline Stepper (Visual Hero Feature) */}
      <div className="mb-3 bg-background-subtle p-2 rounded border border-border-subtle">
        <div className="text-[10px] font-mono uppercase tracking-wider text-foreground-muted mb-1.5 flex justify-between">
          <span>Closed-Loop State Progression</span>
          <span className="text-foreground font-semibold">Stage: {currentStage}</span>
        </div>
        <div className="flex items-center justify-between gap-1 overflow-x-auto pb-1 font-mono text-[9px]">
          {STAGES.map((stage, idx) => {
            const isActive = currentStage === stage;
            const isAlert = stage === 'SLIP DETECTED' || stage === 'ANTI-SLIP';

            return (
              <React.Fragment key={stage}>
                <div
                  className={`px-1.5 py-1 rounded text-center whitespace-nowrap border transition-all ${
                    isActive
                      ? isAlert
                        ? 'bg-technical-red text-white font-bold border-technical-red scale-105 shadow'
                        : 'bg-foreground text-background font-bold border-foreground scale-105 shadow'
                      : 'bg-background-elevated text-foreground-muted border-border-subtle opacity-60'
                  }`}
                >
                  {stage === 'ANTI-SLIP' ? 'ANTI-SLIP +18%' : stage}
                </div>
                {idx < STAGES.length - 1 && (
                  <span className="text-foreground-muted text-[8px]">→</span>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>

      {/* Prominent High-Visibility Slip Alert Banner */}
      {(slip_detected || controller_action === 'SLIP_COMPENSATION') && (
        <div className="mb-3 p-2 bg-technical-red/20 border-2 border-technical-red rounded flex items-center justify-between font-mono animate-pulse">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-technical-red inline-block" />
            <span className="text-xs text-foreground font-bold">
              {slip_detected ? 'SOFTWARE-INJECTED SLIP DISTURBANCE' : 'ANTI-SLIP REFLEX ENGAGED'}
            </span>
          </div>
          <span className="text-xs text-foreground bg-technical-red px-2 py-0.5 rounded font-bold">
            +18% Servo Torque Boost
          </span>
        </div>
      )}

      {/* Primary Feedback Indicators */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-3 font-mono">
        {/* Current Pressure */}
        <div className="bg-background-subtle border border-border-subtle p-2.5 rounded">
          <div className="text-[10px] text-foreground-muted uppercase">Tactile Pressure</div>
          <div className="text-base font-bold text-foreground mt-0.5">
            {current_pressure_n.toFixed(1)} <span className="text-xs text-foreground-muted font-normal">N</span>
          </div>
          <div className="text-[10px] text-foreground-secondary font-medium">Target: {target_pressure_n.toFixed(0)} N</div>
        </div>

        {/* Grip Force / Servo Effort */}
        <div className="bg-background-subtle border border-border-subtle p-2.5 rounded">
          <div className="text-[10px] text-foreground-muted uppercase">Servo Command</div>
          <div className="text-base font-bold text-foreground mt-0.5">
            {grip_force_percent.toFixed(0)} <span className="text-xs text-foreground-muted font-normal">%</span>
          </div>
          <div className="text-[10px] text-foreground-secondary font-medium">Torque effort</div>
        </div>

        {/* Contact Status */}
        <div className="bg-background-subtle border border-border-subtle p-2.5 rounded">
          <div className="text-[10px] text-foreground-muted uppercase">Tactile Contact</div>
          <div className="text-sm font-bold mt-1">
            {contact_detected ? (
              <span className="text-technical-green font-bold">DETECTED</span>
            ) : (
              <span className="text-foreground-muted">NONE</span>
            )}
          </div>
          <div className="text-[10px] text-foreground-muted">Threshold: 5.0 N</div>
        </div>

        {/* Slip Alert */}
        <div className="bg-background-subtle border border-border-subtle p-2.5 rounded">
          <div className="text-[10px] text-foreground-muted uppercase">Slip Monitor</div>
          <div className="text-sm font-bold mt-1">
            {slip_detected ? (
              <span className="text-technical-red font-bold animate-pulse">SLIP DETECTED</span>
            ) : (
              <span className="text-foreground font-medium">STABLE</span>
            )}
          </div>
          <div className="text-[10px] text-foreground-muted">Stability: {stability_index}%</div>
        </div>
      </div>

      {/* Pressure Comparison Gauge Bar */}
      <div className="bg-background-subtle border border-border-subtle p-2.5 rounded mb-3 font-mono">
        <div className="flex justify-between text-xs text-foreground-secondary mb-1">
          <span className="text-foreground font-medium">FSR Pressure Envelope</span>
          <span className="font-bold text-foreground">{current_pressure_n.toFixed(1)} / {max_safe_pressure_n} N Max</span>
        </div>

        <div className="relative w-full bg-background-elevated h-3 rounded overflow-hidden border border-border">
          {/* Target marker */}
          {target_pressure_n > 0 && (
            <div
              className="absolute top-0 bottom-0 w-1 bg-foreground z-10"
              style={{ left: `${targetPct}%` }}
              title={`Target: ${target_pressure_n} N`}
            />
          )}
          {/* Current pressure fill */}
          <div
            className={`h-full transition-all duration-150 ${
              current_pressure_n > 65
                ? 'bg-technical-amber'
                : slip_detected || controller_action === 'SLIP_COMPENSATION'
                ? 'bg-technical-red'
                : 'bg-foreground'
            }`}
            style={{ width: `${pressurePct}%` }}
          />
        </div>

        <div className="flex justify-between text-[10px] text-foreground-muted mt-1 font-mono">
          <span>0 N</span>
          {target_pressure_n > 0 && (
            <span style={{ marginLeft: `${Math.max(5, targetPct - 15)}%` }} className="text-foreground font-semibold">
              ▲ Target ({target_pressure_n} N)
            </span>
          )}
          <span>75 N (Ceiling)</span>
        </div>
      </div>

      {/* Micro-Slip Disturbance Trigger Button */}
      <div className="flex items-center justify-between pt-2 border-t border-border-subtle">
        <div className="text-[11px] text-foreground-secondary font-mono">
          Inject simulated slip disturbance to closed loop:
        </div>
        <button
          onClick={onSimulateSlip}
          disabled={!contact_detected}
          className="text-xs font-mono uppercase tracking-wider px-3.5 py-1.5 rounded border border-border bg-background-elevated hover:bg-border/60 active:bg-border text-foreground font-semibold disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          Simulate Slip Disturbance
        </button>
      </div>
    </div>
  );
};
