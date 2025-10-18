from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from pwn import process

chall = process("/challenge/worker")
data = ""
block_size = 16
iv, ciphertext = bytes.fromhex(data)[:16], bytes.fromhex(data)[16:]

i = 1
while i <= 16:
    found = False
    
    for j in range(256):
        if chall.sendline(strxor(bytes(j), bytes(ciphertext[16 -i]))) != b"Error":
            for k in range
            

    
    

    





