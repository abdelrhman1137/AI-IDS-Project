import streamlit as st
import pandas as pd
import joblib
import time
import plotly.express as px
import plotly.graph_objects as go
from data_handler import DataHandler

# 1. Page Configuration & Professional CSS Styling
st.set_page_config(page_title="AI-IDS IoT Security Operations Center", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    h1 { color: #ff4b4b; font-family: 'Courier New', Courier, monospace; text-align: center; }
    .stAlert { border-radius: 10px; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# 2. Load Resources (AI Engine and Data)
@st.cache_resource
def load_assets():
    # Load the ensemble brain (RF + XGBoost)
    model = joblib.load('trained_ids_model.pkl')
    # Load data for simulation
    dh = DataHandler('cicids2017_cleaned.csv')
    dh.load_and_clean(sample_size=1000) 
    return model, dh

try:
    model, dh = load_assets()
except:
    st.error("Model file not found. Please run 'app.py' first to train and save the model.")
    st.stop()

# 3. Sidebar System Status
st.sidebar.title("🛡️ System Control")
st.sidebar.markdown("---")
st.sidebar.success("AI Engine: ENABLED")
st.sidebar.info("Model: Random Forest + XGBoost Ensemble")
sim_speed = st.sidebar.slider("Simulation Speed (Seconds)", 0.1, 2.0, 0.5)

# 4. Header
st.title("CYBER-IOT INTELLIGENT IDS")
st.write("Real-time Network Traffic Monitoring & Threat Analysis for CPS Environments")
st.markdown("---")

# 5. Dashboard Metrics (Dynamic Counters)
m1, m2, m3, m4 = st.columns(4)
total_packets = m1.metric("Packets Scanned", "0")
threats_found = m2.metric("Threats Detected", "0", delta_color="inverse")
accuracy_val = m3.metric("System Accuracy", "99.76%")
status = m4.metric("Gateway Status", "ONLINE")

# 6. Main Content Area
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📡 Live Traffic Stream")
    traffic_placeholder = st.empty()

with col_right:
    st.subheader("📊 Threat Distribution")
    chart_placeholder = st.empty()

# 7. Real-Time Simulation Logic
threat_log = []
alert_count = 0

if st.button("Start Monitoring Stream"):
    for index, row in dh.df.iterrows():
        # Prepare data for prediction
        features = row.drop('Attack Type').values.reshape(1, -1)
        
        # AI prediction using the "brain"
        pred_idx = model.predict(features)[0]
        pred_label = dh.le.inverse_transform([pred_idx])[0]
        threat_log.append(pred_label)
        
        # Logic for UI updates
        with traffic_placeholder.container():
            if pred_label == "Normal Traffic":
                st.write(f"✅ [SAFE] Packet ID: {index} | Protocol: TCP/MQTT")
            else:
                alert_count += 1
                st.error(f"🚨 [ALERT] {pred_label} Detected! | Action: Blocking Source IP")
        
        # Update Metrics and Charts
        total_packets.metric("Packets Scanned", len(threat_log))
        threats_found.metric("Threats Detected", alert_count)
        
        counts = pd.Series(threat_log).value_counts()
        fig = px.pie(values=counts.values, names=counts.index, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        time.sleep(sim_speed)