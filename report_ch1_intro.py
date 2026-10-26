"""
Chapter 1: Introduction Module for the 80+ Page Final Project Report.
"""

def get_chapter1_html():
    return """
<div class="page-break"></div>

<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title">CHAPTER 1: INTRODUCTION</h1>

<h2 class="section-title">1.1 Technical Background & Domain Overview</h2>
<p>The human hand is an extraordinarily complex, multifunctional biomechatronic organ that integrates 27 individual bones, over 30 intrinsic and extrinsic muscle groups, and an intricate network of specialized tactile mechanoreceptors. Through this sophisticated anatomical framework, the biological hand seamlessly transitions between power grasping (e.g., carrying luggage or gripping a hammer) and fine precision pinch manipulation (e.g., threading a needle, holding a key, or handling delicate glassware). Traumatic amputation, oncological resection, or congenital upper-limb deficiency results in severe functional, occupational, and psychological impairment. Epidemiological studies estimate that several million individuals globally live with major upper-limb amputations, with transradial (below-elbow) amputations representing the most prevalent cohort of productive-age amputees.</p>

<p>For decades, biomedical rehabilitation engineering has pursued the development of externally powered myoelectric prostheses to restore functional manipulation to amputees. The operational foundation of myoelectric control is rooted in <b>Surface Electromyography (sEMG)</b>. When a transradial amputee attempts to execute a phantom hand movement—such as forming a fist or pinching their fingers—the central nervous system transmits efferent motor commands from the motor cortex through descending spinal pathways into residual peripheral nerve endings. These motor neuron impulses induce depolarization waves across the sarcolemma of surviving muscle fibers within the residual forearm stump, specifically recruiting the <i>Flexor Digitorum Superficialis (FDS)</i>, <i>Flexor Carpi Radialis (FCR)</i>, <i>Extensor Digitorum Communis (EDC)</i>, and <i>Extensor Carpi Ulnaris (ECU)</i>. The spatial and temporal superposition of these individual Motor Unit Action Potential (MUAP) trains creates a stochastically interfering biopotential signal measurable on the skin surface using non-invasive biopotential electrodes. Because residual muscle groups preserve functional topographic organization corresponding to original anatomical movements, sEMG signals provide a non-invasive, rich biological control channel for active robotic limbs.</p>

<p>Despite significant mechanical advancements in multi-articulated bionic hands over the past twenty years—exemplified by commercially available multi-degree-of-freedom prostheses such as the Ottobock Michelangelo, Touch Bionics i-Limb, and Steeper Bebionic—clinical utilization remains severely constrained by primitive control paradigms. Commercial prostheses almost universally employ <b>open-loop, dual-site amplitude threshold control</b>. In this conventional architecture, two bipolar electrode pairs monitor the flexor and extensor compartments. When the rectified signal amplitude exceeds an empirical threshold, an electric servomotor closes or opens all digits simultaneously at a fixed velocity. The prosthesis possesses zero sensory awareness of the physical environment: it cannot perceive when contact is made, cannot measure applied grasping pressure, and cannot detect when a grasped object begins to slip.</p>

<p>Consequently, the entire burden of grasp regulation falls onto the human user through <b>visual feedback alone</b>. To manipulate an object without crushing it or dropping it, the amputee must maintain uninterrupted, intense visual concentration on their artificial hand. If their gaze wanders for even a second, an object may be inadvertently crushed due to excessive actuator torque, or slip and fall due to inadequate retention force. This continuous visual vigilance imposes an overwhelming cognitive workload, inducing mental fatigue, user frustration, and social anxiety. Extensive clinical surveys indicate that between 30% and 50% of upper-limb amputees permanently abandon their myoelectric devices, often reverting to passive cosmetic hands or crude body-powered cable hooks that offer physical kinesthetic feedback.</p>

<p>In response to this clinical crisis, modern biomechatronics is undergoing a paradigm shift driven by the convergence of <b>Edge Artificial Intelligence (Edge AI)</b> and <b>closed-loop tactile feedback</b>. Edge AI refers to the deployment of lightweight, high-performance machine learning models directly onto resource-constrained microcontrollers embedded within the prosthetic chassis. Unlike traditional systems that offload computations to cloud servers or tethered smartphones—introducing latency jitter (50–300 ms), privacy risks, and connection vulnerabilities—Edge AI executes deterministic intent recognition locally in under 2 milliseconds. Simultaneously, integrating piezoresistive Force Sensitive Resistors (FSRs) at the artificial fingertips provides real-time tactile awareness. An autonomous adaptive grip controller can detect touch, ramp grasping pressure to a safe setpoint, enforce strict anti-crush safety ceilings, and execute reflexive grip tightening within milliseconds if shear slippage occurs, effectively relieving the amputee of constant visual micro-management.</p>

<h2 class="section-title">1.2 Motivation & Engineering Need</h2>
<p>The motivation for this engineering clinics project stems from a pronounced and critical gap between academic machine learning research and practical prosthetic utility. In academic literature, researchers routinely report offline gesture recognition accuracies exceeding 95% using high-capacity deep learning models, including 2D Convolutional Neural Networks (CNNs), Recurrent Neural Networks (RNNs), and Vision Transformers. However, these complex deep architectures typically require multi-megabyte parameter storage, billions of floating-point operations (FLOPs), and high-power graphical processing units (GPUs). They cannot be executed on the ultra-low-power, battery-operated microcontrollers that must reside inside an amputee's prosthetic socket without rapidly exhausting battery reserves and generating uncomfortable thermal dissipation.</p>

<p>Furthermore, the vast majority of published studies treat intention recognition as an isolated, open-loop classification task. Once a gesture class is predicted, the engineering pipeline terminates, leaving the physical challenge of grasping compliance, force modulation, and slip recovery completely unaddressed. Real-world manipulation is inherently interactive and dynamic: grasping a fragile ceramic mug requires completely different force regulation and slip monitoring than handling a heavy metallic bottle.</p>

<p>The specific engineering needs driving this project are categorized into four critical dimensions:</p>
<ol>
  <li><b>Alleviation of Cognitive Burden via Autonomous Grasping:</b> Establishing an autonomous closed-loop tactile reflex relieves the amputee from micro-managing motor force through visual feedback, restoring natural and intuitive hand usage during daily tasks.</li>
  <li><b>Deterministic Sub-10 Millisecond Edge Latency:</b> Neurophysiological studies demonstrate that sensory-motor control loops require total end-to-end latency below 100–125 ms to feel responsive and avoid perceived sluggishness. Within a standard 200 ms biological decision window, machine learning feature extraction and inference must execute in under 10 ms to leave adequate time for mechanical servo actuation.</li>
  <li><b>Fail-Safe Grasping Regulation & Anti-Crush Intervention:</b> Daily payloads exhibit wide variations in mechanical compliance. An autonomous grip controller must incorporate hard safety thresholds—such as an anti-crush ceiling (75 N) and deadband hysteresis (3 N)—to prevent destructive motor over-torquing while ensuring robust payload retention.</li>
  <li><b>Methodological Rigor Prior to Hardware Prototyping:</b> Directly fabricating multi-finger mechanical prostheses and analog biopotential circuits without verifying control stability leads to hardware failures, actuator burnout, and difficult debugging. Developing a comprehensive, deterministic software simulation platform allows algorithmic edge cases (such as zero-crossing division errors, sensor noise scaling, and race conditions) to be systematically resolved beforehand.</li>
</ol>

<h2 class="section-title">1.3 Project Scope & System Boundaries</h2>
<h3 class="subsection-title">1.3.1 In-Scope Deliverables</h3>
<p>The scope of this Semester VII Engineering Clinics project encompasses the complete architectural design, mathematical modeling, edge machine learning optimization, closed-loop adaptive control implementation, and empirical verification of a digital simulation prototype. The concrete in-scope deliverables include:</p>
<ul>
  <li><b>Synthetic 2-Channel sEMG Signal Generator:</b> Mathematical modeling of 1000 Hz, 200 ms biopotential windows representing flexor (FDS) and extensor (EDC) muscle recruitment across four discrete functional intentions: <i>OPEN</i>, <i>POWER_GRIP</i>, <i>PINCH_GRIP</i>, and <i>RELEASE</i>, utilizing band-limited Gaussian colored noise (30–350 Hz dominant band) and physiological decay envelopes.</li>
  <li><b>Edge-Optimized Feature Extraction Engine:</b> Robust computation of 12 time-domain statistical descriptors per window (Root Mean Square, Mean Absolute Value, Variance, Signal Energy, and Zero-Crossing Rate per channel, alongside inter-channel Interaction Ratio and Difference) with full protection against division-by-zero for empty (N=0) and single-sample (N=1) inputs.</li>
  <li><b>Machine Learning Intention Classifier:</b> Training, optimization, and validation of an edge-deployable Random Forest ensemble (35 estimators, maximum tree depth 7) benchmarked for 5-fold stratified cross-validation, holdout accuracy, Macro-F1, and host CPU execution latency.</li>
  <li><b>Adaptive Closed-Loop Grip Controller:</b> State-machine regulation of simulated actuator effort based on simulated FSR tactile feedback across discrete operational states (IDLE, CLOSING, CONTACT, INCREASING, DECREASING, MAINTAINING, SLIP_COMPENSATION, RELEASING) with strict safety boundaries (75 N ceiling, 3 N deadband).</li>
  <li><b>Simulated Disturbance Injection & Slip Reflex:</b> Software-injected micro-slip disturbance triggers that engage an autonomous compensatory reflex loop (+18% motor torque boost) to arrest payload movement.</li>
  <li><b>Resting Baseline Calibration Module:</b> A user calibration routine measuring resting noise floors and individual Maximum Voluntary Contraction (MVC) gains, dynamically scaling synthetic signal baselines.</li>
  <li><b>Interactive Web Dashboard:</b> A high-contrast, dark monochrome user interface built with React 19, TypeScript, and Vite, featuring 3D virtual hand articulation, responsive High-DPI waveform canvas, and an automated 27-second continuous demonstration sequence.</li>
  <li><b>Automated Regression Test Suite:</b> A comprehensive 27-case automated pytest suite validating signal dimensions, input validation (HTTP 422), controller dynamics, and deterministic reset behavior.</li>
</ul>

<h3 class="subsection-title">1.3.2 Out-of-Scope Limitations & Assumptions</h3>
<p>To uphold scientific integrity and prevent misleading representations, the boundaries of this prototype are explicitly defined:</p>
<ul>
  <li><b>No Physical Hardware Connected:</b> Physical surface electrodes, analog instrumentation amplifiers (AD8232/MyoWare), 3D-printed carbon chassis, and physical servomotors are not included in this phase. Sensor values and tactile pressures are digitally simulated.</li>
  <li><b>Synthetic Dataset Evaluation:</b> Reported classification accuracy and F1-scores represent evaluation on mathematically generated Gaussian process signals. They do not constitute human clinical trial results.</li>
  <li><b>Host CPU Telemetry:</b> Latency measurements are obtained on host workstation hardware using Python monotonic timers. They do not represent physical ESP32-S3 execution times.</li>
  <li><b>Simulated Disturbance:</b> The slip event is a software-triggered state disturbance within the control algorithm, not a physical shear sensor reading.</li>
</ul>

<h2 class="section-title">1.4 Proposed System Overview & High-Level Methodology</h2>
<p>The proposed Edge AI Smart Prosthetic Hand operates along a coordinated five-stage pipeline connecting biological intent to physical grasping:</p>
<pre class="code-block">
Synthetic EMG Input (1000 Hz, 2-Ch)
       |
       v
Time-Domain Feature Extraction (12-Dim Vector)
       |
       v
Edge ML Intention Classification (Random Forest: 35 Trees, Depth 7)
       |
       v
Virtual Prosthetic Hand Actuation (Joint Kinematics & Touch Detection)
       |
       v
Simulated Force / Tactile Feedback (FSR Pressure & Slip Monitoring)
       |
       v
Adaptive Closed-Loop Grip Controller (Deadband Hysteresis & Anti-Crush Ceiling)
       |
       v
Autonomous Grip Adjustment (+18% Anti-Slip Reflex & Safe Equilibrium)
</pre>
<div class="figure-caption">Figure 1.1: End-to-end functional pipeline of the Edge AI Smart Prosthetic Hand simulation.</div>

<p>In Stage 1, the sEMG simulator generates 200 ms windows (200 samples) of dual-channel biopotential data reflecting muscle activation. In Stage 2, the feature engine transforms these raw samples into a 12-dimensional vector. In Stage 3, the Random Forest model performs inference, outputting the predicted grip state and confidence probabilities. In Stage 4, the virtual hand articulates inward until simulated FSR contact occurs (> 5 N). In Stage 5, the closed-loop controller continuously monitors pressure: if pressure is below setpoint, it ramps force; if pressure reaches setpoint within deadband, it holds; if pressure exceeds 75 N, it decreases force; and if a slip disturbance is injected, it triggers an instant +18% torque boost to stabilize the payload.</p>

<h2 class="section-title">1.5 Chapter Roadmap</h2>
<p>This report is organized into six technical chapters following the institutional guidelines of Chandigarh Engineering College Jhanjeri:</p>
<ul>
  <li><b>Chapter 1: Introduction</b> — Formulates the clinical and engineering background, motivation, scope, limitations, and architectural overview.</li>
  <li><b>Chapter 2: Review of Literature</b> — Provides a comprehensive 35-reference literature synthesis tracing myoelectric history, feature engineering, edge AI classifiers, tactile sensing, and research gaps.</li>
  <li><b>Chapter 3: Problem Definition and Objectives</b> — Establishes the mathematical formulation, quantifiable engineering objectives, functional and non-functional requirements, hardware/software specifications, and feasibility risk analysis.</li>
  <li><b>Chapter 4: Design and Implementation</b> — Details the 4-layer architecture, DFD Levels 0/1/2, UML models, REST API contract, and complete algorithmic pseudocode for all four core modules.</li>
  <li><b>Chapter 5: Results and Discussions</b> — Reports empirical metrics on the synthetic dataset, the full 27-test pytest execution log, host latency benchmarks, controller disturbance stress testing, and comparative analyses.</li>
  <li><b>Chapter 6: Conclusion and Future Scope</b> — Summarizes project achievements, novel contributions, operational constraints, and the 5-phase embedded hardware deployment roadmap.</li>
  <li><b>References & Appendices</b> — Provides complete IEEE references, publications division annexure, setup manual, API specifications, and source code listings.</li>
</ul>
"""
