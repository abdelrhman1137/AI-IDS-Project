# 🛡️ AI-Based Intrusion Detection System for IoT Networks
**Course:** Cyber Physical Systems Security (CCY4301)  
**Developed by:** [Your Team Name/Numbers]  
**Status:** 🚀 Live Web Dashboard Optimized

## 📌 Project Overview
This project implements an intelligent, adaptive IDS specifically designed for resource-constrained IoT environments. Using an **Ensemble Learning** approach (Random Forest + XGBoost), the system identifies malicious network traffic with high precision.

### ✅ Key Results
- **Overall Accuracy:** 99.76%
- **Detection Rate:** 100% for DoS and Data Injection attacks.

## ⚔️ Attacks Detected
Our AI model is specifically trained to recognize the four focus attacks requested:
1. **Denial-of-Service (DoS):** Detected via spikes in Flow Duration and Packet count.
2. **Data Injection:** Identified through payload and feature inconsistencies.
3. **Man-in-the-Middle (MITM):** Detected via reconnaissance patterns.
4. **Eavesdropping:** Passive detection through port scanning analysis.

## 🏗️ System Architecture
The system follows a three-layer CPS model:
* **Perception Layer:** IoT Sensors (Temperature, Camera, MQTT).
* **Edge/Gateway Layer:** The AI Engine (This Code) analyzing traffic in real-time.
* **Application Layer:** Streamlit Cloud Dashboard for security alerts.

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Launch Dashboard: `streamlit run dashboard_ids.py`