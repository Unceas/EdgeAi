"""
Edge AI Machine Learning Pipeline.

Performs:
1. Signal feature extraction (RMS, MAV, Variance, Energy, Zero-Crossing Rate, Channel Ratio).
2. Synthetic dataset synthesis across 4 grip classes.
3. Training of an edge-optimized Scikit-Learn Random Forest Classifier.
4. Low-latency inference with calibrated class probabilities.
"""

import time
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from emg_simulator import EMGSimulator


CLASSES = ["OPEN", "POWER_GRIP", "PINCH_GRIP", "RELEASE"]


def extract_channel_features(signal: np.ndarray, threshold: float = 0.015) -> Dict[str, float]:
    """
    Extract standard time-domain statistical features from a single sEMG channel:
    - Root Mean Square (RMS)
    - Mean Absolute Value (MAV)
    - Variance (VAR)
    - Simple Square Integral / Energy (SSI)
    - Zero Crossing Rate (ZCR)
    """
    n = len(signal)
    if n == 0:
        return {"rms": 0.0, "mav": 0.0, "var": 0.0, "energy": 0.0, "zcr": 0.0}
    if n == 1:
        val = float(signal[0])
        return {
            "rms": round(abs(val), 4),
            "mav": round(abs(val), 4),
            "var": 0.0,
            "energy": round(val ** 2, 3),
            "zcr": 0.0
        }

    # Mean Absolute Value
    mav = float(np.mean(np.abs(signal)))
    
    # Root Mean Square
    rms = float(np.sqrt(np.mean(signal ** 2)))
    
    # Variance
    var = float(np.var(signal))
    
    # Signal Energy
    energy = float(np.sum(signal ** 2))
    
    # Zero Crossing Rate with noise threshold
    sign_changes = ((signal[:-1] * signal[1:]) < 0) & (np.abs(signal[:-1] - signal[1:]) > threshold)
    zcr = float(np.sum(sign_changes) / (n - 1)) if n > 1 else 0.0

    return {
        "rms": round(float(np.nan_to_num(rms, nan=0.0)), 4),
        "mav": round(float(np.nan_to_num(mav, nan=0.0)), 4),
        "var": round(float(np.nan_to_num(var, nan=0.0)), 5),
        "energy": round(float(np.nan_to_num(energy, nan=0.0)), 3),
        "zcr": round(float(np.nan_to_num(zcr, nan=0.0)), 4)
    }


def extract_features(ch1: np.ndarray, ch2: np.ndarray) -> Dict[str, float]:
    """
    Extract combined 2-channel feature vector suitable for edge ML classification.
    """
    f1 = extract_channel_features(ch1)
    f2 = extract_channel_features(ch2)
    
    # Channel interaction ratio (Flexor vs Extensor bias)
    denom = f2["mav"] + 1e-4
    ratio = (f1["mav"] + 1e-4) / denom if denom != 0 else 1.0
    ch_diff = f1["mav"] - f2["mav"]

    return {
        "ch1_rms": f1["rms"],
        "ch1_mav": f1["mav"],
        "ch1_var": f1["var"],
        "ch1_energy": f1["energy"],
        "ch1_zcr": f1["zcr"],
        "ch2_rms": f2["rms"],
        "ch2_mav": f2["mav"],
        "ch2_var": f2["var"],
        "ch2_energy": f2["energy"],
        "ch2_zcr": f2["zcr"],
        "ch_ratio": round(float(np.nan_to_num(ratio, nan=1.0)), 4),
        "ch_diff": round(float(np.nan_to_num(ch_diff, nan=0.0)), 4),
        # Aggregate summary features for UI display
        "combined_rms": round((f1["rms"] + f2["rms"]) / 2.0, 4),
        "combined_mav": round((f1["mav"] + f2["mav"]) / 2.0, 4),
        "combined_energy": round(f1["energy"] + f2["energy"], 3),
        "combined_zcr": round((f1["zcr"] + f2["zcr"]) / 2.0, 4)
    }


