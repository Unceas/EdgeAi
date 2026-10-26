"""
Chapter 4: System Architecture & Implementation Details
Module for 80+ page Final Project Report.
Contains Section 4.1 through 4.5 with architectural diagrams, Level 0/1/2 DFDs,
UML models, complete mathematical formulations, and pseudocode for Algorithms 1-4.
"""

def get_chapter4_html():
    return """
<!-- CHAPTER 4 -->
<div class="page-break"></div>
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title">CHAPTER 4<br>SYSTEM ARCHITECTURE &amp; IMPLEMENTATION DETAILS</h1>

<h2>4.1 System Architecture Blueprint &amp; Data Flow Diagrams</h2>
<p>The engineering realization of the Edge AI Smart Prosthetic Hand addresses the fundamental bottleneck of modern myoelectric prosthetics: the lack of closed-loop tactile autonomy and the severe computational overhead of deep learning classifiers. To solve these dual limitations, the architecture introduces a strictly decoupled, hierarchical dual-brain paradigm. High-level user intent recognition (the "Cognitive Brain") is separated from low-level tactile force regulation (the "Autonomic Reflex Brain"). In doing so, muscle intention inference operates at the supervisory tier, selecting discrete kinematic modes, while high-frequency force stabilization, slip prevention, and crush avoidance are delegated to an autonomous, closed-loop sub-controller running at millisecond intervals.</p>

<p>Figure 4.1 illustrates the complete four-tier architectural blueprint of the cyber-physical software simulation system, spanning sensory emulation, edge feature extraction and inference, closed-loop grasp regulation, and full-stack telemetry visualization.</p>

<div class="figure-container">
  <div class="figure-frame">
    <div style="background-color: #0f172a; color: #f8fafc; padding: 18px; border-radius: 6px; font-family: monospace; font-size: 9.5pt; text-align: left; line-height: 1.45;">
      +----------------------------------------------------------------------------------------------------+<br>
      |                     LAYER 1: SENSORY EMULATION &amp; CALIBRATION TIER (1000 Hz)                        |<br>
      |  +-------------------------------------+      +--------------------------------------------------+  |<br>
      |  | Ch1: Flexor Digitorum Superficialis |      | Ch2: Extensor Digitorum Communis (EDC)           |  |<br>
      |  | - Resting Noise Calib (0.005-0.20V) |      | - Physiological Gaussian Process Waveforms       |  |<br>
      |  | - Burst Envelope Activation Dynamics|      | - 200 ms Sliding Window Buffer (N=200 Samples)   |  |<br>
      |  +-------------------------------------+      +--------------------------------------------------+  |<br>
      +-------------------------------------------------+--------------------------------------------------+<br>
                                                        |<br>
                                                        v<br>
      +----------------------------------------------------------------------------------------------------+<br>
      |                 LAYER 2: EDGE INTELLIGENCE &amp; FEATURE EXTRACTION TIER (Host CPU)                    |<br>
      |  +--------------------------------------+     +--------------------------------------------------+  |<br>
      |  | Statistical Feature Extraction (12D) |     | Random Forest Intention Classifier (35 Trees)   |  |<br>
      |  | - RMS, MAV, VAR, SSI, ZCR (Per-Ch)   |--&gt;  | - Max Tree Depth: 7, Stratified Evaluation       |  |<br>
      |  | - Inter-Channel Ratio &amp; Difference   |     | - Classes: Open, Power Grip, Pinch Grip, Release |  |<br>
      |  | - Zero-Divide Protective Guards (N&lt;=1)|    | - Benchmark Latency: 1.40 - 1.88 ms Host Exec    |  |<br>
      |  +--------------------------------------+     +--------------------------------------------------+  |<br>
      +-------------------------------------------------+--------------------------------------------------+<br>
                                                        |<br>
                                                        v<br>
      +----------------------------------------------------------------------------------------------------+<br>
      |                 LAYER 3: AUTONOMOUS CLOSED-LOOP TACTILE REGULATION TIER (50 Hz)                     |<br>
      |  +--------------------------------------+     +--------------------------------------------------+  |<br>
      |  | Distal Force Feedback &amp; Contact Det|     | Adaptive Anti-Slip Reflex &amp; Crush Intervention |  |<br>
      |  | - Virtual FSR Array (0 - 100 N)      |--&gt;  | - Proportional Force Ramping (+1.5 N/cycle)      |  |<br>
      |  | - Contact Threshold Th_c = 5.0 N     |     | - Deadband Hysteresis Delta_db = 3.0 N           |  |<br>
      |  | - Target Setpoint F_target = 50.0 N  |     | - Shear Slip Boost: +18% (+12 N instantaneous)   |  |<br>
      |  | - Hard Crush Ceiling F_max = 75.0 N  |     | - Emergency Safety Freeze on Over-Pressure       |  |<br>
      |  +--------------------------------------+     +--------------------------------------------------+  |<br>
      +-------------------------------------------------+--------------------------------------------------+<br>
                                                        |<br>
                                                        v<br>
      +----------------------------------------------------------------------------------------------------+<br>
      |                 LAYER 4: HIGH-DPI TELEMETRY &amp; PRESENTATION TIER (React 19 / Vite)                 |<br>
      |  +--------------------------------------+     +--------------------------------------------------+  |<br>
      |  | Responsive 2-Ch Oscilloscope Canvas  |     | Kinematic 3D Hand Model &amp; Stage State Machine |  |<br>
      |  | - High-DPI DPR Auto-Scaling Buffer   |     | - 5-Finger Articulation &amp; Tendon Geometry     |  |<br>
      |  | - Real-Time Waveform Rendering       |     | - 8-State Progression &amp; 27s Automated Script  |  |<br>
      |  +--------------------------------------+     +--------------------------------------------------+  |<br>
      +----------------------------------------------------------------------------------------------------+
    </div>
  </div>
  <div class="figure-caption">Figure 4.1: Four-Tier Cyber-Physical System Architecture of the Edge AI Smart Prosthetic Hand.</div>
</div>

<h3>4.1.1 Hierarchical 4-Layer Architecture</h3>
<p>The system execution is segmented into four distinct operational layers:</p>
<ol>
  <li><b>Layer 1 (Sensory Emulation Tier):</b> Emulates two bipolar sEMG electrode channels placed over antagonistic muscle groups of the human forearm: Channel 1 corresponds to the <i>Flexor Digitorum Superficialis</i> (FDS, primarily responsible for digit flexion and grasp closure), while Channel 2 corresponds to the <i>Extensor Digitorum Communis</i> (EDC, primarily responsible for digit extension and hand opening). Signals are generated at an industry-standard sampling rate of \(f_s = 1000\text{ Hz}\) (1.0 ms temporal resolution). Analysis is performed across sliding windows of length \(N = 200\text{ samples}\) (200 ms observation window). A baseline noise calibration parameter \(\sigma_{base} \in [0.005, 0.20]\text{ V}\) governs background thermal electrode impedance and resting muscle tone.</li>
  <li><b>Layer 2 (Edge Intelligence Tier):</b> Operates on the sampled window data to extract a lightweight 12-dimensional feature vector. Features are designed for microsecond execution on edge microcontrollers, avoiding floating-point Fourier or Wavelet transformations. The extracted feature vector is fed to a constrained Random Forest ensemble (35 estimators, maximum tree depth 7). The classifier predicts the discrete human grasp intent and returns the execution latency profiled at microsecond precision on the host CPU.</li>
  <li><b>Layer 3 (Autonomous Closed-Loop Tactile Regulation Tier):</b> Models the physical interaction between the prosthetic digits and a manipulated payload. Utilizing simulated distal Force Sensitive Resistors (FSRs), this layer monitors normal contact force \(F_n(t)\). When contact exceeds the contact threshold (\(F_c = 5.0\text{ N}\)), the controller transitions into closed-loop proportional regulation, increasing force toward a calibrated target setpoint (\(F_{target} = 50.0\text{ N}\)). A deadband hysteresis window of \(\pm 3.0\text{ N}\) prevents actuator chatter. If an external shear slip disturbance is detected, an autonomous spinal-reflex loop injects an instantaneous +18% effort boost (+12 N force) to halt displacement. A non-negotiable safety ceiling (\(F_{max} = 75.0\text{ N}\)) prevents payload crushing.</li>
  <li><b>Layer 4 (Telemetry Presentation Tier):</b> A modern web dashboard built with React 19, TypeScript, and Vite. The dashboard consumes RESTful endpoints served by FastAPI at `127.0.0.1:8000`, rendering multi-channel raw sEMG waveforms, dynamic force progress gauges, an interactive 3D kinematic hand skeleton, and an automated continuous demonstration sequence.</li>
</ol>

<h3>4.1.2 Level 0 Context Data Flow Diagram</h3>
<p>The Level 0 Context Diagram (Figure 4.2) models the prosthetic hand simulation system as a single cohesive process interacting with external entities: the User/Amputee Operator, the Physical Object (Payload), and the Supervisory Clinician/Engineer.</p>

<div class="figure-container">
  <div class="figure-frame">
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 18px; border-radius: 6px; font-family: monospace; font-size: 10pt; line-height: 1.5; color: #0f172a;">
      [ Amputee Operator ] --- (Forearm Muscle Contractions) ---&gt; [ 0.0 ] &lt;--- (Shear / Gravitational Disturbances) --- [ Manipulated Payload ]<br>
                                                                 |     |<br>
      [ Amputee Operator ] &lt;-- (Visual Kinematic / Force State) --| PRO | -- (Dynamic Grip Normal Force F_n) -----&gt; [ Manipulated Payload ]<br>
                                                                 | STH |<br>
      [ Clinician / Eng. ] --- (Noise Calibration / Target F) ---&gt;| SYS | -- (Real-Time Telemetry &amp; Latency Logs) --&gt; [ Clinician / Eng. ]<br>
      [ Clinician / Eng. ] --- (Manual Slip Disturbance Inject) --&gt;| TEM |
    </div>
  </div>
  <div class="figure-caption">Figure 4.2: Level 0 Context Data Flow Diagram for the Edge AI Smart Prosthetic Hand.</div>
</div>

<h3>4.1.3 Level 1 Data Flow Diagram (DFD)</h3>
<p>The Level 1 Data Flow Diagram (Figure 4.3) decomposes the system into four core functional processes: Signal Generation &amp; Buffering (Process 1.0), Edge Feature Extraction &amp; Intent Classification (Process 2.0), Closed-Loop Grip Force Regulation (Process 3.0), and Telemetry Logging &amp; User Interface Orchestration (Process 4.0).</p>

<div class="figure-container">
  <div class="figure-frame">
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 16px; border-radius: 6px; font-family: monospace; font-size: 9pt; line-height: 1.45; color: #0f172a;">
      [ Muscle Model ]<br>
             |<br>
             v (Grip Request: Open, Power, Pinch, Release)<br>
      +----------------------------------------------------+<br>
      | 1.0 Signal Generation &amp; Window Buffering          | &lt;=== [ D1: Calibration Store (Noise Baseline) ]<br>
      |     Generates N=200 Samples @ 1000 Hz              |<br>
      +----------------------------------------------------+<br>
             | Ch1, Ch2 Raw Discrete Arrays [200]<br>
             v<br>
      +----------------------------------------------------+<br>
      | 2.0 Edge Feature Extraction &amp; Classification       | &lt;=== [ D2: Pre-Trained RF Model Store (35 Trees) ]<br>
      |     Computes 12D Time-Domain Vector, RF Inference  |<br>
      +----------------------------------------------------+<br>
             | Predicted Grip State + Confidence + Host Latency (ms)<br>
             v<br>
      +----------------------------------------------------+<br>
      | 3.0 Closed-Loop Grip Force Regulation              | &lt;=== [ D3: Controller State Store (F_current, Mode) ]<br>
      |     Evaluates FSR Feedback, Anti-Slip, Deadband    |<br>
      +----------------------------------------------------+<br>
             | Commanded Motor Step (Duty Cycle / Force Target)<br>
             v<br>
      +----------------------------------------------------+<br>
      | 4.0 Telemetry Broadcast &amp; UI Presentation          | ====&gt; [ React Dashboard / Kinematic 3D Canvas ]<br>
      |     Assembles JSON Packet, Updates Oscilloscope    |<br>
      +----------------------------------------------------+
    </div>
  </div>
  <div class="figure-caption">Figure 4.3: Level 1 Data Flow Diagram showing inter-process communication and persistent data stores.</div>
</div>

<h3>4.1.4 Level 2 DFD: Closed-Loop Grasping &amp; Shear Slip Reflex Loop</h3>
<p>Figure 4.4 details Process 3.0 (Closed-Loop Tactile Grasp Regulation). When an intent trigger arrives, Sub-process 3.1 verifies contact state against \(F_c = 5.0\text{ N}\). Sub-process 3.2 executes error-proportional force adjustment. Concurrently, Sub-process 3.3 polls the shear slip flag; upon detection of displacement, an instantaneous bypass elevates commanded force by 18%, while Sub-process 3.4 asserts a non-overridable anti-crush ceiling of 75.0 N.</p>

<div class="figure-container">
  <div class="figure-frame">
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 16px; border-radius: 6px; font-family: monospace; font-size: 9pt; line-height: 1.45; color: #0f172a;">
      From Process 2.0 (Grip State)<br>
             |<br>
             v<br>
      +-----------------------------------------+<br>
      | 3.1 Contact Threshold Detection         |<br>
      |     Check: F_current &gt;= 5.0 N?          |<br>
      +-----------------------------------------+<br>
             | NO (Free Closing)       | YES (Payload Contacted)<br>
             v                         v<br>
      [ Increment Travel ]     +-----------------------------------------+<br>
                               | 3.2 Proportional Force Regulation       | &lt;--- [ Target Setpoint: 50.0 N ]<br>
                               |     Error e = F_target - F_current      |<br>
                               +-----------------------------------------+<br>
                                       |              ^<br>
                                       v              |<br>
                               +-----------------------------------------+<br>
                               | 3.3 Shear Slip Reflex Subroutine        | &lt;--- [ Slip Disturbance Flag ]<br>
                               |     If Slip: F_cmd = F_current + 18%    |<br>
                               +-----------------------------------------+<br>
                                       |<br>
                                       v<br>
                               +-----------------------------------------+<br>
                               | 3.4 Anti-Crush Safety Ceiling Assertion |<br>
                               |     Clamp: F_cmd = min(F_cmd, 75.0 N)   |<br>
                               +-----------------------------------------+<br>
                                       |<br>
                                       v To Actuator Kinematics &amp; Telemetry
    </div>
  </div>
  <div class="figure-caption">Figure 4.4: Level 2 Data Flow Diagram for the Closed-Loop Grasping and Anti-Slip Autonomous Subroutine.</div>
</div>

<h2>4.2 UML Behavioral Models &amp; System Dynamics</h2>

<h3>4.2.1 Use Case Model &amp; Actor Catalog</h3>
<p>The system interacts with two primary actors: the Amputee Operator (who provides intentional control through muscular activation) and the Clinical Engineer / Researcher (who configures system sensitivity, inspects telemetry, and evaluates stability). Table 4.1 catalogs the formal system use cases.</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 10%;">UC ID</th>
      <th style="width: 20%;">Use Case Name</th>
      <th style="width: 15%;">Primary Actor</th>
      <th style="width: 25%;">Pre-Conditions</th>
      <th style="width: 30%;">Post-Conditions &amp; Side Effects</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>UC-01</b></td>
      <td>Configure Noise Calibration</td>
      <td>Clinical Engineer</td>
      <td>Backend API initialized at port 8000.</td>
      <td>Baseline noise \(\sigma_{base}\) updated in server state; affects subsequent synthetic sEMG generation.</td>
    </tr>
    <tr>
      <td><b>UC-02</b></td>
      <td>Synthesize sEMG Signal Burst</td>
      <td>Amputee / Simulator</td>
      <td>Target grip class selected (0, 1, 2, or 3).</td>
      <td>Returns 2-channel array of \(N=200\) float samples conforming to physiological muscle recruitment envelopes.</td>
    </tr>
    <tr>
      <td><b>UC-03</b></td>
      <td>Predict Intent &amp; Profile Latency</td>
      <td>System Automation</td>
      <td>2-channel signal of valid length (\(N \ge 10\)) provided.</td>
      <td>Returns classified grip label, confidence score, and host CPU inference latency measured in milliseconds.</td>
    </tr>
    <tr>
      <td><b>UC-04</b></td>
      <td>Step Closed-Loop Grip Controller</td>
      <td>System Automation</td>
      <td>Current grip state active; slip flag asserted or unasserted.</td>
      <td>Iterates controller state; calculates updated normal force; manages deadband; asserts crush protection ceiling.</td>
    </tr>
    <tr>
      <td><b>UC-05</b></td>
      <td>Inject Shear Slip Disturbance</td>
      <td>Clinical Engineer</td>
      <td>Prosthetic hand actively holding payload in STABLE_HOLD.</td>
      <td>Sets `slip_detected = True`; triggers autonomous anti-slip reflex (+18% effort boost); updates event log.</td>
    </tr>
    <tr>
      <td><b>UC-06</b></td>
      <td>Reset System State</td>
      <td>Operator / Engineer</td>
      <td>Any operational state active.</td>
      <td>Restores hand to IDLE state; zeroes actuator travel and force; clears slip flag; logs system reset.</td>
    </tr>
    <tr>
      <td><b>UC-07</b></td>
      <td>Run Automated Demonstration</td>
      <td>Clinical Engineer</td>
      <td>UI active; dashboard rendered.</td>
      <td>Executes 27-second continuous multi-phase progression across baseline, grip closure, slip reflex, and reset.</td>
    </tr>
  </tbody>
</table>

<h3>4.2.2 Sequence Model: Real-Time Myoelectric Grasp Execution</h3>
<p>Figure 4.5 illustrates the sequence of messages exchanged between the User Interface, the FastAPI Controller, the Feature Extraction Engine, the Random Forest Model, and the Tactile Grip Sub-controller during an active grasp cycle.</p>

<div class="figure-container">
  <div class="figure-frame">
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 16px; border-radius: 6px; font-family: monospace; font-size: 8.5pt; line-height: 1.4; color: #0f172a;">
  UI Dashboard           FastAPI (/predict)        Feature Engine        RF Classifier      Grip Controller<br>
       |                         |                       |                     |                   |<br>
       |--- POST /predict ------&gt;|                       |                     |                   |<br>
       |    (Ch1, Ch2 Arrays)    |--- extract_features -&gt;|                     |                   |<br>
       |                         |    (Verify N &gt;= 2)    |                     |                   |<br>
       |                         |&lt;-- 12D Vector --------|                     |                   |<br>
       |                         |                                             |                   |<br>
       |                         |--- start_timer() ---------------------------|                   |<br>
       |                         |--- predict(12D Vector) --------------------&gt;|                   |<br>
       |                         |&lt;-- class: Power Grip, conf: 0.98 -----------|                   |<br>
       |                         |--- stop_timer() -&gt; 1.46 ms                  |                   |<br>
       |                         |                                                                 |<br>
       |&lt;-- HTTP 200 (Grip, Lat)-|                                                                 |<br>
       |                                                                                           |<br>
       |--- POST /control/step -------------------------------------------------------------------&gt;| (CLOSING)<br>
       |    (state: Power Grip, slip: False)                                                       |-- Detect Contact (F &gt;= 5N)<br>
       |&lt;-- HTTP 200 (force: 18.5 N, state: PRESSURE_REGULATING) ---------------------------------|   Regulate Proportional<br>
       |                                                                                           |<br>
       |--- POST /control/step (Slip Triggered: True) --------------------------------------------&gt;| (SLIP_DETECTED)<br>
       |&lt;-- HTTP 200 (force: 49.8 N, state: SLIP_RECOVERY, boost: +18%) --------------------------|   Engage Reflex Boost<br>
       |                                                                                           |<br>
       |--- POST /control/reset ------------------------------------------------------------------&gt;| (IDLE)<br>
       |&lt;-- HTTP 200 (force: 0.0 N, state: IDLE, travel: 0.0 mm) ----------------------------------|   Release Hand Actuators
    </div>
  </div>
  <div class="figure-caption">Figure 4.5: UML Sequence Diagram depicting intention prediction, closed-loop regulation, and reflex recovery.</div>
</div>

<h3>4.2.3 Finite State Machine: 8-State Prosthetic Actuation Lifecycle</h3>
<p>To eliminate chaotic state transitions and guarantee deterministic safety under all operating conditions, the prosthetic actuation sub-system is formalized as a rigorous Finite State Machine (FSM) comprising eight mutually exclusive states, as detailed in Table 4.2.</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 15%;">State Name</th>
      <th style="width: 25%;">Entry Condition / Trigger</th>
      <th style="width: 30%;">Internal Operation &amp; Dynamics</th>
      <th style="width: 30%;">Exit Condition / Next State</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>1. IDLE</b></td>
      <td>System boot, post-reset, or explicit `Release` intention.</td>
      <td>Actuators de-energized. Normal force \(F_n = 0.0\text{ N}\). Actuator displacement \(d = 0.0\text{ mm}\).</td>
      <td>Transition to <i>ANALYZING</i> upon reception of sEMG burst signal.</td>
    </tr>
    <tr>
      <td><b>2. ANALYZING</b></td>
      <td>Arrival of sEMG window packet at `/predict`.</td>
      <td>Validate signal length \(N \ge 10\); compute 12D features; evaluate Random Forest; measure CPU latency.</td>
      <td>Transition to <i>CLOSING</i> if grasp class recognized; return to <i>IDLE</i> if `Open Hand` or `Release`.</td>
    </tr>
    <tr>
      <td><b>3. CLOSING</b></td>
      <td>Grip class identified as `Power Grip` or `Pinch Grip`.</td>
      <td>Advance digital flexor servos at constant travel velocity (\(+3.5\text{ mm/cycle}\)). Normal force remains nominal.</td>
      <td>Transition to <i>CONTACT_DETECTED</i> when distal FSR reads \(F_n \ge 5.0\text{ N}\).</td>
    </tr>
    <tr>
      <td><b>4. CONTACT_DETECTED</b></td>
      <td>Distal FSR sensor threshold \(F_c \ge 5.0\text{ N}\) crossed.</td>
      <td>Zero actuator travel velocity; halt pre-contact motion; initialize closed-loop force tracking loop.</td>
      <td>Transition to <i>PRESSURE_REGULATING</i> on next control iteration.</td>
    </tr>
    <tr>
      <td><b>5. PRESSURE_REGULATING</b></td>
      <td>Active contact established; target force setpoint \(F_{target} = 50.0\text{ N}\).</td>
      <td>Compute error \(e(t) = F_{target} - F(t)\). Apply proportional force increment (\(+1.5\text{ N/cycle}\)).</td>
      <td>Transition to <i>STABLE_HOLD</i> when \(|e(t)| \le 3.0\text{ N}\); transition to <i>CRUSH_ABORT</i> if \(F &gt; 75\text{ N}\).</td>
    </tr>
    <tr>
      <td><b>6. STABLE_HOLD</b></td>
      <td>Grip force enters deadband window \([47.0, 53.0]\text{ N}\).</td>
      <td>Maintain actuator pulse-width modulation; suppress motor hunting; monitor shear slip sensor at 50 Hz.</td>
      <td>Transition to <i>SLIP_RECOVERY</i> if `slip_detected = True`; transition to <i>RELEASING</i> on `Release` command.</td>
    </tr>
    <tr>
      <td><b>7. SLIP_RECOVERY</b></td>
      <td>Shear displacement detected during active hold.</td>
      <td>Autonomous reflex bypass: apply instantaneous +18% force boost (+12.0 N) to arrest payload slip.</td>
      <td>Transition to <i>STABLE_HOLD</i> once shear velocity stabilizes; transition to <i>CRUSH_ABORT</i> if \(F \ge 75\text{ N}\).</td>
    </tr>
    <tr>
      <td><b>8. CRUSH_ABORT</b></td>
      <td>Distal FSR force exceeds critical ceiling \(F_{max} = 75.0\text{ N}\).</td>
      <td>Emergency safety clamp: freeze actuator duty cycle; clamp force command to \(75.0\text{ N}\); flash warning telemetry.</td>
      <td>Transition to <i>IDLE</i> only via explicit clinician reset or `Release` intention command.</td>
    </tr>
  </tbody>
</table>

<h3>4.2.4 System Data Dictionary &amp; Telemetry Packet Formats</h3>
<p>Table 4.3 outlines the core parameters, types, engineering units, and valid domains defined across the software pipeline.</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 20%;">Variable Name</th>
      <th style="width: 15%;">Data Type</th>
      <th style="width: 15%;">Physical Units</th>
      <th style="width: 20%;">Valid Operating Range</th>
      <th style="width: 30%;">Functional Description &amp; Safety Boundary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>ch1_signal</code></td>
      <td>List[float]</td>
      <td>Millivolts (mV)</td>
      <td>\([-2.5, +2.5]\text{ mV}\)</td>
      <td>Raw discrete sEMG waveform from Flexor Digitorum Superficialis. Window length \(N = 200\).</td>
    </tr>
    <tr>
      <td><code>ch2_signal</code></td>
      <td>List[float]</td>
      <td>Millivolts (mV)</td>
      <td>\([-2.5, +2.5]\text{ mV}\)</td>
      <td>Raw discrete sEMG waveform from Extensor Digitorum Communis. Window length \(N = 200\).</td>
    </tr>
    <tr>
      <td><code>baseline_noise</code></td>
      <td>float</td>
      <td>Volts (V)</td>
      <td>\([0.005, 0.20]\text{ V}\)</td>
      <td>Resting physiological noise standard deviation configured during calibration. Default: 0.05 V.</td>
    </tr>
    <tr>
      <td><code>grip_class</code></td>
      <td>int / string</td>
      <td>Enumeration</td>
      <td>0 (Open), 1 (Power), 2 (Pinch), 3 (Release)</td>
      <td>Target user intent decoded by Random Forest ensemble.</td>
    </tr>
    <tr>
      <td><code>current_force</code></td>
      <td>float</td>
      <td>Newtons (N)</td>
      <td>\([0.0, 75.0]\text{ N}\)</td>
      <td>Measured distal normal contact force. Capped at 75.0 N by anti-crush ceiling.</td>
    </tr>
    <tr>
      <td><code>slip_detected</code></td>
      <td>boolean</td>
      <td>Boolean Flag</td>
      <td><code>True</code>, <code>False</code></td>
      <td>Indicates dynamic shear displacement of payload across the fingertip elastomer.</td>
    </tr>
    <tr>
      <td><code>inference_latency_ms</code></td>
      <td>float</td>
      <td>Milliseconds (ms)</td>
      <td>\([0.5, 10.0]\text{ ms}\)</td>
      <td>Real measured execution duration of the feature extraction and Random Forest inference on host CPU.</td>
    </tr>
  </tbody>
</table>

<h2>4.3 Algorithmic Formulation &amp; Module-Wise Implementation</h2>

<h3>4.3.1 Algorithm 1: Time-Domain Statistical Feature Extraction with Division-by-Zero Guarding</h3>
<p>To ensure real-time performance on resource-constrained embedded microcontrollers, the feature extraction pipeline calculates six time-domain statistical metrics per channel, plus two inter-channel interaction features, yielding a compact 12-dimensional feature vector. The mathematical formulations are defined as follows:</p>

<p>Given a discrete signal window \(x[n]\) of length \(N\) for channel \(c \in \{1, 2\}\):</p>

<ol>
  <li><b>Root Mean Square (RMS):</b> Quantifies the continuous electrical power of the myoelectric contraction:
    $$\text{RMS} = \sqrt{\frac{1}{N} \sum_{n=1}^{N} x[n]^2}$$
  </li>
  <li><b>Mean Absolute Value (MAV):</b> Measures the average contraction magnitude across the observation window:
    $$\text{MAV} = \frac{1}{N} \sum_{n=1}^{N} |x[n]|$$
  </li>
  <li><b>Variance (VAR):</b> Captures the second central moment of signal power dispersion:
    $$\text{VAR} = \frac{1}{N - 1} \sum_{n=1}^{N} (x[n] - \mu)^2, \quad \text{where } \mu = \frac{1}{N}\sum_{n=1}^{N} x[n]$$
    <i>Guard Condition:</i> If \(N \le 1\), \(\text{VAR} = 0.0\) to prevent floating-point division by zero.
  </li>
  <li><b>Simple Square Integral (SSI):</b> Represents the total cumulative energy contained within the contraction window:
    $$\text{SSI} = \sum_{n=1}^{N} x[n]^2$$
  </li>
  <li><b>Zero-Crossing Rate (ZCR):</b> Quantifies dominant frequency content in the time domain without requiring an FFT:
    $$\text{ZCR} = \frac{1}{N - 1} \sum_{n=1}^{N-1} \mathbb{I}\left( \text{sgn}(x[n]) \ne \text{sgn}(x[n+1]) \land |x[n] - x[n+1]| \ge \epsilon \right)$$
    where \(\mathbb{I}(\cdot)\) is the indicator function, \(\text{sgn}(\cdot)\) is the signum function, and \(\epsilon = 0.01\text{ V}\) is a noise deadband to suppress low-amplitude baseline crossings.
    <i>Critical Edge Guard:</i> For signal buffers where \(N &lt; 2\), the denominator \((N - 1) \le 0\). The algorithm explicitly returns \(\text{ZCR} = 0.0\) when \(N &lt; 2\), permanently eliminating the ZeroDivisionError identified during the initial code audit.
  </li>
  <li><b>Inter-Channel Interaction Metrics:</b> Captures co-activation ratios between antagonistic muscle groups:
    $$\text{Ratio} = \frac{\text{RMS}_1 + \delta}{\text{RMS}_2 + \delta}, \quad \text{where } \delta = 10^{-6}\text{ to avoid division by zero}$$
    $$\text{Difference} = |\text{RMS}_1 - \text{RMS}_2|$$
  </li>
</ol>

<p>The complete pseudocode for the robust feature extraction routine is presented in Algorithm 4.1.</p>

<div class="code-block-box">
  <div class="code-title">Algorithm 4.1: Edge-Compatible Time-Domain Feature Extraction</div>
  <pre>
INPUT:  ch1: Array[float], ch2: Array[float], noise_deadband: float = 0.01, eps: float = 1e-6
OUTPUT: feature_vector: Array[float] of length 12

1:  FUNCTION extract_time_domain_features(ch1, ch2):
2:      N1 &lt;- LENGTH(ch1)
3:      N2 &lt;- LENGTH(ch2)
4:      ASSERT N1 == N2 AND N1 &gt;= 10, "Signal buffer must be equal length and &gt;= 10 samples"
5:      
6:      features &lt;- EMPTY_LIST()
7:      FOR EACH channel IN [ch1, ch2]:
8:          N &lt;- LENGTH(channel)
9:          
10:         // 1. Root Mean Square (RMS) &amp; Simple Square Integral (SSI)
11:         sum_sq &lt;- SUM(x^2 FOR x IN channel)
12:         rms &lt;- SQRT(sum_sq / N)
13:         ssi &lt;- sum_sq
14:         
15:         // 2. Mean Absolute Value (MAV)
16:         mav &lt;- SUM(ABS(x) FOR x IN channel) / N
17:         
18:         // 3. Variance (VAR) with N &lt;= 1 guard
19:         IF N &lt;= 1 THEN
20:             var &lt;- 0.0
21:         ELSE
22:             mean &lt;- SUM(x FOR x IN channel) / N
23:             var &lt;- SUM((x - mean)^2 FOR x IN channel) / (N - 1)
24:         END IF
25:         
26:         // 4. Zero-Crossing Rate (ZCR) with N &lt; 2 guard
27:         IF N &lt; 2 THEN
28:             zcr &lt;- 0.0
29:         ELSE
30:             crossings &lt;- 0
31:             FOR i FROM 0 TO N - 2:
32:                 IF (channel[i] * channel[i+1] &lt; 0) AND (ABS(channel[i] - channel[i+1]) &gt;= noise_deadband) THEN
33:                     crossings &lt;- crossings + 1
34:                 END IF
35:             END FOR
36:             zcr &lt;- crossings / (N - 1)
37:         END IF
38:         
39:         APPEND [rms, mav, var, ssi, zcr] TO features
40:     END FOR
41:     
42:     // Inter-channel antagonistic interaction metrics
43:     rms_ch1 &lt;- features[0]
44:     rms_ch2 &lt;- features[5]
45:     ratio &lt;- (rms_ch1 + eps) / (rms_ch2 + eps)
46:     diff &lt;- ABS(rms_ch1 - rms_ch2)
47:     
48:     APPEND [ratio, diff] TO features
49:     RETURN features  // Length 12
50: END FUNCTION
  </pre>
</div>

<h3>4.3.2 Algorithm 2: Edge-Optimized Random Forest Classifier &amp; Host Latency Profiling</h3>
<p>The classification tier utilizes a Random Forest ensemble comprising \(B = 35\) decorrelated decision trees, constrained to a maximum tree depth \(D_{max} = 7\). This structural constraint guarantees bounded inference time and a compact memory footprint suitable for future embedded deployment on microcontrollers with 512 KB SRAM.</p>

<p>For an input feature vector \(\mathbf{x} \in \mathbb{R}^{12}\), each individual decision tree \(T_b(\mathbf{x})\) outputs a class probability distribution over the four grip classes \(C \in \{0, 1, 2, 3\}\). The final ensemble decision is determined by soft voting:</p>

$$\hat{y} = \arg\max_{c \in C} \frac{1}{B} \sum_{b=1}^{B} P_b(y = c \mid \mathbf{x})$$

<p>The confidence score is the maximum ensemble probability \(\max_{c} P(c \mid \mathbf{x})\). To guarantee verifiable performance telemetry, host CPU inference latency is measured dynamically for every prediction using high-resolution monotonic timers (`time.perf_counter_ns()`), executing 50 warmed-up trials on the host machine to report mean latency in milliseconds.</p>

<div class="code-block-box">
  <div class="code-title">Algorithm 4.2: Intention Classification &amp; Microsecond Latency Profiling</div>
  <pre>
INPUT:  ch1: Array[float], ch2: Array[float], rf_model: TrainedRandomForest
OUTPUT: dict: {grip_class: str, confidence: float, latency_ms: float}

1:  FUNCTION predict_user_intent(ch1, ch2, rf_model):
2:      features &lt;- extract_time_domain_features(ch1, ch2)
3:      feature_matrix &lt;- RESHAPE(features, [1, 12])
4:      
5:      // Host CPU latency benchmarking with microsecond precision
6:      t_start &lt;- TIME_PERF_COUNTER_NS()
7:      probabilities &lt;- rf_model.predict_proba(feature_matrix)[0]
8:      predicted_idx &lt;- ARGMAX(probabilities)
9:      t_end &lt;- TIME_PERF_COUNTER_NS()
10:     
11:     latency_ms &lt;- (t_end - t_start) / 1,000,000.0
12:     confidence &lt;- probabilities[predicted_idx]
13:     class_labels &lt;- ["Open Hand", "Power Grip", "Pinch Grip", "Release"]
14:     
15:     RETURN {
16:         "grip_class": class_labels[predicted_idx],
17:         "confidence": ROUND(confidence, 4),
18:         "inference_latency_ms": ROUND(latency_ms, 3)
19:     }
20: END FUNCTION
  </pre>
</div>

<h3>4.3.3 Algorithm 3: Closed-Loop Adaptive Grip Force Controller</h3>
<p>The closed-loop force regulation engine simulates tactile interaction between the prosthetic digits and a physical payload. The controller implements proportional force regulation, deadband hysteresis, shear slip compensation, and anti-crush safety limits, as defined in Algorithm 4.3.</p>

<div class="code-block-box">
  <div class="code-title">Algorithm 4.3: Closed-Loop Adaptive Grip Force Controller with Deadband Hysteresis &amp; Slip Reflex</div>
  <pre>
INPUT:  current_state: ControllerState, target_grip: str, slip_detected: bool
CONSTANTS:
    F_contact = 5.0 N       // Contact threshold
    F_target  = 50.0 N      // Target hold setpoint
    F_max     = 75.0 N      // Anti-crush safety ceiling
    Delta_db  = 3.0 N       // Deadband hysteresis width
    k_p       = 1.5 N       // Proportional force increment per cycle
    k_slip    = 0.18        // +18% autonomous reflex boost
OUTPUT: updated_state: ControllerState

1:  FUNCTION step_grip_controller(state, target_grip, slip_detected):
2:      // Handle Release intention
3:      IF target_grip IN ["Open Hand", "Release"] THEN
4:          state.current_force &lt;- 0.0
5:          state.actuator_travel &lt;- MAX(0.0, state.actuator_travel - 5.0)
6:          state.status &lt;- "IDLE"
7:          state.slip_counter &lt;- 0
8:          RETURN state
9:      END IF
10:     
11:     // Phase 1: Free travel closing until contact
12:     IF state.current_force &lt; F_contact THEN
13:         state.actuator_travel &lt;- state.actuator_travel + 3.5
14:         state.current_force &lt;- state.current_force + 1.2
15:         state.status &lt;- "CLOSING"
16:         IF state.current_force &gt;= F_contact THEN
17:             state.status &lt;- "CONTACT_DETECTED"
18:         END IF
19:         RETURN state
20:     END IF
21:     
22:     // Phase 2: Active tactile interaction
23:     IF slip_detected THEN
24:         // Autonomous anti-slip reflex: +18% force boost
25:         boost &lt;- state.current_force * k_slip + 12.0
26:         state.current_force &lt;- state.current_force + boost
27:         state.slip_counter &lt;- state.slip_counter + 1
28:         state.status &lt;- "SLIP_RECOVERY"
29:     ELSE
30:         // Proportional tracking toward F_target
31:         error &lt;- F_target - state.current_force
32:         IF ABS(error) &lt;= Delta_db THEN
33:             // Within deadband hysteresis: hold steady
34:             state.status &lt;- "STABLE_HOLD"
35:         ELSE IF error &gt; Delta_db THEN
36:             // Below deadband: increase force
37:             state.current_force &lt;- state.current_force + k_p
38:             state.status &lt;- "PRESSURE_REGULATING"
39:         ELSE
40:             // Above deadband: decrease force
41:             state.current_force &lt;- state.current_force - k_p
42:             state.status &lt;- "DECREASING"
43:         END IF
44:     END IF
45:     
46:     // Phase 3: Enforce hard anti-crush safety ceiling
47:     IF state.current_force &gt;= F_max THEN
48:         state.current_force &lt;- F_max
49:         state.status &lt;- "CRUSH_ABORT"
50:     END IF
51:     
52:     RETURN state
53: END FUNCTION
  </pre>
</div>

<h3>4.3.4 Algorithm 4: Calibrated Synthetic sEMG Signal Generator</h3>
<p>The synthetic sEMG engine generates deterministic, physiologically modeled waveforms matching human forearm activation profiles for each grip class, incorporating the user-configured baseline noise parameter \(\sigma_{base}\), as formalized in Algorithm 4.4.</p>

<div class="code-block-box">
  <div class="code-title">Algorithm 4.4: Calibrated Synthetic sEMG Signal Generator with Recruitment Envelopes</div>
  <pre>
INPUT:  grip_class: int (0..3), baseline_noise: float in [0.005, 0.20], N: int = 200
OUTPUT: (ch1_signal: Array[float], ch2_signal: Array[float])

1:  FUNCTION generate_synthetic_semg(grip_class, baseline_noise, N):
2:      time_steps &lt;- [i / 1000.0 FOR i FROM 0 TO N - 1]  // 1000 Hz time base
3:      
4:      // Set class-specific physiological activation profiles
5:      SWITCH grip_class:
6:          CASE 0 ("Open Hand"):
7:              // Low flexor (FDS), strong extensor (EDC) burst
8:              (amp1, amp2) &lt;- (0.15, 1.80)
9:              (freq1, freq2) &lt;- (35.0, 75.0)
10:         CASE 1 ("Power Grip"):
11:             // Dominant flexor (FDS), moderate extensor co-activation
12:             (amp1, amp2) &lt;- (2.20, 0.85)
13:             (freq1, freq2) &lt;- (65.0, 45.0)
14:         CASE 2 ("Pinch Grip"):
15:             // Focused moderate flexor, balanced extensor
16:             (amp1, amp2) &lt;- (1.20, 1.10)
17:             (freq1, freq2) &lt;- (85.0, 80.0)
18:         CASE 3 ("Release"):
19:             // Rapid extensor transient, fading flexor
20:             (amp1, amp2) &lt;- (0.10, 0.40)
21:             (freq1, freq2) &lt;- (25.0, 30.0)
22:     
23:     ch1 &lt;- EMPTY_ARRAY(N)
24:     ch2 &lt;- EMPTY_ARRAY(N)
25:     
26:     FOR i FROM 0 TO N - 1:
27:         t &lt;- time_steps[i]
28:         // Gaussian baseline noise scaled by calibrated baseline_noise parameter
29:         noise1 &lt;- GAUSSIAN_RANDOM(mean=0.0, std=baseline_noise)
30:         noise2 &lt;- GAUSSIAN_RANDOM(mean=0.0, std=baseline_noise)
31:         
32:         // Physiological recruitment envelope: sinusoidal carrier modulated by Gaussian burst
33:         envelope &lt;- EXP(-((t - 0.10)^2) / (2 * 0.04^2))
34:         
35:         ch1[i] &lt;- (amp1 * envelope * SIN(2 * PI * freq1 * t)) + noise1
36:         ch2[i] &lt;- (amp2 * envelope * SIN(2 * PI * freq2 * t)) + noise2
37:     END FOR
38:     
39:     RETURN (ch1, ch2)
40: END FUNCTION
  </pre>
</div>

<h2>4.4 RESTful API Service Specification &amp; Communications Protocol</h2>
<p>The backend application is implemented using the FastAPI asynchronous framework, exposing seven typed REST endpoints. Table 4.4 details the formal endpoint catalog, HTTP methods, Pydantic request/response schemas, and validation status codes.</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 12%;">Endpoint</th>
      <th style="width: 8%;">Method</th>
      <th style="width: 25%;">Request Body Schema</th>
      <th style="width: 25%;">Response Body Schema</th>
      <th style="width: 15%;">Status Codes</th>
      <th style="width: 15%;">Validation Boundary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>/predict</code></td>
      <td>POST</td>
      <td><code>PredictRequest</code>:<br>{ch1: float[], ch2: float[]}</td>
      <td><code>PredictResponse</code>:<br>{grip_class: str, confidence: float, latency_ms: float}</td>
      <td>200 OK<br>422 Unprocessable</td>
      <td>Validates equal length, \(N \ge 10\), non-empty arrays, numeric types.</td>
    </tr>
    <tr>
      <td><code>/emg/generate</code></td>
      <td>POST</td>
      <td><code>EMGGenerateRequest</code>:<br>{grip_class: int, noise: float}</td>
      <td><code>EMGGenerateResponse</code>:<br>{ch1: float[], ch2: float[], grip_name: str}</td>
      <td>200 OK<br>422 Unprocessable</td>
      <td>Grip class must be in \([0, 3]\); noise must be in \([0.005, 0.20]\).</td>
    </tr>
    <tr>
      <td><code>/control/step</code></td>
      <td>POST</td>
      <td><code>ControlStepRequest</code>:<br>{state: str, slip: bool}</td>
      <td><code>ControlStepResponse</code>:<br>{force: float, status: str, travel: float}</td>
      <td>200 OK<br>422 Unprocessable</td>
      <td>Enforces valid state string; enforces anti-crush ceiling (\(\le 75\text{ N}\)).</td>
    </tr>
    <tr>
      <td><code>/control/reset</code></td>
      <td>POST</td>
      <td>Empty JSON: {}</td>
      <td><code>ResetResponse</code>:<br>{force: 0.0, status: "IDLE", travel: 0.0}</td>
      <td>200 OK</td>
      <td>Deterministic state reset; clears slip counters and active travel.</td>
    </tr>
    <tr>
      <td><code>/calibration</code></td>
      <td>POST</td>
      <td><code>CalibrationRequest</code>:<br>{baseline_noise: float}</td>
      <td><code>CalibrationResponse</code>:<br>{baseline_noise: float, status: str}</td>
      <td>200 OK<br>422 Unprocessable</td>
      <td>Noise bounded to \([0.005, 0.20]\text{ V}\); updates runtime generator state.</td>
    </tr>
    <tr>
      <td><code>/health</code></td>
      <td>GET</td>
      <td>None</td>
      <td><code>HealthResponse</code>:<br>{status: "healthy", model_loaded: bool}</td>
      <td>200 OK</td>
      <td>Verifies model file presence and memory allocation health.</td>
    </tr>
  </tbody>
</table>

<h3>4.4.1 Strict Pydantic Data Contracts &amp; Error Prevention</h3>
<p>A critical vulnerability identified during the repository audit was the risk of unhandled exceptions returning HTTP 500 Internal Server Errors when client requests supplied malformed payloads (such as mismatched channel lengths, empty arrays, or non-numeric values). In compliance with Priority 1 audit mandates, all endpoints now enforce Pydantic field validators with comprehensive custom validation logic, returning standardized HTTP 422 Unprocessable Entity responses with detailed error descriptions.</p>

<h3>4.4.2 Cross-Origin Resource Sharing (CORS) Configuration</h3>
<p>To support secure local development and production hosting across heterogeneous frontend ports, the FastAPI backend implements CORS middleware configured with explicit origin whitelisting:</p>
<pre style="background: #f1f5f9; padding: 10px; border-radius: 4px; font-size: 9.5pt; font-family: monospace;">
origins = [
    "http://localhost:5173",  # Vite development server
    "http://127.0.0.1:5173",  # Loopback IP
    "http://localhost:3000",  # Alternate development port
    "http://127.0.0.1:3000",
    "http://localhost:4173",  # Vite preview port
    "http://127.0.0.1:4173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
</pre>

<h2>4.5 Full-Stack Implementation &amp; Interactive Virtual Dashboard</h2>
<p>The interactive presentation layer provides an intuitive visual interface for clinical monitoring and technical demonstration, built using React 19, TypeScript, and Tailwind CSS.</p>

<h3>4.5.1 Frontend Architecture &amp; Component Hierarchy</h3>
<p>The frontend application is structured into modular components: `App.tsx` acts as the root coordinator; `EMGOscilloscope.tsx` manages real-time canvas rendering of the two sEMG channels; `HandVisualization.tsx` renders an articulated 3D kinematic model of the prosthetic hand; `GripControls.tsx` provides manual and automated grasp selection; `TactileMonitor.tsx` displays normal force, target deadbands, and slip indicators; and `MetricsPanel.tsx` displays host inference latency, accuracy, and system state telemetry.</p>

<h3>4.5.2 Responsive High-DPI Real-Time Oscilloscope</h3>
<p>To resolve canvas blurriness on Retina and high-DPI displays (identified during the audit), the `EMGOscilloscope` component implements dynamic device pixel ratio (DPR) auto-scaling:</p>
<pre style="background: #f1f5f9; padding: 10px; border-radius: 4px; font-size: 9.5pt; font-family: monospace;">
const dpr = window.devicePixelRatio || 1;
canvas.width = rect.width * dpr;
canvas.height = rect.height * dpr;
ctx.scale(dpr, dpr);
</pre>

<h3>4.5.3 27-Second Automated Demonstration Sequence</h3>
<p>The dashboard incorporates an automated continuous demonstration sequence that executes a pre-programmed 27-second clinical testing script across five distinct phases: Baseline Idle Calibration (0–4s), Power Grip Closure &amp; Contact Detection (4–11s), Shear Slip Disturbance &amp; Autonomous Reflex Boost (11–18s), Pinch Grip Precision Grasp (18–23s), and Coordinated Release &amp; Reset (23–27s). Every stage automatically advances, triggers backend API endpoints, and updates the live UI.</p>

<h3>4.5.4 Project Directory Structure &amp; Deployment Scripts</h3>
<p>The complete software repository structure is organized as follows:</p>
<pre style="background: #f1f5f9; padding: 12px; border-radius: 4px; font-size: 9pt; font-family: monospace;">
Edge AI Smart Prosthetic Hand/
|-- backend/
|   |-- main.py              # FastAPI server, endpoints, CORS middleware
|   |-- ml_model.py          # Feature extraction, Random Forest training &amp; inference
|   |-- grip_controller.py   # Closed-loop force regulation, deadband, anti-slip reflex
|   |-- emg_simulator.py     # Deterministic sEMG waveform synthesis &amp; calibration
|   |-- test_pipeline.py     # 27-test automated pytest regression test suite
|   |-- trained_model.joblib # Serialized scikit-learn Random Forest model
|-- frontend/
|   |-- src/
|   |   |-- App.tsx          # Root dashboard component &amp; automated demo controller
|   |   |-- components/      # EMGOscilloscope, HandVisualizer, TactileMonitor, Metrics
|   |-- package.json         # React 19, TypeScript, Vite build configuration
|-- submission/reports/      # Documentation sprint deliverables (.docx, .pdf, .xlsx)
|-- RUN_PROTOTYPE.bat        # One-click dual-stack startup batch script
|-- README.md                # Project overview, architecture, and verification guide
</pre>
"""
