from scapy.all import IP, TCP, send
import time

TARGET_IP = "10.0.0.2"
TARGET_PORT = 31337
NUM_PACKETS = 1000  # adjust safely in your sandbox

for i in range(NUM_PACKETS):
    # Create IP + TCP packet with SYN flag
    pkt = IP(dst=TARGET_IP)/TCP(dport=TARGET_PORT, flags="S")
    send(pkt, verbose=False)
    time.sleep(0.01)  # slight delay to avoid crashing the host
