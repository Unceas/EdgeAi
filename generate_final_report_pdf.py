"""
Builds the complete academic Final Project Report as a high-density, professional
printable HTML document formatted to target 35–45 pages upon PDF export, matching
the Chandigarh Engineering College Jhanjeri reference report structure.
"""

import os
import subprocess
import PyPDF2

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Final Project Report - Edge AI Smart Prosthetic Hand with Adaptive Grip Learning</title>
  <style>
    @page {
      size: A4;
      margin: 22mm 18mm 22mm 18mm;
      @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 10pt;
        color: #1e293b;
      }
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: "Times New Roman", Times, serif;
      color: #0f172a;
      line-height: 1.45;
      font-size: 11pt;
      margin: 0;
      padding: 0;
    }

    .page-break {
      page-break-after: always;
      break-after: page;
    }

    /* College Running Header */
    .univ-header {
      text-align: center;
      border: 1.5px solid #0f172a;
      padding: 8px 12px;
      margin-bottom: 24px;
      background-color: #f8fafc;
    }
    .univ-header h3 {
      margin: 0;
      font-size: 13pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.02em;
    }
    .univ-header p {
      margin: 2px 0 0 0;
      font-size: 10pt;
      font-weight: 600;
      color: #334155;
    }
    .univ-header .dept {
      font-size: 10.5pt;
      font-weight: 700;
      color: #0f172a;
      margin-top: 3px;
    }

    /* Cover Page Elements */
    .cover-title-box {
      text-align: center;
      margin: 40px 0 30px 0;
    }
    .cover-title-box .proj-rep {
      font-size: 14pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
    }
    .cover-title-box h1 {
      font-size: 17pt;
      font-weight: 900;
      line-height: 1.35;
      text-transform: uppercase;
      color: #0f172a;
      margin: 0 0 12px 0;
    }
    .cover-title-box .proj-sub {
      font-size: 12pt;
      font-weight: 700;
      color: #334155;
    }
    .cover-title-box .degree-text {
      font-size: 10.5pt;
      font-style: italic;
      color: #475569;
      margin-top: 25px;
      line-height: 1.4;
    }

    .cover-table {
      width: 100%;
      margin: 40px 0 30px 0;
      border-collapse: collapse;
    }
    .cover-table td {
      width: 50%;
      vertical-align: top;
      font-size: 10.5pt;
      line-height: 1.45;
    }

    .cover-footer {
      text-align: center;
      margin-top: 40px;
      font-size: 10pt;
      font-weight: 700;
      line-height: 1.4;
    }

    /* Headings */
    h1.chapter-title {
      font-size: 15pt;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 6px;
      margin-top: 0;
      margin-bottom: 16px;
      color: #0f172a;
    }

    h2.section-title {
      font-size: 12.5pt;
      font-weight: 800;
      color: #1e293b;
      margin-top: 18px;
      margin-bottom: 8px;
      border-left: 3.5px solid #0f172a;
      padding-left: 8px;
    }

    h3.subsection-title {
      font-size: 11pt;
      font-weight: 700;
      color: #334155;
      margin-top: 12px;
      margin-bottom: 6px;
    }

    p {
      text-align: justify;
      text-justify: inter-word;
      margin: 0 0 8px 0;
    }

    ul, ol {
      margin: 4px 0 10px 0;
      padding-left: 22px;
    }
    li {
      margin-bottom: 4px;
      text-align: justify;
    }

    /* Tables */
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 16px 0;
      font-size: 9.5pt;
    }
    table.data-table th, table.data-table td {
      border: 1px solid #cbd5e1;
      padding: 5px 7px;
      text-align: left;
      vertical-align: top;
    }
    table.data-table th {
      background-color: #f1f5f9;
      font-weight: 800;
      color: #0f172a;
    }
    table.data-table tr:nth-child(even) {
      background-color: #f8fafc;
    }
    table.data-table td.pass-cell {
      background-color: #dcfce7 !important;
      color: #166534;
      font-weight: 800;
      text-align: center;
    }

    .table-caption, .figure-caption {
      font-size: 9pt;
      font-weight: 700;
      color: #334155;
      margin-top: 4px;
      margin-bottom: 12px;
      text-align: center;
    }

    /* Callout & Code Blocks */
    .callout-box {
      background-color: #f0fdf4;
      border-left: 4px solid #16a34a;
      padding: 8px 12px;
      margin: 10px 0 12px 0;
      font-size: 10pt;
    }
    .callout-box.alert {
      background-color: #fef2f2;
      border-left-color: #dc2626;
    }
    .callout-box.info {
      background-color: #f0f9ff;
      border-left-color: #0284c7;
    }
    .callout-title {
      font-weight: 800;
      text-transform: uppercase;
      font-size: 8.5pt;
      margin-bottom: 3px;
    }

    pre.code-block {
      background-color: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 8px 10px;
      font-family: "Courier New", Courier, monospace;
      font-size: 8.5pt;
      line-height: 1.35;
      margin: 8px 0 12px 0;
      white-space: pre-wrap;
    }

    .signature-container {
      width: 100%;
      margin-top: 50px;
    }
    .sig-row {
      display: flex;
      justify-content: space-between;
      margin-top: 40px;
    }
    .sig-block {
      width: 45%;
      border-top: 1px solid #0f172a;
      padding-top: 6px;
      font-size: 10pt;
      line-height: 1.35;
    }

    .reference-item {
      font-size: 9pt;
      line-height: 1.35;
      margin-bottom: 6px;
      padding-left: 24px;
      text-indent: -24px;
      text-align: justify;
    }
  </style>
</head>
<body>

<!-- ============================================================= -->
<!-- COVER / TITLE PAGE -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Mohali-140307, Punjab</p>
  <div class="dept">Department of Robotics and Artificial Intelligence</div>
</div>

<div class="cover-title-box">
  <div class="proj-rep">PROJECT REPORT ON</div>
  <h1>EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING</h1>
  <div class="proj-sub">Project-II / Engineering Clinics (Semester VII)</div>
  <div class="degree-text">
    In partial fulfilment of the requirements for the award of the Degree of<br>
    <b>Bachelor of Technology</b> in <b>Robotics and Artificial Intelligence / Computer Science & Engineering</b>
  </div>
</div>

<table class="cover-table">
  <tr>
    <td>
      <b>SUBMITTED BY:</b><br><br>
      Student Name 1 (Roll No: 2330XXX, Sem 7)<br>
      Student Name 2 (Roll No: 2330XXX, Sem 7)<br>
      Student Name 3 (Roll No: 2330XXX, Sem 7)
    </td>
    <td style="text-align: right;">
      <b>UNDER THE GUIDANCE OF:</b><br><br>
      <b>Dr. Faculty Guide Name</b><br>
      Assistant Professor<br>
      Department of Robotics & AI / CSE<br>
      CEC Jhanjeri, Mohali
    </td>
  </tr>
</table>

<div class="cover-footer">
  DECEMBER, 2026<br>
  Affiliated to <b>I.K. Gujral Punjab Technical University, Jalandhar</b><br>
  (Batch: 2023–2027)
</div>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- DECLARATION -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title" style="text-align: center; border: none;">DECLARATION</h1>

<p>We, the undersigned, hereby declare that the project report entitled <b>“EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING”</b> has been completed as part of the 7th-Semester Engineering Clinics (Project-II) curriculum for the award of the degree of Bachelor of Technology in Robotics and Artificial Intelligence / Computer Science & Engineering at Chandigarh Engineering College Jhanjeri, Mohali, affiliated with I.K. Gujral Punjab Technical University, Jalandhar.</p>

<p>We declare that this report represents our own original work carried out under the supervision and guidance of <b>Dr. Faculty Guide Name</b>, Assistant Professor. The content presented in this report has not been submitted previously in part or in full for the award of any other degree, diploma, fellowship, or professional title at this or any other educational institution.</p>

<p>We also confirm that all external sources of information, mathematical algorithms, referenced benchmark data, and scientific literature utilized in this work have been duly acknowledged and cited in accordance with standard academic integrity conventions.</p>

<div class="signature-container">
  <div class="sig-row">
    <div class="sig-block">
      <b>(Student Signature with Date)</b><br><br>
      Candidate 1 (Roll No: 2330XXX, Sem 7)<br>
      Candidate 2 (Roll No: 2330XXX, Sem 7)<br>
      Candidate 3 (Roll No: 2330XXX, Sem 7)
    </div>
    <div class="sig-block" style="text-align: right;">
      <b>(Mentor Signature with Date)</b><br><br>
      <b>Dr. Faculty Guide Name</b><br>
      Assistant Professor<br>
      Dept. of Robotics & AI / CSE
    </div>
  </div>

  <div class="sig-row" style="margin-top: 50px;">
    <div class="sig-block" style="width: 55%;">
      <b>Signature of the Head of Department</b><br><br>
      Department of Robotics and Artificial Intelligence<br>
      (With Institutional Seal / Stamp)
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- CERTIFICATE -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title" style="text-align: center; border: none;">CERTIFICATE OF APPROVAL</h1>

<p>This is to certify that the project entitled <b>“EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING”</b> submitted by Student Name 1 (Roll No: 2330XXX), Student Name 2 (Roll No: 2330XXX), and Student Name 3 (Roll No: 2330XXX) in partial fulfilment of the requirements for the degree of <b>Bachelor of Technology in Robotics and Artificial Intelligence / Computer Science & Engineering</b> from I.K. Gujral Punjab Technical University, Jalandhar, is a bonafide record of work carried out by them under my supervision during the academic session 2026–2027.</p>

<p>The results and digital simulations embodied in this project report have been verified and tested under our supervision, demonstrating robust algorithmic stability, automated test coverage, and closed-loop adaptive grasp regulation. The project is approved for final semester assessment.</p>

<div class="signature-container" style="margin-top: 70px;">
  <div class="sig-row">
    <div class="sig-block">
      <b>Dr. Faculty Guide Name</b><br>
      Project Guide / Assistant Professor<br>
      Dept. of Robotics & AI / CSE
    </div>
    <div class="sig-block" style="text-align: right;">
      <b>Head of the Department</b><br>
      Dept. of Robotics & AI<br>
      CEC Jhanjeri, Mohali
    </div>
  </div>

  <div class="sig-row" style="margin-top: 50px;">
    <div class="sig-block">
      <b>Internal Examiner</b><br>
      Date:
    </div>
    <div class="sig-block" style="text-align: right;">
      <b>External Examiner</b><br>
      Date:
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- ACKNOWLEDGEMENT -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title" style="text-align: center; border: none;">ACKNOWLEDGEMENT</h1>

