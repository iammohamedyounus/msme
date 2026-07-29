import time
import numpy as np
import pandas as pd

def generate_motor_telemetry(duration_sec=1, sampling_rate=1000, fault_mode="NORMAL", severity=0.0):
    """
    Simulates a 3-phase induction motor (2900 RPM / ~48.3 Hz)
    Adheres to ISO 10816 vibration profile.
    """
    t = np.linspace(0, duration_sec, int(sampling_rate * duration_sec), endpoint=False)
    
    # Fundamental rotational speed (1X = 48.33 Hz)
    f_rot = 48.33 
    
    # Baseline normal operational vibration
    vibration = 0.5 * np.sin(2 * np.pi * f_rot * t) + np.random.normal(0, 0.1, len(t))
    temperature = 45.0 + np.random.normal(0, 0.2)
    current = 12.5 + np.random.normal(0, 0.1) # Amperes
    
    if fault_mode == "UNBALANCE":
        # Increases 1X rotational amplitude
        vibration += (severity * 3.5) * np.sin(2 * np.pi * f_rot * t)
        temperature += severity * 8.0
        
    elif fault_mode == "BEARING_FAULT":
        # Injects high-frequency impact pulses (BPFI ~ 190 Hz)
        bpfi_freq = 193.2
        pulses = np.sin(2 * np.pi * bpfi_freq * t) * (np.sign(np.sin(2 * np.pi * f_rot * t)) + 1)
        vibration += (severity * 4.0) * pulses
        temperature += severity * 18.0
        current += severity * 2.5

    # Compute RMS Vibration (mm/s velocity proxy)
    vibration_rms = np.sqrt(np.mean(vibration**2))
    
    return {
        "timestamp": time.time(),
        "vibration_rms_mms": round(float(vibration_rms), 3),
        "temperature_c": round(float(temperature), 2),
        "current_amps": round(float(current), 2),
        "fault_label": fault_mode if severity > 0.3 else "NORMAL"
    }

# Example usage:
if __name__ == "__main__":
    print("Normal State:", generate_motor_telemetry(fault_mode="NORMAL"))
    print("Degrading Bearing:", generate_motor_telemetry(fault_mode="BEARING_FAULT", severity=0.8))
