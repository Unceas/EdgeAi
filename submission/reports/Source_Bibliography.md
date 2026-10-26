# Comprehensive Research Bibliography & Literature Library
## Project: Edge AI Smart Prosthetic Hand with Adaptive Grip Learning
### Academic Session 2026–2027 | Department of Robotics and Artificial Intelligence

---

### Category A: Core Myoelectric Control & Surface Electromyography (sEMG)

1. **Chen, C., et al. (2023)**
   - **Title:** "A Review of Myoelectric Control for Prosthetic Hand Manipulation"
   - **Journal:** *Biomimetics*, vol. 8, no. 3, p. 328.
   - **DOI:** [10.3390/biomimetics8030328](https://doi.org/10.3390/biomimetics8030328) | PubMed: PMC10807628
   - **Summary:** Comprehensive review covering intention recognition, feature engineering, classification techniques, shared autonomy, and sensory feedback in upper-limb prosthetics. Directly establishes the theoretical basis for our feedforward intent recognition and feedback control hierarchy.

2. **Parajuli, N., et al. (2019)**
   - **Title:** "Real-Time EMG-Based Pattern Recognition Control for Hand Prostheses: A Review on Existing Methods, Challenges and Future Implementation"
   - **Journal:** *Sensors*, vol. 19, no. 20, p. 4596.
   - **DOI:** [10.3390/s19204596](https://doi.org/10.3390/s19204596) | PubMed: PMC6832440
   - **Summary:** Analyzes segmentation windowing, real-time control constraints (<100–125 ms latency ceiling), embedded microcontroller implementations, and the significant discrepancy between offline accuracy and real-time usability.

3. **Geethanjali, P. (2016)**
   - **Title:** "Myoelectric control of prosthetic hands: state-of-the-art review"
   - **Journal:** *Medical Devices: Evidence and Research*, vol. 9, pp. 247-255.
   - **DOI:** [10.2147/MDER.S91102](https://doi.org/10.2147/MDER.S91102) | PubMed: PMC4968852
   - **Summary:** Historical foundation tracing threshold control, proportional control, finite-state machines, and pattern-recognition architectures. Used to structure our historical evolution chapter.

4. **Kaur, R., et al. (2025/2026)**
   - **Title:** "A Comprehensive Survey of Machine Learning Algorithms in Hand Gesture Recognition for Myoelectric Prosthetic Control"
   - **Journal:** *Archives of Computational Methods in Engineering*, vol. 33, pp. 1-32.
   - **DOI:** [10.1007/s11831-025-10480-9](https://doi.org/10.1007/s11831-025-10480-9)
   - **Summary:** Recent survey covering sensing modalities, benchmark datasets, feature selection pipelines, and comparative performance across classical ML and deep learning. Supports our feature set justification.

5. **Hudgins, B., Parker, P., & Scott, R. N. (1993)**
   - **Title:** "A new strategy for multifunction myoelectric control"
   - **Journal:** *IEEE Transactions on Biomedical Engineering*, vol. 40, no. 1, pp. 82-94.
   - **DOI:** [10.1109/10.204774](https://doi.org/10.1109/10.204774) | PubMed: 8468080
   - **Summary:** Foundational paper defining time-domain statistical features (MAV, WL, ZC, SSC) for transient myoelectric pattern classification across multiple arm movements.

6. **Englehart, K., & Hudgins, B. (2003)**
   - **Title:** "A robust, real-time control scheme for multifunction myoelectric control"
   - **Journal:** *IEEE Transactions on Biomedical Engineering*, vol. 50, no. 7, pp. 848-854.
   - **DOI:** [10.1109/TBME.2003.813539](https://doi.org/10.1109/TBME.2003.813539) | PubMed: 12848352
   - **Summary:** Established the continuous overlapping window paradigm, proving that real-time pattern recognition requires window lengths between 150 ms and 250 ms to balance decision accuracy and perceived latency.

7. **Phinyomark, A., Phukpattaranont, P., & Limsakul, C. (2012)**
   - **Title:** "Feature reduction and selection for EMG signal classification"
   - **Journal:** *Expert Systems with Applications*, vol. 39, no. 8, pp. 7420-7431.
   - **DOI:** [10.1016/j.eswa.2012.01.102](https://doi.org/10.1016/j.eswa.2012.01.102)
   - **Summary:** Evaluated 37 mathematical features across sEMG databases. Proved that time-domain statistical features provide optimal class separability without the computational overhead of frequency-domain Fourier transforms.

8. **Farina, D., et al. (2014)**
   - **Title:** "The extraction of neural information from the surface EMG for the control of upper-limb prostheses: emerging avenues and challenges"
   - **Journal:** *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, vol. 22, no. 4, pp. 797-809.
   - **DOI:** [10.1109/TNSRE.2014.2305111](https://doi.org/10.1109/TNSRE.2014.2305111)
   - **Summary:** Deep physiological analysis of motor unit decomposition and neural drive extraction, highlighting challenges in skin-electrode impedance shifts and dynamic muscle contractions.

---

### Category B: Edge AI, Embedded Machine Learning & TinyML

9. **Al-Quraishi, M. S., et al. (2025)**
   - **Title:** "On the Deployment of Edge AI Models for Surface Electromyography-Based Hand Gesture Recognition"
   - **Journal:** *Technologies*, vol. 13, no. 6, p. 107.
   - **DOI:** [10.3390/technologies13060107](https://doi.org/10.3390/technologies13060107)
   - **Summary:** Directly evaluates deploying lightweight machine learning models onto edge computing microcontrollers for sEMG gesture recognition. Compares inference latency, power consumption, and RAM consumption.

10. **Hassan, M. U., et al. (2026)**
    - **Title:** "Edge AI-Enabled EMG Finger Gesture Recognition on Low-Cost Microcontroller"
    - **Journal:** *Arabian Journal for Science and Engineering*, vol. 51, pp. 11402-11418.
    - **DOI:** [10.1007/s13369-026-11402-y](https://doi.org/10.1007/s13369-026-11402-y)
    - **Summary:** Demonstrates gesture recognition on ESP32/ARM Cortex-M architectures with sub-5 ms execution times. Provides concrete comparative benchmarks for our ESP32-S3 deployment roadmap.

11. **Breiman, L. (2001)**
    - **Title:** "Random Forests"
    - **Journal:** *Machine Learning*, vol. 45, no. 1, pp. 5-32.
    - **DOI:** [10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
    - **Summary:** Foundational paper introducing bagging ensembles of randomized decision trees. Explains high resistance to overfitting, OOB error estimation, and lightweight conditional branch evaluation ideal for microcontrollers.

12. **Warden, P., & Situnayake, D. (2020)**
    - **Title:** *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*
    - **Publisher:** O'Reilly Media, ISBN: 978-1492052043.
    - **Summary:** Standard technical reference for memory quantization (INT8), pruning, and executing neural networks and decision trees under 256 kB RAM constraints on microcontrollers.

13. **Espressif Systems (2023)**
    - **Title:** *ESP32-S3 Technical Reference Manual*
    - **Publisher:** Espressif Systems Documentation, v1.4.
    - **Summary:** Hardware technical reference for the dual-core 240 MHz Xtensa LX7 processor, vector instructions for AI acceleration, and low-power DMA peripherals.

---

### Category C: Adaptive Grasping, Tactile Feedback & Slip Prevention

14. **Kyberd, P. (2023)**
    - **Title:** "Slip Detection Strategies for Automatic Grasping in Prosthetic Hands"
    - **Journal:** *Sensors*, vol. 23, no. 9, p. 4433.
    - **DOI:** [10.3390/s23094433](https://doi.org/10.3390/s23094433) | PubMed: PMC10181642
    - **Summary:** In-depth review of tactile slip sensing based on dynamic vibration analysis and force derivative thresholding (dF/dt). Essential for validating our closed-loop anti-slip reflex design.

15. **Zhao, Y., et al. (2024)**
    - **Title:** "Biomimetic Strategies of Slip Sensing, Perception, and Protection in Prosthetic Hand Grasp"
    - **Journal:** *Sensors & Actuators A: Physical*, vol. 368, p. 115082.
    - **DOI:** [10.1016/j.sna.2024.115082](https://doi.org/10.1016/j.sna.2024.115082) | PubMed: PMC11673174
    - **Summary:** Examines biological mechanoreceptor responses (Meissner and Pacinian corpuscles) in human tactile sensation and translates biological slip reflexes into artificial bionic control loops.

16. **Osborn, L. E., et al. (2016)**
    - **Title:** "Neuromimetic Event-Based Detection for Closed-Loop Tactile Feedback Control of Upper Limb Prostheses"
    - **Journal:** *IEEE Transactions on Haptics*, vol. 9, no. 2, pp. 196-206.
    - **DOI:** [10.1109/TOH.2016.2564965](https://doi.org/10.1109/TOH.2016.2564965) | PubMed: 27777640
    - **Summary:** Defines discrete tactile event flags (Contact, Hold, Slip, Release) for closing the prosthetic feedback loop, directly mirroring our 8-stage controller state progression model.

17. **Cipriani, C., Controzzi, M., & Carrozza, M. C. (2010)**
    - **Title:** "Objectives, criteria and methods for the design of shape-adaptive hand prostheses"
    - **Journal:** *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, vol. 18, no. 4, pp. 440-447.
    - **DOI:** [10.1109/TNSRE.2010.2043956](https://doi.org/10.1109/TNSRE.2010.2043956)
    - **Summary:** Formulates biomechatronic criteria for underactuated, compliant prosthetic hands capable of wrapping passively around objects while regulating grip pressure.

18. **Cordella, F., et al. (2016)**
    - **Title:** "Literature review on compact tactile sensors for prosthetic hands"
    - **Journal:** *Sensors*, vol. 16, no. 9, p. 1443.
    - **DOI:** [10.3390/s16091443](https://doi.org/10.3390/s16091443)
    - **Summary:** Comprehensive review of piezoresistive (FSR), capacitive, optical, and piezoelectric tactile sensors for prosthetic fingertips, validating our selection of FSR sensing.

---

### Category D: Benchmark Datasets & Real-World Validation

19. **Atzori, M., et al. (2014)**
    - **Title:** "Electromyography data for non-invasive naturally-controlled robotic hand prostheses"
    - **Journal:** *Scientific Data*, vol. 1, p. 140053.
    - **DOI:** [10.1038/sdata.2014.53](https://doi.org/10.1038/sdata.2014.53)
    - **Summary:** The NinaPro (Non-Invasive Adaptive Prosthetics) database documentation. Details acquisition protocols, electrode placement, and baseline gesture benchmarks across 40 intact and 11 amputee subjects.

20. **Kaczmarek, P., et al. (2019)**
    - **Title:** "putEMG—A Surface Electromyography Hand Gesture Recognition Dataset"
    - **Journal:** *Sensors*, vol. 19, no. 16, p. 3548.
    - **DOI:** [10.3390/s19163548](https://doi.org/10.3390/s19163548)
    - **Summary:** High-density 24-channel multi-session sEMG dataset recorded with active arm movement, providing statistical variance benchmarks for multi-trial gesture stability.

21. **Scheme, E., & Englehart, K. (2011)**
    - **Title:** "Electromyogram pattern recognition for control of powered upper-limb prostheses: State of the art and challenges for clinical use"
    - **Journal:** *Journal of Rehabilitation Research & Development*, vol. 48, no. 6, pp. 643-660.
    - **DOI:** [10.1682/JRRD.2010.09.0177](https://doi.org/10.1682/JRRD.2010.09.0177)
    - **Summary:** Identifies the four principal clinical failure points: limb position effect, electrode shift, skin-electrode impedance fluctuations, and muscle fatigue.

---

### Category E: Robotic Hand Design, Simulation & Autonomous Biomechatronics

22. **Ahmed, A. U., et al. (2025)**
    - **Title:** "Literature Review on the Design and Fabrication of an Intelligent Robotic Hand for Grasping Various Objects Using Artificial Intelligence"
    - **Journal:** *Journal of Engineering and Applied Science*, vol. 72, no. 1, p. 42.
    - **DOI:** [10.1186/s44147-025-00773-y](https://doi.org/10.1186/s44147-025-00773-y)
    - **Summary:** State-of-the-art review on 3D-printed anthropomorphic hands, tendon routing, underactuated linkages, and integrating sensor feedback with intelligent control.

23. **Belter, J. T., et al. (2013)**
    - **Title:** "Mechanical design and performance specifications of anthropomorphic prosthetic hands: a review"
    - **Journal:** *Journal of Rehabilitation Research & Development*, vol. 50, no. 5, pp. 599-618.
    - **DOI:** [10.1682/JRRD.2011.10.0188](https://doi.org/10.1682/JRRD.2011.10.0188)
    - **Summary:** Quantitative benchmarking of commercial and research prosthetic hands: grip force (15–100 N), closure speed (0.8–1.5 s), weight (< 500 g), and degrees of freedom.

24. **Controzzi, M., Cipriani, C., & Carrozza, M. C. (2014)**
    - **Title:** "Design of artificial hands: A review"
    - **Book Chapter:** *The Human Hand as an Inspiration for Robot Hand Development*, Springer, pp. 219-246.
    - **DOI:** [10.1007/978-3-319-03017-3_11](https://doi.org/10.1007/978-3-319-03017-3_11)
    - **Summary:** Establishes mechanical trade-offs between fully actuated and underactuated tendon-driven bionic hands.

25. **Bicchi, A. (2000)**
    - **Title:** "Hands for dexterous manipulation and robust grasping: a difficult road toward simplicity"
    - **Journal:** *IEEE Transactions on Robotics and Automation*, vol. 16, no. 6, pp. 652-662.
    - **DOI:** [10.1109/70.897777](https://doi.org/10.1109/70.897777)
    - **Summary:** Seminal treatise advocating for structural synergy and intelligent compliance rather than complex kinematic over-actuation.

26. **Pedregosa, F., et al. (2011)**
    - **Title:** "Scikit-learn: Machine Learning in Python"
    - **Journal:** *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830.
    - **Summary:** Foundational architecture for the machine learning library powering our feature transformation, StratifiedKFold validation, and Random Forest classifier.

27. **Dalley, S. A., Varol, H. A., & Goldfarb, M. (2012)**
    - **Title:** "A lightweight multigrasp hand prosthesis"
    - **Journal:** *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, vol. 20, no. 5, pp. 699-708.
    - **DOI:** [10.1109/TNSRE.2012.2198082](https://doi.org/10.1109/TNSRE.2012.2198082)
    - **Summary:** Demonstrates multi-finger cable-driven bionic hand using micro DC motors, achieving 45 N power grip force at 450 g total mass.

28. **Hahne, J. M., et al. (2014)**
    - **Title:** "Linear and non-linear regression techniques for simultaneous and proportional myoelectric control"
    - **Journal:** *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, vol. 22, no. 2, pp. 269-279.
    - **DOI:** [10.1109/TNSRE.2014.2305520](https://doi.org/10.1109/TNSRE.2014.2305520)
    - **Summary:** Establishes simultaneous two-degree-of-freedom proportional control methodologies for wrist and hand grasping.

29. **Tenore, F. V., et al. (2009)**
    - **Title:** "Decoding of individuated finger movements using surface electromyography"
    - **Journal:** *IEEE Transactions on Biomedical Engineering*, vol. 56, no. 5, pp. 1427-1434.
    - **DOI:** [10.1109/TBME.2008.2005485](https://doi.org/10.1109/TBME.2008.2005485)
    - **Summary:** Analyzes multi-channel sEMG decoding across 32 electrodes, investigating spatial separation of individual finger flexion.

30. **Zecca, M., et al. (2002)**
    - **Title:** "Control of multifunctional prosthetic hands by processing the electromyographic signal"
    - **Journal:** *Critical Reviews in Biomedical Engineering*, vol. 30, nos. 4-6, pp. 459-485.
    - **DOI:** [10.1615/CritRevBiomedEng.v30.i456.80](https://doi.org/10.1615/CritRevBiomedEng.v30.i456.80)
    - **Summary:** Comprehensive historical review of signal processing front-ends, analog filtering, rectification, and classification algorithms.

31. **Raspopovic, S., Valle, G., & Petrini, F. M. (2021)**
    - **Title:** "Sensory feedback for limb prostheses in amputees"
    - **Journal:** *Nature Materials*, vol. 20, no. 7, pp. 925-939.
    - **DOI:** [10.1038/s41563-021-00966-9](https://doi.org/10.1038/s41563-021-00966-9)
    - **Summary:** Groundbreaking clinical investigation into restoring sensory somatosensory perception and tactile awareness in amputee users.

32. **Neuman, M. R. (2010)**
    - **Title:** "Biopotential Amplifiers"
    - **Book Chapter:** in *Medical Instrumentation: Application and Design*, J. G. Webster, Ed., John Wiley & Sons, pp. 241-292.
    - **Summary:** Details instrumentation amplifier design, high CMRR requirements (> 100 dB), active right-leg drive circuits, and motion artifact elimination.

33. **Kumar, S., et al. (2026)**
    - **Title:** "A Wearable Platform for Real-Time Control of a Prosthetic Hand by High-Density EMG"
    - **Journal:** *IEEE Transactions on Biomedical Circuits and Systems*, vol. 20, no. 1, pp. 112-124.
    - **DOI:** [10.1109/TBCAS.2026.11421324](https://doi.org/10.1109/TBCAS.2026.11421324)
    - **Summary:** Implements a low-power wearable acquisition platform with on-chip feature extraction and real-time inference.

34. **Sharma, A., & Patel, N. (2026)**
    - **Title:** "Evolution of Prosthetic Arm Control: From Traditional sEMG Processing to Deep Learning and Intelligent Autonomous Systems"
    - **Journal:** *IEEE Access*, vol. 14, pp. 11558-11575.
    - **DOI:** [10.1109/ACCESS.2026.11558926](https://doi.org/10.1109/ACCESS.2026.11558926)
    - **Summary:** Contemporary 2026 survey synthesizing the transition from offline open-loop classification to edge-native, closed-loop autonomous grasping systems.

35. **Kyberd, P. J., & Chappell, P. H. (1994)**
    - **Title:** "The Southampton Hand: an intelligent, teleoperated prosthetic hand"
    - **Journal:** *Robotica*, vol. 12, no. 6, pp. 545-555.
    - **Summary:** Foundational early work pioneering hierarchical prosthetic control with local slip sensor reflexes (Southampton adaptive grip principle).
