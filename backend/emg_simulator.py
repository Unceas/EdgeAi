"""
Synthetic Surface EMG (sEMG) Signal Generator.

Simulates 2-channel sEMG signals (Flexor Digitorum Superficialis & Extensor Digitorum Communis)
sampled at 1000 Hz over a 200 ms window (200 samples).
Signal generation uses band-limited Gaussian process noise modulated by muscle recruitment envelopes,
incorporating user calibration offsets and gains.
"""

from typing import Dict, List, Tuple
import numpy as np


class EMGSimulator:
    def __init__(self, sampling_rate_hz: int = 1000, window_size_samples: int = 200):
        self.fs = sampling_rate_hz
        self.n_samples = window_size_samples
        self.time_ms = np.linspace(0, (self.n_samples / self.fs) * 1000, self.n_samples, endpoint=False)
        
        # User calibration state (default normalized parameters)
        self.baseline_noise_floor = 0.04  # Volts
        self.mvc_gain = 1.0               # Maximum Voluntary Contraction scaling factor
        self.calibrated = False

    def set_calibration(self, baseline_noise: float, mvc_gain: float) -> None:
        """Update simulator with user-specific baseline and gain."""
        self.baseline_noise_floor = max(0.01, min(0.15, baseline_noise))
        self.mvc_gain = max(0.5, min(2.0, mvc_gain))
        self.calibrated = True

    def _generate_colored_noise(self, n_samples: int, center_freq: float = 120.0, bandwidth: float = 80.0) -> np.ndarray:
        """
        Generate physiological EMG-like frequency colored noise (approx 30-350 Hz dominant band)
        using frequency-domain filtering of Gaussian white noise.
        """
        white = np.random.normal(0, 1, n_samples)
        freqs = np.fft.rfftfreq(n_samples, d=1.0 / self.fs)
        
        # Gaussian-shaped bandpass envelope typical of surface EMG spectrum
        envelope = np.exp(-((freqs - center_freq) ** 2) / (2 * (bandwidth ** 2)))
        envelope[freqs < 20] = 0.0  # Motion artifact cutoff (<20 Hz)
        envelope[freqs > 450] = 0.0  # High-freq cutoff
        
        fft_coeffs = np.fft.rfft(white) * envelope
        colored = np.fft.irfft(fft_coeffs, n=n_samples)
        std = np.std(colored)
        if std > 1e-6:
            colored = colored / std
        return colored

    def generate_signal(self, grip_state: str, noise_level: float = 1.0) -> Dict[str, any]:
        """
        Generate a 2-channel sEMG window for a designated grip intention:
        - OPEN: Extensor bias, low flexor activity
        - POWER_GRIP: Strong co-contraction, high amplitude in both flexor and extensor
        - PINCH_GRIP: Focused flexor activity, moderate extensor
        - RELEASE: Rapid transient dropping to resting baseline
        """
        state_key = grip_state.upper().replace(" ", "_")
        
        # Scale baseline noise by the user-calibrated resting noise floor
        baseline_sigma = self.baseline_noise_floor * noise_level

        # Define stark, visually distinguishable activation amplitude profiles
        if state_key in ("OPEN", "OPEN_HAND"):
            # Very low baseline resting activity (quiet line)
            ch1_target_amp = 0.025 * self.mvc_gain
            ch2_target_amp = 0.055 * self.mvc_gain  # Subtle extensor baseline
            t_decay = np.ones(self.n_samples)
            baseline = 0.5 * baseline_sigma
        elif state_key in ("POWER_GRIP", "POWER"):
            # Strong, dense, high-amplitude bursts on both flexor and extensor
            ch1_target_amp = 0.92 * self.mvc_gain
            ch2_target_amp = 0.78 * self.mvc_gain
            t_decay = 0.9 + 0.15 * np.sin(np.linspace(0, 2 * np.pi, self.n_samples))
            baseline = 1.0 * baseline_sigma
        elif state_key in ("PINCH_GRIP", "PINCH"):
            # Distinct pattern: Selective moderate flexor burst, extensor nearly silent
            ch1_target_amp = 0.65 * self.mvc_gain
            ch2_target_amp = 0.06 * self.mvc_gain
            # Rhythmic 3-burst precision firing pattern
            t_decay = 0.6 + 0.4 * np.sin(np.linspace(0, 6 * np.pi, self.n_samples)) ** 2
            baseline = 0.625 * baseline_sigma
        elif state_key == "RELEASE":
            # Sharp brief transient spike (first 35 ms) then collapses to resting floor
            ch1_target_amp = 0.45 * self.mvc_gain
            ch2_target_amp = 0.35 * self.mvc_gain
            # Rapid decay: steep exponential dropoff
            decay_curve = np.exp(-np.linspace(0, 5.0, self.n_samples))
            t_decay = decay_curve
            baseline = 0.5 * baseline_sigma
        else:
            ch1_target_amp = 0.03 * self.mvc_gain
            ch2_target_amp = 0.03 * self.mvc_gain
            t_decay = np.ones(self.n_samples)
            baseline = 0.5 * baseline_sigma

        # Generate filtered burst shapes
        ch1_noise = self._generate_colored_noise(self.n_samples, center_freq=110, bandwidth=70)
        ch2_noise = self._generate_colored_noise(self.n_samples, center_freq=130, bandwidth=75)

        # Modulate with envelope and apply noise floor
        ch1_signal = (ch1_target_amp * t_decay * ch1_noise) + np.random.normal(0, baseline, self.n_samples)
        ch2_signal = (ch2_target_amp * t_decay * ch2_noise) + np.random.normal(0, baseline, self.n_samples)

        return {
            "time_ms": self.time_ms.tolist(),
            "channel_1_flexor": np.round(ch1_signal, 4).tolist(),
            "channel_2_extensor": np.round(ch2_signal, 4).tolist(),
            "intended_grip": state_key,
            "sampling_rate_hz": self.fs,
            "calibrated": self.calibrated
        }
