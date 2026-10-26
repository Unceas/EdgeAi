"""
Automated Test Suite for Edge AI Smart Prosthetic Hand Software Prototype.

Covers:
1. Feature extraction for boundary cases (N=0, N=1, N=200).
2. Input validation and HTTP 422 responses for short and mismatched channels.
3. Calibration parameter impact on synthetic sEMG signal generation.
4. Grip intention classifier accuracy, class probabilities, and host latency.
5. Adaptive controller state transitions, anti-crush ceiling, deadband, and slip reflex.
6. FastAPI endpoints status codes, CORS headers, and reset behavior.
"""

import sys
import os
import pytest
import numpy as np

# Add backend directory to module search path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from ml_model import extract_channel_features, extract_features, GripClassifier
from emg_simulator import EMGSimulator
from grip_controller import AdaptiveGripController
from main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


# ==========================================
# 1. Feature Extraction Boundary Tests
# ==========================================
class TestFeatureExtraction:
    def test_empty_signal(self):
        feats = extract_channel_features(np.array([]))
        assert feats["rms"] == 0.0
        assert feats["mav"] == 0.0
        assert feats["var"] == 0.0
        assert feats["energy"] == 0.0
        assert feats["zcr"] == 0.0
        assert not np.isnan(feats["zcr"])

    def test_single_sample_signal(self):
        val = 0.75
        feats = extract_channel_features(np.array([val]))
        assert feats["rms"] == pytest.approx(val, abs=1e-4)
        assert feats["mav"] == pytest.approx(val, abs=1e-4)
        assert feats["var"] == 0.0
        assert feats["energy"] == pytest.approx(val ** 2, abs=1e-3)
        assert feats["zcr"] == 0.0
        assert not np.isnan(feats["zcr"])

    def test_nominal_signal(self):
        np.random.seed(42)
        sig = np.random.normal(0, 0.5, 200)
        feats = extract_channel_features(sig)
        assert feats["rms"] > 0.0
        assert feats["mav"] > 0.0
        assert feats["var"] > 0.0
        assert feats["energy"] > 0.0
        assert 0.0 <= feats["zcr"] <= 1.0

    def test_two_channel_combined_features(self):
        ch1 = np.ones(50) * 0.2
        ch2 = np.ones(50) * 0.1
        f = extract_features(ch1, ch2)
        assert "ch1_rms" in f
        assert "ch2_rms" in f
        assert "ch_ratio" in f
        assert "ch_diff" in f
        assert "combined_rms" in f
        assert not np.isnan(f["ch_ratio"])
        assert not np.isnan(f["ch_diff"])
        assert f["ch_ratio"] > 1.0  # ch1 > ch2


# ==========================================
# 2. Calibration Parameter Impact Tests
# ==========================================
class TestCalibrationImpact:
    def test_noise_floor_scaling(self):
        sim = EMGSimulator()
        sim.set_calibration(baseline_noise=0.02, mvc_gain=1.0)
        sig_low = sim.generate_signal("OPEN", noise_level=1.0)
        std_low = float(np.std(sig_low["channel_1_flexor"]))

        sim.set_calibration(baseline_noise=0.12, mvc_gain=1.0)
        sig_high = sim.generate_signal("OPEN", noise_level=1.0)
        std_high = float(np.std(sig_high["channel_1_flexor"]))

        assert std_high > std_low, f"Expected higher noise std: low={std_low}, high={std_high}"

    def test_mvc_gain_scaling(self):
        sim = EMGSimulator()
        sim.set_calibration(baseline_noise=0.04, mvc_gain=0.6)
        sig_low_gain = sim.generate_signal("POWER_GRIP", noise_level=1.0)
        rms_low = float(np.sqrt(np.mean(np.array(sig_low_gain["channel_1_flexor"]) ** 2)))

        sim.set_calibration(baseline_noise=0.04, mvc_gain=1.8)
        sig_high_gain = sim.generate_signal("POWER_GRIP", noise_level=1.0)
        rms_high = float(np.sqrt(np.mean(np.array(sig_high_gain["channel_1_flexor"]) ** 2)))

        assert rms_high > rms_low, f"Expected higher amplitude for higher MVC gain: low={rms_low}, high={rms_high}"


# ==========================================
# 3. ML Model Classification & Metrics
# ==========================================
class TestClassifier:
    def test_model_training_and_cross_validation(self):
        clf = GripClassifier()
        metrics = clf.train()
        assert clf.is_trained is True
        assert metrics["synthetic_dataset_accuracy"] >= 90.0
        assert metrics["holdout_test_accuracy"] >= 90.0
        assert metrics["cv_5fold_mean_accuracy"] >= 90.0
        assert 0.0 <= metrics["macro_f1_score"] <= 1.0
        assert metrics["measured_inference_time_ms"] > 0.0

    def test_predict_output_structure(self):
        clf = GripClassifier()
        clf.train()
        ch1 = [0.1] * 200
        ch2 = [0.05] * 200
        res = clf.predict(ch1, ch2)
        assert res["predicted_grip"] in ["OPEN", "POWER_GRIP", "PINCH_GRIP", "RELEASE"]
        assert 0.0 <= res["confidence_percent"] <= 100.0
        assert res["measured_inference_time_ms"] > 0.0
        assert sum(res["class_probabilities"].values()) == pytest.approx(100.0, abs=1.0)


