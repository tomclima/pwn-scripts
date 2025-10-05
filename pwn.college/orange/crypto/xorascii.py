from Crypto.Util.strxor import strxor
from pwn import *

chall = process("/challenge/run")

for i in range(9):
    line = 'aaa'
    encrypt = ''
    key = ''
    while line[2] != "E":
        line = chall.readline().decode()[:-1]
        if line[2] == "E":
            print(line)
            encrypt = line.split(": ", 1)[1]
            print(encrypt)
        
    while line[2] != "X":
        line = chall.readline().decode()[:-1]
        if line[2] == "X":
            print(line)
            key = line.split(": ", 1)[1]
            print(key)
            
    ans = strxor(bytes(encrypt, "utf-8"), bytes(key, "utf-8")).decode("utf-8")
    chall.sendline(ans)

print(chall.readline())
print(chall.readline())

print(chall.readline())
