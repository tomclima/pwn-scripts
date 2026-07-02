from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

import time
import sys
from pwn import *


# SYSTEM SETUP
worker = process("/challenge/worker")


# dispatcher = process("/challenge/dispatcher", ["pw"])
# pw_data = dispatcher.recvline()[6:-1].decode()

original_text = b"TASK: ba8a0bba91366a4cf03b6bc56c81e0d7410b50595ac2f3dc95a63c1f37a0497f"
pw_data =original_text[6:].decode()
hex_data = bytes.fromhex(pw_data)

print(hex_data)
orignal_iv = hex_data[:16]
start_message = hex_data[16:]
print(start_message)
# FUNCTION DEFINITION

def get_payload(iv : bytes) -> bytes: 
    return b"TASK: " + (iv + start_message).hex().encode()


def attack_last_nth_byte(n : int, iv_suffix=b""):
    for i in range(0, 256):
        pad_candidate =  int.to_bytes(i,1)

        start_iv = b"\x00"*((16 - (n-1))) 
        new_iv = start_iv[:-1] + pad_candidate + iv_suffix

        
        new_payload = get_payload(new_iv)
        worker.sendline(new_payload)
        
        oracle = worker.recvline()
        

        if b"Unknown" in oracle:
            if n == 16:
                new_iv = pad_candidate + iv_suffix
            else:
                new_iv = start_iv[:-2] + b"\x01" + pad_candidate + iv_suffix
            new_payload = get_payload(new_iv)
            

            worker.sendline(new_payload)
            oracle = worker.recvline()

            print(int.to_bytes(i) + b" " + oracle)
            if b"Unknown" in oracle:
                
            
                return pad_candidate

        



print(worker.recvline())

zeroing_bytes = []
for i in range(1, 17):
    
    worker.info(b"DEFINING BYTE: " + str(16-i).encode())
    
    pad_byte = int.to_bytes(i, 1)

    suffix = b""
    for byte in reversed(zeroing_bytes):
        suffix += xor(byte, pad_byte)

    worker.info("SUFFIX IV-STRING: "+suffix.hex())

    attacked_byte = attack_last_nth_byte(i, suffix)
    print(attacked_byte)

    zeroing_bytes.append(xor(attacked_byte, pad_byte))
    print(zeroing_bytes)
    
zeroing_iv = b"".join(reversed(zeroing_bytes))
print(xor(zeroing_iv, orignal_iv))


