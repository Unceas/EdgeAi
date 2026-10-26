"""
Adaptive Closed-Loop Grip Controller.

Regulates simulated prosthetic actuator force based on real-time FSR tactile feedback,
target pressure thresholds, and slip-detection events to ensure safe, stable grasping
without crushing or dropping grasped objects.
"""

from typing import Dict, Any


class AdaptiveGripController:
    """
    Closed-loop feedback controller.
    
    Demonstrates:
    - Contact detection thresholding
    - Proportional pressure regulation towards target grip force
    - Anti-crush overpressure mitigation
    - Rapid micro-slip recovery reflex
    """

    # Target pressure baselines for each grip intention (in simulated Newtons)
    TARGET_PRESSURES = {
        "OPEN": 0.0,
        "RELEASE": 0.0,
        "POWER_GRIP": 50.0,   # Power grasp needs firmer hold
        "PINCH_GRIP": 25.0    # Precision pinch needs gentle hold
    }

    MAX_SAFE_PRESSURE = 75.0   # Ceiling to prevent crushing
    CONTACT_THRESHOLD = 5.0    # Minimum FSR pressure indicating contact
    DEADBAND = 3.0             # Hysteresis band to prevent actuator jitter

    def __init__(self):
        self.grip_force: float = 0.0           # Actuator effort: 0% to 100%
        self.current_pressure: float = 0.0     # Simulated FSR sensor reading (N)
        self.target_pressure: float = 0.0      # Setpoint (N)
        self.contact_detected: bool = False
        self.slip_detected: bool = False
        self.controller_action: str = "IDLE"   # INCREASING, DECREASING, MAINTAINING, SLIP_COMPENSATION
        self.active_grip: str = "OPEN"
        self.stability_index: float = 100.0    # Grasp stability score %

    def reset(self) -> None:
        self.grip_force = 0.0
        self.current_pressure = 0.0
        self.target_pressure = 0.0
        self.contact_detected = False
        self.slip_detected = False
        self.controller_action = "IDLE"
        self.active_grip = "OPEN"
        self.stability_index = 100.0

    def step(
        self,
        predicted_grip: str,
        simulated_contact: bool = False,
        slip_trigger: bool = False,
        pressure_override: float = None
    ) -> Dict[str, Any]:
        """
        Execute one controller cycle update.
        """
        self.active_grip = predicted_grip.upper().replace(" ", "_")
        self.target_pressure = self.TARGET_PRESSURES.get(self.active_grip, 0.0)

        # Handle release or open intention
        if self.active_grip in ("OPEN", "RELEASE"):
            self.grip_force = max(0.0, self.grip_force - 15.0)
            self.current_pressure = max(0.0, self.current_pressure - 12.0)
            self.contact_detected = False
            self.slip_detected = False
            self.controller_action = "RELEASING" if self.grip_force > 0 else "IDLE"
            self.stability_index = 100.0
            return self.get_state()

        # Update contact status
        if simulated_contact or self.current_pressure >= self.CONTACT_THRESHOLD:
            self.contact_detected = True
        else:
            self.contact_detected = False

        # Apply external sensor override if provided (for interactive slider testing)
        if pressure_override is not None:
            self.current_pressure = max(0.0, pressure_override)

        # Handle slip event
        if slip_trigger:
            self.slip_detected = True
            # Rapid compensatory torque boost (+18% effort, +12 N simulated response)
            self.grip_force = min(100.0, self.grip_force + 18.0)
            self.current_pressure = min(self.MAX_SAFE_PRESSURE, self.current_pressure + 12.0)
            self.controller_action = "SLIP_COMPENSATION"
            self.stability_index = 72.0
            return self.get_state()
        else:
            self.slip_detected = False

        # Closed-loop regulation when gripping an object
        if self.contact_detected:
            error = self.target_pressure - self.current_pressure

            if self.current_pressure > self.MAX_SAFE_PRESSURE:
                # Anti-crush overpressure intervention
                self.grip_force = max(10.0, self.grip_force - 10.0)
                self.current_pressure = max(self.target_pressure, self.current_pressure - 8.0)
                self.controller_action = "DECREASING"
                self.stability_index = 85.0
            elif abs(error) <= self.DEADBAND:
                # Within stable envelope
                self.controller_action = "MAINTAINING"
                self.stability_index = 98.5
                # Slight sensor noise emulation
                self.current_pressure += (0.2 if self.current_pressure < self.target_pressure else -0.2)
            elif error > 0:
                # Insufficient pressure: ramp up motor command
                proportional_step = min(12.0, max(2.5, error * 0.25))
                self.grip_force = min(100.0, self.grip_force + proportional_step)
                self.current_pressure = min(self.target_pressure + 2.0, self.current_pressure + (proportional_step * 0.75))
                self.controller_action = "INCREASING"
                self.stability_index = 91.0
            else:
                # Slight overshoot: ease motor command
                proportional_step = min(10.0, max(2.0, abs(error) * 0.25))
                self.grip_force = max(5.0, self.grip_force - proportional_step)
                self.current_pressure = max(self.target_pressure - 2.0, self.current_pressure - (proportional_step * 0.75))
                self.controller_action = "DECREASING"
                self.stability_index = 94.0
        else:
            # Closing phase before initial contact
            self.grip_force = min(60.0, self.grip_force + 15.0)
            self.current_pressure = 0.0
            self.controller_action = "CLOSING"
            self.stability_index = 95.0

        return self.get_state()

    def get_state(self) -> Dict[str, Any]:
        return {
            "current_pressure_n": round(self.current_pressure, 1),
            "target_pressure_n": round(self.target_pressure, 1),
            "max_safe_pressure_n": self.MAX_SAFE_PRESSURE,
            "grip_force_percent": round(self.grip_force, 1),
            "contact_detected": self.contact_detected,
            "slip_detected": self.slip_detected,
            "controller_action": self.controller_action,
            "active_grip": self.active_grip,
            "stability_index": round(self.stability_index, 1)
        }
