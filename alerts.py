# alerts.py
import requests
import urllib.parse
import streamlit as st

def send_whatsapp_alert(asset_id, fault_type, vibe_rms):
    """
    Reads API credentials from st.secrets and dispatches a WhatsApp alert.
    """
    try:
        phone_number = st.secrets["WHATSAPP_PHONE"]
        api_key = st.secrets["WHATSAPP_API_KEY"]
    except KeyError:
        print("Error: WhatsApp secrets missing from configuration.")
        return False

    message = (
        f"🚨 *CRITICAL ALERT: VibeGuard AI*\n\n"
        f"• *Asset:* {asset_id}\n"
        f"• *Diagnosis:* {fault_type}\n"
        f"• *Vibration RMS:* {vibe_rms} g (Threshold Breached)\n"
        f"• *Action Required:* Inspect Spindle Bearing Immediately."
    )

    encoded_msg = urllib.parse.quote(message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={encoded_msg}&apikey={api_key}"

    try:
        res = requests.get(url, timeout=5)
        return res.status_code == 200
    except Exception as e:
        print(f"Webhook Failed: {e}")
        return False
