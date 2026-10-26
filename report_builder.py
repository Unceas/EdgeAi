"""
Full Report Builder Module
Contains exhaustive, academic-grade text, tables, formulas, algorithms,
and figures for the 80+ page Final Project Report.
"""

import os
import sys

def get_front_matter_html():
    return """
<!-- COVER PAGE -->
<div class="univ-header">
  <div style="font-size: 15pt; font-weight: 900; letter-spacing: 0.05em; color: #0f172a;">CHANDIGARH ENGINEERING COLLEGE JHANJERI</div>
  <div style="font-size: 11pt; font-weight: 700; color: #334155; margin-top: 2px;">MOHALI - 140307, PUNJAB, INDIA</div>
  <div style="font-size: 11.5pt; font-weight: 800; color: #0f172a; margin-top: 4px; text-transform: uppercase;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<div class="cover-box">
  <div style="font-size: 16pt; font-weight: 900; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; color: #0f172a;">
    PROJECT REPORT
  </div>
  <div style="font-size: 12pt; font-weight: 700; margin-bottom: 8px;">ON</div>
  <div style="font-size: 21pt; font-weight: 900; text-transform: uppercase; color: #0f172a; line-height: 1.35; margin-bottom: 14px; letter-spacing: 0.02em;">
    EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING
  </div>
  <div style="font-size: 14pt; font-weight: 800; color: #1e293b; margin-bottom: 24px;">
    Project-II / Engineering Clinics (Semester VII)
  </div>

  <div style="font-size: 11pt; font-style: italic; color: #334155; line-height: 1.5; max-width: 80%; margin: 0 auto 30px auto;">
    A project report submitted in partial fulfilment of the requirements for the award of the degree of<br>
    <b style="font-style: normal; color: #0f172a;">Bachelor of Technology</b> in <b style="font-style: normal; color: #0f172a;">Computer Science & Engineering / Robotics and Artificial Intelligence</b>
  </div>

  <table style="width: 100%; border: none; margin: 30px 0;">
    <tr>
      <td style="width: 50%; vertical-align: top; text-align: left; font-size: 11pt; line-height: 1.5; border: none;">
        <b style="text-transform: uppercase; font-size: 11pt; color: #0f172a;">SUBMITTED BY:</b><br><br>
        <b>Student Name 1</b> (Univ. Roll No: 2330XXX)<br>
        <b>Student Name 2</b> (Univ. Roll No: 2330XXX)<br>
        <b>Student Name 3</b> (Univ. Roll No: 2330XXX)<br>
        <i>Semester VII, Academic Session 2026–2027</i>
      </td>
      <td style="width: 50%; vertical-align: top; text-align: right; font-size: 11pt; line-height: 1.5; border: none;">
        <b style="text-transform: uppercase; font-size: 11pt; color: #0f172a;">UNDER THE GUIDANCE OF:</b><br><br>
        <b>Dr. Faculty Guide Name</b><br>
        Assistant Professor<br>
        Department of Computer Science & Engineering / Robotics & AI<br>
        Chandigarh Engineering College Jhanjeri, Mohali
      </td>
    </tr>
  </table>

  <div style="text-align: center; margin-top: 40px; font-size: 11pt; font-weight: 800; line-height: 1.5;">
    DECEMBER, 2026<br>
    <span style="font-size: 10.5pt; font-weight: 700; color: #334155;">Affiliated to I.K. Gujral Punjab Technical University, Jalandhar</span><br>
    <span style="font-size: 10pt; font-weight: 600; color: #64748b;">(Batch: 2023–2027)</span>
  </div>
</div>

<div class="page-break"></div>

<!-- DECLARATION -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">DECLARATION</h1>

<p>We, the undersigned students of the Department of Computer Science & Engineering / Robotics and Artificial Intelligence, Chandigarh Engineering College Jhanjeri, Mohali, hereby declare that the project report entitled <b>“EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING”</b> has been prepared and submitted by us in partial fulfilment of the requirements for the award of the degree of <b>Bachelor of Technology in Computer Science & Engineering / Robotics and Artificial Intelligence</b>, affiliated with <b>I.K. Gujral Punjab Technical University, Jalandhar</b>, during the academic semester VII (Project-II / Engineering Clinics), 2026–2027.</p>

<p>We solemnly affirm that this report represents our own original work conducted under the supervision and guidance of our project guide, <b>Dr. Faculty Guide Name</b>, Assistant Professor. This work has not been previously submitted, in part or in whole, for the award of any other degree, diploma, fellowship, associateship, or other similar title at this or any other university or educational institution.</p>

<p>We further confirm that all academic literature, benchmark data, mathematical models, and open-source software libraries utilized in the design, development, simulation, and verification of this prototype have been properly cited and acknowledged in strict compliance with ethical engineering standards and university anti-plagiarism guidelines.</p>

<div style="margin-top: 50px;">
  <table style="width: 100%; border: none;">
    <tr>
      <td style="width: 50%; vertical-align: top; border: none; font-size: 10.5pt; line-height: 1.5;">
        <b>(Candidate Signatures with Date)</b><br><br><br>
        ____________________________________<br>
        <b>Student Name 1</b> (Univ. Roll No: 2330XXX)<br><br>
        ____________________________________<br>
        <b>Student Name 2</b> (Univ. Roll No: 2330XXX)<br><br>
        ____________________________________<br>
        <b>Student Name 3</b> (Univ. Roll No: 2330XXX)<br>
        Semester VII (Batch: 2023–2027)
      </td>
      <td style="width: 50%; vertical-align: top; border: none; font-size: 10.5pt; line-height: 1.5; text-align: right;">
        <b>(Project Guide Signature with Date)</b><br><br><br>
        ____________________________________<br>
        <b>Dr. Faculty Guide Name</b><br>
        Assistant Professor<br>
        Dept. of CSE / Robotics & AI<br>
        CEC Jhanjeri, Mohali
      </td>
    </tr>
  </table>

  <div style="margin-top: 60px; border-top: 1px solid #0f172a; width: 45%; padding-top: 8px;">
    <b>Signature of the Head of Department</b><br>
    Department of Computer Science & Engineering / Robotics & AI<br>
    Chandigarh Engineering College Jhanjeri, Mohali<br>
    (With Official Institutional Stamp & Seal)
  </div>
</div>

<div class="page-break"></div>

<!-- CERTIFICATE -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">CERTIFICATE OF APPROVAL</h1>

<p>This is to certify that the project entitled <b>“EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING”</b> submitted by:</p>
<ul style="font-size: 11pt; line-height: 1.6; margin-left: 20px;">
  <li><b>Student Name 1</b> (University Roll No: 2330XXX)</li>
  <li><b>Student Name 2</b> (University Roll No: 2330XXX)</li>
  <li><b>Student Name 3</b> (University Roll No: 2330XXX)</li>
</ul>
<p>in partial fulfilment of the requirements for the award of the Degree of <b>Bachelor of Technology in Computer Science & Engineering / Robotics and Artificial Intelligence</b> of <b>I.K. Gujral Punjab Technical University, Jalandhar</b>, is a bonafide record of work carried out by them under my direct supervision and technical guidance during the academic session 2026–2027.</p>

<p>The software architecture, algorithmic formulations, machine learning classification pipeline, closed-loop adaptive tactile regulation, and automated regression test suites embodied in this report have been independently demonstrated, reviewed, and verified. The results are deemed satisfactory for academic submission.</p>

<div style="margin-top: 60px;">
  <table style="width: 100%; border: none;">
    <tr>
      <td style="width: 50%; vertical-align: top; border: none; font-size: 10.5pt; line-height: 1.5;">
        ____________________________________<br>
        <b>Dr. Faculty Guide Name</b><br>
        Project Supervisor / Assistant Professor<br>
        Dept. of CSE / Robotics & AI<br>
        CEC Jhanjeri, Mohali
      </td>
      <td style="width: 50%; vertical-align: top; border: none; font-size: 10.5pt; line-height: 1.5; text-align: right;">
        ____________________________________<br>
        <b>Head of the Department</b><br>
        Dept. of Computer Science & Engineering<br>
        CEC Jhanjeri, Mohali
      </td>
    </tr>
  </table>

  <table style="width: 100%; border: none; margin-top: 60px;">
    <tr>
      <td style="width: 50%; vertical-align: top; border: none; font-size: 10.5pt; line-height: 1.5;">
        ____________________________________<br>
        <b>Internal Examiner</b><br>
        Date:
      </td>
      <td style="width: 50%; vertical-align: top; border: none; font-size: 10.5pt; line-height: 1.5; text-align: right;">
        ____________________________________<br>
        <b>External Examiner</b><br>
        Date:
      </td>
    </tr>
  </table>
</div>

<div class="page-break"></div>

<!-- ACKNOWLEDGEMENT -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">ACKNOWLEDGEMENT</h1>

<p>It gives us immense pleasure and profound professional satisfaction to present this final project report on <b>“Edge AI Smart Prosthetic Hand with Adaptive Grip Learning”</b> as the culmination of our Semester VII Engineering Clinics (Project-II) curriculum.</p>

<p>First and foremost, we express our heartfelt gratitude and deepest respect to our project mentor, <b>Dr. Faculty Guide Name</b>, Assistant Professor, Department of Computer Science & Engineering / Robotics and Artificial Intelligence, for his inspiring guidance, patient mentoring, rigorous technical critique, and continuous encouragement throughout all phases of mathematical modeling, algorithmic implementation, and academic documentation. His insistence on scientific honesty, reproducible test evidence, and disciplined software architecture shaped this prototype into an academically rigorous deliverable.</p>

<p>We extend our sincere thanks to the <b>Head of the Department</b> and the Project Coordinators of Computer Science & Engineering / Robotics and Artificial Intelligence at Chandigarh Engineering College Jhanjeri, Mohali, for facilitating access to institutional computing facilities, development software, and collaborative laboratory environments.</p>

<p>We are equally grateful to the executive management of Chandigarh Engineering College Jhanjeri and the authorities of <b>I.K. Gujral Punjab Technical University, Jalandhar</b>, for structuring an engineering curriculum that emphasizes real-world clinics, evidence-based software engineering, and translational biomechatronics.</p>

<p>Our sincere appreciation also goes out to our esteemed faculty members and laboratory staff who provided valuable feedback during departmental progress reviews, helping us identify edge-case stability vulnerabilities in our feature extraction routines and closed-loop control state progression. Finally, we express our profound gratitude to our parents, family members, and friends whose unwavering moral support, patience, and encouragement sustained our focus throughout this intensive documentation sprint.</p>

<div style="margin-top: 40px; font-weight: 700; font-size: 11pt; line-height: 1.5;">
  Student Name 1<br>
  Student Name 2<br>
  Student Name 3<br>
  Department of Computer Science & Engineering / Robotics and Artificial Intelligence<br>
  Chandigarh Engineering College Jhanjeri, Mohali
</div>

<div class="page-break"></div>

<!-- ABSTRACT -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">ABSTRACT</h1>

<p>Myoelectric upper-limb prostheses represent a vital clinical intervention to restore manual manipulation capabilities for individuals with transradial amputations. However, commercial bionic hands overwhelmingly rely on open-loop, dual-site amplitude threshold control. In this conventional paradigm, muscle contractions actuate electric motors at fixed speeds until mechanical stall occurs, completely devoid of tactile feedback or grasp adaptation. As a consequence, amputee users face high rates of accidental object dropping or destructive crush deformation, while suffering from severe cognitive fatigue induced by the need for continuous visual monitoring. Although complex deep learning architectures in academic literature achieve high offline gesture recognition accuracy on public benchmarks, their multi-megabyte parameter footprints, high computational demands, and latency jitter prevent embedded execution on ultra-low-power microcontrollers within a prosthetic socket, while cloud-tethered alternatives introduce unacceptable latency delays and data privacy vulnerabilities.</p>

<p>To overcome these fundamental limitations, this project presents the engineering design, mathematical formulation, software architecture, and rigorous empirical validation of an <b>Edge AI Smart Prosthetic Hand with Adaptive Grip Learning</b>. The system establishes a synchronized dual-brain hierarchy that decouples high-level intention classification from low-level autonomous closed-loop tactile force regulation. A deterministic synthetic Surface Electromyography (sEMG) engine models physiological recruitment waveforms from the Flexor Digitorum Superficialis and Extensor Digitorum Communis muscles at a 1000 Hz sampling rate across 200 ms analysis windows for four functional grip states: <i>Open Hand</i>, <i>Power Grip</i>, <i>Pinch Grip</i>, and <i>Release</i>. An edge-compatible feature extraction engine computes 12 time-domain statistical descriptors (RMS, MAV, Variance, Energy, and Zero-Crossing Rate per channel, alongside inter-channel interaction ratio and difference) incorporating full protection against division-by-zero on edge-case signals (N=0, N=1). Intention inference is executed using an edge-optimized Random Forest classifier (35 estimators, maximum tree depth 7) benchmarked on host CPU hardware.</p>

<p>Tactile interaction is closed via simulated distal Force Sensitive Resistor (FSR) models incorporating contact thresholding (5.0 N), proportional force regulation, a closed-loop deadband (3.0 N), and an anti-crush safety ceiling (75.0 N). To address payload slippage without cognitive intervention, a software-injected shear disturbance trigger engages an autonomous anti-slip reflex loop that instantly boosts actuator effort by +18% (+12 N force) to arrest slip movement. The end-to-end pipeline is evaluated across a balanced synthetic dataset of 720 samples. Empirical testing confirms <b>100.0% cross-validation accuracy</b> (5-fold stratified K-fold) and <b>100.0% holdout test accuracy</b> with a <b>Macro-F1 score of 1.0000</b> on the synthetic dataset. Host CPU inference latency benchmarks average <b>1.40 ms to 1.88 ms</b> across 50 warmed-up trials, well within the 10.0 ms real-time edge execution budget. An automated regression suite of 27 test cases verifies signal boundary safety, input validation (HTTP 422), controller state transitions, and deterministic reset behavior. An interactive web dashboard built with React 19, TypeScript, and Vite provides 3D virtual hand kinematics, responsive High-DPI waveform monitoring, and an automated 27-second continuous demonstration sequence. This software prototype establishes an evidence-based foundation for upcoming physical hardware deployment on ESP32-S3 microcontrollers.</p>

<div class="callout-box info" style="margin-top: 25px;">
  <div class="callout-title">Academic & Scope Clarification</div>
  This project report documents a verified software simulation prototype. The 100% accuracy and 1.0000 Macro-F1 are evaluated on synthetic physiological signals, not human EMG data. Latencies represent local host CPU benchmarks, not embedded microcontroller execution. Physical electrodes, servomotors, and clinical trials represent future hardware milestones.
</div>
"""
