import React, { useState, useEffect, useRef, useCallback } from 'react';
import type {
  GripType,
  EMGSignalData,
  PredictionResult,
  ControllerState,
  SystemMetrics,
  LogEntry,
} from './types';
import * as api from './api';
import { HandVisualization } from './components/HandVisualization';
import { EmgChart } from './components/EmgChart';
import { InferencePanel } from './components/InferencePanel';
import { GripControlPanel } from './components/GripControlPanel';
import { ControlToolbar } from './components/ControlToolbar';
import { MetricsPanel } from './components/MetricsPanel';
import { EventLog } from './components/EventLog';

export const App: React.FC = () => {
  // Application State
  const [activeGrip, setActiveGrip] = useState<GripType>('OPEN');
  const [signalData, setSignalData] = useState<EMGSignalData | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [controllerState, setControllerState] = useState<ControllerState>({
    current_pressure_n: 0.0,
    target_pressure_n: 0.0,
    max_safe_pressure_n: 75.0,
    grip_force_percent: 0.0,
    contact_detected: false,
    slip_detected: false,
    controller_action: 'IDLE',
    active_grip: 'OPEN',
    stability_index: 100.0,
  });

  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [calibrated, setCalibrated] = useState<boolean>(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isDemoRunning, setIsDemoRunning] = useState<boolean>(false);
  const [demoPhase, setDemoPhase] = useState<string>('');
  const [demoSuccessCount, setDemoSuccessCount] = useState<number>(0);

  // References for demo interval & simulation loop
  const demoTimerRef = useRef<number | null>(null);
  const loopIntervalRef = useRef<number | null>(null);
  const slipTriggerRef = useRef<boolean>(false);

  // Helper to add timestamped event log
  const addLog = useCallback(
    (category: LogEntry['category'], message: string) => {
      const now = new Date();
      const timeStr = now.toTimeString().split(' ')[0];
      const entry: LogEntry = {
        id: `${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        timestamp: timeStr,
        category,
        message,
      };
      setLogs((prev) => [entry, ...prev.slice(0, 75)]);
    },
    []
  );

  // Initial mount: load metrics & run baseline check
  useEffect(() => {
    api
      .fetchMetrics()
      .then((m) => {
        setMetrics(m);
        addLog('SYSTEM', 'Connected to Edge AI Prosthetic Hand simulation pipeline.');
      })
      .catch((err) => {
        console.error('Failed to load metrics:', err);
        addLog('SYSTEM', 'Backend offline. Retrying connection...');
      });
  }, [addLog]);

  // Core processing step: generate EMG -> extract & predict -> step closed-loop controller
  const executePipelineStep = useCallback(
    async (
      targetGrip: GripType,
      simContactOverride?: boolean,
      simSlipOverride?: boolean
    ) => {
      try {
        // 1. Simulate sEMG Window
        const emg = await api.simulateEMG(targetGrip);
        setSignalData(emg);

        // 2. Inference on EMG Window
        const pred = await api.predictGrip(
          emg.channel_1_flexor,
          emg.channel_2_extensor
        );
        setPrediction(pred);

        // Determine contact status: auto-detect if closed enough or explicitly overridden
        const shouldSimulateContact =
          simContactOverride !== undefined
            ? simContactOverride
            : (targetGrip === 'POWER_GRIP' || targetGrip === 'PINCH_GRIP') &&
              controllerState.grip_force_percent > 35.0;

        const isSlip = simSlipOverride || slipTriggerRef.current;
        if (slipTriggerRef.current) {
          slipTriggerRef.current = false;
        }

        // 3. Step Adaptive Controller
        const ctrl = await api.stepGripControl(
          pred.predicted_grip,
          shouldSimulateContact,
          isSlip
        );
        setControllerState(ctrl);

        return { emg, pred, ctrl };
      } catch (err) {
        console.error('Pipeline step failed:', err);
        return null;
      }
    },
    [controllerState.grip_force_percent]
  );

  // Background loop when manual mode is running (updates every 600 ms)
  useEffect(() => {
    if (isDemoRunning) return;

    loopIntervalRef.current = window.setInterval(() => {
      executePipelineStep(activeGrip);
    }, 600);

    return () => {
      if (loopIntervalRef.current) clearInterval(loopIntervalRef.current);
    };
  }, [activeGrip, isDemoRunning, executePipelineStep]);

  // Manual Grip Selection Handler
  const handleSelectGrip = (grip: GripType) => {
    if (isDemoRunning) {
      handleStopDemo();
    }
    setActiveGrip(grip);
    addLog('SIGNAL', `EMG window generated for intention: ${grip.replace('_', ' ')}`);
    executePipelineStep(grip).then((res) => {
      if (res?.pred) {
        addLog(
          'INFERENCE',
          `Classified: ${res.pred.predicted_grip.replace('_', ' ')} (${res.pred.confidence_percent.toFixed(1)}% conf in ${res.pred.simulated_inference_time_ms} ms)`
        );
      }
    });
  };

  // User Calibration Handler
  const handleCalibrate = async () => {
    addLog('SYSTEM', 'Initiating user EMG baseline calibration routine (2.0s resting window)...');
    try {
      const res = await api.triggerCalibration('subject_01');
      setCalibrated(true);
      addLog(
        'SYSTEM',
        `Calibration complete. Noise floor: ${res.parameters.baseline_noise_floor_v}V, Gain: ${res.parameters.mvc_gain_multiplier}x`
      );
      // Refresh current signal with calibrated parameters
      executePipelineStep(activeGrip);
    } catch {
      addLog('SYSTEM', 'Calibration failed. Backend unavailable.');
    }
  };

  // Simulate Slip Handler
  const handleSimulateSlip = () => {
    slipTriggerRef.current = true;
    addLog('TACTILE', 'Micro-slip event detected by simulated shear FSR sensor!');
    executePipelineStep(activeGrip, true, true).then((res) => {
      if (res?.ctrl) {
        addLog(
          'ADAPTIVE',
          `Slip reflex triggered: adaptive torque boosted to ${res.ctrl.grip_force_percent}% (${res.ctrl.current_pressure_n} N)`
        );
      }
    });
  };

  // Reset Handler
  const handleReset = async () => {
    if (demoTimerRef.current) clearTimeout(demoTimerRef.current);
    setIsDemoRunning(false);
    setDemoPhase('');
    setActiveGrip('OPEN');
    await api.resetBackend();
    const ctrl = await api.stepGripControl('OPEN', false, false);
    setControllerState(ctrl);
    addLog('SYSTEM', 'System and actuator controllers reset to baseline idle.');
  };

  // AUTOMATED 27-SECOND DEMO SEQUENCE
  const handleStartDemo = () => {
    if (isDemoRunning) return;
    setIsDemoRunning(true);
    addLog('SYSTEM', 'Starting automated 27-second end-to-end demonstration sequence.');

    let elapsedSeconds = 0;
    let inFlight = false;
    setDemoPhase('0–3s: Open Hand baseline resting state');
    setActiveGrip('OPEN');
    executePipelineStep('OPEN', false, false).then((res) => {
      addLog('SIGNAL', 'Resting baseline EMG window received');
      if (res?.pred) {
        addLog(
          'INFERENCE',
          `Classifier output: ${res.pred.predicted_grip.replace('_', ' ')} (${res.pred.confidence_percent.toFixed(1)}% conf in ${res.pred.simulated_inference_time_ms} ms)`
        );
      }
    });

    const interval = window.setInterval(async () => {
      if (inFlight) return;
      inFlight = true;
      try {
        elapsedSeconds += 1;

        // 0–3 sec: Open Hand Baseline
        if (elapsedSeconds < 3) {
          setDemoPhase(`0–3s: Open Hand baseline muscle resting state (${elapsedSeconds}s)`);
          setActiveGrip('OPEN');
          await executePipelineStep('OPEN', false, false);
        }

        // 3–6 sec: Power Grip Triggered & Closing Actuation
        else if (elapsedSeconds === 3) {
          setDemoPhase('3–6s: User activates Power Grip intention');
          setActiveGrip('POWER_GRIP');
          const res = await executePipelineStep('POWER_GRIP', false, false);
          addLog('SIGNAL', 'High-amplitude co-contraction EMG surge detected');
          if (res?.pred) {
            addLog(
              'INFERENCE',
              `Classifier output: ${res.pred.predicted_grip.replace('_', ' ')} (${res.pred.confidence_percent.toFixed(1)}% conf in ${res.pred.simulated_inference_time_ms} ms)`
            );
          }
          addLog('ACTUATION', 'Actuator closing command transmitted to finger servos');
        } else if (elapsedSeconds < 6) {
          setDemoPhase(`3–6s: Fingers closing towards object (${elapsedSeconds}s)`);
          setActiveGrip('POWER_GRIP');
          await executePipelineStep('POWER_GRIP', false, false);
        }

        // 6–9 sec: Object Contact Detected on FSR Tactile Sensors
        else if (elapsedSeconds === 6) {
          setDemoPhase('6–9s: Object contact detected on tactile FSR pads');
          const res = await executePipelineStep('POWER_GRIP', true, false);
          if (res?.ctrl) {
            addLog(
              'TACTILE',
              `Initial physical contact detected on distal sensors (${res.ctrl.current_pressure_n.toFixed(1)} N)`
            );
          }
        } else if (elapsedSeconds < 9) {
          setDemoPhase(`6–9s: Tactile engagement and initial pressure (${elapsedSeconds}s)`);
          await executePipelineStep('POWER_GRIP', true, false);
        }

        // 9–12 sec: Grip Pressure Increases toward Target
        else if (elapsedSeconds === 9) {
          setDemoPhase('9–12s: Grip pressure below setpoint; adaptive controller stepping up');
          const res = await executePipelineStep('POWER_GRIP', true, false);
          if (res?.ctrl) {
            addLog(
              'ADAPTIVE',
              `Pressure (${res.ctrl.current_pressure_n.toFixed(1)} N) < Target (${res.ctrl.target_pressure_n.toFixed(1)} N): Proportional force increment applied`
            );
          }
        } else if (elapsedSeconds < 12) {
          setDemoPhase(`9–12s: Adaptive force ramping towards setpoint (${elapsedSeconds}s)`);
          await executePipelineStep('POWER_GRIP', true, false);
        }

        // 12–15 sec: Adaptive Controller Stabilizes Grip
        else if (elapsedSeconds === 12) {
          setDemoPhase('12–15s: Target pressure reached. Controller maintaining stable grip');
          const res = await executePipelineStep('POWER_GRIP', true, false);
          if (res?.ctrl) {
            addLog(
              'ADAPTIVE',
              `Stable grip achieved (${res.ctrl.current_pressure_n.toFixed(1)} N within deadband). Servos holding position.`
            );
          }
        } else if (elapsedSeconds < 15) {
          setDemoPhase(`12–15s: Grasp equilibrium maintained (${elapsedSeconds}s)`);
          await executePipelineStep('POWER_GRIP', true, false);
        }

        // 15–18 sec: Simulated Slip Event Detected
        else if (elapsedSeconds === 15) {
          setDemoPhase('15–18s: Simulated payload slip event detected!');
          slipTriggerRef.current = true;
          const res = await executePipelineStep('POWER_GRIP', true, true);
          addLog('TACTILE', 'ALERT: Sudden micro-slip detected at tactile sensor interface!');
          if (res?.ctrl) {
            addLog(
              'ADAPTIVE',
              `Anti-slip torque response: grip force boosted to ${res.ctrl.grip_force_percent.toFixed(0)}% (${res.ctrl.current_pressure_n.toFixed(1)} N)`
            );
          }
        } else if (elapsedSeconds < 18) {
          setDemoPhase(`15–18s: Anti-slip reflex response active (${elapsedSeconds}s)`);
          await executePipelineStep('POWER_GRIP', true, false);
        }

        // 18–21 sec: Controller Increases Grip Force to Recover Stability
        else if (elapsedSeconds === 18) {
          setDemoPhase('18–21s: Adaptive controller executes compensatory grasp stabilization');
          const res = await executePipelineStep('POWER_GRIP', true, false);
          if (res?.ctrl) {
            addLog(
              'ADAPTIVE',
              `Stabilization in progress: pressure at ${res.ctrl.current_pressure_n.toFixed(1)} N (Stability: ${res.ctrl.stability_index.toFixed(1)}%)`
            );
          }
        } else if (elapsedSeconds < 21) {
          setDemoPhase(`18–21s: Slip recovery and force regulation (${elapsedSeconds}s)`);
          await executePipelineStep('POWER_GRIP', true, false);
        }

        // 21–24 sec: Stable Grip Restored
        else if (elapsedSeconds === 21) {
          setDemoPhase('21–24s: Stable grip re-established. Slip condition cleared');
          const res = await executePipelineStep('POWER_GRIP', true, false);
          if (res?.ctrl) {
            addLog(
              'TACTILE',
              `Payload motion arrested. Grasp stability restored to ${res.ctrl.stability_index.toFixed(1)}% (${res.ctrl.current_pressure_n.toFixed(1)} N)`
            );
          }
        } else if (elapsedSeconds < 24) {
          setDemoPhase(`21–24s: Grasp stabilized and secure (${elapsedSeconds}s)`);
          await executePipelineStep('POWER_GRIP', true, false);
        }

        // 24–27 sec: Release
        else if (elapsedSeconds === 24) {
          setDemoPhase('24–27s: User intention: Release. Fingers extending');
          setActiveGrip('RELEASE');
          const res = await executePipelineStep('RELEASE', false, false);
          addLog('SIGNAL', 'Transient release EMG profile received');
          if (res?.pred) {
            addLog('INFERENCE', `Classifier output: ${res.pred.predicted_grip.replace('_', ' ')}`);
          }
          addLog('ACTUATION', 'Actuator command: open fingers to 0 deg');
        } else if (elapsedSeconds < 27) {
          setDemoPhase(`24–27s: Actuators returning to open position (${elapsedSeconds}s)`);
          setActiveGrip('RELEASE');
          await executePipelineStep('RELEASE', false, false);
        }

        // 27 sec: End of demo
        else {
          clearInterval(interval);
          setIsDemoRunning(false);
          setDemoPhase('');
          setActiveGrip('OPEN');
          await executePipelineStep('OPEN', false, false);
          setDemoSuccessCount((c) => c + 1);
          addLog('SYSTEM', 'Automated demonstration sequence completed successfully.');
        }
      } finally {
        inFlight = false;
      }
    }, 1000);

    demoTimerRef.current = interval;
  };

  const handleStopDemo = () => {
    if (demoTimerRef.current) clearInterval(demoTimerRef.current);
    setIsDemoRunning(false);
    setDemoPhase('');
    addLog('SYSTEM', 'Demo mode stopped by user.');
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col selection:bg-foreground selection:text-background">
      {/* Top Navigation / System Status Header */}
      <header className="border-b border-border bg-background-surface/80 backdrop-blur-sm sticky top-0 z-20 px-4 py-3">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-2">
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-base md:text-lg font-bold tracking-tight text-foreground font-mono">
                Edge AI Smart Prosthetic Hand
              </h1>
              <span className="text-xs px-2 py-0.5 rounded bg-background-elevated border border-border text-foreground-secondary font-mono">
                Software Prototype v0.1
              </span>
            </div>
            <p className="text-xs text-foreground-muted font-mono mt-0.5">
              7th-Semester Engineering Clinics · Digital Simulation & Adaptive Control Pipeline
            </p>
          </div>

          {/* Right Status Tags */}
          <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
            <div className="flex items-center space-x-2 px-3 py-1 rounded bg-background-elevated border border-border">
              <span className="w-2 h-2 rounded-full bg-technical-green inline-block animate-pulse" />
              <span className="text-foreground font-semibold">Simulation Mode Active</span>
            </div>
            <div className="px-2 py-0.5 rounded border border-border-subtle/60 text-foreground-muted text-[10.5px]">
              Hardware Offline (Virtual Pipeline)
            </div>
          </div>
        </div>

        {/* Prototype Validation Disclaimer Banner */}
        <div className="max-w-7xl mx-auto mt-2 pt-2 border-t border-border-subtle/60 flex items-center justify-between text-[11px] font-mono text-foreground-muted">
          <span>
            NOTICE: Sensor inputs are simulated for prototype validation. Physical hardware integration is scheduled for subsequent project phase.
          </span>
          {isDemoRunning && (
            <span className="text-technical-amber font-semibold animate-pulse">
              ● {demoPhase}
            </span>
          )}
        </div>
      </header>

      {/* Main Dashboard Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 space-y-4">
        {/* Top Row: Hand Visualizer & Inference Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          {/* Virtual Hand Canvas (7 cols) */}
          <div className="lg:col-span-7">
            <HandVisualization
              gripState={activeGrip}
              controllerState={controllerState}
            />
          </div>

          {/* ML Inference Panel (5 cols) */}
          <div className="lg:col-span-5">
            <InferencePanel
              prediction={prediction}
              calibrated={calibrated}
            />
          </div>
        </div>

        {/* Middle Row: Synthetic EMG Waveform & Closed-Loop Controller */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          {/* Synthetic EMG Panel (7 cols) */}
          <div className="lg:col-span-7">
            <EmgChart
              signalData={signalData}
              features={prediction?.features || null}
              activeGrip={activeGrip}
            />
          </div>

          {/* Adaptive Grip Panel (5 cols) */}
          <div className="lg:col-span-5">
            <GripControlPanel
              controllerState={controllerState}
              onSimulateSlip={handleSimulateSlip}
            />
          </div>
        </div>

        {/* Control Toolbar */}
        <ControlToolbar
          activeGrip={activeGrip}
          isDemoRunning={isDemoRunning}
          onStartDemo={handleStartDemo}
          onStopDemo={handleStopDemo}
          onSelectGrip={handleSelectGrip}
          onCalibrate={handleCalibrate}
          onSimulateSlip={handleSimulateSlip}
          onReset={handleReset}
        />

        {/* Bottom Row: Benchmarks Metrics & Live Event Log */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          <div className="lg:col-span-5">
            <MetricsPanel
              metrics={metrics}
              stabilityIndex={controllerState.stability_index}
              demoSuccessCount={demoSuccessCount}
            />
          </div>
          <div className="lg:col-span-7">
            <EventLog logs={logs} onClear={() => setLogs([])} />
          </div>
        </div>
      </main>

      {/* Engineering Footer */}
      <footer className="border-t border-border bg-background-surface py-3 px-4 text-center text-xs font-mono text-foreground-muted">
        Department of Electronics & Communication Engineering · Edge AI Smart Prosthetic Hand Software Prototype
      </footer>
    </div>
  );
};

export default App;