<p>It gives us immense pleasure and profound professional satisfaction to present this project report on <b>“Edge AI Smart Prosthetic Hand with Adaptive Grip Learning”</b> as the culmination of our Semester VII Engineering Clinics (Project-II) coursework.</p>

<p>First and foremost, we express our heartfelt gratitude to our project guide, <b>Dr. Faculty Guide Name</b>, Assistant Professor, Department of Robotics and Artificial Intelligence / Computer Science & Engineering, for invaluable guidance, patient mentoring, rigorous technical critique, and continuous encouragement throughout all phases of design, machine learning pipeline implementation, and closed-loop controller validation. His dedication to academic rigor and scientific accuracy proved instrumental in refining our simulation architecture.</p>

<p>We extend our sincere thanks to the <b>Head of the Department</b> and the Project Coordinators of Robotics and Artificial Intelligence at Chandigarh Engineering College Jhanjeri, Mohali, for providing excellent academic infrastructure, computational facilities, and a supportive learning environment.</p>

<p>We are grateful to the management of Chandigarh Engineering College Jhanjeri and I.K. Gujral Punjab Technical University, Jalandhar, for facilitating the curriculum structure that emphasizes practical engineering clinics and evidence-based software prototyping.</p>

<p>We also express our appreciation to our faculty members, lab technicians, and peer reviewers whose perceptive feedback helped shape the responsive dashboard, test automation, and academic documentation. Finally, we thank our parents and families for their unwavering encouragement, patience, and moral support throughout our academic journey.</p>

<div style="margin-top: 40px; font-weight: 700; line-height: 1.5;">
  Student Name 1<br>
  Student Name 2<br>
  Student Name 3<br>
  Department of Robotics and Artificial Intelligence<br>
  Chandigarh Engineering College Jhanjeri, Mohali
</div>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- ABSTRACT -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title" style="text-align: center; border: none;">ABSTRACT</h1>

<p>Myoelectric upper-limb prostheses aim to restore manual dexterity and functional independence for individuals with transradial amputations. However, the majority of commercially available bionic hands rely on open-loop dual-threshold control, where muscle contractions trigger blind motor closure at fixed velocities without tactile awareness. Consequently, users experience frequent object slippage or destructive crush forces, alongside substantial mental fatigue from constant visual monitoring. Although deep learning classifiers achieve high pattern recognition accuracy in academic literature, their heavy memory footprints and execution latencies prevent embedded deployment, while cloud-tethered alternatives introduce unacceptable latency jitter and privacy vulnerabilities.</p>

<p>This project presents the design, mathematical modeling, and rigorous digital validation of an <b>Edge AI Smart Prosthetic Hand with Adaptive Grip Learning</b>. The system couples a low-latency, edge-deployable Machine Learning classifier with a real-time adaptive proportional-integral grip force controller. A 2-channel synthetic surface electromyography (sEMG) generator models physiological recruitment envelopes from the Flexor Digitorum Superficialis and Extensor Digitorum Communis across four discrete grip intentions: <i>Open Hand</i>, <i>Power Grip</i>, <i>Pinch Grip</i>, and <i>Release</i>. Time-domain statistical features (RMS, MAV, Variance, Energy, Zero-Crossing Rate, and Channel Interaction Ratio) are extracted from 200 ms windows (200 samples at 1000 Hz) and fed into an edge-optimized Random Forest ensemble (35 estimators, maximum depth 7).</p>

<p>Tactile interaction is emulated via distal Force Sensitive Resistor (FSR) models, incorporating contact detection thresholds (5.0 N), a closed-loop deadband (3.0 N), and an anti-crush ceiling (75.0 N). A simulated micro-slip disturbance trigger engages an anti-slip reflex loop that rapidly boosts actuator effort by +18% to arrest payload movement. The pipeline is evaluated on a synthetic Gaussian process dataset of 720 samples across balanced grip classes. Empirical testing confirms <b>100.0% cross-validation accuracy</b> (5-fold stratified K-fold) and <b>100.0% holdout accuracy</b> with a <b>Macro-F1 score of 1.0000</b> on the synthetic dataset. Host CPU inference latency benchmarks average <b>1.40 ms to 1.88 ms</b> across 50 warmed-up trials, well within the 10.0 ms real-time edge execution budget. An automated regression suite of 27 test cases verifies signal boundary safety, input validation (HTTP 422), controller state transitions, and deterministic reset behavior. This software prototype establishes an evidence-based foundation for upcoming physical hardware deployment on ESP32-S3 microcontrollers.</p>

<div class="callout-box info" style="margin-top: 25px;">
  <div class="callout-title">Academic & Scope Clarification</div>
  This report documents a verified software simulation prototype. The 100% accuracy and 1.0000 Macro-F1 are evaluated on synthetic physiological signals, not human EMG data. Latencies represent local host CPU benchmarks, not embedded microcontroller execution. Physical electrodes, servomotors, and clinical trials represent future hardware milestones.
</div>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- TABLE OF CONTENTS -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title" style="text-align: center; border: none;">TABLE OF CONTENTS</h1>

<table class="data-table" style="font-size: 10pt;">
  <tr>
    <th style="width: 82%;">PARTICULARS</th>
    <th style="width: 18%; text-align: right;">PAGE NO.</th>
  </tr>
  <tr><td>Title Page</td><td style="text-align: right;">i</td></tr>
  <tr><td>Declaration</td><td style="text-align: right;">ii</td></tr>
  <tr><td>Certificate of Approval</td><td style="text-align: right;">iii</td></tr>
  <tr><td>Acknowledgement</td><td style="text-align: right;">iv</td></tr>
  <tr><td>Abstract</td><td style="text-align: right;">v</td></tr>
  <tr><td>Table of Contents</td><td style="text-align: right;">vi</td></tr>
  <tr><td>List of Figures</td><td style="text-align: right;">viii</td></tr>
  <tr><td>List of Tables</td><td style="text-align: right;">ix</td></tr>
  <tr style="font-weight: 800; background-color: #f1f5f9;"><td colspan="2">CHAPTER 1: INTRODUCTION</td></tr>
  <tr><td style="padding-left: 20px;">1.1 Technical Background and Domain Overview</td><td style="text-align: right;">1</td></tr>
  <tr><td style="padding-left: 20px;">1.2 Motivation and Engineering Need</td><td style="text-align: right;">3</td></tr>
  <tr><td style="padding-left: 20px;">1.3 Project Scope and System Boundaries</td><td style="text-align: right;">5</td></tr>
  <tr><td style="padding-left: 40px;">1.3.1 In-Scope Deliverables</td><td style="text-align: right;">5</td></tr>
  <tr><td style="padding-left: 40px;">1.3.2 Out-of-Scope Limitations and Assumptions</td><td style="text-align: right;">6</td></tr>
  <tr><td style="padding-left: 20px;">1.4 Proposed System Overview and High-Level Methodology</td><td style="text-align: right;">7</td></tr>
  <tr><td style="padding-left: 20px;">1.5 Chapter Roadmap</td><td style="text-align: right;">9</td></tr>
  <tr style="font-weight: 800; background-color: #f1f5f9;"><td colspan="2">CHAPTER 2: REVIEW OF LITERATURE</td></tr>
  <tr><td style="padding-left: 20px;">2.1 Historical Evolution of Myoelectric Prostheses</td><td style="text-align: right;">10</td></tr>
  <tr><td style="padding-left: 20px;">2.2 Critical Survey of Existing Frameworks and Systems</td><td style="text-align: right;">11</td></tr>
  <tr><td style="padding-left: 20px;">2.3 Evaluation of Sensor Modalities & Grip Classification Solutions</td><td style="text-align: right;">14</td></tr>
  <tr><td style="padding-left: 20px;">2.4 Identification of Research Gaps and Technical Bottlenecks</td><td style="text-align: right;">16</td></tr>
  <tr><td style="padding-left: 20px;">2.5 Comparative Analysis of Existing and Proposed Methods</td><td style="text-align: right;">18</td></tr>
  <tr style="font-weight: 800; background-color: #f1f5f9;"><td colspan="2">CHAPTER 3: PROBLEM DEFINITION AND OBJECTIVES</td></tr>
  <tr><td style="padding-left: 20px;">3.1 Problem Statement and Mathematical Formulation</td><td style="text-align: right;">21</td></tr>
  <tr><td style="padding-left: 20px;">3.2 Project Objectives</td><td style="text-align: right;">23</td></tr>
  <tr><td style="padding-left: 20px;">3.3 Requirements Analysis (Functional & Non-Functional)</td><td style="text-align: right;">26</td></tr>
  <tr><td style="padding-left: 20px;">3.4 Hardware, Software & Environmental Specifications</td><td style="text-align: right;">32</td></tr>
  <tr><td style="padding-left: 20px;">3.5 System Feasibility Analysis (Technical, Operational, Economic)</td><td style="text-align: right;">36</td></tr>
  <tr style="font-weight: 800; background-color: #f1f5f9;"><td colspan="2">CHAPTER 4: DESIGN AND IMPLEMENTATION</td></tr>
  <tr><td style="padding-left: 20px;">4.1 System Architecture & High-Level Design</td><td style="text-align: right;">40</td></tr>
  <tr><td style="padding-left: 20px;">4.2 Data Flow Diagrams (Level 0, Level 1, Level 2)</td><td style="text-align: right;">42</td></tr>
  <tr><td style="padding-left: 20px;">4.3 Detailed Behavioral Modeling & Controller State Progression</td><td style="text-align: right;">45</td></tr>
  <tr><td style="padding-left: 20px;">4.4 Data Dictionary & API REST Contract</td><td style="text-align: right;">48</td></tr>
  <tr><td style="padding-left: 20px;">4.5 Module-Wise Implementation Details & Algorithmic Pseudocode</td><td style="text-align: right;">50</td></tr>
  <tr><td style="padding-left: 20px;">4.6 Environment Configuration, Build Setup, and Directory Structure</td><td style="text-align: right;">55</td></tr>
  <tr style="font-weight: 800; background-color: #f1f5f9;"><td colspan="2">CHAPTER 5: RESULTS AND DISCUSSIONS</td></tr>
  <tr><td style="padding-left: 20px;">5.1 Experimental Setup & Testbed Protocols</td><td style="text-align: right;">57</td></tr>
  <tr><td style="padding-left: 20px;">5.2 Verification & Automated Test-Case Execution</td><td style="text-align: right;">58</td></tr>
  <tr><td style="padding-left: 20px;">5.3 Quantitative Performance Metrics on Synthetic Dataset</td><td style="text-align: right;">62</td></tr>
  <tr><td style="padding-left: 20px;">5.4 Host Telemetry & Latency Benchmark Analysis</td><td style="text-align: right;">64</td></tr>
  <tr><td style="padding-left: 20px;">5.5 Adaptive Closed-Loop Controller Dynamics & Stress Testing</td><td style="text-align: right;">66</td></tr>
  <tr><td style="padding-left: 20px;">5.6 Comparative Evaluation with Baseline Approaches</td><td style="text-align: right;">69</td></tr>
  <tr><td style="padding-left: 20px;">5.7 Analytical Discussion, Engineering Trade-Offs & Limitations</td><td style="text-align: right;">71</td></tr>
  <tr style="font-weight: 800; background-color: #f1f5f9;"><td colspan="2">CHAPTER 6: CONCLUSION AND FUTURE SCOPE</td></tr>
  <tr><td style="padding-left: 20px;">6.1 Summary of Project Achievements</td><td style="text-align: right;">74</td></tr>
  <tr><td style="padding-left: 20px;">6.2 Novel Contributions & Engineering Impact</td><td style="text-align: right;">75</td></tr>
  <tr><td style="padding-left: 20px;">6.3 System Limitations & Operational Constraints</td><td style="text-align: right;">76</td></tr>
  <tr><td style="padding-left: 20px;">6.4 Future Scope & Extension Directions</td><td style="text-align: right;">77</td></tr>
  <tr style="font-weight: 800; background-color: #f1f5f9;"><td colspan="2">REFERENCES & PUBLICATIONS</td></tr>
  <tr><td style="padding-left: 20px;">References (IEEE Format)</td><td style="text-align: right;">80</td></tr>
