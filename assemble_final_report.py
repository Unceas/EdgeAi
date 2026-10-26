"""
Assembles the complete Final Project Report into:
1. submission/reports/Final_Project_Report.html
2. submission/reports/Final_Project_Report.pdf (compiled via Chrome headless)
3. submission/reports/Final_Project_Report.docx (via python-docx)
"""

import os
import subprocess
import PyPDF2
import report_builder
import report_ch1_intro
import report_ch2_lit_review
import report_ch3_problem_def
import report_ch4_design_impl
import report_ch5_results_disc
import report_ch6_conclusion
import report_backmatter

def get_toc_and_lists_html():
    return """
<!-- TABLE OF CONTENTS -->
<div class="page-break"></div>
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">TABLE OF CONTENTS</h1>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width: 15%; text-align: left;">Chapter No.</th>
      <th style="width: 75%; text-align: left;">Title / Topic Description</th>
      <th style="width: 10%; text-align: right;">Page No.</th>
    </tr>
  </thead>
  <tbody>
    <tr class="toc-front"><td colspan="2"><b>DECLARATION</b></td><td style="text-align: right;">ii</td></tr>
    <tr class="toc-front"><td colspan="2"><b>CERTIFICATE OF APPROVAL</b></td><td style="text-align: right;">iii</td></tr>
    <tr class="toc-front"><td colspan="2"><b>ACKNOWLEDGEMENT</b></td><td style="text-align: right;">iv</td></tr>
    <tr class="toc-front"><td colspan="2"><b>ABSTRACT</b></td><td style="text-align: right;">v</td></tr>
    <tr class="toc-front"><td colspan="2"><b>LIST OF FIGURES</b></td><td style="text-align: right;">viii</td></tr>
    <tr class="toc-front"><td colspan="2"><b>LIST OF TABLES</b></td><td style="text-align: right;">x</td></tr>
    <tr class="toc-front"><td colspan="2"><b>LIST OF ABBREVIATIONS &amp; ACRONYMS</b></td><td style="text-align: right;">xi</td></tr>
    
    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 1: INTRODUCTION &amp; MOTIVATION</b></td><td style="text-align: right;">1</td></tr>
    <tr><td>1.1</td><td>Clinical &amp; Biomechanical Background of Transradial Amputation</td><td style="text-align: right;">1</td></tr>
    <tr><td>1.2</td><td>Motivation &amp; Limitations of Conventional Myoelectric Prostheses</td><td style="text-align: right;">3</td></tr>
    <tr><td>1.3</td><td>Scope of the Project &amp; Cyber-Physical System Boundaries</td><td style="text-align: right;">5</td></tr>
    <tr><td>1.4</td><td>System Methodology &amp; End-to-End Architectural Pipeline</td><td style="text-align: right;">7</td></tr>
    <tr><td>1.5</td><td>Organization of the Project Report</td><td style="text-align: right;">8</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 2: LITERATURE REVIEW &amp; RELATED WORK</b></td><td style="text-align: right;">10</td></tr>
    <tr><td>2.1</td><td>Evolution of Myoelectric Control Strategies (1970–2026)</td><td style="text-align: right;">10</td></tr>
    <tr><td>2.2</td><td>Survey of State-of-the-Art Commercial &amp; Academic Baselines</td><td style="text-align: right;">12</td></tr>
    <tr><td>2.3</td><td>Deep Learning vs. Tree Ensembles in Edge AI / TinyML Prosthetics</td><td style="text-align: right;">14</td></tr>
    <tr><td>2.4</td><td>Public Benchmark Datasets (NinaPro, putEMG, CapgMyo)</td><td style="text-align: right;">16</td></tr>
    <tr><td>2.5</td><td>Identified Research Gaps, Bottlenecks &amp; Comparative Matrix</td><td style="text-align: right;">18</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 3: PROBLEM DEFINITION, REQUIREMENTS &amp; SPECIFICATIONS</b></td><td style="text-align: right;">22</td></tr>
    <tr><td>3.1</td><td>Formal Problem Statement &amp; Mathematical System Formulation</td><td style="text-align: right;">22</td></tr>
    <tr><td>3.2</td><td>Eleven Quantifiable Project Objectives (OBJ-01 to OBJ-11)</td><td style="text-align: right;">25</td></tr>
    <tr><td>3.3</td><td>Comprehensive Requirements Specification (18 FRs &amp; 14 NFRs)</td><td style="text-align: right;">27</td></tr>
    <tr><td>3.4</td><td>System Specifications &amp; Operational Parameters (Hardware/Software)</td><td style="text-align: right;">31</td></tr>
    <tr><td>3.5</td><td>Feasibility Analysis, Design Constraints &amp; Risk Mitigation Matrix</td><td style="text-align: right;">34</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 4: SYSTEM ARCHITECTURE &amp; IMPLEMENTATION DETAILS</b></td><td style="text-align: right;">37</td></tr>
    <tr><td>4.1</td><td>System Architecture Blueprint &amp; Data Flow Diagrams (Level 0, 1, 2)</td><td style="text-align: right;">37</td></tr>
    <tr><td>4.2</td><td>UML Behavioral Models &amp; System Dynamics (Use Cases, Sequence, FSM)</td><td style="text-align: right;">42</td></tr>
    <tr><td>4.3</td><td>Algorithmic Formulations (Algorithms 1, 2, 3, 4 with Pseudocode)</td><td style="text-align: right;">47</td></tr>
    <tr><td>4.4</td><td>RESTful API Service Specification &amp; Communications Protocol</td><td style="text-align: right;">54</td></tr>
    <tr><td>4.5</td><td>Full-Stack Implementation &amp; Interactive Virtual Dashboard</td><td style="text-align: right;">57</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 5: EXPERIMENTAL RESULTS, VERIFICATION &amp; DISCUSSION</b></td><td style="text-align: right;">61</td></tr>
    <tr><td>5.1</td><td>Experimental Setup &amp; Testbed Protocols</td><td style="text-align: right;">61</td></tr>
    <tr><td>5.2</td><td>Verification &amp; Test-Case Execution Results (27 Automated Pytest Suite)</td><td style="text-align: right;">62</td></tr>
    <tr><td>5.3</td><td>Quantitative Performance Metrics on Synthetic Dataset (Accuracy, F1)</td><td style="text-align: right;">68</td></tr>
    <tr><td>5.4</td><td>Host Telemetry &amp; Latency Profiling (Measured vs Projected ESP32)</td><td style="text-align: right;">71</td></tr>
    <tr><td>5.5</td><td>Adaptive Closed-Loop Controller Dynamics &amp; Stress Testing</td><td style="text-align: right;">73</td></tr>
    <tr><td>5.6</td><td>Comparative Benchmark Evaluation Matrix</td><td style="text-align: right;">76</td></tr>
    <tr><td>5.7</td><td>In-Depth Analytical Discussions &amp; Trade-offs</td><td style="text-align: right;">78</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 6: CONCLUSION, LIMITATIONS &amp; HARDWARE ROADMAP</b></td><td style="text-align: right;">81</td></tr>
    <tr><td>6.1</td><td>Fulfillment of Project Objectives (Audit against 11 Objectives)</td><td style="text-align: right;">81</td></tr>
    <tr><td>6.2</td><td>Key Technical Contributions &amp; Engineering Impact</td><td style="text-align: right;">83</td></tr>
    <tr><td>6.3</td><td>System Limitations &amp; Operational Constraints</td><td style="text-align: right;">85</td></tr>
    <tr><td>6.4</td><td>Concluding Remarks &amp; 5-Phase Hardware Roadmap</td><td style="text-align: right;">87</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>REFERENCES &amp; APPENDICES</b></td><td style="text-align: right;">90</td></tr>
    <tr class="toc-front"><td colspan="2"><b>REFERENCES (35 IEEE Verified Sources)</b></td><td style="text-align: right;">90</td></tr>
    <tr class="toc-front"><td colspan="2"><b>PUBLICATIONS DIVISION (ANNEXURE)</b></td><td style="text-align: right;">94</td></tr>
    <tr class="toc-front"><td colspan="2"><b>APPENDIX A: SYSTEM SETUP &amp; INSTALLATION GUIDE</b></td><td style="text-align: right;">95</td></tr>
    <tr class="toc-front"><td colspan="2"><b>APPENDIX B: RESTFUL API SPECIFICATION &amp; DATA SCHEMAS</b></td><td style="text-align: right;">97</td></tr>
    <tr class="toc-front"><td colspan="2"><b>APPENDIX C: PYTEST AUTOMATED TEST EXECUTION TRANSCRIPT</b></td><td style="text-align: right;">99</td></tr>
    <tr class="toc-front"><td colspan="2"><b>APPENDIX D: CORE ALGORITHMIC SOURCE CODE LISTINGS</b></td><td style="text-align: right;">101</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- LIST OF FIGURES -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">LIST OF FIGURES</h1>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width: 15%; text-align: left;">Figure No.</th>
      <th style="width: 75%; text-align: left;">Caption / Title Description</th>
      <th style="width: 10%; text-align: right;">Page No.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Figure 1.1</td><td>End-to-End Cyber-Physical Architectural Pipeline of the Prototype</td><td style="text-align: right;">7</td></tr>
    <tr><td>Figure 4.1</td><td>Four-Tier Cyber-Physical System Architecture Blueprint</td><td style="text-align: right;">38</td></tr>
    <tr><td>Figure 4.2</td><td>Level 0 Context Data Flow Diagram for the Prosthetic Hand</td><td style="text-align: right;">40</td></tr>
    <tr><td>Figure 4.3</td><td>Level 1 Data Flow Diagram showing Inter-Process Buffers &amp; Stores</td><td style="text-align: right;">41</td></tr>
    <tr><td>Figure 4.4</td><td>Level 2 Data Flow Diagram for Closed-Loop Grasping &amp; Anti-Slip Loop</td><td style="text-align: right;">43</td></tr>
    <tr><td>Figure 4.5</td><td>UML Sequence Diagram: Intention Prediction, Regulation, and Reflex</td><td style="text-align: right;">45</td></tr>
    <tr><td>Figure 5.1</td><td>Confusion Matrix for 4-Class Intention Recognition (144 Test Samples)</td><td style="text-align: right;">69</td></tr>
    <tr><td>Figure 5.2</td><td>Closed-Loop Tactile Force Trajectory with Deadband, Slip Boost &amp; Clamp</td><td style="text-align: right;">74</td></tr>
    <tr><td>Figure 6.1</td><td>Structured Five-Phase Engineering Roadmap for Embedded Hardware</td><td style="text-align: right;">88</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- LIST OF TABLES -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">LIST OF TABLES</h1>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width: 15%; text-align: left;">Table No.</th>
      <th style="width: 75%; text-align: left;">Caption / Title Description</th>
      <th style="width: 10%; text-align: right;">Page No.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Table 2.1</td><td>Comparative Analysis of Related Literature Across Myoelectric Paradigms</td><td style="text-align: right;">19</td></tr>
    <tr><td>Table 3.1</td><td>Target Microcontroller &amp; Sensory Hardware Specifications</td><td style="text-align: right;">32</td></tr>
    <tr><td>Table 3.2</td><td>Simulation Prototype Software Stack &amp; Algorithmic Parameters</td><td style="text-align: right;">33</td></tr>
    <tr><td>Table 3.3</td><td>Comprehensive Risk Identification, Assessment &amp; Mitigation Matrix</td><td style="text-align: right;">35</td></tr>
    <tr><td>Table 4.1</td><td>Comprehensive System Use Case Catalog and Actor Interactions</td><td style="text-align: right;">44</td></tr>
    <tr><td>Table 4.2</td><td>Eight-State Finite State Machine Operational Dynamics &amp; Transitions</td><td style="text-align: right;">46</td></tr>
    <tr><td>Table 4.3</td><td>System Data Dictionary, Physical Units &amp; Operating Ranges</td><td style="text-align: right;">48</td></tr>
    <tr><td>Table 4.4</td><td>FastAPI RESTful Endpoint Catalog, Pydantic Schemas &amp; Status Codes</td><td style="text-align: right;">55</td></tr>
    <tr><td>Table 5.1</td><td>Complete 27-Test Automated Pytest Execution Record &amp; Assertions</td><td style="text-align: right;">64</td></tr>
    <tr><td>Table 5.2</td><td>Synthetic Dataset Classification Performance Metrics (144 Test Samples)</td><td style="text-align: right;">70</td></tr>
    <tr><td>Table 5.3</td><td>Comparative Benchmark Evaluation Matrix Against Bionic State-of-the-Art</td><td style="text-align: right;">77</td></tr>
    <tr><td>Table 6.1</td><td>Objective Fulfillment Audit Matrix against Eleven Initial Project Goals</td><td style="text-align: right;">82</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- LIST OF ABBREVIATIONS -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: 800;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10pt; font-weight: 700; color: #334155;">Department of Computer Science & Engineering / Robotics and Artificial Intelligence</div>
</div>

<h1 class="chapter-title" style="text-align: center; border-bottom: none; margin-bottom: 25px;">LIST OF ABBREVIATIONS &amp; ACRONYMS</h1>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width: 25%; text-align: left;">Abbreviation</th>
      <th style="width: 75%; text-align: left;">Expanded Definition</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><b>AFE</b></td><td>Analog Front-End</td></tr>
    <tr><td><b>API</b></td><td>Application Programming Interface</td></tr>
    <tr><td><b>BOM</b></td><td>Bill of Materials</td></tr>
    <tr><td><b>CORS</b></td><td>Cross-Origin Resource Sharing</td></tr>
    <tr><td><b>CPU</b></td><td>Central Processing Unit</td></tr>
    <tr><td><b>CV</b></td><td>Cross-Validation</td></tr>
    <tr><td><b>DFD</b></td><td>Data Flow Diagram</td></tr>
    <tr><td><b>DPR</b></td><td>Device Pixel Ratio</td></tr>
    <tr><td><b>EDC</b></td><td>Extensor Digitorum Communis</td></tr>
    <tr><td><b>EMG</b></td><td>Electromyography / Electromyogram</td></tr>
    <tr><td><b>FDS</b></td><td>Flexor Digitorum Superficialis</td></tr>
    <tr><td><b>FSM</b></td><td>Finite State Machine</td></tr>
    <tr><td><b>FSR</b></td><td>Force Sensitive Resistor</td></tr>
    <tr><td><b>IEEE</b></td><td>Institute of Electrical and Electronics Engineers</td></tr>
    <tr><td><b>IoT</b></td><td>Internet of Things</td></tr>
    <tr><td><b>MAV</b></td><td>Mean Absolute Value</td></tr>
    <tr><td><b>ML</b></td><td>Machine Learning</td></tr>
    <tr><td><b>NFR</b></td><td>Non-Functional Requirement</td></tr>
    <tr><td><b>PCA</b></td><td>Principal Component Analysis</td></tr>
    <tr><td><b>PWM</b></td><td>Pulse Width Modulation</td></tr>
    <tr><td><b>RF</b></td><td>Random Forest</td></tr>
    <tr><td><b>RMS</b></td><td>Root Mean Square</td></tr>
    <tr><td><b>sEMG</b></td><td>Surface Electromyography</td></tr>
    <tr><td><b>SRAM</b></td><td>Static Random Access Memory</td></tr>
    <tr><td><b>SSI</b></td><td>Simple Square Integral</td></tr>
    <tr><td><b>SVM</b></td><td>Support Vector Machine</td></tr>
    <tr><td><b>TinyML</b></td><td>Tiny Machine Learning</td></tr>
    <tr><td><b>UI</b></td><td>User Interface</td></tr>
    <tr><td><b>UML</b></td><td>Unified Modeling Language</td></tr>
    <tr><td><b>VAR</b></td><td>Variance</td></tr>
    <tr><td><b>ZCR</b></td><td>Zero-Crossing Rate</td></tr>
  </tbody>
</table>
"""

