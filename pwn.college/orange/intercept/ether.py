import scapy as scapy

# Craft a SYN packet
syn_packet = IP(dst="www.example.com")/TCP(dport=80, flags="S", seq=1000)

# Send the SYN packet and wait for a response
ans, unans = sr(syn_packet, timeout=2)

# Analyze the response (if any)
if ans:
    for sent, received in ans:
        if received.haslayer(TCP) and received.getlayer(TCP).flags == "SA":
            print("Received SYN-ACK from:", received.src)
            # Further actions, like sending an ACK to complete the handshake