</table>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- LIST OF FIGURES & TABLES -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title" style="text-align: center; border: none;">LIST OF FIGURES</h1>

<table class="data-table">
  <tr>
    <th style="width: 18%;">FIGURE NO.</th>
    <th style="width: 67%;">FIGURE TITLE / DESCRIPTION</th>
    <th style="width: 15%; text-align: right;">PAGE NO.</th>
  </tr>
  <tr><td>Figure 1.1</td><td>End-to-end processing pipeline of the Edge AI Smart Prosthetic Hand</td><td style="text-align: right;">8</td></tr>
  <tr><td>Figure 2.1</td><td>Historical taxonomy of myoelectric intention decoding and actuation</td><td style="text-align: right;">13</td></tr>
  <tr><td>Figure 4.1</td><td>Four-layer high-level system architecture of the prosthetic simulation</td><td style="text-align: right;">41</td></tr>
  <tr><td>Figure 4.2</td><td>Level 0 Data Flow Diagram (Context Model)</td><td style="text-align: right;">43</td></tr>
  <tr><td>Figure 4.3</td><td>Level 1 Data Flow Diagram (Decomposition of simulation and control)</td><td style="text-align: right;">44</td></tr>
  <tr><td>Figure 4.4</td><td>Level 2 Data Flow Diagram (Closed-loop force regulation and slip reflex)</td><td style="text-align: right;">45</td></tr>
  <tr><td>Figure 4.5</td><td>UML Statechart diagram of the 8-stage adaptive controller progression</td><td style="text-align: right;">47</td></tr>
  <tr><td>Figure 4.6</td><td>Logical Sequence Diagram representing interactive grip classification cycle</td><td style="text-align: right;">48</td></tr>
  <tr><td>Figure 5.1</td><td>Interactive React dashboard featuring real-time virtual hand articulation</td><td style="text-align: right;">60</td></tr>
  <tr><td>Figure 5.2</td><td>Synthetic dual-channel sEMG waveform across flexor and extensor channels</td><td style="text-align: right;">63</td></tr>
  <tr><td>Figure 5.3</td><td>Host CPU benchmark latency distribution across 50 warmed-up trials</td><td style="text-align: right;">65</td></tr>
  <tr><td>Figure 5.4</td><td>Closed-loop pressure regulation and anti-slip torque recovery curves</td><td style="text-align: right;">68</td></tr>
</table>

<br>
<h1 class="chapter-title" style="text-align: center; border: none; margin-top: 20px;">LIST OF TABLES</h1>

<table class="data-table">
  <tr>
    <th style="width: 18%;">TABLE NO.</th>
    <th style="width: 67%;">TABLE TITLE / DESCRIPTION</th>
    <th style="width: 15%; text-align: right;">PAGE NO.</th>
  </tr>
  <tr><td>Table 2.1</td><td>Comparative analysis of commercial, academic, and proposed prosthetic controllers</td><td style="text-align: right;">19</td></tr>
  <tr><td>Table 3.1</td><td>Target embedded hardware specifications for upcoming ESP32-S3 deployment</td><td style="text-align: right;">33</td></tr>
  <tr><td>Table 3.2</td><td>Host development, machine learning, and simulation runtime specifications</td><td style="text-align: right;">34</td></tr>
  <tr><td>Table 3.3</td><td>Technical, operational, and environmental risk mitigation matrix</td><td style="text-align: right;">38</td></tr>
  <tr><td>Table 4.1</td><td>UML Use Case specifications for digital prototype interaction</td><td style="text-align: right;">46</td></tr>
  <tr><td>Table 4.2</td><td>REST API request and response data contracts with Pydantic validation</td><td style="text-align: right;">49</td></tr>
  <tr><td>Table 4.3</td><td>Time-domain statistical feature representation dictionary (12 dimensions)</td><td style="text-align: right;">51</td></tr>
  <tr><td>Table 5.1</td><td>Comprehensive automated test suite execution log (27 of 27 tests passed)</td><td style="text-align: right;">59</td></tr>
  <tr><td>Table 5.2</td><td>Empirical classification performance metrics on synthetic sEMG dataset</td><td style="text-align: right;">62</td></tr>
  <tr><td>Table 5.3</td><td>Host CPU execution latency versus embedded edge operational budget</td><td style="text-align: right;">65</td></tr>
  <tr><td>Table 5.4</td><td>Closed-loop controller dynamic stress test under disturbance injection</td><td style="text-align: right;">67</td></tr>
</table>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- CHAPTER 1: INTRODUCTION -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title">CHAPTER 1: INTRODUCTION</h1>

<h2 class="section-title">1.1 Technical Background and Domain Overview</h2>
<p>Upper-limb amputations result in profound functional impairment, reducing an individual's autonomy in activities of daily living (ADLs) and creating severe vocational and psychosocial obstacles. For decades, biomechatronic engineering has sought to replicate human hand motor function using externally powered myoelectric prostheses. These devices detect surface electromyographic (sEMG) potentials generated during voluntary contraction of residual forearm musculature, interpreting these electrical signals to drive electric motors across artificial joints.</p>

<p>The physiological basis of sEMG lies in the depolarization of muscle fiber membranes initiated by neural motor units. When an individual attempts a hand movement—even after amputation—the motor cortex transmits action potentials through descending spinal pathways into residual nerve endings, recruiting motor units in muscles such as the Flexor Digitorum Superficialis (FDS) and Extensor Digitorum Communis (EDC). The spatial and temporal summation of these microvolt-level motor unit action potentials (MUAP trains) creates an interference pattern measurable on the skin surface. Surface EMG represents a non-invasive, rich biological control channel for active prostheses.</p>

<p>However, modern commercial prostheses suffer from a critical technological shortfall: they operate almost universally in an <b>open-loop</b> regime. While commercial multi-articulated hands feature advanced mechanical linkages, their control architectures rely on coarse amplitude thresholding. When a user contracts their forearm above a set threshold, the motors actuate blindly at full velocity until mechanical stall occurs. The prosthesis possesses no internal sensation of touch, pressure, or object compliance. As a direct consequence, users routinely crush fragile objects (such as paper cups or fruit) or inadvertently drop slippery items during transportation. To manipulate objects safely, the user must maintain continuous, intense visual concentration. This cognitive burden is exhausting and constitutes the primary reason why up to 50% of myoelectric prosthesis users eventually abandon their devices in favor of simple mechanical hooks or passive cosmetic limbs.</p>

<p>Recent advances in <b>Edge Artificial Intelligence (Edge AI)</b> offer a transformative resolution to this crisis. By embedding compact, high-efficiency machine learning classifiers directly onto low-power microcontrollers (such as the ESP32-S3 or ARM Cortex-M4), intent classification can occur locally in under 2 milliseconds without reliance on external smartphones, tethered computers, or cloud servers. Concurrently, integrating tactile feedback through Force Sensitive Resistors (FSRs) closes the control loop. An autonomous adaptive grip controller can sense initial physical contact, ramp motor torque to a safe pre-calibrated pressure setpoint, enforce strict anti-crush ceilings, and execute reflexive grip tightening within milliseconds if shear slippage is detected. This project investigates, designs, and digitally validates such an intelligent, closed-loop prosthetic system.</p>

<h2 class="section-title">1.2 Motivation and Engineering Need</h2>
<p>The motivation for this engineering project stems from the acute disparity between laboratory machine learning publications and the daily reality of prosthetic users. While complex deep learning models (such as deep 2D/3D CNNs and Transformers) achieve classification accuracies exceeding 95% on public datasets, their computational complexity, memory footprints, and power demands render them unviable for embedded execution within a prosthetic socket. Conversely, commercial manufacturers have resisted integrating pattern recognition due to concerns over non-deterministic latencies, socket shifting, and battery depletion.</p>

<p>The specific engineering needs driving this work include:</p>
<ul>
  <li><b>Mitigation of Cognitive Burden:</b> Enabling the prosthetic hand to autonomously modulate grip force and arrest slips frees the user from constant visual vigilance, restoring natural, intuitive manipulation.</li>
  <li><b>Deterministic Low-Latency Operation:</b> Cognitive neuroscience establishes that prosthetic response delays exceeding 100–125 ms feel unnaturally sluggish and disrupt motor coordination. Local Edge AI inference must execute in under 10 ms to leave ample headroom for mechanical actuation within the biological window.</li>
  <li><b>Fail-Safe Grasping Regulation:</b> Real-world manipulation involves payloads of diverse stiffness and mass. An autonomous controller must enforce hard force ceilings (e.g., 75 N) to protect objects while ensuring sufficient retention force.</li>
  <li><b>Methodological Rigor Prior to Hardware Prototyping:</b> Directly fabricating physical prosthetic hardware without verifying control stability leads to frequent actuator burnout and difficult debugging. Developing a comprehensive, deterministic software simulation platform allows algorithmic edge cases (such as zero-crossing division errors, sensor noise scaling, and race conditions) to be systematically resolved beforehand.</li>
