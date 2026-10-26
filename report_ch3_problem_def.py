"""
Chapter 3: Problem Definition and Objectives Module for the 80+ Page Final Project Report.
Exhaustive mathematical formulation, 11 quantifiable objectives, 18 FRs, 14 NFRs, specifications, and feasibility.
"""

def get_chapter3_html():
    return """
<div class="page-break"></div>

<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title">CHAPTER 3: PROBLEM DEFINITION AND OBJECTIVES</h1>

<h2 class="section-title">3.1 Problem Statement & Mathematical Formulation</h2>
<p>Modern commercial myoelectric prostheses suffer from an acute technological trade-off: they either employ primitive, open-loop threshold controls that lack grip variety and sensory feedback, or rely on computationally massive deep neural networks that cannot operate deterministically on embedded, battery-powered bionic hardware. When amputees attempt to grasp everyday objects, the absence of closed-loop tactile force regulation frequently results in destructive object crushing or accidental dropping, while requiring exhausting, continuous visual concentration.</p>

<p>The central engineering challenge addressed in this project is therefore to formulate, implement, and digitally validate a low-latency, edge-compatible machine learning classification pipeline coupled with an autonomous closed-loop tactile force regulation controller that operates within a deterministic sub-10 millisecond processing budget.</p>

<p>Mathematically, the system is modeled as a dual-stage discrete bio-mechatronic pipeline operating over discrete time index <code>t</code>:</p>

<p><b>1. Feedforward Intention Classification Formulation:</b><br>
Let <code>s_1(t)</code> and <code>s_2(t)</code> denote continuous biopotential voltage signals acquired from the flexor (Flexor Digitorum Superficialis) and extensor (Extensor Digitorum Communis) muscle compartments. The analog signals are digitized by an analog-to-digital converter (ADC) at sampling frequency <code>f_s = 1000 Hz</code> over an analysis window <code>W_k = {t_i}_{i=1}^N</code> of duration <code>T_w = 200 ms</code> (sample count <code>N = f_s * T_w = 200 samples</code>). A deterministic feature transformation <code>Phi: R^{200 x 2} -> R^{12}</code> extracts 12 time-domain statistical parameters:</p>
<pre class="code-block">
x_k = [ RMS_1, MAV_1, VAR_1, SSI_1, ZCR_1, 
        RMS_2, MAV_2, VAR_2, SSI_2, ZCR_2, 
        Ratio(ch1, ch2), Diff(ch1, ch2) ]^T
</pre>
<p>Where the mathematical descriptors for channel <code>c in {1, 2}</code> are defined as:</p>
<pre class="code-block">
MAV_c = (1 / N) * sum_{i=1}^N |s_c(t_i)|
RMS_c = sqrt( (1 / N) * sum_{i=1}^N (s_c(t_i))^2 )
VAR_c = (1 / (N - 1)) * sum_{i=1}^N (s_c(t_i) - mu_c)^2
SSI_c = sum_{i=1}^N (s_c(t_i))^2
ZCR_c = (1 / (N - 1)) * sum_{i=1}^{N-1} I( (s_c(t_i) * s_c(t_{i+1}) < 0)  AND  (|s_c(t_i) - s_c(t_{i+1})| > theta) )
Ratio = (MAV_1 + epsilon) / (MAV_2 + epsilon),   Diff = MAV_1 - MAV_2
</pre>
<p>Here, <code>theta = 0.015 V</code> denotes the zero-crossing noise rejection deadband, and <code>epsilon = 10^{-4}</code> prevents division by zero. The classification hypothesis <code>h_theta(x)</code> maps feature vector <code>x_k</code> to discrete grip class <code>y_pred in Y = {OPEN, POWER_GRIP, PINCH_GRIP, RELEASE}</code> by maximizing posterior class probability:</p>
<pre class="code-block">
y_pred = argmax_{c in Y} P(y = c | x_k; theta)
</pre>

<p><b>2. Feedback Tactile Force Regulation Formulation:</b><br>
Let <code>P(t)</code> represent the instantaneous simulated contact pressure (in Newtons) measured by the distal FSR sensors, and <code>P_target(y)</code> represent the target grip pressure setpoint (0.0 N for OPEN/RELEASE, 50.0 N for POWER_GRIP, 25.0 N for PINCH_GRIP). The tracking error is:</p>
<pre class="code-block">
e(t) = P_target(y_pred) - P(t)
</pre>
<p>The closed-loop controller updates motor effort <code>u(t) in [0, 100]%</code> subject to non-linear safety bounds:</p>
<pre class="code-block">
If P(t) > MAX_SAFE_PRESSURE (75.0 N):
    action = 'DECREASING',  u(t+1) = max(10.0, u(t) - 10.0)
Else If |e(t)| <= DEADBAND (3.0 N):
    action = 'MAINTAINING', u(t+1) = u(t)
Else If e(t) > 0:
    action = 'INCREASING',  u(t+1) = min(100.0, u(t) + K_p * e(t))
Else:
    action = 'DECREASING',  u(t+1) = max(5.0, u(t) - K_p * |e(t)|)
</pre>
<p>If a shear slip disturbance <code>S(t) = True</code> is injected, the controller overrides normal regulation:</p>
<pre class="code-block">
u(t+1) = min(100.0, u(t) + 18.0),  action = 'SLIP_COMPENSATION'
</pre>

<h2 class="section-title">3.2 Quantifiable Project Objectives</h2>
<p>The engineering goals of this project are organized into eleven quantifiable, testable objectives:</p>
<ul>
  <li><b>Objective 1: Develop a Physiological Synthetic sEMG Generator:</b> Implement a dual-channel sEMG simulation engine generating 200 ms windows at 1000 Hz, with band-limited colored noise (30–350 Hz) and distinct recruitment envelopes for OPEN, POWER_GRIP, PINCH_GRIP, and RELEASE.
  <br><i>Evaluation Criteria:</i> Output must consist of two float arrays of exactly 200 samples each, with verified amplitude scaling across classes.</li>

  <li><b>Objective 2: Implement a Safe 12-Dimensional Time-Domain Feature Extraction Engine:</b> Formulate mathematical extraction routines for RMS, MAV, Variance, Energy, ZCR, and channel interaction ratio with full division-by-zero protection.
  <br><i>Evaluation Criteria:</i> Functions must return finite real numbers without throwing exceptions or returning NaN on boundary arrays of length 0 or 1.</li>

  <li><b>Objective 3: Train and Optimize an Edge-Deployable Machine Learning Classifier:</b> Train a lightweight Random Forest model (35 estimators, max depth 7) achieving high classification accuracy on the synthetic feature dataset.
  <br><i>Evaluation Criteria:</i> Model must achieve >= 95% 5-fold cross-validation accuracy and Macro-F1 >= 0.95 on synthetic validation data.</li>

  <li><b>Objective 4: Implement a Closed-Loop Adaptive Grip Force Controller:</b> Develop an 8-state finite state machine regulating simulated actuator effort based on FSR contact thresholding (5.0 N) and setpoint targets (50 N for Power, 25 N for Pinch).
  <br><i>Evaluation Criteria:</i> Controller must enter MAINTAINING state within a ± 3.0 N deadband of target setpoints.</li>

  <li><b>Objective 5: Engineer an Anti-Crush Safety Ceiling Mechanism:</b> Prevent actuator over-torquing on rigid objects by enforcing a hard 75.0 N pressure ceiling.
  <br><i>Evaluation Criteria:</i> When pressure exceeds 75.0 N, controller must immediately transition to DECREASING mode and back off motor effort.</li>

  <li><b>Objective 6: Develop an Autonomous Anti-Slip Compensatory Reflex:</b> Implement an instant response loop reacting to software-injected shear slip disturbances.
  <br><i>Evaluation Criteria:</i> Slip trigger must immediately boost actuator effort by +18% and restore grasp stability without user intervention.</li>

  <li><b>Objective 7: Implement a Resting Noise Baseline Calibration Module:</b> Enable user-specific calibration measuring resting biopotential noise floors and MVC gains.
  <br><i>Evaluation Criteria:</i> Baseline noise parameter must scale synthetic signal noise standard deviation proportionally.</li>

  <li><b>Objective 8: Measure and Report Real Host Inference Latency:</b> Profile pipeline execution using monotonic high-resolution timers (`time.perf_counter()`), removing hardcoded claims.
  <br><i>Evaluation Criteria:</i> Return measured execution times in API responses and document host workstation environment.</li>

  <li><b>Objective 9: Build an Interactive Web Telemetry Dashboard:</b> Construct a responsive React 19 / Vite dashboard featuring 3D virtual hand articulation, responsive High-DPI waveform canvas, and live telemetry indicators.
  <br><i>Evaluation Criteria:</i> Dashboard must compile cleanly (`npm run build`) without TypeScript errors and adapt to container resizing.</li>

  <li><b>Objective 10: Automate an End-to-End 27-Second Demonstration Sequence:</b> Implement an automated staged demonstration advancing smoothly every second without dead intervals.
  <br><i>Evaluation Criteria:</i> Demonstration must step on every second tick and populate event log telemetry from real API response objects.</li>

  <li><b>Objective 11: Construct an Automated Regression Test Suite:</b> Build a comprehensive pytest suite covering boundary conditions, input validation, and controller dynamics.
  <br><i>Evaluation Criteria:</i> All test cases must pass deterministically (target: 27/27 passed).</li>
</ul>

<h2 class="section-title">3.3 Requirements Analysis</h2>
<h3 class="subsection-title">3.3.1 Functional Requirements (FR-1 through FR-18)</h3>
<p>Functional requirements specify the operational behaviors and algorithmic expectations of the system:</p>
<ul>
  <li><b>FR-1 (Synthetic Signal Generation):</b> The system must synthesize 200 ms, 200-sample voltage windows at 1000 Hz representing flexor and extensor channels across four discrete grip states (OPEN, POWER_GRIP, PINCH_GRIP, RELEASE).</li>
  <li><b>FR-2 (Time-Domain Feature Extraction):</b> The system must extract 12 statistical descriptors (RMS, MAV, VAR, SSI, ZCR for each channel, plus Channel Interaction Ratio and Difference) with noise deadband thresholding (0.015 V).</li>
  <li><b>FR-3 (Input Validation & HTTP 422):</b> The system must validate that incoming channel sample lists are non-empty, of equal length, contain at least 20 samples, and consist solely of finite real numbers (no NaN or Infinity), returning HTTP 422 for invalid requests.</li>
  <li><b>FR-4 (Intention Classification):</b> The system must evaluate feature vectors through a trained Random Forest model and return the predicted grip class alongside calibrated class probabilities summing to 100%.</li>
  <li><b>FR-5 (Monotonic Latency Measurement):</b> The system must measure single-call inference latency and multi-trial benchmark latency using `time.perf_counter()` and return live values in milliseconds.</li>
  <li><b>FR-6 (Contact Detection Thresholding):</b> The controller must detect initial physical contact whenever simulated pressure exceeds 5.0 N or explicit contact override is asserted.</li>
  <li><b>FR-7 (Proportional Force Regulation):</b> The controller must regulate motor effort toward target pressure setpoints (50 N for Power Grip, 25 N for Pinch Grip) with a ± 3.0 N hysteresis deadband.</li>
  <li><b>FR-8 (Anti-Crush Safety Ceiling):</b> The controller must enforce DECREASING mode whenever measured pressure exceeds 75.0 N, reducing motor effort by -10% per cycle until safe pressure is restored.</li>
  <li><b>FR-9 (Autonomous Slip Recovery Reflex):</b> The controller must detect software-injected slip disturbance triggers and immediately apply a +18% motor torque boost (+12 N force) to arrest payload movement.</li>
  <li><b>FR-10 (User Baseline Calibration):</b> The system must store individualized resting noise floor voltages (0.035–0.055 V) and MVC gain multipliers, scaling synthetic signal baseline noise variance proportionally.</li>
  <li><b>FR-11 (Automated 27-Second Demonstration):</b> The system must execute a scheduled 27-second demonstration advancing through resting baseline, power grasp, contact engagement, force ramping, stable holding, slip disturbance, anti-slip recovery, and voluntary release.</li>
  <li><b>FR-12 (Dynamic Event Logging):</b> Event log entries during manual and automated modes must be constructed from actual API response fields (`confidence_percent`, `current_pressure_n`, `stability_index`) rather than hardcoded strings.</li>
  <li><b>FR-13 (Virtual Hand Kinematic Rendering):</b> The frontend must articulate a high-contrast SVG virtual hand displaying proportional joint flexion angles (0° to 90°) and tactile contact indicator dots.</li>
  <li><b>FR-14 (Responsive Waveform Canvas):</b> The sEMG waveform canvas must utilize a `ResizeObserver` to adapt its High-DPI resolution dynamically to container width changes without visual blur.</li>
  <li><b>FR-15 (Controller State Ribbon):</b> The UI must render an 8-stage state progression ribbon (IDLE, CONTACT, INCREASING, DECREASING, MAINTAINING, SLIP DETECTED, ANTI-SLIP, STABILIZED) highlighting active states.</li>
  <li><b>FR-16 (Deterministic Reset):</b> The system must provide a POST `/reset` endpoint restoring the controller to IDLE, 0 N pressure, 0% effort, and cleared disturbance flags.</li>
  <li><b>FR-17 (RESTful OpenAPI Contract):</b> The backend must expose an OpenAPI JSON schema with strict Pydantic request and response models.</li>
  <li><b>FR-18 (Automated Test Execution):</b> The system must execute a pytest test suite validating feature extraction, validation status codes, controller safety bounds, and calibration impact.</li>
</ul>

<h3 class="subsection-title">3.3.2 Non-Functional Requirements (NFR-1 through NFR-14)</h3>
<ul>
  <li><b>NFR-1 (Real-Time Temporal Budget):</b> Total feature extraction and inference latency must execute in under 10.0 ms per window on the host environment, leaving ample headroom within the 100 ms interaction ceiling.</li>
  <li><b>NFR-2 (Robustness & Numerical Immunity):</b> The system must be fully protected against division-by-zero, negative square roots, and non-finite NaN/Infinity propagation across all boundary inputs.</li>
  <li><b>NFR-3 (Resource Efficiency):</b> Memory utilization must remain below 100 MB RAM on the host environment, and the model weight footprint must not exceed 250 kB to maintain edge portability.</li>
  <li><b>NFR-4 (C/C++ Edge Portability):</b> The Random Forest classifier and feature extraction logic must be directly exportable to static C arrays for microcontroller compilation without external runtime dependencies.</li>
  <li><b>NFR-5 (Architectural Modularity):</b> The codebase must maintain strict modular separation between signal generation, feature extraction, ML inference, closed-loop control, and frontend visualization.</li>
  <li><b>NFR-6 (Responsive High-DPI UI):</b> The web dashboard must maintain a clean, dark technical aesthetic with High-DPI canvas scaling and responsive layouts across desktop and tablet viewports.</li>
  <li><b>NFR-7 (Experimental Reproducibility):</b> Random seeds (seed=42), training configurations, and test cases must be fully documented to permit exact reproduction across independent runs.</li>
  <li><b>NFR-8 (CORS Security Compliance):</b> REST endpoints must explicitly restrict origins to local development servers (`http://localhost:5173`, `http://127.0.0.1:5173`) rather than using insecure wildcard origins with credentials.</li>
  <li><b>NFR-9 (Fail-Safe Anti-Crush Priority):</b> In the controller logic, the anti-crush safety ceiling (P > 75 N) must supersede setpoint ramping at all times to prevent damage to grasped payloads.</li>
  <li><b>NFR-10 (Scientific Metric Integrity):</b> Evaluation metrics must distinguish between 5-fold cross-validation and holdout testing, and explicitly report synthetic dataset constraints.</li>
  <li><b>NFR-11 (Async Concurrency Protection):</b> The demonstration sequence must utilize an `inFlight` execution lock to prevent overlapping asynchronous requests from corrupting controller state.</li>
  <li><b>NFR-12 (Code Maintainability):</b> The codebase must adhere to strict PEP 8 Python formatting and TypeScript strict typing with descriptive docstrings.</li>
  <li><b>NFR-13 (Academic Honesty):</b> All user-facing interfaces and reports must explicitly state that sensor values are simulated and that hardware integration represents a future phase.</li>
  <li><b>NFR-14 (Clean Build Verification):</b> The production frontend build (`npm run build`) must compile cleanly with zero TypeScript errors or unresolved module warnings.</li>
</ul>

<h2 class="section-title">3.4 Hardware, Software & Environmental Specifications</h2>
<p>Table 3.1 details the physical hardware subsystem targeted for upcoming embedded deployment. Table 3.2 specifies the development, scientific computing, and simulation software stack utilized for this software prototype.</p>

<table class="data-table">
  <tr><th>Target Hardware Subsystem</th><th>Specification & Operational Rationale</th></tr>
  <tr><td><b>Microcontroller Unit (MCU)</b></td><td>ESP32-S3 Dual-Core Xtensa LX7 @ 240 MHz, 512 kB SRAM, 8 MB Flash, Vector AI instructions.</td></tr>
  <tr><td><b>sEMG Analog Front-End</b></td><td>MyoWare 2.0 / AD8232 instrumentation amplifier, active bandpass filter (20–450 Hz), 12-bit ADC.</td></tr>
  <tr><td><b>Tactile Pressure Sensors</b></td><td>FSR 402 piezoresistive pressure sensors mounted on distal thumb and fingertips (0.1 N to 100 N range).</td></tr>
  <tr><td><b>Actuation Subsystem</b></td><td>5x TowerPro SG90 / MG996R metal-gear micro servomotors (11 kg-cm torque) driving tendon cables.</td></tr>
  <tr><td><b>Power Delivery</b></td><td>7.4V 2S 2200 mAh Li-Po battery with high-efficiency buck converters (5V 4A servo rail, 3.3V MCU rail).</td></tr>
  <tr><td><b>Mechanical Chassis</b></td><td>Open-source 3D printed anthropomorphic prosthetic hand (Brunel / InMoov design) in carbon PETG.</td></tr>
</table>
<div class="table-caption">Table 3.1: Target embedded hardware specifications for upcoming ESP32-S3 deployment.</div>

<table class="data-table">
  <tr><th>Software Component</th><th>Development & Runtime Configuration</th></tr>
  <tr><td><b>Operating System</b></td><td>Microsoft Windows 11 Pro 64-bit (Host AMD64 Workstation)</td></tr>
  <tr><td><b>Backend Framework</b></td><td>Python 3.12.1, FastAPI 0.157.0, Starlette 1.9.0, Uvicorn 0.28.0 (ASGI Server)</td></tr>
  <tr><td><b>Machine Learning & Math</b></td><td>Scikit-Learn 1.7.0, NumPy 2.2.3, Pandas 2.2.3, SciPy 1.16.0</td></tr>
  <tr><td><b>Data Validation Engine</b></td><td>Pydantic 2.13.4 with custom model and field validators</td></tr>
  <tr><td><b>Automated Test Framework</b></td><td>Pytest 8.2.2 with pytest-mock and FastAPI TestClient</td></tr>
  <tr><td><b>Frontend Dashboard</b></td><td>React 19.0.0, TypeScript 5.7.2, Vite 8.3.0, Tailwind CSS 3.4.17</td></tr>
  <tr><td><b>Code Repository & CI</b></td><td>Git 2.44, GitHub Remote (https://github.com/Unceas/EdgeAi)</td></tr>
</table>
<div class="table-caption">Table 3.2: Host development, machine learning, and simulation runtime specifications.</div>

<h2 class="section-title">3.5 System Feasibility Analysis</h2>
<p>A rigorous feasibility assessment confirms the viability of the project across technical, operational, and economic dimensions:</p>
<ul>
  <li><b>Technical Feasibility:</b> All signal processing algorithms and Random Forest classification utilize proven, standardized mathematical routines. Running the simulation locally via FastAPI and Vite eliminates network latency and distributed failure modes. All 27 automated regression tests pass deterministically.</li>
  <li><b>Operational Feasibility:</b> The prototype provides an intuitive browser dashboard requiring zero specialized software installation beyond standard Python and Node.js. A single batch script (<code>RUN_PROTOTYPE.bat</code>) launches the complete stack in one click.</li>
  <li><b>Economic Feasibility:</b> The software simulation prototype incurred zero component costs. The target embedded hardware bill of materials (BOM) is estimated under $65 USD, presenting an accessible alternative to commercial prostheses costing over $10,000 USD.</li>
</ul>

<table class="data-table">
  <tr><th>Identified Risk Factor</th><th>Potential Failure Mode</th><th>Implemented Engineering Mitigation</th></tr>
  <tr><td><b>Floating-point division by zero</b></td><td>ZCR calculation crashes on N=0 or N=1 inputs.</td><td>Explicit boundary checks returning 0.0 with <code>np.nan_to_num()</code> sanitization.</td></tr>
  <tr><td><b>Input signal corruption</b></td><td>Mismatched channel lengths or NaN samples trigger 500 crashes.</td><td>Pydantic model validator returning descriptive HTTP 422 responses.</td></tr>
  <tr><td><b>Overpressure crushing</b></td><td>Actuators ramp indefinitely during stiff object grasp.</td><td>Hard anti-crush ceiling (75 N) immediately triggering DECREASING mode.</td></tr>
  <tr><td><b>CORS security violation</b></td><td>Wildcard origins fail in credentialed browser requests.</td><td>Configured explicit local origin whitelist matching Vite development ports.</td></tr>
  <tr><td><b>Async race conditions</b></td><td>Overlapping interval requests freeze the 27s demo sequence.</td><td>Implemented <code>inFlight</code> execution lock ensuring sequential pipeline stepping.</td></tr>
</table>
<div class="table-caption">Table 3.3: Technical, operational, and environmental risk mitigation matrix.</div>
"""
