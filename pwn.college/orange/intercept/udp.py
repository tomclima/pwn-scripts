import socket
from socket import SOCK_DGRAM, AF_INET

sip = "10.0.0.1"
dip = "10.0.0.2"
sport = 31337
dport= 31337

sock = socket.socket(AF_INET, SOCK_DGRAM)
sock.bind((sip, sport))
server_address = (dip, dport)

message = b"Hello, World!"
sock.sendto(message, server_address)
message, (ip, port) = sock.recvfrom(1024)
print(message)