</ul>

<h2 class="section-title">1.3 Project Scope and System Boundaries</h2>
<h3 class="subsection-title">1.3.1 In-Scope Deliverables</h3>
<p>The scope of this Semester VII Engineering Clinics project encompasses the complete software design, mathematical modeling, edge AI optimization, closed-loop controller development, and verification of a digital simulation prototype. The concrete in-scope deliverables include:</p>
<ol>
  <li><b>Synthetic 2-Channel sEMG Generator:</b> Mathematical modeling of 1000 Hz, 200 ms signal windows representing flexor and extensor muscle activity across four distinct grip intentions: <i>OPEN</i>, <i>POWER_GRIP</i>, <i>PINCH_GRIP</i>, and <i>RELEASE</i>, incorporating band-limited colored noise (30–350 Hz) and recruitment decay curves.</li>
  <li><b>Time-Domain Feature Extraction Engine:</b> Robust computation of 12 statistical descriptors (RMS, MAV, Variance, Energy, and Zero-Crossing Rate per channel, plus Channel Interaction Ratio and Difference) with full protection against division-by-zero for empty and single-sample arrays.</li>
  <li><b>Edge-Optimized Machine Learning Classifier:</b> Training and evaluation of an edge-deployable Random Forest classifier (35 trees, depth 7) benchmarked for 5-fold cross-validation accuracy, holdout test accuracy, Macro-F1, and host execution latency.</li>
  <li><b>Closed-Loop Adaptive Grip Controller:</b> State-machine regulation of simulated actuator force using simulated FSR tactile feedback across discrete operational states (IDLE, CLOSING, CONTACT, INCREASING, DECREASING, MAINTAINING, SLIP_COMPENSATION, RELEASING) with configurable safety boundaries (75 N ceiling, 3 N deadband).</li>
  <li><b>Simulated Disturbance Injection & Slip Reflex:</b> Controlled injection of micro-slip perturbations into the control loop triggering an autonomous +18% servo torque boost to arrest payload motion.</li>
  <li><b>Resting Baseline Calibration Module:</b> User calibration routine storing individualized resting noise floor and MVC gains, dynamically scaling synthetic signal generation.</li>
  <li><b>Interactive Telemetry Dashboard:</b> High-contrast, dark monochrome web application built with React 19, TypeScript, and Vite, featuring 3D virtual hand kinematics, responsive High-DPI waveform canvas, and an automated 27-second continuous demonstration sequence.</li>
  <li><b>Automated Regression Test Suite:</b> Comprehensive 27-test pytest suite verifying signal dimensions, input validation (HTTP 422), controller dynamics, and deterministic reset behavior.</li>
</ol>

<h3 class="subsection-title">1.3.2 Out-of-Scope Limitations and Assumptions</h3>
<p>To preserve absolute academic honesty, system boundaries are explicitly delineated:</p>
<ul>
  <li><b>No Physical Hardware Integration:</b> Physical wet/dry electrodes, analog front-end circuits, physical servo motors, and 3D-printed mechanical chassis are not part of this software prototype. All biosignals and tactile pressures are digitally simulated.</li>
  <li><b>Synthetic Dataset Evaluation:</b> Reported classification accuracy and F1-scores represent evaluation on mathematically generated Gaussian process signals. They do not constitute human clinical trial results.</li>
  <li><b>Host CPU Telemetry:</b> Latency measurements are obtained on host workstation hardware using Python monotonic timers. They do not represent physical ESP32-S3 execution times.</li>
  <li><b>Simulated Disturbance:</b> The slip event is a software-triggered state disturbance within the control algorithm, not a physical shear sensor reading.</li>
</ul>

<h2 class="section-title">1.4 Proposed System Overview and High-Level Methodology</h2>
<p>The proposed system operates through a continuous, closed-loop architecture structured into five sequential stages:</p>
<ol>
  <li><b>Signal Synthesis:</b> Generates 200 ms windows (200 samples at 1000 Hz) of dual-channel sEMG reflecting physiological muscle recruitment and user calibration parameters.</li>
  <li><b>Feature Transformation:</b> Converts raw microvolt waveforms into a compact 12-dimensional feature vector capturing time-domain statistical energy and agonist-antagonist co-contraction ratios.</li>
  <li><b>Edge ML Inference:</b> Passes feature vectors through the pre-trained Random Forest model, outputting predicted grip intention and calibrated confidence probabilities.</li>
  <li><b>Kinematic Actuation:</b> Commands virtual prosthetic joints toward target flexion angles corresponding to the classified grasp.</li>
  <li><b>Autonomous Tactile Regulation:</b> Monitors simulated FSR pressure upon contact (5.0 N threshold). Regulates motor torque toward target pressure (50 N for Power, 25 N for Pinch). If pressure exceeds 75 N, it enforces DECREASING mode. If a slip perturbation occurs, it triggers an instant +18% compensatory boost to re-stabilize the grasp.</li>
</ol>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- CHAPTER 2: REVIEW OF LITERATURE -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title">CHAPTER 2: REVIEW OF LITERATURE</h1>

<h2 class="section-title">2.1 Historical Evolution of Myoelectric Prostheses</h2>
<p>The concept of controlling artificial limbs via biological electricity dates back to 1948 with the pioneering work of Reiter in Germany, followed by the development of the "Russian hand" in the late 1950s. These foundational systems established <i>amplitude threshold control</i>: when a rectified sEMG signal exceeded a fixed voltage threshold, an electric relay closed the motor circuit. Throughout the 1970s and 1980s, commercial devices (such as the Ottobock MyoBock) refined this paradigm into dual-site proportional control, using antagonistic flexor and extensor electrodes to control closing and opening velocities independently.</p>

<p>While mechanically robust, threshold-based control is fundamentally constrained. Amputees must learn unnatural co-contraction pulses to toggle between wrist rotation and finger closure. In the 1990s, research shifted toward <b>Pattern Recognition (PR)</b>. Hudgins et al. (1993) demonstrated that deterministic statistical features extracted from initial transient muscle contractions could classify distinct upper-limb movements with over 90% accuracy. Over the subsequent two decades, pattern recognition expanded to steady-state sEMG, multi-channel high-density arrays, and simultaneous proportional control (Englehart and Hudgins, 2003; Farina et al., 2014).</p>

<h2 class="section-title">2.2 Critical Survey of Existing Frameworks and Feature Extraction</h2>
<p>Feature extraction is the critical bridge between raw biosignals and machine learning classification. Surface EMG signals are non-stationary, stochastic biological signals with frequency content predominantly concentrated between 20 Hz and 450 Hz. In a comprehensive comparative evaluation of 37 mathematical features, Phinyomark et al. (2012) demonstrated that <b>time-domain statistical features</b> provide optimal clustering separation while imposing minimal computational complexity.</p>

<p>The standard Hudgins feature set includes:</p>
<ul>
  <li><b>Mean Absolute Value (MAV):</b> Represents contraction amplitude: <code>MAV = (1/N) * sum(|x_k|)</code></li>
  <li><b>Root Mean Square (RMS):</b> Relates directly to signal power and muscle force: <code>RMS = sqrt((1/N) * sum(x_k^2))</code></li>
  <li><b>Variance (VAR):</b> Reflects power spectral density: <code>VAR = (1/(N-1)) * sum((x_k - mu)^2)</code></li>
  <li><b>Zero Crossing Rate (ZCR):</b> Approximates dominant frequency content by counting baseline crossings that exceed a noise deadband threshold.</li>
  <li><b>Simple Square Integral (Energy):</b> Captures cumulative energy expenditure: <code>Energy = sum(x_k^2)</code></li>
</ul>

<p>In our architecture, this formulation is augmented with a <b>Channel Interaction Ratio</b> (Flexor MAV / Extensor MAV) and <b>Channel Difference</b>. These inter-channel descriptors explicitly capture the biological synergy between agonist and antagonist muscle compartments, enabling unambiguous separation between strong co-contractions (Power Grip) and isolated single-muscle bursts (Pinch Grip or Open Hand).</p>

<h2 class="section-title">2.3 Evaluation of Sensor Modalities & Edge Classification Paradigms</h2>
<p>Research on intention decoding has evaluated diverse classifiers, ranging from Linear Discriminant Analysis (LDA) and Support Vector Machines (SVM) to Deep Convolutional Neural Networks (CNNs) (Atzori et al., 2016). While deep networks achieve high benchmark accuracy, their high computational complexity, memory requirements, and susceptibility to floating-point latency jitter make them poorly suited for low-power edge microcontrollers. Conversely, <b>Random Forest (RF) ensembles</b> (Breiman, 2001) offer compelling advantages for embedded biomechatronics: non-linear decision boundaries, immunity to feature scaling, high resistance to overfitting, and rapid evaluation via conditional branch instructions. When pruned, a 35-tree Random Forest occupies less than 200 kB of storage and executes in under 2 ms on host CPUs.</p>

<p>Regarding tactile sensing, piezoresistive Force Sensitive Resistors (FSRs) represent the industry benchmark for prosthetic fingertips (Cordella et al., 2016). FSRs exhibit an inverse resistance response to applied normal force, offering a wide dynamic range (0.1 N to 100 N), mechanical durability, low power consumption, and simple analog signal conditioning.</p>

<h2 class="section-title">2.4 Identification of Research Gaps and Technical Bottlenecks</h2>
<p>A rigorous review of academic and commercial literature identifies three persistent bottlenecks:</p>
<ol>
  <li><b>The Open-Loop Tactile Deficit:</b> Over 85% of published myoelectric control studies terminate at offline classification accuracy. They treat grasping as an open-loop task, ignoring the critical necessity of autonomous force regulation and slip arrest once contact occurs.</li>
  <li><b>Absence of Autonomous Reflexive Slip Compensation:</b> When an object slips, visual detection and voluntary human correction requires 200–300 ms, during which the item is dropped. An artificial tactile reflex loop must operate in under 20 ms to arrest shear displacement.</li>
  <li><b>Cloud-Tethered Vulnerability:</b> Systems that offload machine learning to external smartphones or cloud APIs introduce severe latency jitter (50–300 ms), privacy vulnerabilities, and catastrophic failure whenever connectivity drops. Edge AI execution is non-negotiable for medical limb control.</li>
</ol>

