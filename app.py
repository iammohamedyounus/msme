import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmartPredict AI - Enterprise Predictive Maintenance",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. BULLETPROOF CSS & THEME OVERRIDES
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0B0E14;
        color: #E2E8F0;
    }
    
    /* Hide Default Header/Footer elements safely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* KPI Metric Cards */
    .kpi-card {
        background-color: #121824;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 12px 14px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        text-align: left;
    }
    .kpi-title { font-size: 12px; color: #94A3B8; font-weight: 500; }
    .kpi-value { font-size: 24px; font-weight: 700; color: #FFFFFF; margin: 2px 0; }
    .kpi-sub { font-size: 11px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDEBAR CONTROLS & DEMO ENGINE
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ SmartPredict AI")
    st.caption("Coimbatore MSME Pump Cluster")
    st.markdown("---")
    
    st.markdown("#### 🎛️ Stage Demo Fault Controller")
    fault_severity = st.slider(
        "Inject Bearing Fault Severity (MTR-01)",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05,
        help="Slide right during pitch to demonstrate instant ML fault detection"
    )
    
    col_s1, col_s2 = st.columns(2)
    if col_s1.button("🟢 Normal", use_container_width=True):
        fault_severity = 0.0
    if col_s2.button("🔴 Critical", use_container_width=True):
        fault_severity = 0.85
        
    st.markdown("---")
    st.markdown("**System Health:** 🟢 Operational")
    st.caption("Node: ESP32-MPU6050-PLM-04")
    st.caption("Standard: ISO 10816 Vibration Severity")

# ---------------------------------------------------------
# 4. TOP BAR & KPI HEADER
# ---------------------------------------------------------
st.markdown("## 🏭 SmartPredict AI — Enterprise Telemetry Engine")
st.caption("📍 **Deployment Target:** Peelamedu Industrial Cluster, Coimbatore | **Asset:** Texmo 15HP CNC Motor Spindle (#MTR-01)")

# Calculate dynamic health values based on fault slider
mtr_health = max(5.0, round(92.4 * (1.0 - fault_severity * 0.9), 1))
mtr_rul = max(1, int(45 * (1.0 - fault_severity * 0.95)))

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Total Machines</div><div class="kpi-value">120</div><div class="kpi-sub" style="color:#64748B;">Active Fleet</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Healthy</div><div class="kpi-value" style="color:#10B981;">82</div><div class="kpi-sub" style="color:#10B981;">68.3%</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi-card"><div class="kpi-title">At Risk</div><div class="kpi-value" style="color:#F59E0B;">28</div><div class="kpi-sub" style="color:#F59E0B;">23.3%</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Critical</div><div class="kpi-value" style="color:#EF4444;">{"11" if fault_severity > 0.4 else "10"}</div><div class="kpi-sub" style="color:#EF4444;">Active Alerts</div></div>', unsafe_allow_html=True)
with k5:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Today Alerts</div><div class="kpi-value" style="color:#8B5CF6;">18</div><div class="kpi-sub" style="color:#64748B;">Real-Time</div></div>', unsafe_allow_html=True)
with k6:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Avg. Health</div><div class="kpi-value" style="color:#06B6D4;">{round(78.6 - fault_severity*5, 1)}%</div><div class="kpi-sub" style="color:#10B981;">ZED Compliant</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. CHARTS & TELEMETRY ROW
# ---------------------------------------------------------
c1, c2, c3 = st.columns([2.2, 1.4, 1.4])

with c1:
    st.subheader("📈 Live Vibration Waveform & Trend")
    t = np.linspace(0, 1, 200)
    # Dynamic signal calculation
    signal = np.sin(2 * np.pi * 50 * t) + fault_severity * 1.5 * np.sin(2 * np.pi * 380 * t) + np.random.normal(0, 0.08, 200)
    
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(
        y=signal, 
        mode='lines', 
        line=dict(color='#EF4444' if fault_severity > 0.4 else '#2563EB', width=2)
    ))
    fig_time.update_layout(
        template="plotly_dark", 
        height=220, 
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Time Samples", 
        yaxis_title="Acceleration (g)"
    )
    st.plotly_chart(fig_time, use_container_width=True)

with c2:
    st.subheader("📊 Fleet Distribution")
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Healthy', 'At Risk', 'Critical'],
        values=[82, 28, 10 if fault_severity <= 0.4 else 11],
        hole=.6,
        marker_colors=['#10B981', '#F59E0B', '#EF4444']
    )])
    fig_donut.update_layout(
        template="plotly_dark", 
        height=220, 
        margin=dict(l=10, r=10, t=10, b=10), 
        showlegend=False
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with c3:
    st.subheader("🚨 Real-Time Alert Dispatch")
    if fault_severity > 0.4:
        st.error(f"⚠️ **CRITICAL FAULT DETECTED**\n\n**Asset:** MTR-01 (Texmo Spindle)\n- **Vibration Peak:** {round(1.2 + fault_severity*2.5, 2)} g\n- **Predicted RUL:** {mtr_rul} Days\n- **WhatsApp Alert:** Dispatched to Plant Supervisor")
    else:
        st.success("✅ **SYSTEM OPERATIONAL**\n\nAll 120 connected MSME assets operating within normal ISO 10816 thresholds.")

st.markdown("---")

# ---------------------------------------------------------
# 6. FLEET OVERVIEW TABLE
# ---------------------------------------------------------
st.subheader("📋 Connected Asset Fleet Status")

machines_data = [
    {"Machine ID": "MTR-01", "Name": "Texmo Main Motor 01", "Health Score (%)": mtr_health, "RUL (Days)": mtr_rul, "Status": "CRITICAL" if fault_severity > 0.4 else "HEALTHY"},
    {"Machine ID": "PMP-07", "Name": "CRI Water Pump 07", "Health Score (%)": 65.3, "RUL (Days)": 12, "Status": "AT RISK"},
    {"Machine ID": "CMP-02", "Name": "Air Compressor 02", "Health Score (%)": 48.7, "RUL (Days)": 5, "Status": "CRITICAL"},
    {"Machine ID": "TUR-04", "Name": "LMW Turbine 04", "Health Score (%)": 85.1, "RUL (Days)": 30, "Status": "HEALTHY"},
    {"Machine ID": "GEN-03", "Name": "Generator Node 03", "Health Score (%)": 71.6, "RUL (Days)": 18, "Status": "AT RISK"},
]

df_machines = pd.DataFrame(machines_data)

st.dataframe(
    df_machines,
    use_container_width=True,
    hide_index=True
)
