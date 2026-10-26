import type {
  EMGSignalData,
  PredictionResult,
  ControllerState,
  CalibrationResult,
  SystemMetrics
} from './types';

const API_BASE_URL = 'http://127.0.0.1:8000';

export async function checkHealth(): Promise<{ status: string; mode: string }> {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) throw new Error('Backend offline');
  return res.json();
}

export async function simulateEMG(
  gripState: string,
  noiseLevel: number = 1.0
): Promise<EMGSignalData> {
  const res = await fetch(`${API_BASE_URL}/simulate/emg`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ grip_state: gripState, noise_level: noiseLevel }),
  });
  if (!res.ok) throw new Error('Failed to generate synthetic EMG signal');
  return res.json();
}

export async function predictGrip(
  channel1: number[],
  channel2: number[]
): Promise<PredictionResult> {
  const res = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ channel_1: channel1, channel_2: channel2 }),
  });
  if (!res.ok) throw new Error('Failed to run ML inference');
  return res.json();
}

export async function stepGripControl(
  predictedGrip: string,
  simulatedContact: boolean = false,
  slipTrigger: boolean = false,
  pressureOverride?: number | null
): Promise<ControllerState> {
  const res = await fetch(`${API_BASE_URL}/grip/control`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      predicted_grip: predictedGrip,
      simulated_contact: simulatedContact,
      slip_trigger: slipTrigger,
      pressure_override: pressureOverride ?? null,
    }),
  });
  if (!res.ok) throw new Error('Failed to step grip controller');
  return res.json();
}

export async function triggerCalibration(
  subjectId: string = 'clinics_subject_01'
): Promise<CalibrationResult> {
  const res = await fetch(`${API_BASE_URL}/calibrate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ subject_id: subjectId, simulated_duration_s: 2.0 }),
  });
  if (!res.ok) throw new Error('Failed to run calibration routine');
  return res.json();
}

export async function fetchMetrics(): Promise<SystemMetrics> {
  const res = await fetch(`${API_BASE_URL}/metrics`);
  if (!res.ok) throw new Error('Failed to retrieve system metrics');
  return res.json();
}

export async function resetBackend(): Promise<void> {
  await fetch(`${API_BASE_URL}/reset`, { method: 'POST' });
}
