"""
Assembles the complete Final Project Report into:
1. submission/reports/Final_Project_Report.html
2. submission/reports/Final_Project_Report.pdf (compiled via Chrome headless)
3. submission/reports/Final_Project_Report.docx (via python-docx)

Adheres strictly to Chandigarh Engineering College Jhanjeri / IKGPTU Jalandhar guidelines:
- Fonts: Times New Roman, 12pt body, 16pt/14pt/12pt headings
- Margins: Left 2.75cm, Top 2.5cm, Right 1.25cm, Bottom 1.25cm
- Spacing: 1.5 line spacing
- Logos: Embedded CEC Logo and PTU Logo
- Running Header: CEC Jhanjeri, Mohali / Department of Computer Science and Engineering
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
  <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10.5pt; font-weight: bold; color: #334155;">Department of Computer Science and Engineering</div>
</div>

<h1 style="font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 25px; border-bottom: 1.5px solid #0f172a; padding-bottom: 6px;">TABLE OF CONTENTS</h1>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width: 80%; text-align: left;">PARTICULARS</th>
      <th style="width: 20%; text-align: right;">PAGE NO.</th>
    </tr>
  </thead>
  <tbody>
    <tr class="toc-front"><td><b>Title Page</b></td><td style="text-align: right;">I</td></tr>
    <tr class="toc-front"><td><b>Declaration by the Candidate</b></td><td style="text-align: right;">II</td></tr>
    <tr class="toc-front"><td><b>Acknowledgement</b></td><td style="text-align: right;">III</td></tr>
    <tr class="toc-front"><td><b>Table of Contents</b></td><td style="text-align: right;">IV – V</td></tr>
    <tr class="toc-front"><td><b>Abstract</b></td><td style="text-align: right;">VI</td></tr>
    <tr class="toc-front"><td><b>List of Figures</b></td><td style="text-align: right;">VII – VIII</td></tr>
    <tr class="toc-front"><td><b>List of Tables</b></td><td style="text-align: right;">IX – X</td></tr>
    
    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 1: INTRODUCTION</b></td></tr>
    <tr><td style="padding-left: 20px;">1.1 Technical Background &amp; Domain Overview</td><td style="text-align: right;">1</td></tr>
    <tr><td style="padding-left: 20px;">1.2 Motivation &amp; Engineering Need</td><td style="text-align: right;">4</td></tr>
    <tr><td style="padding-left: 20px;">1.3 Project Scope &amp; System Boundaries</td><td style="text-align: right;">6</td></tr>
    <tr><td style="padding-left: 35px;">1.3.1 In-Scope Deliverables</td><td style="text-align: right;">7</td></tr>
    <tr><td style="padding-left: 35px;">1.3.2 Out-of-Scope Limitations &amp; Assumptions</td><td style="text-align: right;">8</td></tr>
    <tr><td style="padding-left: 20px;">1.4 Proposed System Overview &amp; High-Level Methodology</td><td style="text-align: right;">10</td></tr>
    <tr><td style="padding-left: 35px;">1.4.1 Architectural Breakdown &amp; Key Modules</td><td style="text-align: right;">11</td></tr>
    <tr><td style="padding-left: 35px;">1.4.2 Functional Boundaries &amp; Assumptions</td><td style="text-align: right;">12</td></tr>
    <tr><td style="padding-left: 35px;">1.4.3 Chapter Organization of the Report</td><td style="text-align: right;">13</td></tr>
    <tr><td style="padding-left: 20px;">1.5 Chapter Roadmap</td><td style="text-align: right;">13</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 2: REVIEW OF LITERATURE</b></td></tr>
    <tr><td style="padding-left: 20px;">2.1 Historical Evolution &amp; Baseline Approaches</td><td style="text-align: right;">14</td></tr>
    <tr><td style="padding-left: 20px;">2.2 Critical Survey of Existing Frameworks &amp; Systems</td><td style="text-align: right;">19</td></tr>
    <tr><td style="padding-left: 35px;">2.2.1 Classical &amp; Algorithmic Methodologies</td><td style="text-align: right;">21</td></tr>
    <tr><td style="padding-left: 35px;">2.2.2 Modern Learning-Based / Advanced Systems</td><td style="text-align: right;">25</td></tr>
    <tr><td style="padding-left: 20px;">2.3 Evaluation of Benchmark Datasets &amp; Commercial Solutions</td><td style="text-align: right;">30</td></tr>
    <tr><td style="padding-left: 20px;">2.4 Identification of Research Gaps &amp; Bottlenecks</td><td style="text-align: right;">34</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 3: PROBLEM DEFINITION AND OBJECTIVES</b></td></tr>
    <tr><td style="padding-left: 20px;">3.1 Problem Statement</td><td style="text-align: right;">37</td></tr>
    <tr><td style="padding-left: 20px;">3.2 Quantifiable Project Objectives</td><td style="text-align: right;">39</td></tr>
    <tr><td style="padding-left: 20px;">3.3 Requirements Analysis</td><td style="text-align: right;">42</td></tr>
    <tr><td style="padding-left: 35px;">3.3.1 Functional Requirements</td><td style="text-align: right;">43</td></tr>
    <tr><td style="padding-left: 35px;">3.3.2 Non-Functional Requirements</td><td style="text-align: right;">46</td></tr>
    <tr><td style="padding-left: 20px;">3.4 Hardware, Software &amp; Environmental Specifications</td><td style="text-align: right;">48</td></tr>
    <tr><td style="padding-left: 20px;">3.5 System Feasibility Analysis</td><td style="text-align: right;">50</td></tr>
    <tr><td style="padding-left: 35px;">3.5.1 Technical Feasibility</td><td style="text-align: right;">51</td></tr>
    <tr><td style="padding-left: 35px;">3.5.2 Operational &amp; Economic Feasibility</td><td style="text-align: right;">52</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 4: DESIGN AND IMPLEMENTATION</b></td></tr>
    <tr><td style="padding-left: 20px;">4.1 System Architecture &amp; High-Level Design</td><td style="text-align: right;">54</td></tr>
    <tr><td style="padding-left: 35px;">4.1.1 Architectural Block Diagram</td><td style="text-align: right;">55</td></tr>
    <tr><td style="padding-left: 35px;">4.1.2 Data Flow Diagrams (DFDs)</td><td style="text-align: right;">57</td></tr>
    <tr><td style="padding-left: 20px;">4.2 Detailed Modeling &amp; Schemas</td><td style="text-align: right;">60</td></tr>
    <tr><td style="padding-left: 35px;">4.2.1 UML Behavioral &amp; Structural Models</td><td style="text-align: right;">61</td></tr>
    <tr><td style="padding-left: 35px;">4.2.2 Database Design &amp; Data Dictionary</td><td style="text-align: right;">63</td></tr>
    <tr><td style="padding-left: 20px;">4.3 Module-Wise Implementation Details</td><td style="text-align: right;">65</td></tr>
    <tr><td style="padding-left: 35px;">4.3.1 Data Acquisition &amp; Preprocessing Engine</td><td style="text-align: right;">66</td></tr>
    <tr><td style="padding-left: 35px;">4.3.2 Core Algorithms &amp; Pseudocode</td><td style="text-align: right;">68</td></tr>
    <tr><td style="padding-left: 35px;">4.3.3 API Integrations &amp; Security Mechanisms</td><td style="text-align: right;">72</td></tr>
    <tr><td style="padding-left: 20px;">4.4 Environment Configuration &amp; Build Setup</td><td style="text-align: right;">74</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 5: RESULTS AND DISCUSSIONS</b></td></tr>
    <tr><td style="padding-left: 20px;">5.1 Experimental Setup &amp; Testbed Protocols</td><td style="text-align: right;">76</td></tr>
    <tr><td style="padding-left: 20px;">5.2 Verification &amp; Test-Case Execution</td><td style="text-align: right;">77</td></tr>
    <tr><td style="padding-left: 20px;">5.3 Quantitative Performance Metrics</td><td style="text-align: right;">81</td></tr>
    <tr><td style="padding-left: 35px;">5.3.1 Empirical Metric Tabulation</td><td style="text-align: right;">82</td></tr>
    <tr><td style="padding-left: 35px;">5.3.2 Stress &amp; Load Evaluation</td><td style="text-align: right;">84</td></tr>
    <tr><td style="padding-left: 20px;">5.4 Comparative Analysis with Baseline Approaches</td><td style="text-align: right;">86</td></tr>
    <tr><td style="padding-left: 20px;">5.5 Analytical Discussion &amp; Engineering Trade-Offs</td><td style="text-align: right;">88</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>CHAPTER 6: CONCLUSION AND FUTURE SCOPE</b></td></tr>
    <tr><td style="padding-left: 20px;">6.1 Summary of Project Achievements</td><td style="text-align: right;">90</td></tr>
    <tr><td style="padding-left: 20px;">6.2 Novel Contributions &amp; Engineering Impact</td><td style="text-align: right;">92</td></tr>
    <tr><td style="padding-left: 20px;">6.3 System Limitations &amp; Operational Constraints</td><td style="text-align: right;">94</td></tr>
    <tr><td style="padding-left: 20px;">6.4 Future Scope &amp; Extension Directions</td><td style="text-align: right;">95</td></tr>

    <tr class="toc-chap"><td colspan="2"><b>REFERENCES &amp; PUBLICATIONS</b></td></tr>
    <tr class="toc-front"><td><b>REFERENCES (35 IEEE Verified Sources)</b></td><td style="text-align: right;">98</td></tr>
    <tr class="toc-front"><td><b>PUBLICATIONS (IEEE Reprints &amp; Acceptance Letters)</b></td><td style="text-align: right;">102</td></tr>
    <tr class="toc-front"><td><b>APPENDIX A: SYSTEM SETUP &amp; INSTALLATION GUIDE</b></td><td style="text-align: right;">103</td></tr>
    <tr class="toc-front"><td><b>APPENDIX B: RESTFUL API SPECIFICATION &amp; DATA SCHEMAS</b></td><td style="text-align: right;">105</td></tr>
    <tr class="toc-front"><td><b>APPENDIX C: PYTEST AUTOMATED TEST EXECUTION TRANSCRIPT</b></td><td style="text-align: right;">107</td></tr>
    <tr class="toc-front"><td><b>APPENDIX D: CORE SOURCE CODE LISTINGS</b></td><td style="text-align: right;">109</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- LIST OF FIGURES -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10.5pt; font-weight: bold; color: #334155;">Department of Computer Science and Engineering</div>
</div>

<h1 style="font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 25px; border-bottom: 1.5px solid #0f172a; padding-bottom: 6px;">LIST OF FIGURES</h1>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width: 15%; text-align: left;">FIGURE NO.</th>
      <th style="width: 70%; text-align: left;">FIGURE TITLE / DESCRIPTION</th>
      <th style="width: 15%; text-align: right;">PAGE NO.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Figure 1.1</td><td>End-to-End Cyber-Physical Architectural Pipeline of the Prototype</td><td style="text-align: right;">11</td></tr>
    <tr><td>Figure 4.1</td><td>Four-Tier Cyber-Physical System Architecture Blueprint</td><td style="text-align: right;">56</td></tr>
    <tr><td>Figure 4.2</td><td>Level 0 Context Data Flow Diagram for the Prosthetic Hand</td><td style="text-align: right;">58</td></tr>
    <tr><td>Figure 4.3</td><td>Level 1 Data Flow Diagram showing Inter-Process Buffers &amp; Stores</td><td style="text-align: right;">59</td></tr>
    <tr><td>Figure 4.4</td><td>Level 2 Data Flow Diagram for Closed-Loop Grasping &amp; Anti-Slip Loop</td><td style="text-align: right;">60</td></tr>
    <tr><td>Figure 4.5</td><td>UML Sequence Diagram: Intention Prediction, Regulation, and Reflex</td><td style="text-align: right;">62</td></tr>
    <tr><td>Figure 5.1</td><td>Confusion Matrix for 4-Class Intention Recognition (144 Test Samples)</td><td style="text-align: right;">83</td></tr>
    <tr><td>Figure 5.2</td><td>Closed-Loop Tactile Force Trajectory with Deadband, Slip Boost &amp; Clamp</td><td style="text-align: right;">85</td></tr>
    <tr><td>Figure 6.1</td><td>Structured Five-Phase Engineering Roadmap for Embedded Hardware</td><td style="text-align: right;">96</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- LIST OF TABLES -->
<div class="univ-header">
  <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI</div>
  <div style="font-size: 10.5pt; font-weight: bold; color: #334155;">Department of Computer Science and Engineering</div>
</div>

<h1 style="font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 25px; border-bottom: 1.5px solid #0f172a; padding-bottom: 6px;">LIST OF TABLES</h1>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width: 15%; text-align: left;">TABLE NO.</th>
      <th style="width: 70%; text-align: left;">TABLE TITLE / DESCRIPTION</th>
      <th style="width: 15%; text-align: right;">PAGE NO.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Table 2.1</td><td>Comparative Analysis of Related Literature Across Myoelectric Paradigms</td><td style="text-align: right;">35</td></tr>
    <tr><td>Table 3.1</td><td>Target Microcontroller &amp; Sensory Hardware Specifications</td><td style="text-align: right;">49</td></tr>
    <tr><td>Table 3.2</td><td>Simulation Prototype Software Stack &amp; Algorithmic Parameters</td><td style="text-align: right;">50</td></tr>
    <tr><td>Table 3.3</td><td>Comprehensive Risk Identification, Assessment &amp; Mitigation Matrix</td><td style="text-align: right;">53</td></tr>
    <tr><td>Table 4.1</td><td>Comprehensive System Use Case Catalog and Actor Interactions</td><td style="text-align: right;">61</td></tr>
    <tr><td>Table 4.2</td><td>Eight-State Finite State Machine Operational Dynamics &amp; Transitions</td><td style="text-align: right;">63</td></tr>
    <tr><td>Table 4.3</td><td>System Data Dictionary, Physical Units &amp; Operating Ranges</td><td style="text-align: right;">64</td></tr>
    <tr><td>Table 4.4</td><td>FastAPI RESTful Endpoint Catalog, Pydantic Schemas &amp; Status Codes</td><td style="text-align: right;">73</td></tr>
    <tr><td>Table 5.1</td><td>Complete 27-Test Automated Pytest Execution Record &amp; Assertions</td><td style="text-align: right;">78</td></tr>
    <tr><td>Table 5.2</td><td>Synthetic Dataset Classification Performance Metrics (144 Test Samples)</td><td style="text-align: right;">84</td></tr>
    <tr><td>Table 5.3</td><td>Comparative Benchmark Evaluation Matrix Against Bionic State-of-the-Art</td><td style="text-align: right;">87</td></tr>
    <tr><td>Table 6.1</td><td>Objective Fulfillment Audit Matrix against Eleven Initial Project Goals</td><td style="text-align: right;">91</td></tr>
  </tbody>
</table>
"""