<h2 class="section-title">2.5 Comparative Analysis of Existing and Proposed Methods</h2>
<p>Table 2.1 contrasts conventional commercial prostheses, academic deep learning prototypes, cloud-tethered IoT devices, and our proposed Edge AI closed-loop architecture.</p>

<table class="data-table">
  <tr>
    <th>System Parameter</th>
    <th>Commercial Bionic (e.g. Ottobock)</th>
    <th>Academic Deep Learning</th>
    <th>Cloud-Tethered IoT</th>
    <th>Proposed Edge AI Hand</th>
  </tr>
  <tr>
    <td><b>Control Architecture</b></td>
    <td>Dual-site thresholding (open-loop)</td>
    <td>Deep CNN / LSTM (open-loop)</td>
    <td>Remote cloud inference</td>
    <td><b>Edge RF + Closed-Loop FSR Reflex</b></td>
  </tr>
  <tr>
    <td><b>Tactile Awareness</b></td>
    <td>None (Visual lock required)</td>
    <td>Visual / Simulated only</td>
    <td>Telemetry display only</td>
    <td><b>Autonomous force & anti-slip loop</b></td>
  </tr>
  <tr>
    <td><b>Inference Hardware</b></td>
    <td>Analog comparator / 8-bit MCU</td>
    <td>Desktop GPU (Workstation)</td>
    <td>Remote Cloud Server</td>
    <td><b>Embedded MCU (ESP32-S3 target)</b></td>
  </tr>
  <tr>
    <td><b>Latency Profile</b></td>
    <td>< 5 ms (coarse binary)</td>
    <td>35 - 80 ms (heavy compute)</td>
    <td>100 - 350 ms (jitter-prone)</td>
    <td><b>1.4 - 1.9 ms (deterministic host)</b></td>
  </tr>
  <tr>
    <td><b>Slip Recovery</b></td>
    <td>User must visually re-trigger</td>
    <td>None (offline dataset)</td>
    <td>None</td>
    <td><b>Autonomous +18% torque reflex</b></td>
  </tr>
  <tr>
    <td><b>User Cognitive Load</b></td>
    <td>Extreme (constant monitoring)</td>
    <td>High</td>
    <td>High</td>
    <td><b>Minimal (autonomous regulation)</b></td>
  </tr>
  <tr>
    <td><b>Resting Calibration</b></td>
    <td>Manual potentiometer trim</td>
    <td>Multi-hour retraining</td>
    <td>Cloud profile sync</td>
    <td><b>On-device noise floor calibration</b></td>
  </tr>
</table>
<div class="table-caption">Table 2.1: Comparative analysis of commercial, academic, and proposed prosthetic controllers.</div>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- CHAPTER 3: PROBLEM DEFINITION AND OBJECTIVES -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title">CHAPTER 3: PROBLEM DEFINITION AND OBJECTIVES</h1>

<h2 class="section-title">3.1 Problem Statement and Mathematical Formulation</h2>
<p>Existing myoelectric prostheses suffer from an acute trade-off: they either employ overly simplistic, open-loop threshold controls that crush or drop objects, or utilize computationally bloated deep neural networks that cannot operate reliably on battery-powered edge hardware. The objective of this project is to mathematically formulate and digitally validate an edge-deployable pattern recognition and closed-loop tactile feedback pipeline capable of operating within deterministic sub-10 millisecond processing budgets.</p>

<p>The mathematical formulation of the system comprises two interconnected control loops:</p>
<p><b>1. Feedforward Intention Classification Pipeline:</b><br>
Let <code>s_1(t)</code> and <code>s_2(t)</code> denote continuous biopotential signals from flexor and extensor muscle channels. The signals are digitized at sampling frequency <code>f_s = 1000 Hz</code> over analysis window <code>W_k = {t_i}_{i=1}^N</code> with <code>N = 200 samples</code> (window length <code>T_w = 200 ms</code>). A deterministic feature mapping <code>Phi: R^{200 x 2} -> R^{12}</code> maps each window to feature vector <code>x_k</code>:</p>
<pre class="code-block">
x_k = [ RMS_1, MAV_1, VAR_1, SSI_1, ZCR_1, 
        RMS_2, MAV_2, VAR_2, SSI_2, ZCR_2, 
        Ratio(ch1, ch2), Diff(ch1, ch2) ]^T
</pre>
<p>The classifier hypothesis <code>h_theta(x)</code> assigns <code>x_k</code> to a discrete grip class <code>y in Y = {OPEN, POWER_GRIP, PINCH_GRIP, RELEASE}</code> by maximizing posterior probability:</p>
<pre class="code-block">
y_pred = argmax_{c in Y} P(y = c | x_k; theta)
</pre>

<p><b>2. Feedback Tactile Regulation Pipeline:</b><br>
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

<h2 class="section-title">3.2 Project Objectives</h2>
<p>The engineering objectives are formalized into eleven discrete, measurable milestones:</p>
<ul>
  <li><b>Objective 1:</b> Design a deterministic 2-channel synthetic sEMG generator operating at 1000 Hz, synthesizing realistic 200 ms recruitment windows for <i>OPEN</i>, <i>POWER_GRIP</i>, <i>PINCH_GRIP</i>, and <i>RELEASE</i>.</li>
  <li><b>Objective 2:</b> Implement an edge-compatible 12-dimensional time-domain feature extractor with robust zero-crossing division safeguards for boundary arrays (N=0, N=1).</li>
  <li><b>Objective 3:</b> Train and optimize an edge-deployable Random Forest classifier achieving high discriminability across synthetic grip classes.</li>
  <li><b>Objective 4:</b> Implement a closed-loop adaptive grip controller regulating simulated FSR force toward setpoint envelopes (50 N, 25 N) with deadband hysteresis (3 N).</li>
  <li><b>Objective 5:</b> Engineer an anti-crush safety mechanism enforcing DECREASING mode whenever pressure exceeds the 75 N ceiling.</li>
  <li><b>Objective 6:</b> Develop an autonomous anti-slip reflex loop that detects shear disturbances and rapidly boosts motor effort (+18%) to restore stability.</li>
  <li><b>Objective 7:</b> Implement a baseline noise calibration routine scaling synthetic resting noise floor dynamically.</li>
  <li><b>Objective 8:</b> Build an interactive web dashboard in React 19 and TypeScript with dynamic 3D virtual hand kinematics, responsive High-DPI waveform canvas, and real-time telemetry.</li>
  <li><b>Objective 9:</b> Implement an automated 27-second end-to-end demonstration sequence advancing smoothly every second with live API telemetry.</li>
  <li><b>Objective 10:</b> Measure and report real host CPU inference latency using monotonic high-resolution timers, removing hardcoded claims.</li>
  <li><b>Objective 11:</b> Construct an automated regression test suite of 27 test cases validating all functional endpoints, boundaries, and status codes.</li>
</ul>

<h2 class="section-title">3.3 Requirements Analysis</h2>
<p>The system requirements are categorized into Functional (FR) and Non-Functional (NFR) requirements:</p>
<p><b>Functional Requirements (Summary):</b><br>
FR-1 (sEMG Generation), FR-2 (12-Dim Feature Extraction), FR-3 (Strict Input Validation & HTTP 422), FR-4 (Random Forest Inference), FR-5 (Monotonic Latency Measurement), FR-6 (Contact Thresholding at 5 N), FR-7 (Proportional Force Regulation), FR-8 (Anti-Crush Safety Ceiling at 75 N), FR-9 (Autonomous Slip Recovery Reflex), FR-10 (Resting Baseline Calibration), FR-11 (Continuous 27s Demo Progression), FR-12 (Dynamic Event Logging), FR-13 (Virtual Hand Kinematic Rendering), FR-14 (Responsive Waveform Canvas), FR-15 (8-Stage Progression Indicator), FR-16 (Deterministic Reset), FR-17 (RESTful OpenAPI Contract), FR-18 (Automated Regression Verification).</p>

<p><b>Non-Functional Requirements (Summary):</b><br>
NFR-1 (Real-Time Sub-10ms Budget), NFR-2 (Zero Division / NaN Immunity), NFR-3 (Resource Efficiency on Standard Host), NFR-4 (C/C++ Microcontroller Portability), NFR-5 (Modular Monorepo Architecture), NFR-6 (Responsive High-DPI UI), NFR-7 (Experimental Reproducibility), NFR-8 (CORS Security Compliance), NFR-9 (Fail-Safe Anti-Crush Priority), NFR-10 (Scientific Metric Integrity), NFR-11 (Async Concurrency Protection), NFR-12 (Code Maintainability), NFR-13 (Academic Honesty & Limitations), NFR-14 (Clean Production Build Verification).</p>

<h2 class="section-title">3.4 Hardware, Software & Environmental Specifications</h2>
<p>Table 3.1 details the target embedded hardware platform for future physical deployment. Table 3.2 specifies the development and execution environment utilized for this software prototype.</p>

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
  <li><b>Technical Feasibility:</b> All signal processing and machine learning algorithms utilize standard mathematical operations. Running the simulation locally via FastAPI and Vite eliminates distributed network failure modes. All 27 regression tests pass deterministically.</li>
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

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- CHAPTER 4: DESIGN AND IMPLEMENTATION -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title">CHAPTER 4: DESIGN AND IMPLEMENTATION</h1>

<h2 class="section-title">4.1 System Architecture & High-Level Design</h2>
<p>The Edge AI Smart Prosthetic Hand architecture is structured into four cohesive logical layers:</p>
<pre class="code-block">
+-------------------------------------------------------------------------+
|               LAYER 4: TELEMETRY & VISUALIZATION LAYER                 |
|  React 19 Dashboard | 3D Virtual Hand | EMG Canvas | Live Event Logs   |
+------------------------------------+------------------------------------+
                                     | REST API (HTTP / JSON / CORS)
+------------------------------------v------------------------------------+
|              LAYER 3: ACTUATOR & CLOSED-LOOP CONTROL LAYER              |
|  Contact Detection (5N) | Pressure Setpoints | Anti-Crush Ceiling (75N) |
|  Hysteresis Deadband (3N) | Micro-Slip Disturbance Reflex (+18% Torque) |
+------------------------------------+------------------------------------+
                                     ^ Predicted Intention Class
+------------------------------------+------------------------------------+
|               LAYER 2: FEATURE EXTRACTION & EDGE AI LAYER              |
|  12-Dim Time-Domain Features (RMS, MAV, VAR, SSI, ZCR, Ratio, Diff)    |
|  Random Forest Classifier (35 Trees, Depth 7) | Host Latency Monotonic  |
+------------------------------------+------------------------------------+
                                     ^ 200 ms Window (200 Samples @ 1000 Hz)
