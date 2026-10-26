export type GripType = 'OPEN' | 'POWER_GRIP' | 'PINCH_GRIP' | 'RELEASE';

export interface EMGSignalData {
  time_ms: number[];
  channel_1_flexor: number[];
  channel_2_extensor: number[];
  intended_grip: string;
  sampling_rate_hz: number;
  calibrated: boolean;
}

export interface EMGFeatures {
  ch1_rms: number;
  ch1_mav: number;
  ch1_var: number;
  ch1_energy: number;
  ch1_zcr: number;
  ch2_rms: number;
  ch2_mav: number;
  ch2_var: number;
  ch2_energy: number;
  ch2_zcr: number;
  ch_ratio: number;
  ch_diff: number;
  combined_rms: number;
  combined_mav: number;
  combined_energy: number;
  combined_zcr: number;
}

export interface PredictionResult {
  predicted_grip: GripType;
  confidence_percent: number;
  simulated_inference_time_ms: number;
  measured_inference_time_ms?: number;
  class_probabilities: Record<string, number>;
  features: EMGFeatures;
}

export interface ControllerState {
  current_pressure_n: number;
  target_pressure_n: number;
  max_safe_pressure_n: number;
  grip_force_percent: number;
  contact_detected: boolean;
  slip_detected: boolean;
  controller_action: 'IDLE' | 'CLOSING' | 'INCREASING' | 'DECREASING' | 'MAINTAINING' | 'SLIP_COMPENSATION' | 'RELEASING';
  active_grip: string;
  stability_index: number;
}

export interface CalibrationResult {
  status: string;
  subject_id: string;
  parameters: {
    baseline_noise_floor_v: number;
    mvc_gain_multiplier: number;
    sampling_window_samples: number;
    adc_resolution_bits: number;
  };
  message: string;
}

export interface SystemMetrics {
  synthetic_dataset_accuracy_percent: number;
  holdout_test_accuracy_percent?: number;
  cv_5fold_mean_accuracy_percent?: number;
  cv_5fold_std_percent?: number;
  simulated_inference_time_ms: number;
  measured_inference_time_ms?: number;
  macro_f1_score: number;
  weighted_f1_score?: number;
  total_synthetic_samples: number;
  model_architecture: string;
  supported_classes: string[];
  controller_deadband_n: number;
  controller_max_safe_pressure_n: number;
  disclaimer: string;
}

export interface LogEntry {
  id: string;
  timestamp: string;
  category: 'SIGNAL' | 'INFERENCE' | 'ACTUATION' | 'TACTILE' | 'ADAPTIVE' | 'SYSTEM';
  message: string;
}
