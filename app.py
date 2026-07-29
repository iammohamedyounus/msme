import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# Import modular helper functions
from dsp_engine import (
    generate_synthetic_signal,
    extract_vibration_features,
    evaluate_iso_severity,
    AnomalyDetector
)
from alerts import send_whatsapp_alert

# ---------------------------------------------------------
# 1. PAGE SETUP & CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="PulseGuard AI — Enterprise Predictive Telemetry",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded" # Force sidebar visible
)

# Initialize ML Anomaly Detector once in memory
@st.cache_resource
def load_detector():
    return AnomalyDetector()

detector = load_detector()

# ---------------------------------------------------------
# 2. CUSTOM DARK INDUSTRIAL THEME
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #0B0F19; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    header[data-testid="stHeader"] { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    .kpi-card {
        background: rgba(18, 24, 38, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .kpi-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #64748B; font-weight: 600; }
    .kpi-value { font-size: 26px; font-weight: 800; color: #FFFFFF; margin: 4px 0; }
    .kpi-sub { font-size: 11px; font-weight: 500; }

    .pulse-green { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #10B981; box-shadow: 0 0 8px #10B981; }
    .pulse-red { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #EF4444; box-shadow: 0 0 10px #EF4444; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDEBAR CONTROLS & LIVE STREAM TOGGLE
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <div style="background:#00E5FF; padding:8px 12px; border-radius:8px; color:#000; font-weight:900;">⚡</div>
            <div>
                <h3 style="margin:0; font-size:16px; font-weight:800; color:#FFF;">PulseGuard AI</h3>
                <p style="margin:0; font-size:10px; color:#64748B;">Peelamedu Telemetry Node</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎛️ Live Pitch Controls")
    
    # Live Streaming Mode Switch
    live_stream = st.toggle("📡 Live Streaming Mode", value=True, help="Continuously updates telemetry graphs in real-time")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    fault_severity = st.slider(
        "Bearing Severity Level",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get("severity_val", 0.05),
        step=0.05,
        key="severity_slider"
    )
    
    col_b1, col_b2 = st.columns(2)
    if col_b1.button("🟢 Normal", use_container_width=True):
        st.session_state["severity_val"] = 0.05
        st.rerun()
    if col_b2.button("🔴 Critical", use_container_width=True):
        st.session_state["severity_val"] = 0.85
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🛡️ System Specifications")
    st.markdown("- **Location:** Peelamedu MSME Cluster")
    st.markdown("- **Standard:** ISO 10816-3 Class II")
    st.markdown("- **Sampling Rate:** 2,000 Hz Edge Stream")

# ---------------------------------------------------------
# 4. SIGNAL GENERATION & LIVE DSP PROCESSING
# ---------------------------------------------------------
# Add live stochastic noise when streaming mode is active so waveform actively shifts
noise_offset = np.random.normal(0, 0.03) if live_stream else 0.0
effective_severity = max(0.0, fault_severity + noise_offset)

t_samples, raw_vibration_signal = generate_synthetic_signal(fault_severity=effective_severity)

# Phase shift for live scrolling effect
if live_stream:
    time_shift = int((time.time() * 50) % len(raw_vibration_signal))
    raw_vibration_signal = np.roll(raw_vibration_signal, time_shift)

# Extract DSP metrics from dsp_engine.py
features = extract_vibration_features(raw_vibration_signal)
iso_eval = evaluate_iso_severity(features["rms_g"])
anomaly_score = detector.predict_anomaly_score(features["rms_g"], features["kurtosis"], features["crest_factor"])
rul_days = max(1, int(45 * (1.0 - fault_severity * 0.95)))

# Automatically dispatch alert if threshold breached
if features["rms_g"] > 2.80:
    send_whatsapp_alert(
        asset_id="MTR-01",
        fault_type="Inner Race Bearing Wear (380 Hz)",
        vibe_rms=features["rms_g"]
    )

# ---------------------------------------------------------
# 5. HEADER BAR
# ---------------------------------------------------------
col_h1, col_h2 = st.columns([3, 1.2])

with col_h1:
    st.title("⚡ PulseGuard AI — Predictive Telemetry")
    st.caption("📍 **Monitored Asset:** Texmo 15HP CNC Motor Spindle (#MTR-01) | **Sampling Frequency:** 2,000 Hz Continuous")

with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if features["rms_g"] > 2.80:
        st.markdown('<div style="background:rgba(239,68,68,0.2); border:1px solid #EF4444; padding:10px; border-radius:10px; text-align:center;"><span class="pulse-red"></span> <b style="color:#EF4444;">CRITICAL ANOMALY DETECTED</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:rgba(16,185,129,0.2); border:1px solid #10B981; padding:10px; border-radius:10px; text-align:center;"><span class="pulse-green"></span> <b style="color:#10B981;">SYSTEM OPERATIONAL (ISO 10816)</b></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. KPI METRICS CARDS
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Vibration RMS</div>
            <div class="kpi-value" style="color:{iso_eval['color']};">{features['rms_g']} <span style="font-size:14px;">g</span></div>
            <div class="kpi-sub" style="color:#64748B;">Standard: {iso_eval['zone']} ({iso_eval['status']})</div>
        </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Kurtosis / Crest Factor</div>
            <div class="kpi-value" style="color:{'#EF4444' if features['kurtosis'] > 4.0 else '#10B981'};">{features['kurtosis']} <span style="font-size:14px;">K</span></div>
            <div class="kpi-sub" style="color:#64748B;">Crest Factor: {features['crest_factor']}</div>
        </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Predicted RUL</div>
            <div class="kpi-value" style="color:{'#EF4444' if rul_days < 7 else '#00E5FF'};">{rul_days} <span style="font-size:14px;">Days</span></div>
            <div class="kpi-sub" style="color:#64748B;">Remaining Useful Life</div>
        </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Isolation Forest Score</div>
            <div class="kpi-value" style="color:{'#EF4444' if anomaly_score > 0.6 else '#10B981'};">{anomaly_score:.2f}</div>
            <div class="kpi-sub" style="color:#64748B;">ZED Quality Index</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. SIGNAL PLOTS & LIVE ALERTS
# ---------------------------------------------------------
c_left, c_right = st.columns([2.3, 1.1])

with c_left:
    with st.container(border=True):
        st.subheader("⚡ DSP Signal & Spectral Analysis")
        tab_time, tab_fft = st.tabs(["📈 Time Domain Acceleration g(t)", "🔬 FFT Frequency Spectrum (Hz)"])
        
        with tab_time:
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(x=t_samples, y=raw_vibration_signal, mode='lines', line=dict(color='#00E5FF' if fault_severity < 0.4 else '#EF4444', width=2)))
            fig_t.update_layout(template="plotly_dark", height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Time (s)", yaxis_title="Acceleration (g)")
            st.plotly_chart(fig_t, use_container_width=True)
            
        with tab_fft:
            fig_f = go.Figure()
            fig_f.add_trace(go.Scatter(x=features['fft_freqs'][:200], y=features['fft_vals'][:200], mode='lines', line=dict(color='#10B981' if fault_severity < 0.4 else '#F59E0B', width=2)))
            if fault_severity > 0.2:
                fig_f.add_annotation(x=380, y=np.max(features['fft_vals']), text="⚠️ 380 Hz Bearing Defect", showarrow=True, arrowhead=2, arrowcolor="#EF4444")
            fig_f.update_layout(template="plotly_dark", height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Frequency (Hz)", yaxis_title="Spectral Energy")
            st.plotly_chart(fig_f, use_container_width=True)

with c_right:
    with st.container(border=True):
        st.subheader("💬 Automated Alert Webhook")
        if features["rms_g"] > 2.80:
            st.error(f"""
            **🚨 DISPATCHED VIA WHATSAPP API**
            * **Target:** Plant Supervisor
            * **Timestamp:** {datetime.now().strftime('%H:%M:%S')}
            * **Asset:** MTR-01 (Texmo Spindle)
            * **Diagnosis:** Bearing Wear (380 Hz)
            * **Downtime Losses Prevented:** ₹2,40,000
            """)
        else:
            st.info("🟢 Monitoring active. Webhooks fire automatically when ISO thresholds are breached.")
            
        st.markdown("**📡 Live Telemetry Payload**")
        st.json({
            "asset_id": "MTR-01",
            "rms_g": features["rms_g"],
            "kurtosis": features["kurtosis"],
            "isolation_score": anomaly_score,
            "iso_zone": iso_eval["zone"],
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
        })

# ---------------------------------------------------------
# 8. FLEET MATRIX TABLE
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
with st.container(border=True):
    st.subheader("📋 Connected MSME Cluster Fleet Matrix")
    
    fleet_df = pd.DataFrame([
        {"Machine ID": "MTR-01", "Name": "Texmo Main Motor Spindle 01", "Vibration (g)": features["rms_g"], "Kurtosis": features["kurtosis"], "RUL (Days)": rul_days, "Status": "CRITICAL" if features["rms_g"] > 2.80 else "HEALTHY"},
        {"Machine ID": "PMP-07", "Name": "CRI Water Pump Node 07", "Vibration (g)": 0.82, "Kurtosis": 3.12, "RUL (Days)": 18, "Status": "AT RISK"},
        {"Machine ID": "CMP-02", "Name": "ELGi Air Compressor Node 02", "Vibration (g)": 3.12, "Kurtosis": 5.40, "RUL (Days)": 3, "Status": "CRITICAL"},
        {"Machine ID": "TUR-04", "Name": "LMW Machine Turbine 04", "Vibration (g)": 0.38, "Kurtosis": 2.95, "RUL (Days)": 38, "Status": "HEALTHY"},
    ])
    
    st.dataframe(fleet_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# 9. AUTO-REFRESH ANIMATION LOOP
# ---------------------------------------------------------
if live_stream:
    time.sleep(0.8)  # Refresh every 800ms
    st.rerun()
