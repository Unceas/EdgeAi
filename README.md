# Edge AI Smart Prosthetic Hand with Adaptive Grip Learning

Software Prototype & Digital Simulation Pipeline  
Academic Engineering Clinics Project (Semester VII)

---

## 1. Project Overview

This project presents a software simulation prototype for an **Edge AI Smart Prosthetic Hand with Adaptive Grip Learning**. The objective is to demonstrate the intelligence and closed-loop control pipeline intended for an intelligent prosthetic terminal device. The system models myoelectric user intention recognition, real-time machine learning inference, virtual actuation, simulated force sensing feedback, and adaptive grip stabilization to prevent slippage and object crushing.

## 2. Problem Statement

Conventional myoelectric prostheses typically rely on rigid threshold-based switching or open-loop motor commands (e.g., mapping a raw muscle contraction burst directly to a fixed servo position). This paradigm suffers from critical limitations:
- Inability to dynamically adjust grip pressure according to object compliance or mass.
- High risk of dropping delicate or slippery objects due to absence of real-time tactile slip compensation.
- High risk of structural damage or crushing soft payloads due to lack of closed-loop tactile force regulation.
- Significant cognitive fatigue on the amputee, who must manually hold muscle tension to sustain grasp force.

## 3. Prototype Objective

Physical hardware (electrodes, microcontrollers, servos, and tactile sensors) is not physically present in this development phase. Consequently, this system provides a **software-only prototype and digital simulation** to validate:
1. Synthetic surface electromyography (sEMG) multi-channel generation for distinct grasp intentions.
2. Time-domain statistical feature extraction.
3. Edge-compatible machine learning classification of user grip intention.
4. Dynamic 2D kinematics simulation of an articulated 5-DOF prosthetic hand.
5. Closed-loop adaptive grip force regulation with simulated force-sensitive resistor (FSR) tactile feedback and anti-slip reflexes.

> **Important Disclosure**: Sensor inputs, motor angles, and force values are simulated for digital prototype validation. Physical hardware integration is scheduled for a subsequent development phase.

## 4. System Architecture

The software architecture is divided into two primary sub-systems: an asynchronous Python backend implementing signal synthesis, feature engineering, ML inference, and closed-loop control logic; and a React frontend rendering virtual hand kinematics, real-time waveforms, and engineering telemetry.

```
+-------------------------------------------------------------------+
|                           USER / DEMO                             |
+-------------------------------------------------------------------+
                                  |
                                  v
                  +-------------------------------+
                  |  Synthetic sEMG Generator     |
                  |  (Flexor & Extensor Ch, 1kHz) |
                  +-------------------------------+
                                  |
                                  v
                  +-------------------------------+
                  |   Feature Extraction Engine   |
                  |   (RMS, MAV, VAR, SSI, ZCR)   |
                  +-------------------------------+
                                  |
                                  v
                  +-------------------------------+
                  |   Edge ML Classifier          |
                  |   (Scikit-Learn Random Forest)|
                  +-------------------------------+
                                  | Predicted Grip + Confidence
                                  v
+-------------------------------------------------------------------+
|               CLOSED-LOOP ADAPTIVE GRIP CONTROLLER                |
|                                                                   |
|   Tactile Sensor Feedback (Simulated FSR Pressure, Newtons)       |
|                                 |                                 |
|                                 v                                 |
|   Proportional Force Regulation & Micro-Slip Perturbation Reflex  |
|                                 |                                 |
|                                 v                                 |
|   Actuator Command Generation (0-100% Servo Duty Effort)          |
+-------------------------------------------------------------------+
                                  |
                                  v
                  +-------------------------------+
                  |   Articulated Hand Visualizer |
                  |   (SVG 5-DOF Kinematics Canvas|
                  +-------------------------------+
```

## 5. Technology Stack

### Backend
- **Language**: Python 3.12+
- **Framework**: FastAPI (Asynchronous REST API)
- **Machine Learning**: Scikit-Learn (Edge-compatible Random Forest Classifier)
- **Numerical Processing**: NumPy, Pandas
- **Server**: Uvicorn ASGI

### Frontend
- **Framework**: React 19, TypeScript
- **Bundler & Dev Server**: Vite
- **Styling**: Tailwind CSS (Dark technical monochrome palette)
- **Waveform Rendering**: HTML5 Canvas 2D
- **Hand Visualization**: Responsive SVG coordinate transformation

## 6. Machine Learning Pipeline

### Data Synthesis & Characteristics
The system models two differential sEMG channels sampled at 1000 Hz with a 200 ms sliding observation window (200 samples per channel):
- **Channel 1**: Anterior flexor compartment (*Flexor Digitorum Superficialis*).
- **Channel 2**: Posterior extensor compartment (*Extensor Digitorum Communis*).

Four discrete physiological intentions are recognized:
1. **Open Hand**: Resting flexor noise floor, slight extensor activation.
2. **Power Grip**: High-amplitude co-contraction across both flexor and extensor compartments.
3. **Pinch Grip**: Moderate, selective flexor firing with minimal extensor involvement.
4. **Release**: Sharp transient profile with exponential decay toward baseline relaxation.

### Extracted Numerical Features
From each 200-sample window, the feature extraction engine derives:
- **Root Mean Square (RMS)**: Amplitude and energy metric:
  $$\text{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} x_i^2}$$
- **Mean Absolute Value (MAV)**: Measure of muscle contraction intensity:
  $$\text{MAV} = \frac{1}{N} \sum_{i=1}^{N} |x_i|$$
- **Variance (VAR)**: Signal power spread:
  $$\text{VAR} = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \bar{x})^2$$
- **Simple Square Integral / Energy (SSI)**: Total signal energy:
  $$\text{SSI} = \sum_{i=1}^{N} x_i^2$$
