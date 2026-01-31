import pandas as pd
import numpy as np
from scapy.all import sniff, IP, TCP, UDP
import time
from threading import Thread

class NetworkReceptor:
    def __init__(self):
        self.active_flows = {}
        self.flow_timeout = 0.2 # Ultra-fast detection for live demo
        self.feature_columns = [
            'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Length of Fwd Packets',
            'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std',
            'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std',
            'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
            'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total',
            'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd Header Length', 'Bwd Header Length',
            'Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length', 'Packet Length Mean',
            'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'PSH Flag Count', 'ACK Flag Count',
            'Average Packet Size', 'Subflow Fwd Bytes', 'Init_Win_bytes_forward', 'Init_Win_bytes_backward',
            'act_data_pkt_fwd', 'min_seg_size_forward', 'Active Mean', 'Active Max', 'Active Min',
            'Idle Mean', 'Idle Max', 'Idle Min'
        ]

    def packet_callback(self, packet):
        if IP in packet:
            proto = packet[TCP] if TCP in packet else (packet[UDP] if UDP in packet else None)
            if proto:
                flow_key = (packet[IP].src, packet[IP].dst, proto.sport, proto.dport)
                if flow_key not in self.active_flows:
                    self.active_flows[flow_key] = {'start': time.time(), 'lens': [len(packet)], 'port': proto.dport}
                else:
                    self.active_flows[flow_key]['lens'].append(len(packet))

    def get_latest_flow(self):
        now = time.time()
        for key, data in list(self.active_flows.items()):
            if now - data['start'] > self.flow_timeout:
                # Minimal data filter to keep dashboard quiet during normal use
                if len(data['lens']) < 3: 
                    del self.active_flows[key]
                    continue

                row = {col: 0.0 for col in self.feature_columns}
                row.update({'Init_Win_bytes_forward': 8192.0, 'Init_Win_bytes_backward': 8192.0, 'min_seg_size_forward': 32.0})
                
                duration_us = (now - data['start']) * 1e6
                row.update({
                    'Destination Port': float(data['port']),
                    'Flow Duration': float(min(duration_us, 1000000)),
                    'Total Fwd Packets': float(len(data['lens'])),
                    'Total Length of Fwd Packets': float(sum(data['lens'])),
                    'Average Packet Size': float(np.mean(data['lens'])),
                })
                final_df = pd.DataFrame([[row[col] for col in self.feature_columns]], columns=self.feature_columns)
                del self.active_flows[key]
                return final_df
        return None

    def start_sniffing(self, interface):
        t = Thread(target=lambda: sniff(iface=interface, prn=self.packet_callback, store=0))
        t.daemon = True
        t.start()