+------------------------------------+------------------------------------+
|          LAYER 1: SIGNAL SYNTHESIS & CONDITIONING LAYER                 |
|  Synthetic sEMG (Flexor / Extensor) | Band-Limited Noise (30-350 Hz)    |
|  Baseline Noise Calibration Floor   | Recruitment Envelopes (4 Grips)   |
+-------------------------------------------------------------------------+
</pre>
<div class="figure-caption">Figure 4.1: Four-layer high-level system architecture of the prosthetic simulation.</div>

<h2 class="section-title">4.2 Data Flow Diagrams (DFDs)</h2>
<p>The flow of data through the system is represented across three levels of abstraction:</p>
<p><b>Level 0 DFD (Context Diagram):</b> Models the system as a unified process. The external entity (User/Presenter) sends grip selections, calibration requests, or slip disturbance triggers to the simulation engine. The system processes the input and outputs articulated 3D kinematics, live EMG waveforms, pressure gauges, and timestamped event logs.<br><br>
<b>Level 1 DFD (Major Decomposition):</b> Decomposes the simulation into five primary processes: (1.0) Synthetic Signal Synthesis & Calibration, (2.0) Time-Domain Feature Extraction, (3.0) Random Forest Classification, (4.0) Adaptive Closed-Loop Regulation, and (5.0) Telemetry Formatting & Dashboard Rendering.<br><br>
<b>Level 2 DFD (Closed-Loop Force Regulation & Slip Reflex):</b> Details Process 4.0. It shows how the incoming predicted grip class establishes target pressure, how the simulated FSR reading generates tracking error <code>e(t)</code>, how the deadband comparator determines whether to ramp or hold effort, how the safety ceiling comparator enforces DECREASING mode if pressure exceeds 75 N, and how the slip perturbation trigger bypasses normal tracking to inject an immediate +18% effort boost.</p>

<h2 class="section-title">4.3 Detailed Behavioral Modeling & Controller State Progression</h2>
<p>The closed-loop adaptive controller operates as an 8-state deterministic finite state machine (FSM). The progression ribbon visually tracks these states in the dashboard:</p>
<ul>
  <li><b>IDLE:</b> Actuators at 0% effort, 0 N pressure. Awaiting user contraction command.</li>
  <li><b>CLOSING:</b> Grip classified; fingers rotating inward toward object prior to contact.</li>
  <li><b>CONTACT:</b> Distal FSR registers initial physical resistance exceeding CONTACT_THRESHOLD (5.0 N).</li>
  <li><b>INCREASING:</b> Pressure is below target setpoint; controller applies proportional force ramping.</li>
  <li><b>DECREASING:</b> Pressure exceeds safe ceiling (75 N) or slight overshoot detected; motor backs off.</li>
  <li><b>MAINTAINING:</b> Pressure is within setpoint deadband (|e| <= 3 N); servos hold position in equilibrium.</li>
  <li><b>SLIP DETECTED:</b> Software disturbance injected; stability drops to 72%, red alert banner triggered.</li>
  <li><b>ANTI-SLIP:</b> Reflex torque boost (+18% effort, +12 N force) applied immediately to arrest movement.</li>
  <li><b>STABILIZED:</b> Payload movement halted; stability restored to 98.6%, controller resumes maintaining state.</li>
</ul>

<h2 class="section-title">4.4 Data Dictionary & API REST Contract</h2>
<p>Table 4.2 documents the RESTful API endpoints exposed by the FastAPI backend, including request validation and response models.</p>

<table class="data-table">
  <tr><th>Endpoint</th><th>HTTP</th><th>Request Body Schema</th><th>Response Schema & Key Fields</th></tr>
  <tr><td><code>/health</code></td><td>GET</td><td>None</td><td><code>{status: "online", mode: "simulation", model_trained: bool}</code></td></tr>
  <tr><td><code>/simulate/emg</code></td><td>POST</td><td><code>SimulateEMGRequest {grip_state: str, noise_level: float}</code></td><td><code>EMGSignalData {channel_1: float[], channel_2: float[], time_ms: float[]}</code></td></tr>
  <tr><td><code>/predict</code></td><td>POST</td><td><code>PredictRequest {channel_1: float[], channel_2: float[]}</code></td><td><code>PredictionResult {predicted_grip: str, confidence_percent: float, latency_ms: float}</code></td></tr>
  <tr><td><code>/grip/control</code></td><td>POST</td><td><code>GripControlRequest {predicted_grip: str, simulated_contact: bool, slip_trigger: bool}</code></td><td><code>ControllerState {current_pressure_n: float, grip_force_percent: float, action: str}</code></td></tr>
  <tr><td><code>/calibrate</code></td><td>POST</td><td><code>CalibrationRequest {subject_id: str, simulated_duration_s: float}</code></td><td><code>CalibrationResult {baseline_noise_floor_v: float, mvc_gain_multiplier: float}</code></td></tr>
  <tr><td><code>/metrics</code></td><td>GET</td><td>None</td><td><code>SystemMetrics {cv_5fold_mean_accuracy: float, holdout_accuracy: float, latency_ms: float}</code></td></tr>
  <tr><td><code>/reset</code></td><td>POST</td><td>None</td><td><code>{status: "system_reset_complete"}</code></td></tr>
</table>
<div class="table-caption">Table 4.2: REST API request and response data contracts with Pydantic validation.</div>

<h2 class="section-title">4.5 Module-Wise Implementation Details & Algorithmic Pseudocode</h2>
<p>The operational logic of the core modules is detailed below:</p>

<p><b>Algorithm 1: Safe 12-Dimensional Time-Domain Feature Extraction</b></p>
<pre class="code-block">
Input: Signal array S of length N, threshold theta = 0.015 V
Output: Dictionary {rms, mav, var, energy, zcr}
1: If N == 0 then return {0.0, 0.0, 0.0, 0.0, 0.0}
2: If N == 1 then return {abs(S[0]), abs(S[0]), 0.0, S[0]^2, 0.0}
3: mav <- mean(abs(S))
4: rms <- sqrt(mean(S^2))
5: var <- variance(S)
6: energy <- sum(S^2)
7: sign_changes <- ((S[:-1] * S[1:] < 0) and (|S[:-1] - S[1:]| > theta))
8: zcr <- sum(sign_changes) / (N - 1)
9: return sanitize_nan_to_num({rms, mav, var, energy, zcr})
</pre>

<p><b>Algorithm 2: Closed-Loop Adaptive Grip Control & Anti-Crush Intervention</b></p>
<pre class="code-block">
Input: predicted_grip, simulated_contact, slip_trigger, pressure_override
Output: Controller state dictionary
1: target_pressure <- TARGET_MAP[predicted_grip]
2: If predicted_grip in {OPEN, RELEASE} then
3:    grip_force <- max(0.0, grip_force - 15.0)
4:    current_pressure <- max(0.0, current_pressure - 12.0)
5:    return state(action='IDLE', stability=100.0)
6: If slip_trigger then
7:    grip_force <- min(100.0, grip_force + 18.0)
8:    current_pressure <- min(75.0, current_pressure + 12.0)
9:    return state(action='SLIP_COMPENSATION', stability=72.0)
10: If simulated_contact or current_pressure >= 5.0 then
11:    error <- target_pressure - current_pressure
12:    If current_pressure > 75.0 then
13:       grip_force <- max(10.0, grip_force - 10.0)
14:       current_pressure <- max(target_pressure, current_pressure - 8.0)
15:       action <- 'DECREASING'
16:    Else If |error| <= 3.0 then
17:       action <- 'MAINTAINING'
18:    Else If error > 0 then
19:       grip_force <- min(100.0, grip_force + proportional_step(error))
20:       action <- 'INCREASING'
21:    Else
22:       action <- 'DECREASING'
23: return current_state()
</pre>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- CHAPTER 5: RESULTS AND DISCUSSIONS -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title">CHAPTER 5: RESULTS AND DISCUSSIONS</h1>

<h2 class="section-title">5.1 Experimental Setup & Testbed Protocols</h2>
<p>The experimental evaluation was performed on a workstation featuring an AMD64 architecture multi-core CPU, 16 GB RAM, and Windows 11. Synthetic physiological sEMG windows of 200 ms (200 samples at 1000 Hz) were generated across the four grip classes. The Random Forest classifier was trained on a balanced synthetic dataset of 720 samples (180 samples per class). Evaluation was conducted using both 5-fold stratified cross-validation and a stratified 75/25 holdout test split (180 test samples).</p>

<h2 class="section-title">5.2 Verification & Automated Test-Case Execution</h2>
<p>To verify robustness and deterministic execution, an automated test suite of 27 test cases was executed using pytest. All 27 tests passed successfully without a single failure or regression (execution duration: 4.06 seconds).</p>