- **Zero Crossing Rate (ZCR)**: Frequency content indicator with noise deadband.
- **Channel Interaction Ratios**: Flexor-to-extensor ratio and differential activation.

### Classification Engine
A Scikit-Learn Random Forest Classifier (35 estimators, maximum depth 7) performs inference. On the synthetic benchmark distribution, the model demonstrates:
- **Synthetic Dataset Accuracy**: ~98-100%
- **Simulated Inference Time**: ~1.5 - 3.0 ms
- **Memory Footprint**: < 30 KB (readily convertible to embedded C arrays via TinyML / MicroML tools).

## 7. Adaptive Grip Logic & Closed-Loop Control

Rather than statically mapping classified grips to arbitrary motor angles, the system implements closed-loop tactile force regulation:

1. **Intention Setpoint**:
   - `OPEN`: Target pressure = 0.0 N
   - `RELEASE`: Target pressure = 0.0 N
   - `POWER_GRIP`: Target pressure = 50.0 N
   - `PINCH_GRIP`: Target pressure = 25.0 N
2. **Contact Detection**:
   When simulated fingertip/palm contact exceeds 5.0 N, the controller shifts from free closing to contact regulation mode.
3. **Pressure Regulation**:
   - If `current_pressure < target_pressure - deadband`: The controller increases servo effort proportionally.
   - If `current_pressure > target_pressure + deadband`: The controller decreases servo effort.
   - If within acceptable deadband (+/- 3.0 N): The controller locks actuation and enters `MAINTAINING` state.
4. **Overpressure Protection**:
   If pressure exceeds safety ceiling (75.0 N), immediate anti-crush force reduction is applied.
5. **Anti-Slip Reflex**:
   When simulated payload micro-slip occurs (simulating shear displacement detected by a tactile matrix), the controller bypasses steady-state regulation and applies an instantaneous compensatory torque boost (+18% effort, +12 N) to arrest slip before returning to equilibrium.

## 8. Running the Project

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```
Backend API will be accessible at: `http://127.0.0.1:8000` (Interactive Swagger docs at `http://127.0.0.1:8000/docs`).

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend dashboard will be accessible at: `http://127.0.0.1:5173/`.

## 9. Demo Instructions

The user interface supports both an automated 27-second sequence and manual interactive testing.

### Automated Demo Flow
Click the prominent **START DEMO** button on the toolbar:
1. **0–3 sec (Open Hand)**: Baseline muscle resting state, virtual hand open, tactile pressure 0 N.
2. **3–6 sec (Power Grip)**: High-amplitude sEMG burst classified; actuator command triggers finger flexion.
3. **6–9 sec (Contact Detection)**: Virtual hand encounters cylindrical payload; tactile FSR pads register contact (18.5 N).
4. **9–12 sec (Adaptive Step-Up)**: Pressure is below setpoint (50 N); adaptive controller increases motor command.
5. **12–15 sec (Grip Stabilization)**: Equilibrium achieved within deadband; controller state enters `MAINTAINING`.
6. **15–18 sec (Slip Event Injection)**: Simulated shear disturbance occurs; slip alert flag triggers.
7. **18–21 sec (Slip Compensation Reflex)**: Controller automatically boosts grip force to arrest displacement.
8. **21–24 sec (Stable Grasp Restored)**: Equilibrium re-established, stability index restored to 98.6%.
9. **24–27 sec (Release)**: User intention shifts to `RELEASE`; fingers extend outwards to 0 degrees.

### Manual Interactive Testing
- **Grip Selectors**: Click `OPEN HAND`, `POWER GRIP`, `PINCH GRIP`, or `RELEASE` to observe real-time waveform changes, feature extractions, and SVG joint kinematics.
- **Inject Slip Event**: Click `SIMULATE SLIP` when gripping an object to observe closed-loop compensatory torque recovery in real time.
- **Calibrate**: Click `CALIBRATE` to simulate a 2-second user resting baseline noise and MVC gain acquisition routine.
- **Reset**: Click `RESET` to return all actuators, filters, and controller state to idle baseline.

## 10. Current Limitations

- **Simulated Signal Domain**: sEMG signals are generated using stochastic mathematical models and frequency filtering rather than physical bio-potential instrumentation amplifiers.
- **Planar Kinematics**: The virtual hand visualizer operates in 2D vector coordinates rather than a 3D non-linear multibody physics engine.
- **Tactile Model**: Contact mechanics and slip triggers are modeled as discrete state transitions rather than continuous elastomeric friction dynamics.
- **Local Execution**: The system is designed for single-node local execution without physical telemetry buses (e.g., I2C, SPI, or CAN).

## 11. Future Hardware Integration Roadmap

The subsequent phase of this engineering project will deploy this verified control pipeline onto physical embedded hardware:
1. **Bio-Potential Acquisition**: 2-channel differential surface EMG analog front-end (e.g., AD8232 or MyoWare 2.0 sensors with Ag/AgCl wet electrodes).
2. **Tactile Sensing Array**: Piezoresistive Force Sensitive Resistors (Interlink FSR 402) or piezoresistive array at fingertips and thenar eminence.
3. **Embedded Edge AI Compute**: STMicroelectronics STM32F4 (ARM Cortex-M4) or Espressif ESP32-S3 microcontroller executing the trained classification model via Edge Impulse or TensorFlow Lite for Microcontrollers (TFLite Micro).
4. **Actuation Hardware**: 3D-printed bionic hand chassis actuated by MG996R or coreless metal-gear micro servos driven via PWM with PCA9685 driver.
5. **Power Management**: Regulated dual-rail lithium-ion battery system (7.4V servo supply, 3.3V isolated microcontroller supply).
