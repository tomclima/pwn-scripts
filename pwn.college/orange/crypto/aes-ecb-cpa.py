from pwn import *

max_char = 256

chall = process("/challenge/run")

def stringify(challline):
    return challline.decode("utf-8")[:-1]

def send_plaintext(chall, char):
    line = 'a'
    while line[0] != '2':
        line = stringify(chall.readline())
    chall.sendline(b"1")
    chall.sendline(char)
    
    line = 'a'
    while 'Result' not in line:
        line = stringify(chall.readline())
    return line.split(': ', 2)[1]



def get_flagchar(chall, index):
    line = 'a'
    while line[0] != '2':
        line = stringify(chall.readline())
    chall.sendline(b"2")
    chall.sendline(str(index))
    chall.sendline(b"1")
    line = 'a'
    while ':' not in line:
        line = stringify(chall.readline())
    
    return line.split(': ', 1)[1]


i = 0
flagchar = ''
flag = ''
while i < 100 and flagchar != '}':
    flag_enc = get_flagchar(chall, i)
    for char  in range(32, max_char):
        candidate = chr(char)
        encrypt = send_plaintext(chall, candidate)
        if flag_enc == encrypt:
            flag += chr(char)
            print(flag)
            flagchar = candidate
            i += 1
            break 