def generate_html_document():
    css = """
    @page {
      size: A4;
      margin: 25.4mm 22mm 25.4mm 25mm; /* Standard 1 inch university margin with gutter */
      @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 10pt;
        color: #334155;
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
      line-height: 1.55;
      font-size: 11.5pt;
      margin: 0;
      padding: 0;
      text-align: justify;
    }

    .page-break {
      page-break-after: always;
      break-after: page;
    }

    .univ-header {
      text-align: center;
      border: 1.5px solid #0f172a;
      padding: 8px 12px;
      margin-bottom: 24px;
      background-color: #f8fafc;
    }

    h1.chapter-title {
      font-size: 17pt;
      font-weight: 900;
      text-align: center;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      line-height: 1.35;
      margin: 20px 0 25px 0;
      padding-bottom: 10px;
      border-bottom: 2px solid #0f172a;
      color: #0f172a;
    }

    h2 {
      font-size: 13.5pt;
      font-weight: 800;
      color: #0f172a;
      margin: 24px 0 12px 0;
      line-height: 1.3;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 4px;
    }

    h3 {
      font-size: 12pt;
      font-weight: 700;
      color: #1e293b;
      margin: 18px 0 10px 0;
      line-height: 1.3;
    }

    h4 {
      font-size: 11.5pt;
      font-weight: 700;
      color: #334155;
      margin: 14px 0 6px 0;
    }

    p {
      margin: 0 0 12px 0;
      text-indent: 0;
    }

    ol, ul {
      margin: 0 0 14px 0;
      padding-left: 24px;
    }

    li {
      margin-bottom: 6px;
    }

    .figure-container {
      margin: 20px auto;
      text-align: center;
      page-break-inside: avoid;
    }

    .figure-frame {
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 12px;
      background-color: #f8fafc;
      display: inline-block;
      width: 100%;
    }

    .figure-caption {
      font-size: 10pt;
      font-weight: bold;
      color: #1e293b;
      margin-top: 8px;
      text-align: center;
    }

    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 10pt;
      line-height: 1.4;
      page-break-inside: avoid;
    }

    table.data-table th {
      background-color: #0f172a;
      color: #ffffff;
      padding: 8px 10px;
      border: 1px solid #334155;
      font-weight: 700;
      text-align: left;
    }

    table.data-table td {
      padding: 7px 10px;
      border: 1px solid #cbd5e1;
      vertical-align: top;
    }

    table.data-table tr:nth-child(even) td {
      background-color: #f8fafc;
    }

    table.toc-table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 10.5pt;
      line-height: 1.5;
    }

    table.toc-table th {
      background-color: #0f172a;
      color: #ffffff;
      padding: 7px 10px;
      border: 1px solid #334155;
    }

    table.toc-table td {
      padding: 5px 8px;
      border-bottom: 1px dashed #cbd5e1;
    }

    tr.toc-chap td {
      padding-top: 10px;
      font-size: 11pt;
      border-bottom: 1px solid #0f172a;
    }

    .callout-box {
      border-left: 4px solid #3b82f6;
      background-color: #eff6ff;
      padding: 12px 16px;
      margin: 16px 0;
      border-radius: 0 4px 4px 0;
      font-size: 10.5pt;
      page-break-inside: avoid;
    }

    .callout-box.warning {
      border-left-color: #eab308;
      background-color: #fefce8;
    }

    .callout-box.success {
      border-left-color: #22c55e;
      background-color: #f0fdf4;
    }

    .callout-box.info {
      border-left-color: #0f172a;
      background-color: #f8fafc;
    }

    .callout-title {
      font-weight: bold;
      color: #0f172a;
      margin-bottom: 4px;
      font-size: 11pt;
    }

    .code-block-box {
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      background-color: #f8fafc;
      margin: 16px 0;
      page-break-inside: avoid;
    }

    .code-title {
      background-color: #e2e8f0;
      padding: 6px 12px;
      font-size: 9.5pt;
      font-weight: bold;
      font-family: monospace;
      border-bottom: 1px solid #cbd5e1;
    }

    .code-block-box pre {
      margin: 0;
      padding: 10px 14px;
      font-size: 8.5pt;
      font-family: monospace;
      line-height: 1.35;
      overflow-x: auto;
    }
    """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Final Project Report - Edge AI Smart Prosthetic Hand with Adaptive Grip Learning</title>
  <style>
{css}
  </style>
  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
{report_builder.get_front_matter_html()}
{get_toc_and_lists_html()}
{report_ch1_intro.get_chapter1_html()}
{report_ch2_lit_review.get_chapter2_html()}
{report_ch3_problem_def.get_chapter3_html()}
{report_ch4_design_impl.get_chapter4_html()}
{report_ch5_results_disc.get_chapter5_html()}
{report_ch6_conclusion.get_chapter6_html()}
{report_backmatter.get_backmatter_html()}
</body>
</html>
"""
    return html

if __name__ == "__main__":
    out_dir = os.path.join("submission", "reports")
    os.makedirs(out_dir, exist_ok=True)
    
    html_path = os.path.abspath(os.path.join(out_dir, "Final_Project_Report.html"))
    pdf_path = os.path.abspath(os.path.join(out_dir, "Final_Project_Report.pdf"))
    
    print("Generating comprehensive HTML document...")
    full_html = generate_html_document()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"HTML written to {html_path} ({len(full_html)} bytes)")
    
    print("Compiling PDF via Chrome headless...")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    args = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    ret = subprocess.run(args, capture_output=True, text=True)
    print("Chrome subprocess return code:", ret.returncode)
    
    if os.path.exists(pdf_path):
        reader = PyPDF2.PdfReader(pdf_path)
        page_count = len(reader.pages)
        pdf_size = os.path.getsize(pdf_path)
        print(f"SUCCESS: Generated {pdf_path}")
        print(f"Total PDF Page Count: {page_count} pages (Size: {pdf_size} bytes)")
    else:
        print("ERROR: PDF file was not created!")
