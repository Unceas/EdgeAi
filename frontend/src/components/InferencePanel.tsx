import React from 'react';
import type { PredictionResult, GripType } from '../types';

interface InferencePanelProps {
  prediction: PredictionResult | null;
  calibrated: boolean;
}

const CLASS_LABELS: { key: GripType; name: string }[] = [
  { key: 'OPEN', name: 'Open Hand' },
  { key: 'POWER_GRIP', name: 'Power Grip' },
  { key: 'PINCH_GRIP', name: 'Pinch Grip' },
  { key: 'RELEASE', name: 'Release' },
];

export const InferencePanel: React.FC<InferencePanelProps> = ({
  prediction,
  calibrated,
}) => {
  const predictedGrip = prediction?.predicted_grip || 'OPEN';
  const confidence = prediction?.confidence_percent ?? 0;
  const inferenceTime = prediction?.measured_inference_time_ms ?? prediction?.simulated_inference_time_ms ?? 1.9;
  const probabilities = prediction?.class_probabilities || {
    OPEN: 25.0,
    POWER_GRIP: 25.0,
    PINCH_GRIP: 25.0,
    RELEASE: 25.0,
  };

  return (
    <div className="bg-background-surface border border-border rounded-md p-4 flex flex-col justify-between h-full">
      {/* Panel Header */}
      <div className="flex items-center justify-between border-b border-border-subtle pb-2 mb-3">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono uppercase tracking-wider text-foreground font-semibold">
            ML Classifier
          </span>
          <span className="text-[10px] bg-background-elevated border border-border px-1.5 py-0.5 rounded text-foreground-secondary font-mono">
            Scikit-Learn RF
          </span>
        </div>
        <div className="flex items-center space-x-1.5 text-[11px] font-mono">
          <span
            className={`w-2 h-2 rounded-full inline-block ${
              calibrated ? 'bg-technical-green' : 'bg-foreground-muted'
            }`}
          />
          <span className="text-foreground-secondary">
            {calibrated ? 'Calibrated Baseline' : 'Default Baseline'}
          </span>
        </div>
      </div>

      {/* Main Prediction Display */}
      <div className="bg-background-subtle border border-border p-3.5 rounded-md mb-3">
        <div className="text-[10px] font-mono uppercase tracking-wider text-foreground-muted mb-1 flex justify-between">
          <span>Predicted Intention</span>
          <span className="text-foreground-secondary">Edge-Ready Model</span>
        </div>
        <div className="flex items-baseline justify-between">
          <div className="text-2xl font-bold tracking-tight text-foreground font-mono">
            {predictedGrip.replace('_', ' ')}
          </div>
          <div className="text-right">
            <span className="text-xs text-foreground-muted font-mono mr-1">Confidence:</span>
            <span className="text-lg font-bold text-foreground font-mono">
              {confidence.toFixed(1)}%
            </span>
          </div>
        </div>

        {/* Confidence meter bar */}
        <div className="w-full bg-background-elevated h-2 rounded-full mt-2 overflow-hidden border border-border-subtle">
          <div
            className="bg-foreground h-full transition-all duration-200"
            style={{ width: `${Math.min(100, Math.max(0, confidence))}%` }}
          />
        </div>
      </div>

      {/* Probability Distribution Breakdown */}
      <div className="space-y-2 mb-3">
        <div className="text-[10px] font-mono uppercase tracking-wider text-foreground-muted">
          Class Posterior Probabilities
        </div>

        {CLASS_LABELS.map(({ key, name }) => {
          const prob = probabilities[key] ?? 0;
          const isSelected = predictedGrip === key;

          return (
            <div key={key} className="space-y-0.5 font-mono">
              <div className="flex justify-between text-xs">
                <span
                  className={
                    isSelected ? 'text-foreground font-bold' : 'text-foreground-secondary'
                  }
                >
                  {name}
                </span>
                <span
                  className={
                    isSelected ? 'text-foreground font-bold' : 'text-foreground-muted'
                  }
                >
                  {prob.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-background-subtle h-1.5 rounded-full overflow-hidden border border-border-subtle">
                <div
                  className={`h-full transition-all duration-150 ${
                    isSelected ? 'bg-foreground' : 'bg-[#485368]'
                  }`}
                  style={{ width: `${Math.min(100, prob)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Latency & Hardware Metrics Footer */}
      <div className="pt-2 border-t border-border-subtle grid grid-cols-2 gap-2 text-[11px] font-mono">
        <div className="bg-background-subtle border border-border-subtle p-2 rounded">
          <div className="text-[10px] text-foreground-muted">Simulated Latency</div>
          <div className="text-foreground font-bold mt-0.5">{inferenceTime.toFixed(1)} ms</div>
        </div>
        <div className="bg-background-subtle border border-border-subtle p-2 rounded">
          <div className="text-[10px] text-foreground-muted">Feature Space</div>
          <div className="text-foreground font-bold mt-0.5">12 dimensions</div>
        </div>
      </div>
    </div>
  );
};