def generate_html_document():
    css = """
    @page {
      size: A4;
      margin: 25mm 12.5mm 12.5mm 27.5mm; /* Top: 2.5cm, Right: 1.25cm, Bottom: 1.25cm, Left: 2.75cm */
      @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 11pt;
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
      line-height: 1.5;
      font-size: 12pt;
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
      padding: 6px 12px;
      margin-bottom: 22px;
      background-color: #f8fafc;
    }

    h1.chapter-title {
      font-size: 16pt;
      font-weight: bold;
      text-align: center;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      line-height: 1.35;
      margin: 18px 0 22px 0;
      padding-bottom: 8px;
      border-bottom: 2px solid #0f172a;
      color: #0f172a;
    }

    h2 {
      font-size: 14pt;
      font-weight: bold;
      color: #0f172a;
      margin: 22px 0 10px 0;
      line-height: 1.3;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 4px;
    }

    h3 {
      font-size: 12pt;
      font-weight: bold;
      color: #1e293b;
      margin: 16px 0 8px 0;
      line-height: 1.3;
    }

    h4 {
      font-size: 12pt;
      font-weight: bold;
      color: #334155;
      margin: 12px 0 6px 0;
    }

    p {
      margin: 0 0 10px 0;
    }

    ol, ul {
      margin: 0 0 12px 0;
      padding-left: 24px;
    }

    li {
      margin-bottom: 5px;
    }

    .figure-container {
      margin: 18px auto;
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
      font-size: 10.5pt;
      font-weight: bold;
      color: #1e293b;
      margin-top: 8px;
      text-align: center;
    }

    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 10pt;
      line-height: 1.35;
      page-break-inside: avoid;
    }

    table.data-table th {
      background-color: #0f172a;
      color: #ffffff;
      padding: 7px 9px;
      border: 1px solid #334155;
      font-weight: bold;
      text-align: left;
    }

    table.data-table td {
      padding: 6px 9px;
      border: 1px solid #cbd5e1;
      vertical-align: top;
    }

    table.data-table tr:nth-child(even) td {
      background-color: #f8fafc;
    }

    table.toc-table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
      font-size: 11pt;
      line-height: 1.45;
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
      font-size: 11.5pt;
      border-bottom: 1.5px solid #0f172a;
    }

    .callout-box {
      border-left: 4px solid #3b82f6;
      background-color: #eff6ff;
      padding: 12px 16px;
      margin: 14px 0;
      border-radius: 0 4px 4px 0;
      font-size: 10.5pt;
      page-break-inside: avoid;
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
      margin: 14px 0;
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
    
    print("Generating comprehensive HTML document with exact logos and headers...")
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
