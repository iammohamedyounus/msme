# ⚡ VibeGuard AI — Enterprise Predictive Telemetry Engine
> **Sub-₹3,000 Edge-AI Predictive Maintenance for Industrial Pump & Motor Clusters**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![ESP32](https://img.shields.io/badge/Hardware-ESP32%20%2B%20MPU6050-000000?style=for-the-badge&logo=espressif&logoColor=white)
![ISO Standard](https://img.shields.io/badge/Compliance-ISO%2010816--3-10B981?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)


## 📌 Executive Summary & Financial Impact

Unscheduled machinery breakdown in industrial SME clusters (such as the Coimbatore Pump Manufacturing Belt) leads to catastrophic production halts. A single 15HP CNC motor spindle failure causes an average of **₹2.5 Lakhs ($3,000+) in unscheduled daily losses**. Enterprise predictive maintenance solutions (Siemens, Honeywell) require capital expenditures exceeding ₹10 Lakhs, making them unfeasible for local MSMEs.

**VibeGuard AI** bridges this gap. By coupling a low-cost **ESP32 Edge Node** ($30) with an **Unsupervised Isolation Forest ML Engine**, VibeGuard AI delivers real-time Fast Fourier Transform (FFT) spectral analysis, remaining useful life (RUL) estimation, and automated emergency WhatsApp webhook dispatches—aligning with India's **MSME ZED Scheme (Zero Defect, Zero Effect)**.


## 🏗️ System Architecture



                           ┌─────────────────────────┐
                           │   Texmo CNC Spindle     │
                           └───────────┬─────────────┘
                                       │ Vibration
                           ┌───────────▼─────────────┐
                           │ ESP32 + MPU6050 (I2C)   │
                           │ High-Speed g(t) Sample  │
                           └───────────┬─────────────┘
                                       │ Serial / MQTT JSON Stream
                           ┌───────────▼─────────────┐
                           │      dsp_engine.py      │
                           │  RMS, Kurtosis & FFT    │
                           └───────────┬─────────────┘
                                       │ Processed Feature Vector
             ┌─────────────────────────┴─────────────────────────┐
             │                                                   │
┌────────────▼────────────┐                         ┌────────────▼────────────┐
│ Isolation Forest Model  │                         │ Streamlit UI Dashboard │
│ Anomaly Score [0.0 - 1] │                         │ Live Signal & FFT Plot  │
└────────────┬────────────┘                         └─────────────────────────┘
             │
             │ Anomaly Score > 0.75
┌────────────▼────────────┐
│       alerts.py         │
│ Twilio / CallMeBot API  │
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│ Live WhatsApp Alert     │
│  to Plant Supervisor    │
└─────────────────────────┘




## ✨ Key Features & Technical Innovation

* **🔬 High-Frequency DSP Signal Analysis:** Extracts Time-Domain metrics (RMS Acceleration, Crest Factor, Kurtosis) and Frequency-Domain spectra (FFT) to isolate 380 Hz inner-race bearing harmonics.
* **🧠 Unsupervised Anomaly Detection:** Utilizes an **Isolation Forest** model to detect incipient mechanical wear without requiring pre-labeled failure datasets.
* **⚡ Real-Time Emergency Webhooks:** Automatically fires instant WhatsApp alert dispatches with exact failure diagnostics to shop-floor supervisors when ISO 10816 thresholds are breached.
* **📊 ZED Quality Audit Exporting:** Generates compliant CSV audit logs formatted for Government ZED Quality Scheme certification.



## 🛠️ Repository File Structure

vibeguard-ai/
├── app.py                 # Streamlit UI Command Center
├── dsp_engine.py          # DSP, Kurtosis, FFT & Feature Extraction
├── alerts.py              # WhatsApp Webhook Dispatcher (st.secrets secured)
├── esp32_firmware.ino     # C++ Firmware for ESP32 + MPU6050 Accelerometer
├── requirements.txt       # Production dependencies
├── .gitignore             # Shields credentials & bytecode
└── README.md              # Project Pitch & Documentation


## 🚀 Quick Start Guide

### 1. Clone & Install Dependencies

```bash
git clone [https://github.com/your-username/vibeguard-ai.git](https://github.com/your-username/vibeguard-ai.git)
cd vibeguard-ai
pip install -r requirements.txt

```

### 2. Configure Credentials (`.streamlit/secrets.toml`)

Create a local secrets file inside `.streamlit/secrets.toml`:

```toml
WHATSAPP_PHONE = "+91XXXXXXXXXX"
WHATSAPP_API_KEY = "YOUR_CALLMEBOT_API_KEY"

```

### 3. Launch the Application

```bash
python -m streamlit run app.py

```


## 🧮 Mathematical Formulations

### 1. Isolation Forest Anomaly Metric

$$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$

### 2. Spectral Kurtosis (Transient Impact Sensitivity)

$$K = \frac{\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^4}{\left(\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^2\right)^2}$$



## 📜 License & Compliance

Distributed under the MIT License. Built for industrial alignment with **ISO 10816-3 Mechanical Vibration Standards**.

