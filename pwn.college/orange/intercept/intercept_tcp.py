from scapy.all import *

a = sniff(filter="tcp and dst host 10.0.0.3", count=1)
syn = a[0]
if syn[TCP].flags == "S":
     ans = TCP(
         dport=syn[TCP].sport,
         sport=syn[TCP].dport,
         flags="SA",
         seq=syn[TCP].seq,
         ack=syn[TCP].seq + 1)
     send(IP(src="10.0.0.3", dst="10.0.0.2")/ans)
