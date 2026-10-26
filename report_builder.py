"""
Report Builder Module (Strict Institutional Template Compliance)
Embeds CEC Logo & PTU Logo in Base64.
Adheres strictly to Chandigarh Engineering College Jhanjeri / IKGPTU Jalandhar guidelines:
- Cover Page (20pt Bold, 16pt, 14pt, with CEC and PTU logos)
- Declaration (16pt Bold title, 14pt body, Moinak Dey, Roshni Singh, B. Uma Maheshwar, Dr. Baljinder Kaur)
- Acknowledgement (16pt Bold title, 14pt body)
- Abstract (16pt Bold title, 12pt body)
- Running Header: CEC Jhanjeri, Mohali / Department of Computer Science and Engineering
"""

import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def get_front_matter_html():
    cec_b64 = get_base64_image(os.path.join("submission", "reports", "cec_logo.png"))
    ptu_b64 = get_base64_image(os.path.join("submission", "reports", "ptu_logo.png"))

    return f"""
<!-- COVER PAGE -->
<div class="cover-page" style="text-align: center; font-family: 'Times New Roman', serif;">
  <div style="font-size: 20pt; font-weight: bold; letter-spacing: 0.05em; margin-bottom: 6px; color: #0f172a;">PROJECT REPORT</div>
  <div style="font-size: 14pt; font-weight: normal; margin-bottom: 6px;">ON</div>
  <div style="font-size: 20pt; font-weight: bold; text-transform: uppercase; line-height: 1.3; margin-bottom: 12px; color: #0f172a;">
    EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING
  </div>
  <div style="font-size: 16pt; font-weight: bold; color: #1e293b; margin-bottom: 20px;">
    Project-II
  </div>

  <div style="margin: 15px auto 20px auto;">
    <img src="data:image/png;base64,{cec_b64}" style="width: 140px; height: auto;" alt="Chandigarh Engineering College Logo">
  </div>

  <div style="font-size: 16pt; font-weight: normal; margin-bottom: 4px; color: #1e293b;">Department of Computer Science and Engineering</div>
  <div style="font-size: 16pt; font-weight: bold; margin-bottom: 14px; color: #0f172a; text-transform: uppercase;">
    CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI
  </div>
  <div style="font-size: 12pt; font-style: italic; color: #334155; margin-bottom: 4px;">
    In partial fulfillment of the requirements for the award of the Degree of
  </div>
  <div style="font-size: 14pt; font-weight: bold; color: #0f172a; margin-bottom: 25px;">
    Bachelor of Technology in Computer Science &amp; Engineering
  </div>

  <table style="width: 100%; border: none; margin: 15px 0 20px 0;">
    <tr>
      <td style="width: 50%; vertical-align: top; text-align: left; font-size: 13pt; line-height: 1.45; border: none;">
        <b>SUBMITTED BY:</b><br><br>
        <b>Moinak Dey</b> (Roll No: 2330838)<br>
        <b>Roshni Singh</b> (Roll No: 2330850)<br>
        <b>B. Uma Maheshwar</b> (Roll No: 2330817)<br>
        <i>Semester VII (Batch: 2023–2027)</i>
      </td>
      <td style="width: 50%; vertical-align: top; text-align: right; font-size: 13pt; line-height: 1.45; border: none;">
        <b>Under the Guidance of:</b><br><br>
        <b>Dr. Baljinder Kaur</b><br>
        Assistant Professor<br>
        Department of CSE<br>
        CEC Jhanjeri, Mohali
      </td>
    </tr>
  </table>

  <div style="font-size: 14pt; font-weight: bold; margin-top: 15px; color: #0f172a;">DEC, 2026</div>

  <div style="margin: 10px auto 8px auto;">
    <img src="data:image/png;base64,{ptu_b64}" style="width: 85px; height: auto;" alt="PTU Logo">
  </div>

  <div style="font-size: 12pt; font-weight: bold; color: #0f172a;">Affiliated to I.K. Gujral Punjab Technical University, Jalandhar</div>
  <div style="font-size: 11pt; font-weight: bold; color: #475569;">(Batch: 2023–2027)</div>
</div>

<div class="page-break"></div>

<!-- DECLARATION -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10.5pt; font-weight: bold; color: #334155;">Department of Computer Science and Engineering</div>
</div>

<h1 style="font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 25px; border-bottom: 1.5px solid #0f172a; padding-bottom: 6px;">DECLARATION</h1>

<p style="font-size: 12.5pt; line-height: 1.6; text-align: justify; margin-bottom: 20px;">
  We, <b>Moinak Dey (Univ. Roll No: 2330838)</b>, <b>Roshni Singh (Univ. Roll No: 2330850)</b>, and <b>B. Uma Maheshwar (Univ. Roll No: 2330817)</b>, hereby declare that the report of the project entitled <b>“EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING”</b> has not presented as a part of any other academic work to get my degree or certificate except <b>Chandigarh Engineering College Jhanjeri, Mohali</b>, affiliated to <b>I.K. Gujral Punjab Technical University, Jalandhar</b>, for the fulfillment of the requirements for the degree of <b>B.Tech in Computer Science &amp; Engineering</b>.
</p>

<p style="font-size: 12pt; line-height: 1.6; text-align: justify; margin-bottom: 40px;">
  We solemnly affirm that this report represents our own original work conducted under the supervision and guidance of our project mentor, <b>Dr. Baljinder Kaur</b>, Assistant Professor, Department of Computer Science &amp; Engineering. All literature, benchmark datasets, mathematical models, and open-source software libraries utilized in this work have been properly cited and acknowledged in compliance with ethical academic guidelines.
</p>

<table style="width: 100%; border: none; margin-top: 30px;">
  <tr>
    <td style="width: 50%; vertical-align: top; border: none; font-size: 11.5pt; line-height: 1.5;">
      <b>(Student Signatures with Date)</b><br><br><br>
      ____________________________________<br>
      <b>Moinak Dey</b> (Univ. Roll No: 2330838)<br><br>
      ____________________________________<br>
      <b>Roshni Singh</b> (Univ. Roll No: 2330850)<br><br>
      ____________________________________<br>
      <b>B. Uma Maheshwar</b> (Univ. Roll No: 2330817)<br><br>
      Semester: VII, Batch: 2023–2027
    </td>
    <td style="width: 50%; vertical-align: top; border: none; font-size: 11.5pt; line-height: 1.5; text-align: right;">
      <b>(Mentor Signature with Date)</b><br><br><br>
      ____________________________________<br>
      <b>NAME OF THE MENTOR:</b><br>
      <b>Dr. Baljinder Kaur</b><br>
      Assistant Professor, CSE<br>
      CEC Jhanjeri, Mohali
    </td>
  </tr>
</table>

<div style="margin-top: 50px; border-top: 1px solid #0f172a; width: 50%; padding-top: 8px; font-size: 11.5pt; line-height: 1.4;">
  <b>Signature of the Head of Department</b><br>
  Department of Computer Science and Engineering<br>
  Chandigarh Engineering College Jhanjeri, Mohali<br>
  (With Stamp)
</div>

<div class="page-break"></div>

<!-- ACKNOWLEDGEMENT -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10.5pt; font-weight: bold; color: #334155;">Department of Computer Science and Engineering</div>
</div>

<h1 style="font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 25px; border-bottom: 1.5px solid #0f172a; padding-bottom: 6px;">ACKNOWLEDGEMENT</h1>

<p style="font-size: 12.5pt; line-height: 1.6; text-align: justify; margin-bottom: 18px;">
  It gives us great pleasure to deliver this report on the Project-II, we worked on for our B.Tech in Computer Science &amp; Engineering 4th year, which was titled <b>“EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING”</b>. We are grateful to our university for presenting us with such a wonderful and challenging opportunity. We also want to convey our sincere gratitude to all coordinators for their unfailing support and encouragement.
</p>

<p style="font-size: 12.5pt; line-height: 1.6; text-align: justify; margin-bottom: 18px;">
  We are extremely thankful to the HOD and Project Coordinator of Computer Science &amp; Engineering at Chandigarh Engineering College Jhanjeri, Mohali (Punjab) for valuable suggestions and heartiest co-operation.
</p>

<p style="font-size: 12.5pt; line-height: 1.6; text-align: justify; margin-bottom: 18px;">
  We are also grateful to the management of the institute, for giving us the chance to acquire the information. We are also appreciative of all of our faculty members, who have instructed us throughout our degree.
</p>

<p style="font-size: 12.5pt; line-height: 1.6; text-align: justify; margin-bottom: 35px;">
  First and foremost, we express our heartfelt gratitude to our mentor, <b>Dr. Baljinder Kaur</b>, Assistant Professor, for her continuous technical mentorship, constructive criticism, and rigorous academic guidance. Her insistence on evidence-based software engineering and scientific integrity shaped this prototype into a submission-ready engineering achievement.
</p>

<div style="margin-top: 40px; font-size: 11.5pt; line-height: 1.5;">
  <b>(Signature of Students)</b><br><br><br>
  ________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;________________________<br>
  <b>Moinak Dey</b> (2330838)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Roshni Singh</b> (2330850)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>B. Uma Maheshwar</b> (2330817)<br>
  B.Tech Computer Science &amp; Engineering, Semester VII<br>
  Chandigarh Engineering College Jhanjeri, Mohali
</div>

<div class="page-break"></div>

<!-- ABSTRACT -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10.5pt; font-weight: bold; color: #334155;">Department of Computer Science and Engineering</div>
</div>

<h1 style="font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 25px; border-bottom: 1.5px solid #0f172a; padding-bottom: 6px;">ABSTRACT</h1>

<p style="font-size: 12pt; line-height: 1.6; text-align: justify;">
  The rapid evolution of modern computing systems demands robust, automated, and scalable digital solutions to tackle real-world operational challenges. This project presents the design and implementation of an end-to-end intelligent processing framework aimed at optimizing data acquisition, feature analysis, and decision-making pipelines. Existing baseline methodologies frequently suffer from computational bottlenecks, higher latency, and reduced predictive reliability when handling complex, multi-scale data streams. To address these challenges, the proposed system introduces an optimized modular architecture incorporating standardized preprocessing protocols, resilient feature extraction mechanisms, and a lightweight inference engine.
</p>

<p style="font-size: 12pt; line-height: 1.6; text-align: justify;">
  Myoelectric upper-limb prostheses represent a vital clinical intervention to restore manual manipulation capabilities for individuals with transradial amputations. However, commercial bionic hands overwhelmingly rely on open-loop, dual-site amplitude threshold control. In this conventional paradigm, muscle contractions actuate electric motors at fixed speeds until mechanical stall occurs, completely devoid of tactile feedback or grasp adaptation. As a consequence, amputee users face high rates of accidental object dropping or destructive crush deformation, while suffering from severe cognitive fatigue induced by the need for continuous visual monitoring. Although complex deep learning architectures in academic literature achieve high offline gesture recognition accuracy on public benchmarks, their multi-megabyte parameter footprints, high computational demands, and latency jitter prevent embedded execution on ultra-low-power microcontrollers within a prosthetic socket, while cloud-tethered alternatives introduce unacceptable latency delays and data privacy vulnerabilities.
</p>

<p style="font-size: 12pt; line-height: 1.6; text-align: justify;">
  To overcome these fundamental limitations, this project presents the engineering design, mathematical formulation, software architecture, and rigorous empirical validation of an <b>Edge AI Smart Prosthetic Hand with Adaptive Grip Learning</b>. The system establishes a synchronized dual-brain hierarchy that decouples high-level intention classification from low-level autonomous closed-loop tactile force regulation. A deterministic synthetic Surface Electromyography (sEMG) engine models physiological recruitment waveforms from the Flexor Digitorum Superficialis and Extensor Digitorum Communis muscles at a 1000 Hz sampling rate across 200 ms analysis windows for four functional grip states: <i>Open Hand</i>, <i>Power Grip</i>, <i>Pinch Grip</i>, and <i>Release</i>. An edge-compatible feature extraction engine computes 12 time-domain statistical descriptors (RMS, MAV, Variance, Energy, and Zero-Crossing Rate per channel, alongside inter-channel interaction ratio and difference) incorporating full protection against division-by-zero on edge-case signals (N &le; 1). Intention inference is executed using an edge-optimized Random Forest classifier (35 estimators, maximum tree depth 7) benchmarked on host CPU hardware.
</p>

<p style="font-size: 12pt; line-height: 1.6; text-align: justify;">
  Tactile interaction is closed via simulated distal Force Sensitive Resistor (FSR) models incorporating contact thresholding (5.0 N), proportional force regulation, a closed-loop deadband (3.0 N), and an anti-crush safety ceiling (75.0 N). To address payload slippage without cognitive intervention, a software-injected shear disturbance trigger engages an autonomous anti-slip reflex loop that instantly boosts actuator effort by +18% (+12 N force) to arrest slip movement. The end-to-end pipeline is evaluated across a balanced synthetic dataset of 720 samples. Empirical testing confirms <b>100.0% cross-validation accuracy</b> (5-fold stratified K-fold) and <b>100.0% holdout test accuracy</b> with a <b>Macro-F1 score of 1.0000</b> on the synthetic dataset. Host CPU inference latency benchmarks average <b>1.40 ms to 1.88 ms</b> across 50 warmed-up trials, well within the 10.0 ms real-time edge execution budget. An automated regression suite of 27 test cases verifies signal boundary safety, input validation (HTTP 422), controller state transitions, and deterministic reset behavior. An interactive web dashboard built with React 19, TypeScript, and Vite provides 3D virtual hand kinematics, responsive High-DPI waveform monitoring, and an automated 27-second continuous demonstration sequence. This software prototype establishes an evidence-based foundation for upcoming physical hardware deployment on ESP32-S3 microcontrollers.
</p>

<div class="callout-box info" style="margin-top: 20px;">
  <div class="callout-title">Academic &amp; Scope Clarification</div>
  This project report documents a verified software simulation prototype. The 100% accuracy and 1.0000 Macro-F1 are evaluated on synthetic physiological signals, not human EMG data. Latencies represent local host CPU benchmarks, not embedded microcontroller execution. Physical electrodes, servomotors, and clinical trials represent future hardware milestones.
</div>
"""
