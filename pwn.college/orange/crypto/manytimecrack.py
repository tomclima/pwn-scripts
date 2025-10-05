from pwn import *
from Crypto.Util.strxor import strxor

chall = process("/challenge/run")

flag = chall.readline().decode("utf-8")[:-1].split(": ", 1)[1]
print(flag)

i = 0
flagchars = []
while i < len(flag):
    flagchars.append(flag[i:i+2])
    i += 2

print(flagchars)
cypherchars = []
for char in flagchars:
    chall.sendline(char)

    cypherchar  = chall.readline().decode("utf-8")[:-1].split(": ", 2)[2]

    cypherchars.append(cypherchar)


keychars = []
flag = []

print(cypherchars)
for i in range(len(flagchars)):
    print(flagchars[i] + " " + cypherchars[i])
    keychars.append((strxor(bytes.fromhex(flagchars[i]), bytes.fromhex(cypherchars[i]))))
    flag.append(strxor(bytes.fromhex(flagchars[i]), keychars[i]).decode())
    print(flag)

print(flag)
print(keychars)
