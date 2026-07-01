from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

import time
import sys
from pwn import *



worker = process("/challenge/worker")

start_iv = b"\x00"*16
start_message = b"\x00"*16
worker.recvline()
# get one byte
values = []
for i in range(0, 256):

    new_iv = start_iv[:-1] + int.to_bytes(i,1, 'little')
    new_payload = b"TASK: " + (new_iv + start_message).hex().encode()
    print(new_payload)
    worker.sendline(new_payload)
    
    oracle = worker.recvline()
    if(oracle[:5] == b'Error'):
        print("test")

worker.interactive()

