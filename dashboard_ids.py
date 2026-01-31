import streamlit as st
import pandas as pd
import joblib
import time
import json
import plotly.express as px
import plotly.graph_objects as go
from data_handler import DataHandler

# 1. Page Config & High-End Cyber Theme
st.set_page_config(page_title="AI-IDS IoT Security Center", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        padding: 20px; 
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    h1 { color: #ff4b4b; font-family: 'Courier New', Courier, monospace; text-align: center; font-size: 3rem; }
    .stAlert { border-radius: 12px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# 2. Load Resources
@st.cache_resource
def load_assets():
    model = joblib.load('trained_ids_model.pkl')
    dh = DataHandler('cicids2017_cleaned.csv')
    dh.load_and_clean(sample_size=1500) 
    return model, dh

try:
    model, dh = load_assets()
except:
    st.error("🚨 System Error: Model file missing. Run app.py first.")
    st.stop()

# 3. Sidebar Controls
st.sidebar.title("🛡️ System Control")
st.sidebar.markdown("---")
st.sidebar.success("AI Engine: ENABLED")
st.sidebar.info("Mode: Static Simulation")
sim_speed = st.sidebar.slider("Simulation Speed", 0.1, 2.0, 0.43)
if st.sidebar.button("Reset Dashboard"):
    st.rerun()

# 4. Header Section
st.title("CYBER-IOT INTELLIGENT IDS")
st.markdown("<p style='text-align: center; color: #8b949e;'>Historical Traffic Analysis & Threat Classification</p>", unsafe_allow_html=True)
st.markdown("---")

# 5. Top-Level Metrics (Added Standby Logic)
m1, m2, m3, m4 = st.columns(4)

total_packets_placeholder = m1.empty()
threats_detected_placeholder = m2.empty()
latency_placeholder = m3.empty() 
status_placeholder = m4.empty() # Placeholder for Gateway Status

# Initial state (STANDBY)
total_packets_placeholder.metric("Packets Scanned", "0")
threats_detected_placeholder.metric("Threats Detected", "0")
latency_placeholder.metric("Avg Latency", "0.00 ms")
status_placeholder.metric("Gateway Status", "STANDBY")

st.markdown("---")

# 6. Main Dashboard Layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📡 Simulation Traffic Stream")
    traffic_container = st.container(height=450)

with col_right:
    st.subheader("📊 Threat Distribution")
    chart_placeholder = st.empty()

# 7. Simulation Engine
if st.button("🚀 Start Monitoring Stream", use_container_width=True):
    # Update Status to ONLINE when button is clicked
    status_placeholder.metric("Gateway Status", "ONLINE", delta="ACTIVE")
    
    threat_log = []
    alert_count = 0
    total_latency = 0 
    
    for index, row in dh.df.iterrows():
        # Start Latency Timer
        start_time = time.time()
        
        # AI Logic
        features = row.drop('Attack Type').values.reshape(1, -1)
        pred_idx = model.predict(features)[0]
        pred_label = dh.le.inverse_transform([pred_idx])[0]
        
        # End Latency Timer
        current_latency = (time.time() - start_time) * 1000
        total_latency += current_latency
        threat_log.append(pred_label)
        
        # UI Updates - Stream
        with traffic_container:
            if pred_label == "Normal Traffic":
                st.write(f"✅ [SAFE] Packet ID: {index} | Latency: {current_latency:.2f}ms")
            else:
                alert_count += 1
                st.error(f"🚨 [ALERT] {pred_label} Detected! | Latency: {current_latency:.2f}ms")
        
        # UI Updates - Metrics
        avg_latency = total_latency / len(threat_log)
        total_packets_placeholder.metric("Packets Scanned", len(threat_log))
        threats_detected_placeholder.metric("Threats Detected", alert_count, delta=alert_count, delta_color="inverse")
        latency_placeholder.metric("Avg Latency", f"{avg_latency:.2f} ms")
        
        # UI Updates - Chart
        counts = pd.Series(threat_log).value_counts()
        fig = px.pie(
            values=counts.values, 
            names=counts.index, 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu_r
        )
        fig.update_layout(
            template="plotly_dark", 
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        time.sleep(sim_speed)