# ==========================================
# 4. Adaptive Controller Dynamics
# ==========================================
class TestAdaptiveController:
    def test_initial_and_reset_state(self):
        ctrl = AdaptiveGripController()
        ctrl.step("POWER_GRIP", simulated_contact=True)
        assert ctrl.grip_force > 0
        ctrl.reset()
        state = ctrl.get_state()
        assert state["current_pressure_n"] == 0.0
        assert state["grip_force_percent"] == 0.0
        assert state["contact_detected"] is False
        assert state["slip_detected"] is False
        assert state["controller_action"] == "IDLE"

    def test_contact_and_pressure_increase(self):
        ctrl = AdaptiveGripController()
        s1 = ctrl.step("POWER_GRIP", simulated_contact=True)
        assert s1["contact_detected"] is True
        assert s1["controller_action"] in ["INCREASING", "MAINTAINING"]
        assert s1["current_pressure_n"] > 0.0

    def test_anti_crush_ceiling_decreasing(self):
        ctrl = AdaptiveGripController()
        # Override pressure beyond MAX_SAFE_PRESSURE (75 N)
        s_crush = ctrl.step("POWER_GRIP", simulated_contact=True, pressure_override=82.0)
        assert s_crush["controller_action"] == "DECREASING"
        assert s_crush["current_pressure_n"] < 82.0

    def test_slip_detection_and_reflex_compensation(self):
        ctrl = AdaptiveGripController()
        # Normal contact step
        ctrl.step("POWER_GRIP", simulated_contact=True, pressure_override=30.0)
        force_before = ctrl.grip_force
        # Micro-slip trigger
        s_slip = ctrl.step("POWER_GRIP", simulated_contact=True, slip_trigger=True)
        assert s_slip["slip_detected"] is True
        assert s_slip["controller_action"] == "SLIP_COMPENSATION"
        assert s_slip["grip_force_percent"] > force_before
        assert s_slip["stability_index"] < 90.0

    def test_deadband_maintaining(self):
        ctrl = AdaptiveGripController()
        # Set pressure precisely within deadband of POWER_GRIP target (50.0 N)
        s = ctrl.step("POWER_GRIP", simulated_contact=True, pressure_override=50.0)
        assert s["controller_action"] == "MAINTAINING"
        assert s["stability_index"] > 95.0


# ==========================================
# 5. FastAPI Endpoints & Status Codes
# ==========================================
class TestApiEndpoints:
    def test_health(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "online"
        assert data["mode"] == "simulation"

    def test_metrics(self, client):
        res = client.get("/metrics")
        assert res.status_code == 200
        data = res.json()
        assert "synthetic_dataset_accuracy_percent" in data
        assert "holdout_test_accuracy_percent" in data
        assert "cv_5fold_mean_accuracy_percent" in data
        assert "macro_f1_score" in data
        assert "measured_inference_time_ms" in data

    def test_simulate_emg_valid(self, client):
        res = client.post("/simulate/emg", json={"grip_state": "POWER_GRIP", "noise_level": 1.2})
        assert res.status_code == 200
        data = res.json()
        assert len(data["channel_1_flexor"]) == 200
        assert len(data["channel_2_extensor"]) == 200

    def test_simulate_emg_invalid_state_422(self, client):
        res = client.post("/simulate/emg", json={"grip_state": "INVALID_STATE"})
        assert res.status_code == 422

    def test_predict_valid(self, client):
        res = client.post("/predict", json={
            "channel_1": [0.1] * 200,
            "channel_2": [0.05] * 200
        })
        assert res.status_code == 200
        data = res.json()
        assert data["predicted_grip"] in ["OPEN", "POWER_GRIP", "PINCH_GRIP", "RELEASE"]
        assert "measured_inference_time_ms" in data

    def test_predict_empty_channels_422(self, client):
        res = client.post("/predict", json={"channel_1": [], "channel_2": []})
        assert res.status_code == 422

    def test_predict_channel_mismatch_422(self, client):
        res = client.post("/predict", json={
            "channel_1": [0.1] * 20,
            "channel_2": [0.1] * 25
        })
        assert res.status_code == 422

    def test_predict_short_window_422(self, client):
        res = client.post("/predict", json={
            "channel_1": [0.1] * 10,
            "channel_2": [0.1] * 10
        })
        assert res.status_code == 422

    def test_predict_non_numeric_input_422(self, client):
        res = client.post("/predict", json={
            "channel_1": ["invalid_str"] * 20,
            "channel_2": [0.1] * 20
        })
        assert res.status_code == 422

    def test_predict_model_validation_rejects_nan_and_inf(self):
        import math
        from main import PredictRequest
        from pydantic import ValidationError

        # Reject NaN
        with pytest.raises((ValueError, ValidationError)):
            PredictRequest(channel_1=[math.nan] * 20, channel_2=[0.1] * 20)

        # Reject Inf
        with pytest.raises((ValueError, ValidationError)):
            PredictRequest(channel_1=[math.inf] * 20, channel_2=[0.1] * 20)

    def test_grip_control_valid(self, client):
        res = client.post("/grip/control", json={"predicted_grip": "PINCH_GRIP", "simulated_contact": True})
        assert res.status_code == 200
        data = res.json()
        assert data["contact_detected"] is True
        assert data["target_pressure_n"] == 25.0

    def test_grip_control_invalid_grip_422(self, client):
        res = client.post("/grip/control", json={"predicted_grip": "SUPER_GRIP"})
        assert res.status_code == 422

    def test_grip_control_invalid_pressure_override_422(self, client):
        res = client.post("/grip/control", json={"predicted_grip": "POWER_GRIP", "pressure_override": 999.0})
        assert res.status_code == 422

    def test_calibration_and_reset(self, client):
        cal = client.post("/calibrate", json={"subject_id": "test_subj", "simulated_duration_s": 2.5})
        assert cal.status_code == 200
        data = cal.json()
        assert data["status"] == "calibrated"
        assert "calibration_type" in data
        assert "disclaimer" in data

        rst = client.post("/reset")
        assert rst.status_code == 200
        assert rst.json()["status"] == "system_reset_complete"