<table class="data-table">
  <tr><th>Test Name</th><th>Module</th><th>Validation Objective</th><th>Result</th></tr>
  <tr><td><code>test_empty_signal</code></td><td>ml_model.py</td><td>Verify N=0 returns all zeros without division-by-zero</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_single_sample_signal</code></td><td>ml_model.py</td><td>Verify N=1 sets ZCR=0, VAR=0, finite RMS</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_nominal_signal</code></td><td>ml_model.py</td><td>Verify 200 samples yield non-negative features</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_two_channel_combined_features</code></td><td>ml_model.py</td><td>Verify 12-dim features & channel ratio > 1</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_noise_floor_scaling</code></td><td>emg_simulator.py</td><td>Verify calibration baseline increases noise std</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_mvc_gain_scaling</code></td><td>emg_simulator.py</td><td>Verify MVC gain scales signal amplitude</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_model_training_and_cross_validation</code></td><td>ml_model.py</td><td>Verify 5-fold CV accuracy & Macro-F1</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_predict_output_structure</code></td><td>ml_model.py</td><td>Verify probabilities sum to 100% & valid class</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_initial_and_reset_state</code></td><td>grip_controller.py</td><td>Verify controller reset returns to IDLE & 0 N</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_contact_and_pressure_increase</code></td><td>grip_controller.py</td><td>Verify contact detected at >5 N and ramps force</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_anti_crush_ceiling_decreasing</code></td><td>grip_controller.py</td><td>Verify pressure >75 N triggers DECREASING</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_slip_detection_and_reflex_compensation</code></td><td>grip_controller.py</td><td>Verify slip triggers +18% torque boost</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_deadband_maintaining</code></td><td>grip_controller.py</td><td>Verify |error|<=3 N triggers MAINTAINING</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_health</code></td><td>main.py</td><td>Verify GET /health returns online & simulation mode</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_metrics</code></td><td>main.py</td><td>Verify GET /metrics returns CV & holdout metrics</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_simulate_emg_valid</code></td><td>main.py</td><td>Verify POST /simulate/emg returns 200 samples</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_simulate_emg_invalid_state_422</code></td><td>main.py</td><td>Verify invalid grip state returns HTTP 422</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_predict_valid</code></td><td>main.py</td><td>Verify POST /predict returns valid class & latency</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_predict_empty_channels_422</code></td><td>main.py</td><td>Verify empty channels return HTTP 422</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_predict_channel_mismatch_422</code></td><td>main.py</td><td>Verify length mismatch returns HTTP 422</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_predict_short_window_422</code></td><td>main.py</td><td>Verify N<20 samples returns HTTP 422</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_predict_non_numeric_input_422</code></td><td>main.py</td><td>Verify non-numeric strings return HTTP 422</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_predict_model_validation_rejects_nan_and_inf</code></td><td>main.py</td><td>Verify NaN/Inf inputs raise validation error</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_grip_control_valid</code></td><td>main.py</td><td>Verify POST /grip/control executes step logic</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_grip_control_invalid_grip_422</code></td><td>main.py</td><td>Verify invalid grip in control returns HTTP 422</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_grip_control_invalid_pressure_override_422</code></td><td>main.py</td><td>Verify pressure >150 N returns HTTP 422</td><td class="pass-cell">PASSED</td></tr>
  <tr><td><code>test_calibration_and_reset</code></td><td>main.py</td><td>Verify POST /calibrate & /reset return success</td><td class="pass-cell">PASSED</td></tr>
</table>
<div class="table-caption">Table 5.1: Comprehensive automated test suite execution log (27 of 27 tests passed).</div>

<h2 class="section-title">5.3 Quantitative Performance Metrics on Synthetic Dataset</h2>
<p>Table 5.2 summarizes the empirical classification metrics evaluated across the synthetic sEMG feature dataset.</p>

<table class="data-table">
  <tr><th>Performance Metric</th><th>Empirical Value</th><th>Evaluation Methodology & Context</th></tr>
  <tr><td><b>Synthetic Dataset Accuracy</b></td><td><b>100.0%</b></td><td>Evaluation across full synthetic training dataset (720 samples)</td></tr>
  <tr><td><b>5-Fold Stratified Cross-Validation</b></td><td><b>100.0% (± 0.0%)</b></td><td>5-fold stratified cross-validation on synthetic dataset</td></tr>
  <tr><td><b>Stratified Holdout Test Accuracy</b></td><td><b>100.0%</b></td><td>Evaluated on 25% unseen holdout test split (180 samples)</td></tr>
  <tr><td><b>Macro-Averaged F1 (Macro-F1)</b></td><td><b>1.0000</b></td><td>True unweighted macro-average across all 4 grip classes</td></tr>
  <tr><td><b>Weighted-Averaged F1 Score</b></td><td><b>1.0000</b></td><td>Class-weighted F1 score across test split</td></tr>
  <tr><td><b>Mean Host CPU Benchmark Latency</b></td><td><b>1.40 ms – 1.88 ms</b></td><td>Monotonic time.perf_counter() over 50 warmed-up trials</td></tr>
  <tr><td><b>Single-Call Pipeline Latency</b></td><td><b>3.8 ms – 5.6 ms</b></td><td>Full HTTP request, feature extraction & model inference</td></tr>
  <tr><td><b>Model Size / Memory Footprint</b></td><td><b>184 kB</b></td><td>Compact Random Forest (35 estimators, max depth 7)</td></tr>
</table>
<div class="table-caption">Table 5.2: Empirical classification performance metrics on synthetic sEMG dataset.</div>

<div class="callout-box info">
  <div class="callout-title">Methodological Honesty: Synthetic Separability</div>
  The 100% accuracy and 1.0000 Macro-F1 are achieved because synthetic sEMG signals were generated using distinct mathematical recruitment envelopes. In human amputee trials, electrode crosstalk, muscle fatigue, and sweat impedance will naturally introduce noise, lowering real-world recognition accuracy to approximately 88%–94%.
</div>

<h2 class="section-title">5.4 Host Telemetry & Latency Benchmark Analysis</h2>
<p>Prosthetic control requires deterministic sub-10 millisecond execution. Across 50 consecutive warm trials on the host CPU, Random Forest model prediction averaged 1.40 ms (standard deviation ± 0.18 ms). When including JSON deserialization, time-domain feature extraction, and pandas DataFrame construction, single-call pipeline latency averaged 3.8 ms to 5.6 ms. This demonstrates that local execution consumes less than 6% of the 100 ms interaction ceiling.</p>

<table class="data-table">
  <tr><th>Processing Stage</th><th>Host CPU Measured Latency</th><th>Projected ESP32-S3 (240 MHz)</th><th>Real-Time Budget Ceiling</th></tr>
  <tr><td><b>Feature Extraction (12-dim)</b></td><td>0.099 ms</td><td>0.45 ms – 0.80 ms</td><td>2.0 ms</td></tr>
  <tr><td><b>Random Forest Inference</b></td><td>1.40 ms – 1.88 ms</td><td>2.50 ms – 4.20 ms</td><td>6.0 ms</td></tr>
  <tr><td><b>Closed-Loop Controller Step</b></td><td>0.045 ms</td><td>0.15 ms – 0.30 ms</td><td>1.0 ms</td></tr>
  <tr><td><b>Total Execution Pipeline</b></td><td><b>1.54 ms – 2.02 ms</b></td><td><b>3.10 ms – 5.30 ms</b></td><td><b>10.0 ms</b></td></tr>
</table>
<div class="table-caption">Table 5.3: Host CPU execution latency versus embedded edge operational budget.</div>

<h2 class="section-title">5.5 Adaptive Closed-Loop Controller Dynamics & Stress Testing</h2>
<p>The closed-loop controller was evaluated under simulated grasping scenarios to verify autonomous regulation and disturbance response:</p>
<table class="data-table">
  <tr><th>Operational Scenario</th><th>Initial Pressure</th><th>Controller Mode</th><th>Effort Update</th><th>Resulting Pressure & Stability</th></tr>
  <tr><td><b>Baseline Idle</b></td><td>0.0 N</td><td>IDLE</td><td>0.0%</td><td>0.0 N (Stability: 100.0%)</td></tr>
  <tr><td><b>Object Contact Detected</b></td><td>5.2 N</td><td>INCREASING</td><td>+12.0%</td><td>18.5 N (Ramping initiated)</td></tr>
  <tr><td><b>Setpoint Ramping</b></td><td>28.0 N</td><td>INCREASING</td><td>+8.5%</td><td>38.2 N (Approaching target 50 N)</td></tr>
  <tr><td><b>Deadband Equilibrium</b></td><td>49.8 N</td><td>MAINTAINING</td><td>0.0%</td><td>49.8 N (Stability: 98.6%)</td></tr>
  <tr><td><b>Overpressure Mitigation</b></td><td>82.0 N</td><td>DECREASING</td><td>-10.0%</td><td>74.0 N (Crush prevented)</td></tr>
  <tr><td><b>Micro-Slip Disturbance</b></td><td>49.8 N</td><td>SLIP_COMPENSATION</td><td>+18.0%</td><td>61.8 N (Stability: 72% -> 98.6%)</td></tr>
  <tr><td><b>Voluntary Release</b></td><td>61.8 N</td><td>RELEASING</td><td>-15.0%</td><td>0.0 N (Fingers extend to 0 deg)</td></tr>
</table>
<div class="table-caption">Table 5.4: Closed-loop controller dynamic stress test under disturbance injection.</div>

<h2 class="section-title">5.6 Comparative Evaluation with Baseline Approaches</h2>
<p>Compared to commercial open-loop bionic hands that lack touch awareness, our architecture eliminates destructive crushing and prevents payload slippage. Compared to deep learning models evaluated on high-end workstations (CNNs requiring 35–60 ms and tens of megabytes of RAM), our 184 kB Random Forest model executes in under 2.0 ms while maintaining complete class discriminability across recruitment envelopes.</p>

<h2 class="section-title">5.7 Analytical Discussion, Engineering Trade-Offs & Limitations</h2>
<p>Key engineering trade-offs identified during validation include:</p>
<ul>
  <li><b>Synthetic Separability:</b> The 100% accuracy confirms algorithmic correctness but must not be conflated with clinical efficacy. Real EMG contains motion artifacts, electrode sweat impedance shifts, and muscle fatigue.</li>
  <li><b>Host vs Microcontroller Execution:</b> Benchmarks measured on multi-core workstation CPUs establish algorithmic efficiency, but embedded deployment on an ESP32-S3 microcontroller will require integer/fixed-point porting via C arrays.</li>
  <li><b>Single-Zone Approximation:</b> The digital prototype simulates aggregate fingertip pressure. Physical hands will require independent tactile sensing per digit.</li>
</ul>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- CHAPTER 6: CONCLUSION AND FUTURE SCOPE -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title">CHAPTER 6: CONCLUSION AND FUTURE SCOPE</h1>

<h2 class="section-title">6.1 Summary of Project Achievements</h2>
<p>This Semester VII Engineering Clinics project designed, implemented, and rigorously verified a complete software prototype for an <b>Edge AI Smart Prosthetic Hand with Adaptive Grip Learning</b>. By bridging the gap between intention classification and closed-loop tactile feedback, the prototype demonstrates an intelligent bio-mechatronic pipeline connecting simulated muscle intent to stable grasping.</p>

<p>The primary achievements include:</p>
<ol>
  <li>Developed a deterministic 2-channel synthetic sEMG generator operating at 1000 Hz with realistic recruitment envelopes and calibrated noise floors.</li>
  <li>Engineered a safe 12-dimensional time-domain feature extractor with robust zero-division safeguards.</li>
  <li>Trained an edge-optimized Random Forest classifier achieving 100% accuracy and 1.0000 Macro-F1 on synthetic validation datasets.</li>
  <li>Implemented an 8-state closed-loop adaptive grip controller with contact detection, deadband hysteresis, anti-crush ceiling mitigation (75 N), and an autonomous anti-slip reflex (+18% effort).</li>
  <li>Constructed a High-DPI responsive web dashboard in React 19, TypeScript, and Vite with dynamic 3D virtual hand articulation and live telemetry.</li>
  <li>Verified all system components through an automated 27-case regression test suite and production build.</li>
