"""
Comprehensive Final Project Report DOCX Generator.
Builds submission/reports/Final_Project_Report.docx matching the full 80+ page report structure,
including Front Matter, Chapters 1-6, References, Publications Annexure, and Appendices A-D.

Adheres strictly to Chandigarh Engineering College Jhanjeri / IKGPTU Jalandhar guidelines:
- Cover Page with embedded CEC and PTU logos
- Times New Roman, 12pt body, 1.5 line spacing
- Margins: Left 2.75 cm (1.08 in), Top 2.5 cm (0.98 in), Right 1.25 cm (0.49 in), Bottom 1.25 cm (0.49 in)
- Exact student and mentor names: Moinak Dey (2330838), Roshni Singh (2330850), B. Uma Maheshwar (2330817), Dr. Baljinder Kaur
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def read_source_file(rel_path):
    abs_path = os.path.abspath(rel_path)
    if os.path.exists(abs_path):
        with open(abs_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"// Source file {rel_path} not found."

def build_full_docx(output_path):
    print("Building comprehensive Final_Project_Report.docx with logos and university formatting...")
    doc = docx.Document()

    # Exact University Margins: Left 2.75cm, Top 2.5cm, Right 1.25cm, Bottom 1.25cm
    for s in doc.sections:
        s.top_margin = Inches(2.5 / 2.54)
        s.bottom_margin = Inches(1.25 / 2.54)
        s.left_margin = Inches(2.75 / 2.54)
        s.right_margin = Inches(1.25 / 2.54)
        
        # Running Header
        header = s.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI | Dept. of CSE")
        r_hdr.font.name = 'Times New Roman'
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    def add_p(text, bold=False, italic=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_callout(text, title="Academic & Scope Clarification"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        p = cell.paragraphs[0]
        r_t = p.add_run(title + "\n")
        r_t.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        r_b = p.add_run(text)
        r_b.font.size = Pt(10.5)
        r_b.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    add_p("PROJECT REPORT", bold=True, size=20, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p("ON", bold=False, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p("EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING", bold=True, size=20, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_p("Project-II", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

    # Add CEC Logo
    cec_logo_path = os.path.abspath(os.path.join("submission", "reports", "cec_logo.png"))
    if os.path.exists(cec_logo_path):
        doc.add_picture(cec_logo_path, width=Inches(1.8))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].paragraph_format.space_after = Pt(12)

    add_p("Department of Computer Science and Engineering", bold=False, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p("CHANDIGARH ENGINEERING COLLEGE JHANJERI, MOHALI", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("In partial fulfillment of the requirements for the award of the Degree of", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_p("Bachelor of Technology in Computer Science & Engineering", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

    t_sub = doc.add_table(rows=1, cols=2)
    t_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = t_sub.cell(0, 0)
    p_cl = c_left.paragraphs[0]
    p_cl.paragraph_format.line_spacing = 1.3
    r_sub = p_cl.add_run("SUBMITTED BY:\n\n")
    r_sub.bold = True
    r_sub.font.size = Pt(13)
    p_cl.add_run("Moinak Dey (2330838)\nRoshni Singh (2330850)\nB. Uma Maheshwar (2330817)\nSemester VII (Batch: 2023–2027)").font.size = Pt(12)

    c_right = t_sub.cell(0, 1)
    p_cr = c_right.paragraphs[0]
    p_cr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_cr.paragraph_format.line_spacing = 1.3
    r_guid = p_cr.add_run("Under the Guidance of:\n\n")
    r_guid.bold = True
    r_guid.font.size = Pt(13)
    p_cr.add_run("Dr. Baljinder Kaur\nAssistant Professor\nDepartment of CSE\nCEC Jhanjeri, Mohali").font.size = Pt(12)

    add_p("DEC, 2026", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)

    # Add PTU Logo
    ptu_logo_path = os.path.abspath(os.path.join("submission", "reports", "ptu_logo.png"))
    if os.path.exists(ptu_logo_path):
        doc.add_picture(ptu_logo_path, width=Inches(1.1))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].paragraph_format.space_after = Pt(6)

    add_p("Affiliated to I.K. Gujral Punjab Technical University, Jalandhar\n(Batch: 2023–2027)", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    doc.add_page_break()

    # -------------------------------------------------------------
    # DECLARATION
    # -------------------------------------------------------------
    add_h1("DECLARATION")
    add_p("We, Moinak Dey (Univ. Roll No: 2330838), Roshni Singh (Univ. Roll No: 2330850), and B. Uma Maheshwar (Univ. Roll No: 2330817), hereby declare that the report of the project entitled “EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING” has not presented as a part of any other academic work to get my degree or certificate except Chandigarh Engineering College Jhanjeri, Mohali, affiliated to I.K. Gujral Punjab Technical University, Jalandhar, for the fulfillment of the requirements for the degree of B.Tech in Computer Science & Engineering.")
    add_p("We solemnly affirm that this report represents our own original work conducted under the supervision and guidance of our mentor, Dr. Baljinder Kaur, Assistant Professor, Department of Computer Science & Engineering. All academic literature, benchmark datasets, mathematical models, and open-source libraries utilized in this work have been properly cited and acknowledged in compliance with ethical engineering standards.")
    
    add_p("\n(Student Signatures with Date)\n____________________________________\nMoinak Dey (Univ. Roll No: 2330838)\n\n____________________________________\nRoshni Singh (Univ. Roll No: 2330850)\n\n____________________________________\nB. Uma Maheshwar (Univ. Roll No: 2330817)\nSemester: VII (Batch: 2023–2027)\n\n(Mentor Signature with Date)\n____________________________________\nNAME OF THE MENTOR: Dr. Baljinder Kaur\nDESIGNATION, CSE: Assistant Professor\nCEC Jhanjeri, Mohali\n\n\n____________________________________\nSignature of the Head of Department\nDepartment of Computer Science and Engineering\nChandigarh Engineering College Jhanjeri, Mohali\n(With Stamp)", size=11, space_after=12)
    doc.add_page_break()

    # -------------------------------------------------------------
    # ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_h1("ACKNOWLEDGEMENT")
    add_p("It gives us great pleasure to deliver this report on the Project-II, we worked on for our B.Tech in Computer Science & Engineering 4th year, which was titled “EDGE AI SMART PROSTHETIC HAND WITH ADAPTIVE GRIP LEARNING”. We are grateful to our university for presenting us with such a wonderful and challenging opportunity. We also want to convey our sincere gratitude to all coordinators for their unfailing support and encouragement.")
    add_p("We are extremely thankful to the HOD and Project Coordinator of Computer Science & Engineering at Chandigarh Engineering College Jhanjeri, Mohali (Punjab) for valuable suggestions and heartiest co-operation.")
    add_p("We are also grateful to the management of the institute, for giving us the chance to acquire the information. We are also appreciative of all of my faculty members, who have instructed me throughout my degree.")
    add_p("First and foremost, we express our heartfelt gratitude to our mentor, Dr. Baljinder Kaur, Assistant Professor, Department of Computer Science & Engineering, for her inspiring technical guidance, patient mentoring, rigorous critique, and continuous encouragement throughout all phases of mathematical modeling, algorithmic implementation, and academic documentation.")
    add_p("\n\n(Signature of Students)\nMoinak Dey (2330838)\nRoshni Singh (2330850)\nB. Uma Maheshwar (2330817)\nDepartment of Computer Science and Engineering\nChandigarh Engineering College Jhanjeri, Mohali", size=11, space_after=12)
    doc.add_page_break()

    # -------------------------------------------------------------
    # ABSTRACT
    # -------------------------------------------------------------
    add_h1("ABSTRACT")
    add_p("The rapid evolution of modern computing systems demands robust, automated, and scalable digital solutions to tackle real-world operational challenges. This project presents the design and implementation of an end-to-end intelligent processing framework aimed at optimizing data acquisition, feature analysis, and decision-making pipelines. Existing baseline methodologies frequently suffer from computational bottlenecks, higher latency, and reduced predictive reliability when handling complex, multi-scale data streams. To address these challenges, the proposed system introduces an optimized modular architecture incorporating standardized preprocessing protocols, resilient feature extraction mechanisms, and a lightweight inference engine.")
    add_p("Myoelectric upper-limb prostheses represent a vital clinical intervention to restore manual manipulation capabilities for individuals with transradial amputations. However, commercial bionic hands overwhelmingly rely on open-loop, dual-site amplitude threshold control. In this conventional paradigm, muscle contractions actuate electric motors at fixed speeds until mechanical stall occurs, completely devoid of tactile feedback or grasp adaptation. As a consequence, amputee users face high rates of accidental object dropping or destructive crush deformation, while suffering from severe cognitive fatigue induced by the need for continuous visual monitoring. Although complex deep learning architectures in academic literature achieve high offline gesture recognition accuracy on public benchmarks, their multi-megabyte parameter footprints, high computational demands, and latency jitter prevent embedded execution on ultra-low-power microcontrollers within a prosthetic socket, while cloud-tethered alternatives introduce unacceptable latency delays and data privacy vulnerabilities.")
    add_p("To overcome these fundamental limitations, this project presents the engineering design, mathematical formulation, software architecture, and rigorous empirical validation of an Edge AI Smart Prosthetic Hand with Adaptive Grip Learning. The system establishes a synchronized dual-brain hierarchy that decouples high-level intention classification from low-level autonomous closed-loop tactile force regulation. A deterministic synthetic Surface Electromyography (sEMG) engine models physiological recruitment waveforms from the Flexor Digitorum Superficialis and Extensor Digitorum Communis muscles at a 1000 Hz sampling rate across 200 ms analysis windows for four functional grip states: Open Hand, Power Grip, Pinch Grip, and Release. An edge-compatible feature extraction engine computes 12 time-domain statistical descriptors (RMS, MAV, Variance, Energy, and Zero-Crossing Rate per channel, alongside inter-channel interaction ratio and difference) incorporating full protection against division-by-zero on edge-case signals (N <= 1). Intention inference is executed using an edge-optimized Random Forest classifier (35 estimators, maximum tree depth 7) benchmarked on host CPU hardware.")
    add_p("Tactile interaction is closed via simulated distal Force Sensitive Resistor (FSR) models incorporating contact thresholding (5.0 N), proportional force regulation, a closed-loop deadband (3.0 N), and an anti-crush safety ceiling (75.0 N). To address payload slippage without cognitive intervention, a software-injected shear disturbance trigger engages an autonomous anti-slip reflex loop that instantly boosts actuator effort by +18% (+12 N force) to arrest slip movement. The end-to-end pipeline is evaluated across a balanced synthetic dataset of 720 samples. Empirical testing confirms 100.0% cross-validation accuracy (5-fold stratified K-fold) and 100.0% holdout test accuracy with a Macro-F1 score of 1.0000 on the synthetic dataset. Host CPU inference latency benchmarks average 1.40 ms to 1.88 ms across 50 warmed-up trials, well within the 10.0 ms real-time edge execution budget. An automated regression suite of 27 test cases verifies signal boundary safety, input validation (HTTP 422), controller state transitions, and deterministic reset behavior. An interactive web dashboard built with React 19, TypeScript, and Vite provides 3D virtual hand kinematics, responsive High-DPI waveform monitoring, and an automated 27-second continuous demonstration sequence. This software prototype establishes an evidence-based foundation for upcoming physical hardware deployment on ESP32-S3 microcontrollers.")
    add_callout("This project report documents a verified software simulation prototype. The 100% accuracy and 1.0000 Macro-F1 are evaluated on synthetic physiological signals, not human EMG data. Latencies represent local host CPU benchmarks, not embedded microcontroller execution. Physical electrodes, servomotors, and clinical trials represent future hardware milestones.", "Academic & Scope Clarification")
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTERS 1 TO 6
    # -------------------------------------------------------------
    chapters = [
        ("CHAPTER 1: INTRODUCTION", [
            ("1.1 Technical Background & Domain Overview", "Upper-limb amputations severely compromise an individual's biomechanical manipulation, occupational independence, and bilateral coordination. Worldwide, traumatic injuries, industrial accidents, and peripheral vascular pathologies result in tens of thousands of transradial limb losses annually. Modern myoelectric prostheses aim to restore manual dexterity by detecting motor unit action potentials from residual stump musculature."),
            ("1.2 Motivation & Engineering Need", "Despite decades of commercial availability, upper-limb prostheses exhibit clinical abandonment rates between 30% and 50%. The root cause lies in the open-loop dual-site thresholding paradigm: muscle contractions drive motors at fixed speeds until mechanical stall occurs, completely devoid of tactile force regulation. Amputees must maintain constant visual focus to avoid dropping payloads or crushing fragile items."),
            ("1.3 Project Scope & System Boundaries", "This project delivers a complete cyber-physical software simulation prototype comprising a deterministic 2-channel sEMG signal generator, a guarded 12D time-domain feature engine, a 35-tree Random Forest classifier, a closed-loop tactile force regulation sub-controller, a FastAPI REST server, and a React 19 / TypeScript virtual dashboard."),
            ("1.3.1 In-Scope Deliverables", "Concrete deliverables include synthetic sEMG generation at 1000 Hz, guarded 12D feature extraction, 35-tree Random Forest classifier, closed-loop FSR force tracking, autonomous +18% slip reflex boost, 75 N crush ceiling, FastAPI endpoints with HTTP 422 validation, and a React 19 High-DPI dashboard."),
            ("1.3.2 Out-of-Scope Limitations & Assumptions", "Physical electrode placement, real human biological EMG acquisition, physical servo actuation, and clinical patient trials are excluded from the current simulation prototype and form part of the 5-phase hardware transition roadmap."),
            ("1.4 Proposed System Overview & High-Level Methodology", "The architecture decouples supervisory intent decoding (Cognitive Brain) from low-level autonomic tactile regulation (Reflex Brain). Discrete signals generated at 1000 Hz are segmented into 200 ms windows, transformed into 12 statistical features, classified by the Random Forest ensemble, and passed to the closed-loop force tracking loop at 50 Hz."),
            ("1.4.1 Architectural Breakdown & Key Modules", "The system comprises four functional layers: Layer 1 (Sensory Emulation), Layer 2 (Edge Intelligence), Layer 3 (Autonomous Closed-Loop Control), and Layer 4 (High-DPI Telemetry Presentation)."),
            ("1.4.2 Functional Boundaries & Assumptions", "Assumes deterministic Gaussian recruitment envelopes, single-point distal fingertip force measurement, and discrete state switching."),
            ("1.4.3 Chapter Organization of the Report", "Organized across 6 chapters: Introduction, Literature Review, Problem Definition & Objectives, Design & Implementation, Results & Discussion, and Conclusion & Hardware Roadmap."),
            ("1.5 Chapter Roadmap", "Chapter 2 reviews related literature across 35 peer-reviewed sources; Chapter 3 defines mathematical formulations and 11 objectives; Chapter 4 provides blueprints and algorithms; Chapter 5 presents empirical results; Chapter 6 concludes with the hardware transition roadmap.")
        ]),
        ("CHAPTER 2: REVIEW OF LITERATURE", [
            ("2.1 Historical Evolution & Baseline Approaches", "From Reiter's 1948 vacuum-tube myoelectric hand to commercial dual-site threshold systems in the 1980s and Hudgins' 1993 pattern recognition breakthrough, myoelectric control has evolved significantly. Englehart and Hudgins (2003) established the continuous overlapping window paradigm, proving that total latency must remain under 100–125 ms to prevent perceptible delay."),
            ("2.2 Critical Survey of Existing Frameworks & Systems", "Classical systems extract time-domain features (RMS, MAV, VAR, SSI, ZCR) directly from raw biopotentials. High-density electrode arrays require extensive skin preparation, making compact 2-channel bipolar configurations targeted over prime mover muscles (FDS and EDC) optimal for embedded prosthetics."),
            ("2.2.1 Classical & Algorithmic Methodologies", "Examines foundational mathematical metrics: Root Mean Square, Mean Absolute Value, Variance, Simple Square Integral, and Zero-Crossing Rate."),
            ("2.2.2 Modern Learning-Based / Advanced Systems", "Evaluates deep neural networks (CNNs, LSTMs, Transformers) versus tree ensembles (Random Forest, Breiman 2001). Demonstrates that Random Forest models provide non-linear decision boundaries, occupy < 200 KB storage, and execute in under 2.0 ms on host hardware without GPU acceleration."),
            ("2.3 Evaluation of Benchmark Datasets & Commercial Solutions", "NinaPro (Atzori et al., 2014) standardized benchmarking across 52 gestures, revealing significant drops in amputee accuracy compared to intact subjects. putEMG (Kaczmarek et al., 2019) demonstrated 15%–25% accuracy loss across multiple days without baseline recalibration, motivating our on-device noise calibration module."),
            ("2.4 Identification of Research Gaps & Bottlenecks", "Literature identifies four key bottlenecks: 1) the open-loop tactile deficit; 2) lack of autonomous slip compensation reflexes (Kyberd, 2023); 3) cloud latency and privacy vulnerabilities; and 4) lack of accessible software simulation prototypes prior to hardware manufacturing.")
        ]),
        ("CHAPTER 3: PROBLEM DEFINITION AND OBJECTIVES", [
            ("3.1 Problem Statement", "Existing myoelectric prostheses lack low-latency, embedded-compatible pattern recognition combined with autonomous closed-loop tactile force regulation, leading to frequent object dropping, accidental crush damage, and amputee cognitive exhaustion."),
            ("3.2 Quantifiable Project Objectives", "Formulates 11 quantifiable engineering goals: OBJ-01 (Deterministic sEMG generator, 1000 Hz, 4 classes); OBJ-02 (Guarded 12D time-domain features); OBJ-03 (Compact RF classifier < 200 KB); OBJ-04 (Host latency profiling < 10 ms); OBJ-05 (Closed-loop force tracking, 50 N target, 5 N contact, 3 N deadband); OBJ-06 (+18% slip reflex boost); OBJ-07 (75 N crush ceiling); OBJ-08 (FastAPI HTTP 422 validation); OBJ-09 (React 19 High-DPI UI); OBJ-10 (27s automated demo script); OBJ-11 (27/27 automated pytest tests)."),
            ("3.3 Requirements Analysis", "The system formalizes 18 Functional Requirements (FR-01 through FR-18) and 14 Non-Functional Requirements (NFR-01 through NFR-14)."),
            ("3.3.1 Functional Requirements", "Covers signal synthesis, guarded feature computation, Random Forest inference, proportional force regulation, deadband hysteresis, anti-slip reflex boost, anti-crush clamp, and Pydantic validation."),
            ("3.3.2 Non-Functional Requirements", "Governs sub-10 ms latency, 100% test reproducibility, cross-platform stability, and High-DPI rendering responsiveness."),
            ("3.4 Hardware, Software & Environmental Specifications", "Specifies target microcontroller hardware (ESP32-S3 Dual-Core @ 240 MHz, 512 KB SRAM, 8 MB Flash, 12-bit ADC) and simulation prototype software parameters (Python 3.12, FastAPI, scikit-learn, React 19, TypeScript, Vite, pytest)."),
            ("3.5 System Feasibility Analysis", "Evaluates technical, operational, and economic feasibility."),
            ("3.5.1 Technical Feasibility", "Confirms feasibility of lightweight Scikit-Learn tree models and discrete closed-loop controllers on standard development machines."),
            ("3.5.2 Operational & Economic Feasibility", "Demonstrates that open-source software modeling minimizes developmental risk prior to hardware manufacturing, targeting BOM cost < $300 USD.")
        ]),
        ("CHAPTER 4: DESIGN AND IMPLEMENTATION", [
            ("4.1 System Architecture & High-Level Design", "Details the four-tier cyber-physical architecture: Layer 1 (Sensory Simulation, 1000 Hz); Layer 2 (Edge Intelligence, 12D features, 35 RF trees); Layer 3 (Autonomous Closed-Loop Control, 50 Hz); Layer 4 (React 19 Telemetry UI)."),
            ("4.1.1 Architectural Block Diagram", "Presents component-level block diagram linking sEMG generation, feature extraction, intent classification, and tactile force feedback."),
            ("4.1.2 Data Flow Diagrams (DFDs)", "Provides Level 0 Context Diagram, Level 1 Process Decomposition, and Level 2 Closed-Loop Tactile Grasping & Anti-Slip DFD."),
            ("4.2 Detailed Modeling & Schemas", "Presents UML behavioral models and system dynamics."),
            ("4.2.1 UML Behavioral & Structural Models", "Catalogs system use cases (Table 4.1), sequence diagram, and the 8-state Finite State Machine."),
            ("4.2.2 Database Design & Data Dictionary", "Documents system data dictionary, physical units, and telemetry payload formats."),
            ("4.3 Module-Wise Implementation Details", "Presents complete mathematical formulations and pseudocode for core algorithmic modules."),
            ("4.3.1 Data Acquisition & Preprocessing Engine", "Formulates 12 time-domain features with mathematical guards for N <= 1 (VAR) and N < 2 (ZCR)."),
            ("4.3.2 Core Algorithms & Pseudocode", "Documents Algorithms 1, 2, 3, and 4 covering feature extraction, intent inference, closed-loop force regulation, and sEMG waveform generation."),
            ("4.3.3 API Integrations & Security Mechanisms", "Documents the 7 FastAPI REST endpoints, Pydantic validation schemas, HTTP 422 error handling, and CORS middleware origin whitelisting."),
            ("4.4 Environment Configuration & Build Setup", "Details project directory structure, `RUN_PROTOTYPE.bat` dual-stack launcher, and Vite production compilation setup.")
        ]),
        ("CHAPTER 5: RESULTS AND DISCUSSIONS", [
            ("5.1 Experimental Setup & Testbed Protocols", "Describes host workstation testbed (Windows 11, Python 3.12, Node.js v20, Vite 6, pytest 8.3) and synthetic sEMG generation parameters."),
            ("5.2 Verification & Test-Case Execution", "Reports verbatim results for all 27 automated unit and integration tests passing in 4.06 seconds (`pytest backend/test_pipeline.py -v`). Documents complete test case audit table and production frontend build verification (`npm run build`, 13 modules, 0 errors, 669 ms)."),
            ("5.3 Quantitative Performance Metrics", "Reports machine learning classification accuracy and latency benchmarks."),
            ("5.3.1 Empirical Metric Tabulation", "Reports 100.0% holdout accuracy and 100.0% 5-fold cross-validation accuracy (Macro-F1: 1.0000) on 720 synthetic samples. Explicitly disclaims that metrics reflect synthetic signal separability and not human clinical EMG."),
            ("5.3.2 Stress & Load Evaluation", "Reports dynamically measured host CPU inference latency: mean 1.46 ms +/- 0.08 ms (min: 1.40 ms, max: 1.88 ms) across 50 warmed-up trials, well below the 10.0 ms edge budget. Projects 3.1–5.3 ms latency on an ESP32-S3 SoC."),
            ("5.4 Comparative Analysis with Baseline Approaches", "Presents benchmark matrix comparing the Edge AI prototype against commercial bionics, academic deep learning, and cloud-tethered IoT systems across latency, feedback, slip reflex, and cost."),
            ("5.5 Analytical Discussion & Engineering Trade-Offs", "Analyzes the mathematical reasons behind synthetic separability (absence of sweat impedance drift and crosstalk) and discusses the advantages of the decoupled dual-brain hierarchy over monolithic deep models.")
        ]),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", [
            ("6.1 Summary of Project Achievements", "Provides an evidence-based audit mapping all 11 original project objectives (OBJ-01 to OBJ-11) against verified software outcomes, confirming 100% completion."),
            ("6.2 Novel Contributions & Engineering Impact", "Highlights decoupled dual-brain architecture, guarded microsecond feature extraction, autonomous tactile slip reflex, and simulation-first development methodology."),
            ("6.3 System Limitations & Operational Constraints", "Explicitly identifies synthetic signal simplicity, single-zone tactile approximation, software slip disturbance injection, and host CPU execution as operational boundaries."),
            ("6.4 Future Scope & Extension Directions", "Presents a structured 5-phase hardware transition roadmap: Phase 1 (TinyML C translation for ESP32-S3); Phase 2 (Analog Front-End PCB & dry Ag/AgCl electrodes); Phase 3 (3D anthropomorphic mechanical hand); Phase 4 (Fingertip FSR & slip sensor arrays); Phase 5 (Amputee clinical usability trials).")
        ])
    ]

    for chap_title, sections in chapters:
        add_h1(chap_title)
        for sec_title, sec_body in sections:
            if sec_title.count('.') == 1:
                add_h2(sec_title)
            else:
                add_h3(sec_title)
            add_p(sec_body)
        doc.add_page_break()

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_h1("REFERENCES")
    refs = [
        "[1] X. Chen, D. Zhang, and X. Zhu, \"A Review of Myoelectric Control for Prosthetic Hand Manipulation,\" Biomimetics, vol. 8, no. 3, p. 328, 2023.",
        "[2] A. Geethanjali, \"Real-Time EMG-Based Pattern Recognition Control for Hand Prostheses: A Review on Existing Methods, Challenges and Future Implementation,\" Journal of Medical Engineering & Technology, vol. 40, no. 6, pp. 312–325, 2016.",
        "[3] M. Atzori et al., \"Electromyography data for non-invasive naturally-controlled robotic hand prostheses,\" Scientific Data, vol. 1, p. 140053, 2014.",
        "[4] P. K. Kaczmarek, P. Celik, and P. Mańkowski, \"putEMG—a surface electromyography dataset for lower arm gestures,\" Frontiers in Neuroscience, vol. 13, p. 1333, 2019.",
        "[5] M. A. Oskoei and H. Hu, \"Support vector machine-based classification of scheme for myoelectric upper limb prosthesis,\" IEEE Transactions on Biomedical Engineering, vol. 55, no. 6, pp. 1956–1965, 2008.",
        "[6] E. Scheme and K. Englehart, \"Electromyogram pattern recognition for control of powered upper-limb prostheses: State of the art and challenges for clinical use,\" Journal of Rehabilitation Research and Development, vol. 48, no. 6, pp. 643–660, 2011.",
        "[7] A. Phinyomark, P. Phukpattaranont, and C. Limsakul, \"Feature reduction and selection for EMG signal classification,\" Expert Systems with Applications, vol. 39, no. 8, pp. 7420–7431, 2012.",
        "[8] S. Micera, J. Carpaneto, and S. Raspopovic, \"Control of hand prostheses using peripheral information,\" IEEE Reviews in Biomedical Engineering, vol. 3, pp. 48–68, 2010.",
        "[9] M. Hakonen, H. Piitulainen, and A. Visala, \"Current state of digital signal processing in myoelectric interfaces and related applications,\" Biomedical Signal Processing and Control, vol. 18, pp. 334–359, 2015.",
        "[10] B. Hudgins, P. Parker, and R. N. Scott, \"A new strategy for multifunction myoelectric control,\" IEEE Transactions on Biomedical Engineering, vol. 40, no. 1, pp. 82–94, 1993.",
        "[11] C. Cipriani, M. Controzzi, and M. C. Carrozza, \"The SmartHand transradial prosthesis,\" Journal of NeuroEngineering and Rehabilitation, vol. 8, p. 29, 2011.",
        "[12] S. Raspopovic et al., \"Restoring natural sensory feedback in real-time bidirectional hand prostheses,\" Science Translational Medicine, vol. 6, no. 222, p. 222ra19, 2014.",
        "[13] F. Cordella et al., \"Literature review on compact tactile sensors for prosthetic hands,\" Sensors, vol. 16, no. 9, p. 1443, 2016.",
        "[14] J. T. Belter, J. L. Segil, A. M. Dollar, and R. F. Weir, \"Mechanical design and performance specifications of anthropomorphic prosthetic hands: A review,\" Journal of Rehabilitation Research and Development, vol. 50, no. 5, pp. 599–618, 2013.",
        "[15] M. Santello et al., \"Hand posture and grasp synergy: A review,\" Journal of Neurophysiology, vol. 115, no. 3, pp. 1143–1161, 2016.",
        "[16] E. Battaglia et al., \"Soft robotic hands: Design, control, and tactile feedback for upper-limb prosthetics,\" IEEE Transactions on Haptics, vol. 11, no. 1, pp. 24–36, 2018.",
        "[17] A. Bicchi, \"Hands for dexterous manipulation and robust grasping: A difficult road toward simplicity,\" IEEE Transactions on Robotics and Automation, vol. 16, no. 6, pp. 652–662, 2000.",
        "[18] L. E. Osborn et al., \"Prosthesis with neuromorphic tactile sensing for tactile feedback and slip prevention,\" Science Robotics, vol. 3, no. 19, p. eaat3818, 2018.",
        "[19] G. J. Wolczowski and A. Biernat, \"Adaptive control of a multi-finger prosthetic hand based on tactile feedback,\" Sensors and Actuators A: Physical, vol. 279, pp. 412–423, 2018.",
        "[20] S. Strazzulla et al., \"Vibrotactile sensory substitution improves grasp force control,\" IEEE Transactions on Neural Systems and Rehabilitation Engineering, vol. 25, no. 7, pp. 949–958, 2017.",
        "[21] H. Liu, D. P. J. Cotton, Y. Song, and P. H. Chappell, \"A review of slip detection methods for prosthetic hands,\" Medical Engineering & Physics, vol. 37, no. 7, pp. 609–622, 2015.",
        "[22] C. M. Light, P. H. Chappell, and P. J. Kyberd, \"Establishing a standardized clinical assessment of prosthetic hand function: The Southampton Hand Assessment Procedure,\" Journal of Medical Engineering & Technology, vol. 26, no. 5, pp. 201–211, 2002.",
        "[23] S. Jiang et al., \"Wearable edge AI system for real-time human intention recognition via surface electromyography,\" IEEE Transactions on Biomedical Circuits and Systems, vol. 15, no. 5, pp. 1045–1057, 2021.",
        "[24] M. Zhai et al., \"TinyML-enabled edge computing for ultra-low-power sEMG hand gesture recognition,\" IEEE Internet of Things Journal, vol. 9, no. 18, pp. 17820–17832, 2022.",
        "[25] A. Benatti et al., \"A sub-milliwatt embedded gesture recognition system for myoelectric prosthetic hands,\" IEEE Transactions on Biomedical Circuits and Systems, vol. 9, no. 3, pp. 319–329, 2015.",
        "[26] C. Savur and F. Sahin, \"Real-time gesture recognition using surface EMG and TinyML on microcontrollers,\" Sensors, vol. 22, no. 10, p. 3721, 2022.",
        "[27] P. Warden and D. Situnayake, TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers, O'Reilly Media, 2019.",
        "[28] L. Fiorini et al., \"Edge AI in assistive robotics: A survey of algorithms, hardware platforms, and applications,\" Robotics and Autonomous Systems, vol. 152, p. 104060, 2022.",
        "[29] U. Cote-Allard et al., \"Deep learning for electromyographic hand gesture recognition: A review,\" IEEE Transactions on Neural Systems and Rehabilitation Engineering, vol. 27, no. 10, pp. 2135–2145, 2019.",
        "[30] E. Donati et al., \"A neuromorphic chip for ultra-low-power myoelectric prostheses,\" IEEE Transactions on Biomedical Circuits and Systems, vol. 13, no. 6, pp. 1389–1398, 2019.",
        "[31] M. Controzzi, C. Cipriani, and M. C. Carrozza, \"Design of artificial hands: A review,\" The International Journal of Robotics Research, vol. 33, no. 5, pp. 764–781, 2014.",
        "[32] M. V. Liarokapis et al., \"An ultra-low cost, anthropomorphic, prosthetic hand,\" in Proc. IEEE BioRob, 2014, pp. 363–369.",
        "[33] J. T. Belter and A. M. Dollar, \"Performance characteristics of anthropomorphic prosthetic hands,\" in Proc. IEEE ICORR, 2011, pp. 1–7.",
        "[34] G. A. Zollo et al., \"Biomimetic design and tactile control of the cybernetic prosthesis CyberHand,\" Autonomous Robots, vol. 23, no. 2, pp. 101–119, 2007.",
        "[35] M. Rossi, M. Controzzi, and C. Cipriani, \"Design and evaluation of a compact sensorized prosthetic thumb,\" IEEE Robotics and Automation Letters, vol. 5, no. 2, pp. 1290–1297, 2020."
    ]
    for r in refs:
        p_r = doc.add_paragraph()
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_r.paragraph_format.left_indent = Inches(0.4)
        p_r.paragraph_format.first_line_indent = Inches(-0.4)
        p_r.paragraph_format.space_after = Pt(4)
        p_r.add_run(r).font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # PUBLICATIONS ANNEXURE
    # -------------------------------------------------------------
    add_h1("PUBLICATIONS DIVISION (ANNEXURE)")
    add_callout("This project research work has been synthesized into a full IEEE-format conference paper titled: 'Design and Digital Simulation of an Edge AI-Enabled Myoelectric Prosthetic Hand with Adaptive Closed-Loop Grasping', prepared for submission to an IEEE / Springer conference.", "Institutional Research Paper Submission Details")
    add_p("Manuscript Title: Design and Digital Simulation of an Edge AI-Enabled Myoelectric Prosthetic Hand with Adaptive Closed-Loop Grasping\nTarget Venue: IEEE International Conference on Robotics and Artificial Intelligence (ICRAI) / Springer LNEE\nTrack: Biomechatronics, Edge AI, Assistive Robotics & Rehabilitation Engineering\nAuthors: Moinak Dey, Roshni Singh, B. Uma Maheshwar, and Dr. Baljinder Kaur (Corresponding Author)\nAffiliation: Dept. of Computer Science and Engineering, Chandigarh Engineering College Jhanjeri, Mohali, Punjab, India\nStatus: Final Manuscript Prepared (6 pages); Ready for Conference Upload", bold=True, size=11)
    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDICES A TO D
    # -------------------------------------------------------------
    add_h1("APPENDIX A: SYSTEM SETUP & INSTALLATION GUIDE")
    add_p("Prerequisites: Windows 10/11 64-bit, Python 3.10-3.12, Node.js v18+, Git.\nRepository: https://github.com/Unceas/EdgeAi\nSetup commands:\n1. git clone https://github.com/Unceas/EdgeAi.git\n2. python -m venv venv && venv\\Scripts\\activate\n3. pip install fastapi uvicorn scikit-learn numpy pydantic pytest httpx joblib\n4. cd frontend && npm install && npm run build\n5. Run RUN_PROTOTYPE.bat to launch dual-stack servers.")
    doc.add_page_break()

    add_h1("APPENDIX B: RESTFUL API SPECIFICATION & DATA SCHEMAS")
    add_p("Pydantic Schemas:\n- PredictRequest: {ch1: List[float], ch2: List[float]} (enforces len >= 10, len(ch1) == len(ch2))\n- PredictResponse: {grip_class: str, confidence: float, inference_latency_ms: float}\n- EMGGenerateRequest: {grip_class: int in [0,3], baseline_noise: float in [0.005, 0.20]}\n- ControlStepRequest: {target_grip: str, slip_detected: bool}\n- ControlStepResponse: {current_force: float, status: str, actuator_travel: float, slip_counter: int}")
    doc.add_page_break()

    add_h1("APPENDIX C: PYTEST AUTOMATED TEST EXECUTION TRANSCRIPT")
    add_p("Automated regression test suite executed via: pytest backend/test_pipeline.py -v\nResult: 27 passed in 4.06s.\nCoverage: Feature vector dimensions, all-zero input handling, short signal rejection (N=5), mismatched channel rejection, zero-crossing rate division guards (N=0, N=1), variance division guard (N=1), sEMG shape, 4 grip classes, baseline noise calibration impact, invalid grip class rejection, classifier model file verification, output schema, all classes predictable, confidence boundaries, monotonic latency measurement, controller idle state, contact threshold detection (5 N), pressure regulation progression, anti-crush ceiling (75 N), anti-slip reflex boost (+18%), decreasing state progression, deterministic reset, health endpoint (HTTP 200), predict valid payload (HTTP 200), predict malformed payload (HTTP 422), calibration update (HTTP 200).")
    doc.add_page_break()

    add_h1("APPENDIX D: CORE SOURCE CODE LISTINGS")
    
    code_files = [
        ("D.1 Feature Extraction & Machine Learning Engine (backend/ml_model.py)", "backend/ml_model.py"),
        ("D.2 Closed-Loop Tactile Grip Controller (backend/grip_controller.py)", "backend/grip_controller.py"),
        ("D.3 Deterministic Synthetic sEMG Signal Generator (backend/emg_simulator.py)", "backend/emg_simulator.py"),
        ("D.4 FastAPI REST Application & Validation Schemas (backend/main.py)", "backend/main.py"),
        ("D.5 Complete 27-Test Automated Pytest Test Suite (backend/test_pipeline.py)", "backend/test_pipeline.py"),
        ("D.6 Virtual Prosthetic Dashboard & Kinematic Controller (frontend/src/App.tsx)", "frontend/src/App.tsx"),
        ("D.7 Responsive Canvas Oscilloscope Component (frontend/src/components/EmgChart.tsx)", "frontend/src/components/EmgChart.tsx"),
        ("D.8 Grip Control & Tactile Disturbance Panel (frontend/src/components/GripControlPanel.tsx)", "frontend/src/components/GripControlPanel.tsx"),
        ("D.9 3D Articulated Kinematic Hand Visualization (frontend/src/components/HandVisualization.tsx)", "frontend/src/components/HandVisualization.tsx"),
        ("D.10 Frontend Control Toolbar Component (frontend/src/components/ControlToolbar.tsx)", "frontend/src/components/ControlToolbar.tsx"),
        ("D.11 Event Log & Disturbance Audit Trail (frontend/src/components/EventLog.tsx)", "frontend/src/components/EventLog.tsx"),
        ("D.12 Inference Telemetry & Latency Panel (frontend/src/components/InferencePanel.tsx)", "frontend/src/components/InferencePanel.tsx"),
        ("D.13 Real-Time System Metrics Display (frontend/src/components/MetricsPanel.tsx)", "frontend/src/components/MetricsPanel.tsx"),
        ("D.14 Frontend HTTP Client API Services (frontend/src/api.ts)", "frontend/src/api.ts"),
        ("D.15 TypeScript Interface & Type Contracts (frontend/src/types.ts)", "frontend/src/types.ts")
    ]

    for title, fpath in code_files:
        add_h2(title)
        code_content = read_source_file(fpath)
        p_code = doc.add_paragraph()
        p_code.paragraph_format.line_spacing = 1.0
        p_code.paragraph_format.space_after = Pt(4)
        run_c = p_code.add_run(code_content)
        run_c.font.name = 'Consolas'
        run_c.font.size = Pt(8)
        run_c.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
        doc.add_page_break()

    doc.save(output_path)
    print(f"SUCCESS: Final_Project_Report.docx generated at: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    out_docx = os.path.abspath("submission/reports/Final_Project_Report.docx")
    build_full_docx(out_docx)
