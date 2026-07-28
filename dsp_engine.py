"""
VibeGuard AI — Digital Signal Processing & Machine Learning Engine
Handles time-domain statistical feature extraction, Fast Fourier Transform (FFT) 
frequency decomposition, ISO 10816-3 compliance checks, and Isolation Forest anomaly scoring.
"""

import numpy as np
from scipy.stats import kurtosis, skew
from sklearn.ensemble import IsolationForest


def generate_synthetic_signal(fs: int = 2000, duration: float = 0.2, fault_severity: float = 0.05):
    """
    Generates a high-frequency vibration signal g(t) simulating industrial motor spindle behavior.
    
    Parameters:
        fs (int): Sampling frequency in Hz (default 2000 Hz)
        duration (float): Time window in seconds
        fault_severity (float): Anomaly intensity from 0.0 (clean) to 1.0 (critical failure)
        
    Returns:
        tuple: (time_array, combined_vibration_signal)
    """
    num_samples = int(fs * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    
    # 50 Hz fundamental rotational frequency (3000 RPM spindle baseline)
    base_wave = np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.08, num_samples)
    
    # 380 Hz BPFI (Ball Pass Frequency Inner Race) bearing defect transient harmonics
    fault_impacts = fault_severity * (2.2 * np.sin(2 * np.pi * 380 * t) + np.random.normal(0, 0.35, num_samples))
    
    combined_signal = base_wave + fault_impacts
    return t, combined_signal


def extract_vibration_features(raw_signal: np.ndarray, fs: int = 2000):
    """
    Extracts statistical time-domain and frequency-domain features from raw acceleration data.
    
    Metrics Computed:
    - RMS (Root Mean Square): Total vibration energy
    - Peak Amplitude: Maximum absolute acceleration
    - Crest Factor: Ratio of peak to RMS (detects sharp impacts)
    - Kurtosis: Tailedness of distribution (pure noise ~ 3.0, damaged bearings > 4.5)
    - Skewness: Asymmetry of the vibration wave
    - FFT Spectrum: Frequency magnitude decomposition
    - Spectral Centroid: Center of gravity of frequency spectrum
    
    Parameters:
        raw_signal (np.ndarray): 1D array of acceleration samples in g
        fs (int): Sampling rate in Hz
        
    Returns:
        dict: Complete feature vector and spectral vectors for plotting
    """
    # ---------------------------------------------------------
    # 1. TIME-DOMAIN STATISTICAL METRICS
    # ---------------------------------------------------------
    rms = np.sqrt(np.mean(raw_signal ** 2))
    peak = np.max(np.abs(raw_signal))
    crest_factor = peak / (rms + 1e-6)
    kurt_val = kurtosis(raw_signal) + 3.0  # Normalized so Gaussian noise = 3.0
    skew_val = skew(raw_signal)
    
    # ---------------------------------------------------------
    # 2. FREQUENCY-DOMAIN METRICS (FAST FOURIER TRANSFORM)
    # ---------------------------------------------------------
    num_samples = len(raw_signal)
    fft_vals = np.abs(np.fft.rfft(raw_signal)) / num_samples
    fft_freqs = np.fft.rfftfreq(num_samples, 1 / fs)
    
    # Peak Frequency and Spectral Centroid
    peak_freq_idx = np.argmax(fft_vals)
    peak_frequency_hz = fft_freqs[peak_freq_idx]
    peak_fft_db = float(20 * np.log10(fft_vals[peak_freq_idx] + 1e-6) + 60) # dB normalized scale
    
    spectral_centroid = np.sum(fft_freqs * fft_vals) / (np.sum(fft_vals) + 1e-6)
    
    return {
        "rms_g": float(np.round(rms, 3)),
        "peak_g": float(np.round(peak, 3)),
        "crest_factor": float(np.round(crest_factor, 2)),
        "kurtosis": float(np.round(kurt_val, 2)),
        "skewness": float(np.round(skew_val, 2)),
        "peak_freq_hz": float(np.round(peak_frequency_hz, 1)),
        "peak_fft_db": float(np.round(peak_fft_db, 1)),
        "spectral_centroid": float(np.round(spectral_centroid, 1)),
        "fft_vals": fft_vals,
        "fft_freqs": fft_freqs
    }


def evaluate_iso_severity(vibe_rms: float) -> dict:
    """
    Evaluates vibration severity based on international ISO 10816-3 standards for Class II industrial motors.
    
    Zone Definitions:
    - Zone A/B (< 2.80 g): Good / Acceptable unrestricted continuous operation.
    - Zone C (2.80 g - 4.50 g): Unsatisfactory / Warning state (maintenance needed).
    - Zone D (> 4.50 g): Critical / Danger state (imminent damage risk).
    """
    if vibe_rms < 1.80:
        return {"zone": "Zone A", "status": "EXCELLENT", "color": "#10B981"}
    elif vibe_rms < 2.80:
        return {"zone": "Zone B", "status": "ACCEPTABLE", "color": "#00E5FF"}
    elif vibe_rms < 4.50:
        return {"zone": "Zone C", "status": "WARNING", "color": "#F59E0B"}
    else:
        return {"zone": "Zone D", "status": "CRITICAL DANGER", "color": "#EF4444"}


class AnomalyDetector:
    """
    Wrapper for Scikit-Learn Isolation Forest model.
    Learns normal baseline operational characteristics and returns anomaly scores [0.0 - 1.0].
    """
    def __init__(self, contamination: float = 0.05):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42
        )
        self._fit_baseline()

    def _fit_baseline(self):
        """Generates 500 baseline normal industrial samples to fit model tree paths."""
        np.random.seed(42)
        normal_rms = np.random.normal(0.40, 0.05, 500)
        normal_kurt = np.random.normal(3.0, 0.1, 500)
        normal_crest = np.random.normal(2.5, 0.2, 500)
        
        X_train = np.column_stack((normal_rms, normal_kurt, normal_crest))
        self.model.fit(X_train)

    def predict_anomaly_score(self, rms: float, kurtosis_val: float, crest_factor: float) -> float:
        """
        Computes anomaly score. 
        Returns a probability score between 0.0 (Normal) and 1.0 (Severe Anomaly).
        """
        X_test = np.array([[rms, kurtosis_val, crest_factor]])
        # decision_function returns negative values for anomalies
        raw_score = self.model.decision_function(X_test)[0]
        
        # Scale score normalized to [0, 1] range for intuitive dashboard display
        normalized_score = 1.0 - (raw_score + 0.5)
        return float(np.clip(normalized_score, 0.05, 0.98))
