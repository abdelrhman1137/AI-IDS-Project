AI-Based Intelligent IDS for IoT Networks (CPS Security)

Course: Cyber Physical Systems Security (CCY4301)

Developed by: Abdelrhman Mohamed

Status: Multi-Phase Security Operations Center (SOC) Completed

Project Overview

This project implements an intelligent, adaptive Intrusion Detection System (IDS) specifically designed for resource-constrained IoT environments. The system uses a Hybrid Ensemble Learning approach (Random Forest + XGBoost) to classify network traffic and protect the Edge/Gateway layer of a CPS architecture.

Implementation Versions

1. Simulation and Historical Analysis Version (Static)

Project Scope: In this version, the focus was on verifying the AI engine against historical data. A professional SOC dashboard was developed to simulate a network stream by processing the CICIDS2017 dataset.

Data Flow: The system pulls raw samples, removes labels, and requires the AI to predict the attack type based on 52 network features.

Performance Tracking: High-resolution timers calculate the Inference Latency for every individual packet, demonstrating that the model can handle historical traffic with sub-millisecond processing speeds.

2. Live Gateway Monitoring Version (Real-Time)

Implementation Details:
This version transitions from theoretical simulation to active defense through a Live Network Receptor that interfaces directly with physical hardware (Wi-Fi or Ethernet cards).

Live Sniffing: Utilizing the NetworkReceptor class, the system captures raw packets, aggregates them into logical flows, and performs feature extraction in real-time.

Confidence Logic: To manage the noise of real-world traffic, a 90% Confidence Threshold was implemented. The system only triggers a critical alert if the AI reaches this certainty level, significantly reducing False Positives.

Hardware Interception: The system was successfully tested against live attacks (DoS and Brute Force) launched via a secondary attacker console.

AI Engine and Technical Architecture

Model Serialization (The .pkl file)

The project utilizes a trained_ids_model.pkl file. This represents the serialized intelligence of the system. By saving the trained model, the dashboards can perform instant detection without requiring retraining on millions of rows during system boot.

The Hybrid Ensemble

The system utilizes a Soft-Voting Ensemble rather than a single model:

Random Forest: Provides stability and handles complex data logic.

XGBoost: Provides high-speed processing and identifies subtle attack patterns.

Performance: A combined 99.76% Accuracy across seven distinct traffic categories.

Feature Engineering

The system analyzes 52 distinct network features, including:

Temporal Features: Flow Duration and Inter-Arrival Times (IAT).

Dynamic Features: Packet Length Mean, Forward/Backward counts, and TCP Flag analysis.

Attacks Detected

The system is optimized for the following threat vectors:

Denial-of-Service (DoS): Identified via spikes in Flow Duration and Packet count.

Brute Force: Identified through credential stuffing patterns on Port 22.

Port Scanning: Detection of reconnaissance and eavesdropping patterns.

Data Injection/Bots: Identified through feature inconsistencies and payload anomalies.

System Architecture

Perception Layer: IoT Devices and raw network packets.

Edge/Gateway Layer: The AI Engine (model_manager.py) performing deep packet inspection.

Application Layer: Streamlit SOC Dashboards providing real-time visual alerts and threat analytics.

Execution Instructions

Install Requirements: pip install -r requirements.txt

Train AI: python app.py (Generates the .pkl file)

Run Simulation: streamlit run static_dashboard.py

Run Live Gateway: streamlit run live_dashboard.py
