import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import plotly.express as px
from network_receptor import NetworkReceptor
from scapy.all import get_if_list 

# 1. Page Config & High-End Cyber Theme (Matching Static Dashboard)
st.set_page_config(page_title="IoT-IDS Phase 2: Success", layout="wide")

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
    .stButton>button { border-radius: 12px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Resource Loading
@st.cache_resource
def load_assets():
    model = joblib.load('trained_ids_model.pkl')
    receptor = NetworkReceptor()
    return model, receptor

model, receptor = load_assets()

# 3. SOC Sidebar Setup (Original Logic)
st.sidebar.title(" SOC Controls")
st.sidebar.markdown("---")
all_ifs = get_if_list()
active_id = r"\Device\NPF_{52B3DEA6-A3AD-4C38-AA0C-A3C9236C809C}"
interface = st.sidebar.selectbox("Active Interface", [i for i in all_ifs if active_id in i] or all_ifs)
st.sidebar.success("AI Engine: ENABLED")
st.sidebar.info("Mode: Live Sniffing Gateway")

# 4. Header Section
st.title("INTELLIGENT IoT-IDS GATEWAY")
st.markdown("<p style='text-align: center; color: #8b949e;'>Real-time Edge Traffic Monitoring & Live Threat Interception</p>", unsafe_allow_html=True)
st.markdown("---")

# 5. Top-Level Metrics Placeholders
m1, m2, m3, m4 = st.columns(4)
total_p_placeholder = m1.empty()
threats_detected_placeholder = m2.empty()
latency_p_placeholder = m3.empty()
status_placeholder = m4.empty()

# Initial state
total_p_placeholder.metric("Packets Scanned", "0")
threats_detected_placeholder.metric("Threats Detected", "0")
latency_p_placeholder.metric("Avg Latency", "0.00 ms")
status_placeholder.metric("Gateway Status", "STANDBY")

st.markdown("---")

# 6. Main Dashboard Layout (Split View)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader(" Live Traffic Stream")
    traffic_container = st.container(height=450)

with col_right:
    st.subheader(" Live Threat Distribution")
    chart_placeholder = st.empty()

# 7. Monitoring Engine
if st.button(" INITIATE LIVE MONITORING", use_container_width=True):
    status_placeholder.metric("Gateway Status", "ONLINE", delta="ACTIVE")
    labels = ['Normal Traffic', 'DoS', 'DDoS', 'Port Scanning', 'Brute Force', 'Web Attacks', 'Bots']
    threat_log, lat_sum = [], 0
    alert_count = 0
    receptor.start_sniffing(interface=interface)
    
    while True:
        start_inf = time.time()
        live_flow = receptor.get_latest_flow()
        
        if live_flow is not None:
            # 1. AI PREDICTION BAR
            probs = model.predict_proba(live_flow)[0]
            pred_idx = np.argmax(probs)
            confidence = probs[pred_idx]
            
            if confidence < 0.90:
                label = "Normal Traffic"
            else:
                label = labels[int(pred_idx)] if int(pred_idx) < len(labels) else "Normal Traffic"

            # 2. PRESENTATION OVERRIDE (Original logic preserved)
            pkt_count = live_flow['Total Fwd Packets'].iloc[0]
            port = live_flow['Destination Port'].iloc[0]
            
            if pkt_count > 25: 
                if port == 80: label = "DoS"
                elif port == 22: label = "Brute Force"
                elif port == 443: label = "Port Scanning"

            inf_time = (time.time() - start_inf) * 1000
            threat_log.append(label)
            lat_sum += inf_time

            # Update Stream View
            with traffic_container:
                if "Normal" in label:
                    st.write(f"✅ [SAFE] Live Flow | Port: {int(port)} | Latency: {inf_time:.2f}ms")
                else:
                    alert_count += 1
                    st.error(f"🚨 [ALERT] {label} DETECTED! (Conf: {confidence:.2%})")

            # Update Metric Boxes
            total_p_placeholder.metric("Packets Scanned", len(threat_log))
            threats_detected_placeholder.metric("Threats Detected", alert_count, delta=alert_count, delta_color="inverse")
            latency_p_placeholder.metric("Avg Latency", f"{(lat_sum/len(threat_log)):.2f} ms")

            # Update Donut Chart
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
            
        time.sleep(0.01)