class GripClassifier:
    """Lightweight classifier representing edge-deployable model (e.g. TinyML / ARM Cortex-M target)."""

    FEATURE_KEYS = [
        "ch1_rms", "ch1_mav", "ch1_var", "ch1_energy", "ch1_zcr",
        "ch2_rms", "ch2_mav", "ch2_var", "ch2_energy", "ch2_zcr",
        "ch_ratio", "ch_diff"
    ]

    def __init__(self):
        # Compact Random Forest suited for embedded/edge conversion
        self.model = RandomForestClassifier(
            n_estimators=35,
            max_depth=7,
            min_samples_split=4,
            random_state=42
        )
        self.classes = CLASSES
        self.metrics: Dict[str, Any] = {}
        self.is_trained = False
        self.simulator = EMGSimulator()

    def generate_synthetic_dataset(self, samples_per_class: int = 200) -> Tuple[pd.DataFrame, np.ndarray]:
        """Synthesize training windows using varying physiological parameters."""
        X_rows = []
        y_labels = []

        for label in self.classes:
            for _ in range(samples_per_class):
                # Apply randomized gain and noise variations to mimic inter-trial subject variance
                random_gain = np.random.uniform(0.85, 1.15)
                random_noise = np.random.uniform(0.8, 1.25)
                self.simulator.set_calibration(
                    baseline_noise=0.04 * random_noise,
                    mvc_gain=random_gain
                )
                raw = self.simulator.generate_signal(label, noise_level=random_noise)
                feats = extract_features(
                    np.array(raw["channel_1_flexor"]),
                    np.array(raw["channel_2_extensor"])
                )
                X_rows.append([feats[k] for k in self.FEATURE_KEYS])
                y_labels.append(label)

        X = pd.DataFrame(X_rows, columns=self.FEATURE_KEYS)
        y = np.array(y_labels)
        return X, y

    def train(self) -> Dict[str, Any]:
        """Train classifier and evaluate holdout and 5-fold cross-validation metrics."""
        X, y = self.generate_synthetic_dataset(samples_per_class=180)

        # 5-fold Stratified Cross-Validation on entire synthetic dataset
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(self.model, X, y, cv=cv, scoring='accuracy')
        cv_mean = float(np.mean(cv_scores))
        cv_std = float(np.std(cv_scores))

        # Stratified holdout split (75% train, 25% test) for detailed classification metrics
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )

        start_time = time.perf_counter()
        self.model.fit(X_train, y_train)
        training_duration_s = time.perf_counter() - start_time

        # Test evaluation
        y_preds = self.model.predict(X_test)
        holdout_acc = accuracy_score(y_test, y_preds)

        # True Macro-averaged F1 and Weighted-averaged F1
        macro_prec, macro_rec, macro_f1, _ = precision_recall_fscore_support(
            y_test, y_preds, average='macro', zero_division=0
        )
        weighted_prec, weighted_rec, weighted_f1, _ = precision_recall_fscore_support(
            y_test, y_preds, average='weighted', zero_division=0
        )

        # Benchmark real host inference latency over 50 repetitions with warm-up
        sample_df = X_test.iloc[[0]]
        for _ in range(5):
            _ = self.model.predict(sample_df)

        bench_latencies = []
        for _ in range(50):
            t_bench = time.perf_counter()
            _ = self.model.predict(sample_df)
            bench_latencies.append((time.perf_counter() - t_bench) * 1000.0)
        mean_bench_latency_ms = round(float(np.mean(bench_latencies)), 2)

        self.metrics = {
            "synthetic_dataset_accuracy": round(float(cv_mean) * 100, 2),
            "holdout_test_accuracy": round(float(holdout_acc) * 100, 2),
            "cv_5fold_mean_accuracy": round(float(cv_mean) * 100, 2),
            "cv_5fold_std": round(float(cv_std) * 100, 2),
            "macro_f1_score": round(float(macro_f1), 4),
            "weighted_f1_score": round(float(weighted_f1), 4),
            "simulated_inference_time_ms": mean_bench_latency_ms,
            "measured_inference_time_ms": mean_bench_latency_ms,
            "training_duration_s": round(training_duration_s, 3),
            "total_synthetic_samples": len(X),
            "feature_count": len(self.FEATURE_KEYS),
            "model_type": "Scikit-Learn Random Forest (35 trees, depth 7)",
            "classes": self.classes
        }
        self.is_trained = True
        return self.metrics

    def predict(self, ch1: List[float], ch2: List[float]) -> Dict[str, Any]:
        """Predict grip class from raw EMG windows."""
        if not self.is_trained:
            self.train()

        arr_ch1 = np.array(ch1, dtype=np.float32)
        arr_ch2 = np.array(ch2, dtype=np.float32)
        
        t0 = time.perf_counter()
        features = extract_features(arr_ch1, arr_ch2)
        input_vector = [features[k] for k in self.FEATURE_KEYS]
        input_df = pd.DataFrame([input_vector], columns=self.FEATURE_KEYS)

        pred_class = self.model.predict(input_df)[0]
        probs = self.model.predict_proba(input_df)[0]
        measured_latency_ms = round((time.perf_counter() - t0) * 1000.0, 2)

        class_probabilities = {
            cls: round(float(prob) * 100, 1)
            for cls, prob in zip(self.model.classes_, probs)
        }
        confidence = class_probabilities.get(pred_class, 0.0)

        return {
            "predicted_grip": pred_class,
            "confidence_percent": confidence,
            "simulated_inference_time_ms": measured_latency_ms,
            "measured_inference_time_ms": measured_latency_ms,
            "class_probabilities": class_probabilities,
            "features": features
        }
