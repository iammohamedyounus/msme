import streamlit as st
import pandas as pd
import time
from motor_simulator import generate_motor_telemetry

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="PulseGuard AI | MSME Predictive Maintenance",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ PulseGuard AI: MSME Predictive Maintenance")
st.caption("Coimbatore Pump & Motor Cluster — Real-Time Telemetry Monitor")

# ---------------------------------------------------------
# SIDEBAR: Demo Fault Injection Panel
# ---------------------------------------------------------
st.sidebar.header("🎛️ Hardware Digital Twin Controls")
st.sidebar.info("Inject fault dynamics into the physics simulation stream.")

motor_id = st.sidebar.selectbox("Target Asset", ["Texmo 10HP Motor #01", "CRI Pump #02", "LMW Spindle #03"])
fault_mode = st.sidebar.radio("Operating Condition", ["NORMAL", "UNBALANCE", "BEARING_FAULT"])
severity = st.sidebar.slider("Fault Severity", min_value=0.0, max_value=1.0, value=0.0 if fault_mode == "NORMAL" else 0.85)

is_running = st.sidebar.toggle("Start Real-Time Stream", value=True)

# ---------------------------------------------------------
# DASHBOARD LAYOUT & METRICS
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
metric_rms = col1.empty()
metric_temp = col2.empty()
metric_status = col3.empty()

chart_placeholder = st.empty()

# Initialize Session State Buffer for Live Streaming Chart
if "telemetry_buffer" not in st.session_state:
    st.session_state.telemetry_buffer = pd.DataFrame(
        columns=["timestamp", "vibration_rms_mms", "temperature_c", "current_amps", "fault_label"]
    )

# ---------------------------------------------------------
# TELEMETRY PROCESSING LOOP
# ---------------------------------------------------------
if is_running:
    # 1. Fetch synthetic telemetry data point
    telemetry = generate_motor_telemetry(fault_mode=fault_mode, severity=severity)
    
    # 2. Append data to dynamic sliding buffer (keep last 30 readings)
    new_point = pd.DataFrame([telemetry])
    st.session_state.telemetry_buffer = pd.concat(
        [st.session_state.telemetry_buffer, new_point]
    ).tail(30)
    
    # 3. Update Real-Time KPI Cards
    rms_val = telemetry["vibration_rms_mms"]
    temp_val = telemetry["temperature_c"]
    
    metric_rms.metric("Vibration RMS (ISO 10816)", f"{rms_val} mm/s", delta=round(rms_val - 1.2, 2), delta_color="inverse")
    metric_temp.metric("Operating Temp", f"{temp_val} °C")
    
    if rms_val > 4.5:
        metric_status.error("CRITICAL: Immediate Bearing Failure Likely")
    elif rms_val > 1.8:
        metric_status.warning("WARNING: Mechanical Degradation")
    else:
        metric_status.success("HEALTHY: Class I Normal Operation")
        
    # 4. Render Live Vibration Waveform
    with chart_placeholder.container():
        st.subheader("Live Vibration Severity (mm/s)")
        st.line_chart(
            st.session_state.telemetry_buffer.set_index("timestamp")[["vibration_rms_mms"]]
        )
        
    time.sleep(1) # Stream update interval
