import streamlit as st
from dsp_engine import extract_vibration_features
from alerts import send_whatsapp_alert

# Extract DSP metrics cleanly
features = extract_vibration_features(raw_vibration_signal)

# Trigger alert when fault threshold is exceeded
if features["rms"] > 2.8:
    send_whatsapp_alert(
        asset_id="MTR-01", 
        fault_type="Inner Race Bearing Wear", 
        vibe_rms=features["rms"]
    )
