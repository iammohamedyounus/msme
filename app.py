import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(
    page_title="VibeGuard AI — Enterprise Predictive Maintenance",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. CUSTOM INDUSTRIAL DARK THEME & GLASSMORPHISM
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Clean Header */
    header[data-testid="stHeader"] { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Glassmorphism Metric Cards */
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

    /* Live Pulsating Indicator */
    .pulse-green {
        display: inline-block; width: 10px; height: 10px; border-radius: 50%;
        background: #10B981; box-shadow: 0 0 8px #10B981;
    }
    .pulse-red {
        display: inline-block; width: 10px; height: 10px; border-radius: 50%;
        background: #EF4444; box-shadow: 0 0 10px #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDEBAR CONTROLS & DEMO ENGINE
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <div style="background:#00E5FF; padding:8px 12px; border-radius:8px; color:#000; font-weight:900;">⚡</div>
            <div>
                <h3 style="margin:0; font-size:16px; font-weight:800; color:#FFF;">VibeGuard AI</h3>
                <p style="margin:0; font-size:10px; color:#64748B;">MSME Industrial Telemetry Node</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎛️ Live Pitch Controls")
    st.caption("Use these triggers during judge presentation to demonstrate real-time AI response.")
    
    fault_severity = st.slider(
        "Bearing Wear Severity (MTR-01)",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        step=0.05
    )
    
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("🟢 Normal", use_container_width=True):
        fault_severity = 0.05
    if col_btn2.button("🔴 Critical", use_container_width=True):
        fault_severity = 0.85
        
    st.markdown("---")
    st.markdown("### 🛡️ System Specifications")
    st.markdown("- **Location:** Peelamedu Pump Cluster")
    st.markdown("- **Standard:** ISO 10816 Vibration Severity")
    st.markdown("- **Hardware:** ESP32 + MPU6050 Edge Node")

# ---------------------------------------------------------
# 4. TOP HERO BAR
# ---------------------------------------------------------
col_h1, col_h2 = st.columns([3, 1.2])

with col_h1:
    st.title("⚡ VibeGuard AI — Predictive Telemetry")
    st.caption("📍 **Monitored Asset:** Texmo 15HP CNC Motor Spindle (#MTR-01) | **Sampling Frequency:** 2,000 Hz Continuous")

with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if fault_severity > 0.4:
        st.markdown('<div style="background:rgba(239,68,68,0.2); border:1px solid #EF4444; padding:10px; border-radius:10px; text-align:center;"><span class="pulse-red"></span> <b style="color:#EF4444;">CRITICAL ANOMALY DETECTED</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:rgba(16,185,129,0.2); border:1px solid #10B981; padding:10px; border-radius:10px; text-align:center;"><span class="pulse-green"></span> <b style="color:#10B981;">SYSTEM OPERATIONAL (ISO 10816)</b></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Dynamic Telemetry Math
vibe_rms = round(0.42 + fault_severity * 3.8, 3)
peak_fft = round(14.2 + fault_severity * 68.5, 1)
rul_days = max(1, int(45 * (1.0 - fault_severity * 0.95)))
health_score = max(5.0, round(96.4 * (1.0 - fault_severity * 0.9), 1))

# ---------------------------------------------------------
# 5. KPI CARDS ROW
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Vibration RMS</div>
            <div class="kpi-value" style="color:{'#EF4444' if vibe_rms > 2.8 else '#00E5FF'};">{vibe_rms} <span style="font-size:14px;">g</span></div>
            <div class="kpi-sub" style="color:#64748B;">ISO Limit: 2.80 g</div>
        </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Peak FFT Frequency</div>
            <div class="kpi-value" style="color:{'#EF4444' if peak_fft > 50 else '#10B981'};">{peak_fft} <span style="font-size:14px;">dB</span></div>
            <div class="kpi-sub" style="color:#64748B;">380 Hz Inner Race Defect</div>
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
            <div class="kpi-label">Health Index</div>
            <div class="kpi-value" style="color:{'#EF4444' if health_score < 50 else '#10B981'};">{health_score}%</div>
            <div class="kpi-sub" style="color:#64748B;">ZED Quality Standard</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. GRAPHICAL TELEMETRY & DISPATCH ENGINE
# ---------------------------------------------------------
c_left, c_right = st.columns([2.3, 1.1])

with c_left:
    with st.container(border=True):
        st.subheader("⚡ Signal Processing & Spectral Analysis")
        tab_time, tab_fft, tab_math = st.tabs(["📈 Time Domain Acceleration", "🔬 FFT Frequency Spectrum", "🧮 ML Math Model"])
        
        fs = 2000
        t = np.linspace(0, 0.2, int(fs * 0.2))
        base_signal = np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.08, len(t))
        fault_signal = fault_severity * (2.2 * np.sin(2 * np.pi * 380 * t) + np.random.normal(0, 0.3, len(t)))
        combined_signal = base_signal + fault_signal
        
        fft_vals = np.abs(np.fft.rfft(combined_signal))
        fft_freqs = np.fft.rfftfreq(len(combined_signal), 1/fs)
        
        with tab_time:
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(y=combined_signal, mode='lines', line=dict(color='#00E5FF' if fault_severity < 0.4 else '#EF4444', width=2)))
            fig_t.update_layout(template="plotly_dark", height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Time Samples (2kHz)", yaxis_title="Acceleration (g)")
            st.plotly_chart(fig_t, use_container_width=True)
            
        with tab_fft:
            fig_f = go.Figure()
            fig_f.add_trace(go.Scatter(x=fft_freqs[:200], y=fft_vals[:200], mode='lines', line=dict(color='#10B981' if fault_severity < 0.4 else '#F59E0B', width=2)))
            if fault_severity > 0.2:
                fig_f.add_annotation(x=380, y=np.max(fft_vals), text="380 Hz Inner Race Defect", showarrow=True, arrowhead=2, arrowcolor="#EF4444")
            fig_f.update_layout(template="plotly_dark", height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Frequency (Hz)", yaxis_title="Spectral Energy")
            st.plotly_chart(fig_f, use_container_width=True)
            
        with tab_math:
            st.markdown("**1. Isolation Forest Anomaly Metric:**")
            st.latex(r"s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}")
            st.markdown("**2. Spectral Kurtosis (Impact Transient Detection):**")
            st.latex(r"K = \frac{\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^4}{\left(\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^2\right)^2}")

with c_right:
    with st.container(border=True):
        st.subheader("💬 Automated Webhook Alert")
        if fault_severity > 0.4:
            st.error(f"""
            **🚨 DISPATCHED VIA TWILIO / WHATSAPP API**
            * **Target:** Plant Supervisor (Peelamedu Branch)
            * **Timestamp:** {datetime.now().strftime('%H:%M:%S')}
            * **Asset:** MTR-01 (Texmo CNC Spindle)
            * **Fault Type:** Bearing Inner Race Wear (380 Hz)
            * **Downtime Losses Prevented:** ₹2,40,000
            """)
        else:
            st.info("🟢 Monitoring active. Webhook triggers automatically when isolation anomaly score exceeds 0.75.")
            
        st.markdown("**📡 Live MQTT Data Stream**")
        st.json({
            "asset_id": "MTR-01",
            "cluster": "Peelamedu_Coimbatore",
            "rms_g": vibe_rms,
            "isolation_score": round(0.18 + fault_severity * 0.75, 2),
            "zed_status": "PASS" if fault_severity < 0.4 else "ACTION_REQUIRED"
        })

# ---------------------------------------------------------
# 7. CONNECTED FLEET TABLE & REPORT DOWNLOAD
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
with st.container(border=True):
    st.subheader("📋 Connected MSME Cluster Assets")
    
    fleet_df = pd.DataFrame([
        {"Machine ID": "MTR-01", "Name": "Texmo Main Motor Spindle 01", "Vibration (g)": vibe_rms, "Health Index (%)": health_score, "RUL (Days)": rul_days, "Status": "CRITICAL" if fault_severity > 0.4 else "HEALTHY"},
        {"Machine ID": "PMP-07", "Name": "CRI Water Pump Node 07", "Vibration (g)": 0.82, "Health Index (%)": 71.2, "RUL (Days)": 14, "Status": "AT RISK"},
        {"Machine ID": "CMP-02", "Name": "ELGi Air Compressor Node 02", "Vibration (g)": 3.12, "Health Index (%)": 41.0, "RUL (Days)": 3, "Status": "CRITICAL"},
        {"Machine ID": "TUR-04", "Name": "LMW Machine Turbine 04", "Vibration (g)": 0.38, "Health Index (%)": 92.5, "RUL (Days)": 38, "Status": "HEALTHY"},
    ])
    
    st.dataframe(fleet_df, use_container_width=True, hide_index=True)
    
    csv_report = fleet_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Official MSME ZED Quality Audit Report (CSV)",
        data=csv_report,
        file_name="MSME_ZED_Compliance_Report.csv",
        mime="text/csv"
    )
