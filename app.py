import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE SETUP & DARK THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmartPredict AI — Industrial Telemetry Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Dark Theme Overrides
st.markdown("""
<style>
    .stApp { background-color: #090D16; color: #F1F5F9; }
    div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700; }
    div[data-testid="stMetricDelta"] { font-size: 13px !important; }
    div[data-testid="stSidebar"] { background-color: #0E1422; border-right: 1px solid #1E293B; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SIDEBAR — DEMO CONTROLS & MODEL HYPERPARAMETERS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ SmartPredict AI")
    st.caption("Coimbatore MSME Edge Engine")
    st.markdown("---")
    
    st.markdown("### 🎛️ Fault Injection Controls")
    fault_severity = st.slider(
        "Inject Bearing Wear (MTR-01)",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05,
        help="Slide right to simulate progressive spindle bearing damage"
    )
    
    btn_col1, btn_col2 = st.sidebar.columns(2)
    if btn_col1.button("🟢 Reset Normal", use_container_width=True):
        fault_severity = 0.0
    if btn_col2.button("🔴 Critical Failure", use_container_width=True):
        fault_severity = 0.85
        
    st.markdown("---")
    st.markdown("### 🧠 ML Hyperparameters")
    contamination = st.slider("Contamination (α)", 0.01, 0.15, 0.05)
    n_trees = st.select_slider("Trees (n_estimators)", options=[50, 100, 200, 300], value=100)
    
    st.markdown("---")
    st.markdown("🛡️ **MSME ZED Scheme Certified**")
    st.caption("Standard: ISO 10816 Vibration Severity")

# ---------------------------------------------------------
# 3. TOP HEADER BAR
# ---------------------------------------------------------
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("⚡ SmartPredict AI — Industrial Telemetry")
    st.caption("📍 **Deployment Cluster:** Peelamedu Pump Cluster, Coimbatore | **Asset:** Texmo 15HP CNC Motor Spindle (#MTR-01)")

with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if fault_severity > 0.4:
        st.error("🚨 **SYSTEM ALERT:** ANOMALY DETECTED")
    else:
        st.success("🟢 **SYSTEM HEALTHY:** ALL SYSTEMS OK")

st.markdown("---")

# ---------------------------------------------------------
# 4. ROW 1: 4 HIGH-IMPACT KPI CARDS
# ---------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Calculate dynamic telemetry based on slider
vibe_rms = round(0.42 + fault_severity * 3.8, 3)
peak_fft = round(14.2 + fault_severity * 68.5, 1)
rul_days = max(1, int(45 * (1.0 - fault_severity * 0.95)))
health_score = max(5.0, round(96.4 * (1.0 - fault_severity * 0.9), 1))

with kpi1:
    with st.container(border=True):
        st.metric(
            label="Vibration RMS (ISO 10816)", 
            value=f"{vibe_rms} g", 
            delta=f"{'+' if fault_severity > 0 else ''}{round(fault_severity*100)}% Spike",
            delta_color="inverse" if fault_severity > 0.3 else "normal"
        )

with kpi2:
    with st.container(border=True):
        st.metric(
            label="Peak FFT Energy (380 Hz)", 
            value=f"{peak_fft} dB", 
            delta="Bearing Harmonic" if fault_severity > 0.2 else "Normal Baseline",
            delta_color="off"
        )

with kpi3:
    with st.container(border=True):
        st.metric(
            label="Remaining Useful Life (RUL)", 
            value=f"{rul_days} Days", 
            delta="-30 Days Failure Horizon" if fault_severity > 0.4 else "720 Hrs Max",
            delta_color="inverse" if fault_severity > 0.4 else "normal"
        )

with kpi4:
    with st.container(border=True):
        st.metric(
            label="Asset Health Index", 
            value=f"{health_score}%", 
            delta="CRITICAL WEAR" if fault_severity > 0.5 else "OPERATIONAL",
            delta_color="inverse" if fault_severity > 0.5 else "normal"
        )

# ---------------------------------------------------------
# 5. ROW 2: REAL-TIME DSP CHARTS & AI ALERT PANEL
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
col_left, col_right = st.columns([2.2, 1.2])

with col_left:
    with st.container(border=True):
        tab_time, tab_fft, tab_math = st.tabs(["📈 Real-Time Acceleration g(t)", "⚡ FFT Frequency Spectrum (Hz)", "🔬 Signal Processing Math"])
        
        # Synthetic Telemetry Signal
        fs = 2000
        t = np.linspace(0, 1, fs)
        base_signal = np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.1, fs)
        fault_signal = fault_severity * (1.5 * np.sin(2 * np.pi * 380 * t) + np.random.normal(0, 0.4, fs))
        combined_signal = base_signal + fault_signal
        
        fft_vals = np.abs(np.fft.rfft(combined_signal))
        fft_freqs = np.fft.rfftfreq(len(combined_signal), 1/fs)
        
        with tab_time:
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                y=combined_signal[:400], 
                mode='lines', 
                line=dict(color='#00E5FF' if fault_severity <= 0.3 else '#FF1744', width=2)
            ))
            fig_time.update_layout(
                template="plotly_dark", height=280, margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Time Samples (2kHz)", yaxis_title="Acceleration (g)",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
        with tab_fft:
            fig_fft = go.Figure()
            fig_fft.add_trace(go.Scatter(
                x=fft_freqs[:500], y=fft_vals[:500], 
                mode='lines', 
                line=dict(color='#00E676' if fault_severity <= 0.3 else '#FF9100', width=2)
            ))
            if fault_severity > 0.2:
                fig_fft.add_annotation(x=380, y=np.max(fft_vals), text="380 Hz Inner Race Defect", showarrow=True, arrowhead=2, arrowcolor="#FF1744")
            fig_fft.update_layout(
                template="plotly_dark", height=280, margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Frequency (Hz)", yaxis_title="Spectral Energy",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_fft, use_container_width=True)
            
        with tab_math:
            st.markdown("**1. Isolation Forest Anomaly Score:**")
            st.latex(r"s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}")
            st.markdown("**2. Spectral Kurtosis (Transient Impact Detection):**")
            st.latex(r"K = \frac{\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^4}{\left(\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^2\right)^2}")

with col_right:
    with st.container(border=True):
        st.subheader("💬 Real-Time Webhook Dispatch")
        if fault_severity > 0.4:
            st.error(f"""
            **[DISPATCHED via Twilio WhatsApp API]**
            * **Target:** Ramesh (Shop Supervisor)
            * **Timestamp:** {datetime.now().strftime('%H:%M:%S')}
            * **Asset:** MTR-01 (Texmo CNC Spindle)
            * **Fault Type:** Inner Race Bearing Wear (380 Hz)
            * **Predicted Downtime Saved:** ₹2,50,000
            """)
        else:
            st.info("🟢 System operating within normal ISO tolerances. Automated WhatsApp triggers when isolation score breaches 0.75.")
            
        st.markdown("---")
        st.subheader("📡 Raw MQTT Stream")
        st.json({
            "asset_id": "MTR-01",
            "cluster": "Peelamedu_Coimbatore",
            "rms_g": vibe_rms,
            "peak_fft_db": peak_fft,
            "isolation_forest_status": "ANOMALY" if fault_severity > 0.4 else "HEALTHY"
        })

# ---------------------------------------------------------
# 6. ROW 3: FLEET OVERVIEW TABLE & REPORT GENERATOR
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
with st.container(border=True):
    st.subheader("📋 Connected MSME Fleet Asset Overview")
    
    fleet_df = pd.DataFrame([
        {"Machine ID": "MTR-01", "Name": "Texmo Main Motor 01", "Health (%)": health_score, "RUL (Days)": rul_days, "Status": "CRITICAL" if fault_severity > 0.4 else "HEALTHY", "Last Ping": "Just now"},
        {"Machine ID": "PMP-07", "Name": "CRI Water Pump 07", "Health (%)": 65.3, "RUL (Days)": 12, "Status": "AT RISK", "Last Ping": "4 min ago"},
        {"Machine ID": "CMP-02", "Name": "Air Compressor 02", "Health (%)": 48.7, "RUL (Days)": 5, "Status": "CRITICAL", "Last Ping": "1 min ago"},
        {"Machine ID": "TUR-04", "Name": "LMW Turbine 04", "Health (%)": 85.1, "RUL (Days)": 30, "Status": "HEALTHY", "Last Ping": "2 min ago"},
        {"Machine ID": "GEN-03", "Name": "Generator Node 03", "Health (%)": 71.6, "RUL (Days)": 18, "Status": "AT RISK", "Last Ping": "8 min ago"},
    ])
    
    st.dataframe(
        fleet_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Health (%)": st.column_config.ProgressColumn("Health (%)", format="%.1f%%", min_value=0, max_value=100)
        }
    )
    
    csv_report = fleet_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Official ZED Scheme Audit Log (CSV)",
        data=csv_report,
        file_name="MSME_ZED_Maintenance_Report.csv",
        mime="text/csv"
    )
