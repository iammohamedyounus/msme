import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmartPredict AI - Predictive Maintenance",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM DARK ENTERPRISE UI STYLING (CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Dark Theme Core Colors */
    .main { background-color: #0B0E14; }
    .stApp { color: #E2E8F0; font-family: 'Inter', -apple-system, sans-serif; }
    
    /* Hide Streamlit Default Headers */
    header[data-testid="stHeader"] { visibility: hidden; }
    
    /* Card Container Base */
    .dashboard-card {
        background-color: #121824;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 12px;
    }
    
    /* Metric KPI Cards */
    .kpi-card {
        background-color: #121824;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .kpi-title { font-size: 13px; color: #94A3B8; font-weight: 500; }
    .kpi-value { font-size: 26px; font-weight: 700; color: #FFFFFF; margin: 4px 0; }
    .kpi-sub { font-size: 11px; font-weight: 500; }
    
    /* Status Badges */
    .badge-healthy { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; display: inline-block; }
    .badge-atrisk { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; display: inline-block; }
    .badge-critical { background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.3); padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; display: inline-block; }
    .badge-warning { background: rgba(234, 179, 8, 0.15); color: #EAB308; border: 1px solid rgba(234, 179, 8, 0.3); padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; display: inline-block; }

    /* Timeline & Alert Lists */
    .item-box {
        background-color: #1A2234;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid #3B82F6;
    }
    
    /* Custom Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0C101A;
        border-right: 1px solid #1E293B;
    }
    
    /* Tables */
    .dataframe { background-color: #121824 !important; color: #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
            <div style="background:#2563EB; padding:8px; border-radius:8px; color:white; font-size:18px;">⚙️</div>
            <div>
                <h3 style="margin:0; font-size:16px; color:#FFF;">SmartPredict AI</h3>
                <p style="margin:0; font-size:11px; color:#64748B;">Predictive Maintenance</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["Dashboard", "Machines", "AI Predictions", "Real-time Monitor", "Alerts", "Analytics", "Reports", "Maintenance", "Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # Coimbatore Project Controller / Fault Injector
    st.markdown("### 🎛️ Demo Fault Injector")
    fault_severity = st.slider("Inject Bearing Fault (MTR-01)", 0.0, 1.0, 0.1, step=0.05)
    
    st.markdown("---")
    st.markdown("""
        <div style="background:#121824; border:1px solid #1E293B; padding:12px; border-radius:8px;">
            <p style="margin:0; font-size:12px; color:#10B981;">🟢 <b>System Status</b></p>
            <p style="margin:4px 0 0 0; font-size:11px; color:#94A3B8;">All Systems Operational</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TOP HEADER BAR
# ---------------------------------------------------------
top_col1, top_col2, top_col3 = st.columns([2, 2, 1])

with top_col1:
    st.markdown("<h2 style='margin:0; font-size:22px; font-weight:700;'>Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; font-size:12px; color:#64748B;'>Welcome back, Engineer! | Coimbatore MSME Cluster</p>", unsafe_allow_html=True)

with top_col2:
    st.text_input("🔍 Search machines, sensors, alerts...", label_visibility="collapsed")

with top_col3:
    st.markdown("""
        <div style="text-align:right; font-size:12px;">
            <span style="color:#FFF; font-weight:600;">Engineer</span> <span style="color:#10B981;">● Online</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ROW 1: 6 KPI METRIC CARDS
# ---------------------------------------------------------
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Total Machines</div>
            <div class="kpi-value">120</div>
            <div class="kpi-sub" style="color:#64748B;">All Connected Machines</div>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Healthy Machines</div>
            <div class="kpi-value" style="color:#10B981;">82</div>
            <div class="kpi-sub" style="color:#10B981;">68.3% of total</div>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Machines at Risk</div>
            <div class="kpi-value" style="color:#F59E0B;">28</div>
            <div class="kpi-sub" style="color:#F59E0B;">23.3% of total</div>
        </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Critical Machines</div>
            <div class="kpi-value" style="color:#EF4444;">10</div>
            <div class="kpi-sub" style="color:#EF4444;">8.4% of total</div>
        </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Today's Alerts</div>
            <div class="kpi-value" style="color:#8B5CF6;">18</div>
            <div class="kpi-sub" style="color:#64748B;">Updated just now</div>
        </div>
    """, unsafe_allow_html=True)

with kpi6:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Avg. Health Score</div>
            <div class="kpi-value" style="color:#06B6D4;">78.6%</div>
            <div class="kpi-sub" style="color:#10B981;">↑ 5.2% vs yesterday</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ROW 2: ANALYTICS GRID (4 COLUMNS)
# ---------------------------------------------------------
m_col1, m_col2, m_col3, m_col4 = st.columns([2, 1.6, 1.7, 1.7])

# 1. Machine Health Trend (Line Chart)
with m_col1:
    st.markdown("<div style='font-size:13px; font-weight:600; margin-bottom:8px;'>Machine Health Trend</div>", unsafe_allow_html=True)
    dates = pd.date_range(end=datetime.today(), periods=8).strftime('%b %d')
    # Dynamic health degradation based on slider
    health_trend = [80, 85, 78, 65, 50, 62, 75, int(85 * (1 - fault_severity*0.5))]
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=dates, y=health_trend,
        mode='lines+markers',
        line=dict(color='#2563EB', width=2),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.1)'
    ))
    fig_trend.update_layout(
        template="plotly_dark",
        height=200,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis=dict(range=[0, 100], gridcolor='#1E293B'),
        xaxis=dict(gridcolor='#1E293B')
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# 2. Equipment Health Distribution (Doughnut Chart)
with m_col2:
    st.markdown("<div style='font-size:13px; font-weight:600; margin-bottom:8px;'>Equipment Health Distribution</div>", unsafe_allow_html=True)
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Healthy', 'At Risk', 'Critical'],
        values=[82, 28, 10],
        hole=.6,
        marker_colors=['#10B981', '#F59E0B', '#EF4444'],
        textinfo='none'
    )])
    fig_donut.add_annotation(text="<b>120</b><br><span style='font-size:10px;'>Total</span>", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#FFF")
    fig_donut.update_layout(
        template="plotly_dark",
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(font=dict(size=10), orientation="v")
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# 3. Failure Prediction Timeline
with m_col3:
    st.markdown("<div style='font-size:13px; font-weight:600; margin-bottom:8px;'>Failure Prediction Timeline</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background:#121824; border:1px solid #1E293B; padding:10px; border-radius:10px; height:200px; overflow-y:auto;">
            <div class="item-box" style="border-left-color:#EF4444;">
                <div><b style="font-size:12px;">MTR-01 (Texmo CNC)</b><br><span style="font-size:10px; color:#64748B;">Predicted Failure: May 20</span></div>
                <span class="badge-critical">Critical</span>
            </div>
            <div class="item-box" style="border-left-color:#F59E0B;">
                <div><b style="font-size:12px;">PMP-07 (Water Pump)</b><br><span style="font-size:10px; color:#64748B;">Predicted Failure: May 25</span></div>
                <span class="badge-atrisk">At Risk</span>
            </div>
            <div class="item-box" style="border-left-color:#EAB308;">
                <div><b style="font-size:12px;">CMP-02 (Compressor)</b><br><span style="font-size:10px; color:#64748B;">Predicted Failure: Jun 02</span></div>
                <span class="badge-warning">Warning</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 4. Recent Alerts
with m_col4:
    st.markdown("<div style='font-size:13px; font-weight:600; margin-bottom:8px;'>Recent Alerts</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background:#121824; border:1px solid #1E293B; padding:10px; border-radius:10px; height:200px; overflow-y:auto;">
            <div style="margin-bottom:10px; border-bottom:1px solid #1E293B; padding-bottom:6px;">
                <span style="color:#EF4444; font-weight:600; font-size:11px;">⚠️ Motor-01</span>
                <span style="color:#64748B; font-size:10px; float:right;">2 min ago</span>
                <p style="margin:2px 0 0 0; font-size:11px; color:#94A3B8;">High vibration 380Hz spectral spike detected.</p>
            </div>
            <div style="margin-bottom:10px; border-bottom:1px solid #1E293B; padding-bottom:6px;">
                <span style="color:#F59E0B; font-weight:600; font-size:11px;">⚠️ Pump-07</span>
                <span style="color:#64748B; font-size:10px; float:right;">15 min ago</span>
                <p style="margin:2px 0 0 0; font-size:11px; color:#94A3B8;">Temperature threshold exceeded (78°C).</p>
            </div>
            <div>
                <span style="color:#EAB308; font-weight:600; font-size:11px;">⚠️ Compressor-02</span>
                <span style="color:#64748B; font-size:10px; float:right;">1 hr ago</span>
                <p style="margin:2px 0 0 0; font-size:11px; color:#94A3B8;">Pressure fluctuation warning.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ROW 3: MAIN MACHINE OVERVIEW TABLE & AI ASSISTANT
# ---------------------------------------------------------
b_col1, b_col2 = st.columns([3.2, 1.2])

with b_col1:
    st.markdown("<div style='font-size:15px; font-weight:600; margin-bottom:12px;'>Machine Overview</div>", unsafe_allow_html=True)
    
    # Machine Dataset
    machines_data = [
        {"Machine ID": "MTR-01", "Machine Name": "Texmo Main Motor 01", "Health (%)": max(10, int(92.4 * (1 - fault_severity))), "RUL (Days)": max(1, int(45 * (1 - fault_severity))), "Status": "Critical" if fault_severity > 0.5 else "Healthy", "Last Updated": "Just now"},
        {"Machine ID": "PMP-07", "Machine Name": "CRI Water Pump 07", "Health (%)": 65.3, "RUL (Days)": 12, "Status": "At Risk", "Last Updated": "5 min ago"},
        {"Machine ID": "CMP-02", "Machine Name": "Air Compressor 02", "Health (%)": 48.7, "RUL (Days)": 5, "Status": "Critical", "Last Updated": "1 min ago"},
        {"Machine ID": "TUR-04", "Machine Name": "LMW Turbine 04", "Health (%)": 85.1, "RUL (Days)": 30, "Status": "Healthy", "Last Updated": "3 min ago"},
        {"Machine ID": "GEN-03", "Machine Name": "Generator Node 03", "Health (%)": 71.6, "RUL (Days)": 18, "Status": "At Risk", "Last Updated": "10 min ago"},
    ]
    
    df_machines = pd.DataFrame(machines_data)
    
    # Styled Table Display
    st.dataframe(
        df_machines,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Health (%)": st.column_config.ProgressColumn("Health (%)", format="%.1f%%", min_value=0, max_value=100),
            "Status": st.column_config.TextColumn("Status")
        }
    )

with b_col2:
    st.markdown("<div style='font-size:15px; font-weight:600; margin-bottom:12px;'>System Overview & AI Assistant</div>", unsafe_allow_html=True)
    
    # Overview Panel
    st.markdown("""
        <div style="background:#121824; border:1px solid #1E293B; padding:14px; border-radius:10px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px;">
                <span style="color:#94A3B8;">Performance</span>
                <b style="color:#FFF;">78.6%</b>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px;">
                <span style="color:#94A3B8;">Efficiency</span>
                <b style="color:#FFF;">82.4%</b>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px;">
                <span style="color:#94A3B8;">Reliability</span>
                <b style="color:#FFF;">91.2%</b>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # AI Assistant Box
    st.markdown("""
        <div style="background:#121824; border:1px solid #1E293B; padding:14px; border-radius:10px;">
            <div style="font-size:12px; font-weight:600; color:#3B82F6; margin-bottom:8px;">✨ AI Assistant ● Online</div>
            <p style="font-size:12px; color:#CBD5E1; margin-bottom:10px;">Hello Engineer! How can I help you analyze the Coimbatore MSME telemetry today?</p>
        </div>
    """, unsafe_allow_html=True)
    
    chat_prompt = st.text_input("Ask AI Assistant...", placeholder="Type your message...", label_visibility="collapsed")
    if chat_prompt:
        st.info(f"🤖 **AI Response:** Analyzing telemetry for '{chat_prompt}'... No critical failure risk detected beyond MTR-01.")