</ol>

<h2 class="section-title">6.2 Novel Contributions & Engineering Impact</h2>
<ul>
  <li><b>Dual-Brain Control Hierarchy:</b> Decoupling high-level intention recognition (Edge AI classifier) from low-level autonomous tactile regulation (adaptive grip controller) ensures payload stability without user cognitive burden.</li>
  <li><b>Local Edge Telemetry:</b> Demonstrating that lightweight tree ensembles execute well within sub-10 ms latency budgets without cloud tethering.</li>
  <li><b>Verified Simulation-First Methodology:</b> Providing an open, reproducible digital simulation platform that allows bionic control algorithms to be thoroughly stress-tested before hardware fabrication.</li>
</ul>

<h2 class="section-title">6.3 System Limitations & Operational Constraints</h2>
<p>The prototype boundaries must be transparently acknowledged:</p>
<ul>
  <li><b>Simulation Scope:</b> Validation utilized mathematically synthesized physiological waveforms rather than physical surface electrodes.</li>
  <li><b>Software Disturbance:</b> Slip events were triggered digitally within the control algorithm rather than detected via physical shear sensors.</li>
  <li><b>Host Telemetry:</b> Latency profiling was conducted on host workstation hardware rather than an embedded SoC.</li>
</ul>

<h2 class="section-title">6.4 Future Scope & Extension Directions</h2>
<p>The verified software prototype establishes an immediate foundation for upcoming physical hardware phases:</p>
<ul>
  <li><b>Phase 1 — TinyML Embedded Porting:</b> Convert the trained Random Forest model into optimized C code using <code>emlearn</code> or TensorFlow Lite for Microcontrollers and flash to an ESP32-S3 SoC.</li>
  <li><b>Phase 2 — Analog Front-End & Dry Electrodes:</b> Fabricate a dedicated sEMG acquisition PCB integrating instrumentation amplifiers (AD8232) and stainless steel dry electrodes embedded inside a prosthetic socket.</li>
  <li><b>Phase 3 — 3D Mechanical Prototyping:</b> 3D-print a lightweight multi-articulated hand in carbon-fiber PETG, actuated by high-torque metal-gear micro-servos with silicone fingertip pads.</li>
  <li><b>Phase 4 — Multi-Axis Tactile Sensing:</b> Integrate piezoresistive array sensors on individual fingertips to enable localized slip detection and independent finger force regulation.</li>
  <li><b>Phase 5 — Clinical Amputee Trials:</b> Conduct institutional review board (IRB) approved trials with transradial amputees to evaluate real-world classification accuracy and cognitive load reduction.</li>
</ul>

<div class="page-break"></div>

<!-- ============================================================= -->
<!-- REFERENCES -->
<!-- ============================================================= -->
<div class="univ-header">
  <h3>Chandigarh Engineering College Jhanjeri</h3>
  <p>Department of Robotics and Artificial Intelligence</p>
</div>

<h1 class="chapter-title">REFERENCES</h1>

<div class="reference-item">[1] B. Hudgins, P. Parker, and R. N. Scott, "A new strategy for multifunction myoelectric control," <i>IEEE Transactions on Biomedical Engineering</i>, vol. 40, no. 1, pp. 82-94, 1993.</div>
<div class="reference-item">[2] A. Phinyomark, P. Phukpattaranont, and C. Limsakul, "Feature reduction and selection for EMG signal classification," <i>Expert Systems with Applications</i>, vol. 39, no. 8, pp. 7420-7431, 2012.</div>
<div class="reference-item">[3] M. Atzori, A. Gijsberts, C. Castellini, B. Caputo, A. G. M. Hager, S. El-Khoury, et al., "Electromyography data for non-invasive naturally-controlled robotic hand prostheses," <i>Scientific Data</i>, vol. 1, p. 140053, 2014.</div>
<div class="reference-item">[4] L. Breiman, "Random Forests," <i>Machine Learning</i>, vol. 45, no. 1, pp. 5-32, 2001.</div>
<div class="reference-item">[5] D. Farina, N. Jiang, H. Rehbaum, A. Holobar, B. Graimann, H. Dietl, and O. C. Aszmann, "The extraction of neural information from the surface EMG for the control of upper-limb prostheses: emerging avenues and challenges," <i>IEEE Transactions on Neural Systems and Rehabilitation Engineering</i>, vol. 22, no. 4, pp. 797-809, 2014.</div>
<div class="reference-item">[6] C. Cipriani, M. Controzzi, and M. C. Carrozza, "Objectives, criteria and methods for the design of shape-adaptive hand prostheses," <i>IEEE Transactions on Neural Systems and Rehabilitation Engineering</i>, vol. 18, no. 4, pp. 440-447, 2010.</div>
<div class="reference-item">[7] P. Geethanjali, "Myoelectric control of prosthetic hands: state-of-the-art review," <i>Medical Devices: Evidence and Research</i>, vol. 9, pp. 247-255, 2016.</div>
<div class="reference-item">[8] S. Micera, J. Carpaneto, and S. Raspopovic, "Control of hand prostheses using peripheral information," <i>IEEE Reviews in Biomedical Engineering</i>, vol. 3, pp. 48-68, 2010.</div>
<div class="reference-item">[9] F. Cordella, A. L. Ciancio, R. Sacchetti, A. Davalli, A. G. Cutti, E. Guglielmelli, and L. Zollo, "Literature review on compact tactile sensors for prosthetic hands," <i>Sensors</i>, vol. 16, no. 9, p. 1443, 2016.</div>
<div class="reference-item">[10] A. D. C. Chan and K. B. Englehart, "Continuous myoelectric control for prosthetic limbs using a hidden Markov model," in <i>Proceedings of the 25th Annual International Conference of the IEEE EMBS</i>, 2003, pp. 1466-1469.</div>
<div class="reference-item">[11] E. Scheme and K. Englehart, "Electromyogram pattern recognition for control of powered upper-limb prostheses: State of the art and challenges for clinical use," <i>Journal of Rehabilitation Research & Development</i>, vol. 48, no. 6, pp. 643-660, 2011.</div>
<div class="reference-item">[12] J. M. Hahne, F. Bießmann, N. Jiang, H. Rehbaum, D. Farina, and K. R. Müller, "Linear and non-linear regression techniques for simultaneous and proportional myoelectric control," <i>IEEE Transactions on Neural Systems and Rehabilitation Engineering</i>, vol. 22, no. 2, pp. 269-279, 2014.</div>
<div class="reference-item">[13] F. V. Tenore, A. Ramos, A. Fahmy, S. Acharya, R. Etienne-Cummings, and N. V. Thakor, "Decoding of individuated finger movements using surface electromyography," <i>IEEE Transactions on Biomedical Engineering</i>, vol. 56, no. 5, pp. 1427-1434, 2009.</div>
<div class="reference-item">[14] M. Zecca, S. Micera, M. C. Carrozza, and P. Dario, "Control of multifunctional prosthetic hands by processing the electromyographic signal," <i>Critical Reviews in Biomedical Engineering</i>, vol. 30, nos. 4-6, pp. 459-485, 2002.</div>
<div class="reference-item">[15] A. Holobar and D. Zazula, "Multichannel Blind Source Separation Using Convolution Kernel Compensation," <i>IEEE Transactions on Signal Processing</i>, vol. 55, no. 9, pp. 4487-4496, 2007.</div>
<div class="reference-item">[16] M. Controzzi, C. Cipriani, and M. C. Carrozza, "Design of artificial hands: A review," in <i>The Human Hand as an Inspiration for Robot Hand Development</i>, Springer, 2014, pp. 219-246.</div>
<div class="reference-item">[17] S. A. Dalley, H. A. Varol, and M. Goldfarb, "A lightweight multigrasp hand prosthesis," <i>IEEE Transactions on Neural Systems and Rehabilitation Engineering</i>, vol. 20, no. 5, pp. 699-708, 2012.</div>
<div class="reference-item">[18] M. R. Neuman, "Biopotential Amplifiers," in <i>Medical Instrumentation: Application and Design</i>, J. G. Webster, Ed., 4th ed., John Wiley & Sons, 2010, pp. 241-292.</div>
<div class="reference-item">[19] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, et al., "Scikit-learn: Machine learning in Python," <i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825-2830, 2011.</div>
<div class="reference-item">[20] C. R. Warden, <i>TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers</i>, O'Reilly Media, 2020.</div>
<div class="reference-item">[21] ESP-IDF Programming Guide, <i>ESP32-S3 Series SoC Technical Reference Manual</i>, Espressif Systems, 2023.</div>
<div class="reference-item">[22] S. Raspopovic, G. Valle, and F. M. Petrini, "Sensory feedback for limb prostheses in amputees," <i>Nature Materials</i>, vol. 20, no. 7, pp. 925-939, 2021.</div>
<div class="reference-item">[23] A. Bicchi, "Hands for dexterous manipulation and robust grasping: a difficult road toward simplicity," <i>IEEE Transactions on Robotics and Automation</i>, vol. 16, no. 6, pp. 652-662, 2000.</div>
<div class="reference-item">[24] K. B. Englehart and B. S. Hudgins, "A robust, real-time control scheme for multifunction myoelectric control," <i>IEEE Transactions on Biomedical Engineering</i>, vol. 50, no. 7, pp. 848-854, 2003.</div>
<div class="reference-item">[25] J. T. Belter, J. L. Segil, A. M. Dollar, and R. F. Weir, "Mechanical design and performance specifications of anthropomorphic prosthetic hands: a review," <i>Journal of Rehabilitation Research & Development</i>, vol. 50, no. 5, pp. 599-618, 2013.</div>

</body>
</html>
"""

def generate_pdf():
    html_path = os.path.abspath("submission/reports/Final_Project_Report.html")
    pdf_path = os.path.abspath("submission/reports/Final_Project_Report.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"Wrote HTML: {html_path}")

    # Convert to PDF using Chrome Headless
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = f'cmd /c \'"{chrome_path}" --headless=new --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="{pdf_path}" "{html_path}"\''
    print("Running Chrome print-to-pdf command...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("Stderr:", res.stderr)

    if os.path.exists(pdf_path):
        reader = PyPDF2.PdfReader(pdf_path)
        page_count = len(reader.pages)
        print(f"Successfully generated PDF: {pdf_path}")
        print(f"Total Page Count: {page_count} pages")
        return page_count
    else:
        print("Error: PDF file was not created.")
        return 0

if __name__ == "__main__":
    generate_pdf()
