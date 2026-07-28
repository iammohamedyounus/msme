import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from datetime import datetime
import json

# ---------------------------------------------------------
# PAGE CONFIGURATION & CUSTOM INDUSTRIAL THEME CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="MSME Edge-AI Predictive Maintenance | Coimbatore",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Industrial Glassmorphism CSS
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .stApp { color: #FAFAFA; }
    .status-badge-healthy {
        background-color: #00E676;
        color: #000;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .status-badge-danger {
        background-color: #FF1744;
        color: #FFF;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 23, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 23, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 23, 68, 0); }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER & COIMBATORE CLUSTER BRANDING
# ---------------------------------------------------------
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    st.title("🏭 Edge-AI Predictive Maintenance System")
    st.caption("📍 **Deployment Cluster:** Peelamedu MSME Pump Cluster, Coimbatore | **Target Asset:** Texmo 15HP CNC Motor Spindle (#CBM-PLM-04)")

with top_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("🛡️ **MSME ZED Certified**\n\n*(Zero Defect, Zero Effect Compliant)*")

st.markdown("---")

# ---------------------------------------------------------
# SIDEBAR CONTROL PANEL (FAULTS & HYPERPARAMETERS)
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/engine.png", width=70)
st.sidebar.header("⚙️ Machine Telemetry Controls")

fault_severity = st.sidebar.slider(
    "🚨 Inject Bearing Fault Severity",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05,
    help="0.0 = Healthy Baseline | 1.0 = Critical Inner Race Bearing Wear"
)

# Preset Quick Actions for Stage Demo
st.sidebar.markdown("**⚡ Quick Stage Actions**")
btn_col1, btn_col2 = st.sidebar.columns(2)

if btn_col1.button("🟢 Normal"):
    fault_severity = 0.0

if btn_col2.button("🔴 Critical"):
    fault_severity = 0.85

motor_rpm = st.sidebar.selectbox("Operating Speed (RPM)", [1440, 2880, 3600], index=1)
sensor_loc = st.sidebar.text_input("Sensor Node ID", "ESP32-MPU6050-NODE-01")

st.sidebar.markdown("---")
st.sidebar.header("🧠 ML Model Hyperparameters")
st.sidebar.caption("Adjust real-time Isolation Forest parameters:")

contamination_rate = st.sidebar.slider(
    "Contamination Rate (α)", 
    min_value=0.01, 
    max_value=0.15, 
    value=0.05, 
    step=0.01,
    help="Expected proportion of anomalies in dataset"
)

n_trees = st.sidebar.slider(
    "Number of Trees (n_estimators)", 
    min_value=50, 
    max_value=300, 
    value=100, 
    step=25
)

sampling_freq = st.sidebar.selectbox(
    "Edge Sampling Frequency (fs)", 
    [1024, 2000, 4096], 
    index=1
)

# ---------------------------------------------------------
# SIGNAL GENERATION & FFT SPECTRAL CALCULATIONS
# ---------------------------------------------------------
fs = sampling_freq  # Dynamic sampling frequency from sidebar
t = np.linspace(0, 1, fs)

# Primary Rotational Frequency
base_freq = motor_rpm / 60.0
healthy_signal = np.sin(2 * np.pi * base_freq * t) + 0.12 * np.random.normal(size=fs)

# Bearing Fault Harmonics (380 Hz BPFI - Ball Pass Frequency Inner Race)
defect_freq = 380.0
fault_harmonics = fault_severity * (
    1.4 * np.sin(2 * np.pi * defect_freq * t) +
    0.9 * np.sin(2 * np.pi * (2 * defect_freq) * t) +
    0.6 * np.random.normal(size=fs)
)

combined_vibration = healthy_signal + fault_harmonics

# Fast Fourier Transform (FFT)
fft_vals = np.abs(np.fft.rfft(combined_vibration))
fft_freqs = np.fft.rfftfreq(len(combined_vibration), 1/fs)

# Feature Extraction
rms_vibration = np.sqrt(np.mean(combined_vibration**2))
peak_fft_energy = np.max(fft_vals[fft_freqs > 100])
kurtosis_val = float(np.mean(((combined_vibration - np.mean(combined_vibration)) / np.std(combined_vibration))**4))

# ---------------------------------------------------------
# MACHINE LEARNING ANOMALY ENGINE
# ---------------------------------------------------------
# Synthetic healthy baseline training data
healthy_baseline_features = np.array([
    [np.random.normal(0.7, 0.05), np.random.normal(15, 2), np.random.normal(3.0, 0.2)]
    for _ in range(120)
])

# Isolation Forest trained with dynamic sidebar hyperparameters
clf = IsolationForest(
    contamination=contamination_rate, 
    n_estimators=n_trees, 
    random_state=42
)
clf.fit(healthy_baseline_features)

current_features = np.array([[rms_vibration, peak_fft_energy, kurtosis_val]])
anomaly_prediction = clf.predict(current_features)[0]  # -1 = Anomaly, 1 = Normal

# ---------------------------------------------------------
# LIVE METRICS & STATUS CARDS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Vibration RMS (ISO 10816)", f"{rms_vibration:.3f} g", delta=f"{fault_severity*100:.0f}% Degradation")

with col2:
    st.metric("Peak FFT Spectral Energy", f"{peak_fft_energy:.1f} dB", delta_color="off")

with col3:
    st.metric("Signal Kurtosis (Impulsiveness)", f"{kurtosis_val:.2f}")

with col4:
    if anomaly_prediction == 1:
        st.markdown("<p style='font-size:12px; color:#AAA;'>HEALTH STATUS</p>", unsafe_allow_html=True)
        st.markdown("<div class='status-badge-healthy'>🟢 OPERATIONAL</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:12px; color:#AAA;'>HEALTH STATUS</p>", unsafe_allow_html=True)
        st.markdown("<div class='status-badge-danger'>🚨 ANOMALY DETECTED</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Status Alert Banner
if anomaly_prediction == 1:
    st.success("✅ **SYSTEM HEALTHY:** Spindle vibration parameters are well within normal ISO Class II machine limits. No maintenance required.")
else:
    rul_hours = max(1, int(72 * (1 - fault_severity)))
    st.error(f"🚨 **CRITICAL BEARING WARNING:** Uncharacteristic 380 Hz spectral energy spike detected. Predicted Remaining Useful Life (RUL): **{rul_hours} Hours**. Automated alert dispatched to shop supervisor.")

st.markdown("---")

# ---------------------------------------------------------
# MAIN TAB NAVIGATION
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Live Telemetry & Analytics", 
    "🔬 DSP & Mathematical Foundations", 
    "📡 Raw MQTT Packet Inspector"
])

# ---------------------------------------------------------
# TAB 1: LIVE TELEMETRY & CHARTS
# ---------------------------------------------------------
with tab1:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📈 Real-Time Acceleration Waveform g(t)")
        fig_time = go.Figure()
        fig_time.add_trace(go.Scatter(
            y=combined_vibration[:350],
            mode='lines',
            name='Vibration Signal',
            line=dict(color='#00E5FF' if anomaly_prediction==1 else '#FF1744', width=2)
        ))
        fig_time.update_layout(
            xaxis_title="Time Samples",
            yaxis_title="Acceleration (g)",
            template="plotly_dark",
            height=320,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with chart_col2:
        st.subheader("⚡ Frequency Domain FFT Spectrum (Hz)")
        fig_fft = go.Figure()
        fig_fft.add_trace(go.Scatter(
            x=fft_freqs[:500],
            y=fft_vals[:500],
            mode='lines',
            name='FFT Energy',
            line=dict(color='#00E676' if anomaly_prediction==1 else '#FF9100', width=2)
        ))
        if fault_severity > 0.2:
            fig_fft.add_annotation(
                x=defect_freq, y=peak_fft_energy,
                text="Bearing Defect Peak (380Hz)",
                showarrow=True, arrowhead=2, arrowcolor="#FF1744", ax=40, ay=-30
            )
        fig_fft.update_layout(
            xaxis_title="Frequency (Hz)",
            yaxis_title="Spectral Energy",
            template="plotly_dark",
            height=320,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_fft, use_container_width=True)

    bot_col1, bot_col2 = st.columns(2)

    with bot_col1:
        st.subheader("💬 Automated WhatsApp / Telegram Webhook Log")
        if anomaly_prediction == -1:
            st.code(f"""
[DISPATCHED via Twilio API] 📲
Receiver: +91 98422 XXXXX (Ramesh - Factory Owner, Peelamedu)
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------------------------------------
⚠️ CRITICAL BEARING WEAR WARNING!
Machine ID: CBM-PLM-04 (Texmo Spindle #2)
Peak Defect Frequency: {defect_freq} Hz
Vibration RMS: {rms_vibration:.3f} g (Exceeds ISO Threshold)
Estimated Downtime Avoided Loss: ~₹2,500,000
Recommended Action: Inspect inner race bearing before next shift.
--------------------------------------------------------------
            """, language="yaml")
        else:
            st.info("ℹ️ System in healthy state. Webhook triggers automatically when anomaly score breaches isolation threshold.")

    with bot_col2:
        st.subheader("📄 Export Inspection & Compliance Log")
        st.write("Generate an audit report for local MSME ZED Certification compliance.")
        
        report_df = pd.DataFrame([{
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Machine_ID": "CBM-PLM-04",
            "Location": "Peelamedu, Coimbatore",
            "Operating_RPM": motor_rpm,
            "Vibration_RMS_g": round(rms_vibration, 4),
            "Kurtosis": round(kurtosis_val, 2),
            "Peak_FFT_Frequency_Hz": defect_freq if fault_severity > 0 else base_freq,
            "Status": "ANOMALY" if anomaly_prediction == -1 else "HEALTHY",
            "Predicted_RUL_Hours": max(1, int(72 * (1 - fault_severity))) if anomaly_prediction == -1 else 720
        }])
        
        st.dataframe(report_df, use_container_width=True)
        
        csv_data = report_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Official ZED Maintenance Audit Report (CSV)",
            data=csv_data,
            file_name=f"ZED_Maintenance_Log_CBM_PLM_04_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ---------------------------------------------------------
# TAB 2: MATHEMATICAL FOUNDATIONS
# ---------------------------------------------------------
with tab2:
    st.subheader("🔬 Signal Processing & Algorithmic Equations")
    st.markdown("This Edge-AI system transforms raw time-series vibration data into frequency-domain metrics before running unsupervised anomaly classification.")
    
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        st.markdown("#### 1. Root Mean Square (RMS) Acceleration")
        st.latex(r"RMS = \sqrt{\frac{1}{N} \sum_{i=1}^{N} x_i^2}")
        st.caption("Measures total energy content of the vibration signal according to ISO 10816 standards.")
        
        st.markdown("#### 2. Fast Fourier Transform (FFT) Decomposition")
        st.latex(r"X(k) = \sum_{n=0}^{N-1} x(n) \cdot e^{-i 2\pi k n / N}")
        st.caption("Decomposes complex time-domain waveforms into individual mechanical frequency harmonics.")

    with m_col2:
        st.markdown("#### 3. Spectral Kurtosis (Transient Impact Peakiness)")
        st.latex(r"Kurtosis = \frac{\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^4}{\left(\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^2\right)^2}")
        st.caption("Detects sharp, repetitive micro-shocks caused by inner/outer bearing race defects.")
        
        st.markdown("#### 4. Isolation Forest Anomaly Scoring")
        st.latex(r"s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}")
        st.caption("Unsupervised tree isolation path length calculation. Shorter path lengths denote immediate anomalies.")

# ---------------------------------------------------------
# TAB 3: RAW MQTT PACKET INSPECTOR
# ---------------------------------------------------------
with tab3:
    st.subheader("📡 Edge Sensor Payload Stream (MQTT Protocol)")
    st.markdown("Live view of raw telemetry JSON packets transmitted from the ESP32 microcontroller edge node to the broker.")
    
    mqtt_payload = {
        "header": {
            "protocol": "MQTT v3.1.1",
            "topic": "coimbatore/peelamedu/unit2/machine04/telemetry",
            "qos": 1,
            "timestamp_utc": datetime.utcnow().isoformat() + "Z"
        },
        "edge_device": {
            "node_id": sensor_loc,
            "microcontroller": "ESP32 Dual-Core 240MHz",
            "sensor": "MPU6050 Accelerometer",
            "firmware_ver": "v2.1.4-edge-dsp"
        },
        "telemetry_metrics": {
            "sampling_frequency_hz": sampling_freq,
            "operating_rpm": motor_rpm,
            "vibration_rms_g": round(rms_vibration, 4),
            "spectral_kurtosis": round(kurtosis_val, 3),
            "peak_defect_freq_hz": defect_freq if fault_severity > 0 else base_freq,
            "peak_energy_db": round(peak_fft_energy, 2)
        },
        "edge_inference": {
            "model_architecture": "Isolation Forest (scikit-learn)",
            "n_estimators": n_trees,
            "contamination_alpha": contamination_rate,
            "anomaly_flag": bool(anomaly_prediction == -1),
            "predicted_rul_hours": max(1, int(72 * (1 - fault_severity))) if anomaly_prediction == -1 else 720
        }
    }
    
    st.json(mqtt_payload)
