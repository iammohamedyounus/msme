import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE SETUP & METADATA
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmartPredict AI — Industrial Telemetry Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. HIGH-END GLASSMORPHISM DARK CSS THEME
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Dark Cyberpunk Theme Core */
    .stApp {
        background: #080B11;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Hide Default Headers */
    header[data-testid="stHeader"] { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Pulsating Status Dot CSS */
    .pulsating-dot {
        height: 10px;
        width: 10px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 rgba(16, 185, 129, 0.4);
        animation: pulse 1.5s infinite;
    }
    .pulsating-dot-red {
        height: 10px;
        width: 10px;
        background-color: #EF4444;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 rgba(239, 68, 68, 0.4);
        animation: pulse-red 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* Enterprise Glassmorphism Metric Cards */
    .metric-card {
        background: rgba(18, 24, 38, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(0, 229, 255, 0.4);
        transform: translateY(-2px);
    }
    .metric-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #94A3B8; font-weight: 600; }
    .metric-val { font-size: 28px; font-weight: 800; color: #FFFFFF; margin: 4px 0; }
    .metric-sub { font-size: 11px; font-weight: 500; }
    
    /* Sidebar Overrides */
    section[data-testid="stSidebar"] {
        background-color: #0D121F !important;
        border-right: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDEBAR CONTROLS & STAGE PITCH FAULT INJECTOR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
            <div style="background:linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); padding:10px; border-radius:10px; color:black; font-weight:900; font-size:20px;">⚡</div>
            <div>
                <h3 style="margin:0; font-size:17px; color:#FFF; font-weight:700;">SmartPredict AI</h3>
                <p style="margin:0; font-size:11px; color:#64748B;">Industrial Telemetry Engine v2.4</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎛️ Stage Pitch Fault Injector")
    st.caption("Simulate real-time sensor anomalies for live demonstration")
    
    fault_type = st.selectbox(
        "Select Fault Dynamics",
        ["Inner Race Bearing Wear (380 Hz)", "Unbalance & Misalignment (50 Hz)", "Pump Cavitation / Aeration", "Stator Overheating"]
    )
    
    fault_severity = st.slider(
        "Fault Severity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        step=0.05,
        help="Slide right to simulate dynamic machine degradation"
    )

    st.markdown("#### ⚡ Pitch Presets")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    # Store preset states in Session State
    if "preset_sev" not in st.session_state:
        st.session_state.preset_sev = fault_severity

    if col_p1.button("🟢 Normal", use_container_width=True):
        st.session_state.preset_sev = 0.05
    if col_p2.button("⚠️ Warning", use_container_width=True):
        st.session_state.preset_sev = 0.45
    if col_p3.button("🔴 Critical", use_container_width=True):
        st.session_state.preset_sev = 0.90

    # Sync slider with preset if clicked
    if st.session_state.preset_sev != fault_severity:
        fault_severity = st.session_state.preset_sev

    st.markdown("---")
    st.markdown("### 🛡️ Compliance & Nodes")
    st.markdown("- **Cluster:** Peelamedu MSME, Coimbatore")
    st.markdown("- **Standard:** ISO 10816-3 Class II")
    st.markdown("- **Edge Hardware:** ESP32 + MPU6050 Accelerometer")

# ---------------------------------------------------------
# 4. TOP HERO BAR
# ---------------------------------------------------------
top_l, top_r = st.columns([3, 1.2])

with top_l:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px;">
            <h1 style="margin:0; font-size:26px; font-weight:800; letter-spacing:-0.5px;">Peelamedu Pump Cluster — Asset #MTR-01</h1>
        </div>
        <p style="margin:4px 0 0 0; font-size:13px; color:#94A3B8;">
            <b>Asset Focus:</b> Texmo 15HP CNC Motor Spindle | <b>Location:</b> Coimbatore, TN | <b>Sampling Rate:</b> 2,000 Hz Continuous
        </p>
    """, unsafe_allow_html=True)

with top_r:
    if fault_severity > 0.5:
        st.markdown("""
            <div style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; padding:10px 16px; border-radius:10px; text-align:right;">
                <span class="pulsating-dot-red"></span> <b style="color:#EF4444; font-size:14px;">CRITICAL ANOMALY DETECTED</b>
                <div style="font-size:11px; color:#FCA5A5;">Isolation Forest Score: 0.89</div>
            </div>
        """, unsafe_allow_html=True)
    elif fault_severity > 0.3:
        st.markdown("""
            <div style="background:rgba(245,158,11,0.15); border:1px solid #F59E0B; padding:10px 16px; border-radius:10px; text-align:right;">
                <span class="pulsating-dot" style="background-color:#F59E0B;"></span> <b style="color:#F59E0B; font-size:14px;">INCIPIENT WEAR WARNING</b>
                <div style="font-size:11px; color:#FDE68A;">Isolation Forest Score: 0.62</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background:rgba(16,185,129,0.15); border:1px solid #10B981; padding:10px 16px; border-radius:10px; text-align:right;">
                <span class="pulsating-dot"></span> <b style="color:#10B981; font-size:14px;">SYSTEM OPERATIONAL</b>
                <div style="font-size:11px; color:#6EE7B7;">ISO 10816 Zone A (Healthy)</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. DYNAMIC CALCULATIONS & METRIC HERO CARDS
# ---------------------------------------------------------
# Physics-based synthetic signal processing calculation
vibe_rms = round(0.38 + fault_severity * 4.2, 3)
peak_fft_db = round(12.4 + fault_severity * 72.1, 1)
temp_c = round(42.0 + fault_severity * 38.5, 1)
rul_days = max(1, int(45 * (1.0 - fault_severity * 0.95)))
health_index = max(4.0, round(97.2 * (1.0 - fault_severity * 0.91), 1))

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Vibration RMS</div>
            <div class="metric-val" style="color:{'#EF4444' if vibe_rms > 2.8 else '#00E5FF'};">{vibe_rms} <span style="font-size:14px;">g</span></div>
            <div class="metric-sub" style="color:#94A3B8;">Limit: 2.80 g (ISO)</div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Peak FFT Energy</div>
            <div class="metric-val" style="color:{'#EF4444' if peak_fft_db > 50 else '#10B981'};">{peak_fft_db} <span style="font-size:14px;">dB</span></div>
            <div class="metric-sub" style="color:#94A3B8;">380 Hz Harmonic</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Bearing Temp</div>
            <div class="metric-val" style="color:{'#EF4444' if temp_c > 65 else '#F59E0B'};">{temp_c} <span style="font-size:14px;">°C</span></div>
            <div class="metric-sub" style="color:#94A3B8;">Max Thermal Threshold: 75°C</div>
        </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Predicted RUL</div>
            <div class="metric-val" style="color:{'#EF4444' if rul_days < 7 else '#00E5FF'};">{rul_days} <span style="font-size:14px;">Days</span></div>
            <div class="metric-sub" style="color:#94A3B8;">Downtime Horizon</div>
        </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Asset Health Index</div>
            <div class="metric-val" style="color:{'#EF4444' if health_index < 50 else '#10B981'};">{health_index}%</div>
            <div class="metric-sub" style="color:#94A3B8;">ZED Quality Index</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. DSP GRAPHICAL ENGINE & REAL-TIME DISPATCH
# ---------------------------------------------------------
col_left, col_right = st.columns([2.4, 1.2])

with col_left:
    st.markdown("<h3 style='font-size:16px; margin-bottom:10px;'>⚡ High-Frequency DSP Telemetry Analysis</h3>", unsafe_allow_html=True)
    
    tab_time, tab_fft, tab_iso = st.tabs(["📈 Time Domain Acceleration g(t)", "🔬 FFT Frequency Spectrum (Hz)", "📊 Anomaly Distribution"])
    
    # Generate Synthetic High-Frequency DSP Signal
    fs = 2000
    t = np.linspace(0, 0.2, int(fs * 0.2))
    base_wave = np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.08, len(t))
    fault_wave = fault_severity * (2.2 * np.sin(2 * np.pi * 380 * t) + np.random.normal(0, 0.35, len(t)))
    combined_wave = base_wave + fault_wave
    
    fft_vals = np.abs(np.fft.rfft(combined_wave))
    fft_freqs = np.fft.rfftfreq(len(combined_wave), 1/fs)
    
    with tab_time:
        fig_time = go.Figure()
        fig_time.add_trace(go.Scatter(
            x=t, y=combined_wave,
            mode='lines',
            line=dict(color='#00E5FF' if fault_severity < 0.4 else '#EF4444', width=2),
            name="Acceleration Signal"
        ))
        fig_time.update_layout(
            template="plotly_dark",
            height=280,
            margin=dict(l=10, r=10, t=15, b=10),
            xaxis_title="Time (Seconds)",
            yaxis_title="Acceleration (g)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(18,24,38,0.5)',
            xaxis=dict(gridcolor='#1E293B'),
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with tab_fft:
        fig_fft = go.Figure()
        fig_fft.add_trace(go.Scatter(
            x=fft_freqs[:250], y=fft_vals[:250],
            mode='lines',
            line=dict(color='#10B981' if fault_severity < 0.4 else '#F59E0B', width=2),
            name="Spectral Energy"
        ))
        if fault_severity > 0.2:
            fig_fft.add_annotation(
                x=380, y=np.max(fft_vals),
                text="⚠️ 380 Hz Inner Race Defect",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#EF4444",
                font=dict(color="#EF4444", size=12)
            )
        fig_fft.update_layout(
            template="plotly_dark",
            height=280,
            margin=dict(l=10, r=10, t=15, b=10),
            xaxis_title="Frequency (Hz)",
            yaxis_title="Spectral Density",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(18,24,38,0.5)',
            xaxis=dict(gridcolor='#1E293B'),
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_fft, use_container_width=True)

    with tab_iso:
        st.markdown("<p style='font-size:12px; color:#94A3B8;'>Isolation Forest Unsupervised Anomaly Probability vs Historical Normal Distribution</p>", unsafe_allow_html=True)
        # Iso forest distribution chart
        normal_dist = np.random.normal(0.2, 0.05, 500)
        current_score = min(0.95, 0.2 + fault_severity * 0.7)
        
        fig_iso = go.Figure()
        fig_iso.add_trace(go.Histogram(x=normal_dist, name="Baseline Normal", marker_color="#10B981", opacity=0.6))
        fig_iso.add_vline(x=current_score, line_width=3, line_dash="dash", line_color="#EF4444", annotation_text=f"Current Asset Score ({current_score:.2f})")
        fig_iso.update_layout(
            template="plotly_dark",
            height=250,
            margin=dict(l=10, r=10, t=15, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(18,24,38,0.5)',
            xaxis_title="Anomaly Score [0 = Normal, 1 = Fault]",
            yaxis_title="Sample Density"
        )
        st.plotly_chart(fig_iso, use_container_width=True)

with col_right:
    st.markdown("<h3 style='font-size:16px; margin-bottom:10px;'>💬 Automated Emergency Webhook Dispatch</h3>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
            <div style="background:#121826; border:1px solid #1E293B; padding:14px; border-radius:12px; height:320px; overflow-y:auto;">
        """, unsafe_allow_html=True)
        
        if fault_severity > 0.4:
            st.error(f"""
            **🚨 CRITICAL FAULT DISPATCHED**
            
            * **Target:** Plant Manager (Coimbatore Branch)
            * **Channel:** WhatsApp Business API + Twilio SMS
            * **Timestamp:** {datetime.now().strftime('%H:%M:%S')}
            * **Asset:** MTR-01 (Texmo CNC Spindle)
            * **Diagnosis:** {fault_type}
            * **Estimated Repair Cost:** ₹12,500
            * **Prevented Unscheduled Losses:** ₹2,40,000
            """)
        else:
            st.info("""
            **🟢 AUTOMATED MONITORING ACTIVE**
            
            All 120 connected MSME assets in the Coimbatore cluster are sending telemetry pings every 500ms. 
            
            *Thresholds:* ISO 10816 Zone A/B compliant.
            """)
            
        st.markdown("<br><b>📡 Live MQTT Sensor Packet Stream</b>", unsafe_allow_html=True)
        st.json({
            "node_id": "ESP32_COIMBATORE_01",
            "vibration_rms_g": vibe_rms,
            "peak_hz": 380 if fault_severity > 0.3 else 50,
            "isolation_score": round(0.2 + fault_severity * 0.7, 2),
            "zed_scheme_pass": True if fault_severity < 0.5 else False
        })
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. CONNECTED ASSET FLEET MATRIX & ZED REPORT DOWNLOADER
# ---------------------------------------------------------
st.markdown("<h3 style='font-size:18px;'>📋 Connected Cluster Asset Status Matrix</h3>", unsafe_allow_html=True)

fleet_data = [
    {"Machine ID": "MTR-01", "Asset Name": "Texmo Main Motor Spindle 01", "Vibration (g)": vibe_rms, "Health Index (%)": health_index, "RUL (Days)": rul_days, "Status": "CRITICAL" if fault_severity > 0.5 else "HEALTHY"},
    {"Machine ID": "PMP-07", "Asset Name": "CRI Submersible Pump Node 07", "Vibration (g)": 0.82, "Health Index (%)": 72.4, "RUL (Days)": 18, "Status": "AT RISK"},
    {"Machine ID": "CMP-02", "Asset Name": "ELGi Industrial Air Compressor", "Vibration (g)": 3.10, "Health Index (%)": 38.1, "RUL (Days)": 4, "Status": "CRITICAL"},
    {"Machine ID": "TUR-04", "Asset Name": "LMW CNC Machine Turbine", "Vibration (g)": 0.41, "Health Index (%)": 94.8, "RUL (Days)": 42, "Status": "HEALTHY"},
    {"Machine ID": "GEN-03", "Asset Name": "Kirloskar Diesel Generator 03", "Vibration (g)": 1.12, "Health Index (%)": 68.2, "RUL (Days)": 15, "Status": "AT RISK"},
]

df_fleet = pd.DataFrame(fleet_data)

st.dataframe(
    df_fleet,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Health Index (%)": st.column_config.ProgressColumn("Health Index (%)", format="%.1f%%", min_value=0, max_value=100),
        "Vibration (g)": st.column_config.NumberColumn("Vibration (g)", format="%.2f g")
    }
)

# Downloadable Audit Log for Pitch Impression
csv_report = df_fleet.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📄 Download Official MSME ZED Quality Scheme Audit Report (CSV)",
    data=csv_report,
    file_name=f"MSME_Predictive_Maintenance_Report_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)
