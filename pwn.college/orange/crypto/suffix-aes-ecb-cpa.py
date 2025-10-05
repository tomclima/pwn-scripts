from pwn import *

max_char = 128

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



def get_flagbytes(chall, length):
    line = 'a'
    while line[0] != '2':
        line = stringify(chall.readline())
    chall.sendline(b"2")
    chall.sendline(str(length))
    line = 'a'
    while ':' not in line:
        line = stringify(chall.readline())
    
    return line.split(': ', 1)[1]


i = 1
flagchar = ''
flag_known = ''

while i < 100:
    flag_enc = get_flagbytes(chall, i)
    for char  in range(32, max_char):
        candidate = chr(char)
        encrypt = send_plaintext(chall, candidate+flag_known)
        if flag_enc == encrypt:
            flag_known = chr(char)+flag_known
            print(flag_known)
            flagchar = candidate
            i += 1
            break 
