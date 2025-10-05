from pwn import *

chall = process("/challenge/run")

def getline(chall):
    return chall.readline()[:-1].decode("utf-8")



def find_padsize(chall):
    flag_original = prepend_to_flag(chall, 0)
    size = 0
    blocks = []
    while len(blocks) <= len(flag_original):
        blocks = to_blocks(prepend_to_flag(chall, size))
        size += 1
        
     
    return size - 1

def to_blocks(aes_cyphertext):
    blocks = []
    i = 0
    while i < len(aes_cyphertext):
        blocks.append(aes_cyphertext[i:i+32])
        i += 32    
    return blocks


    

def prepend_to_flag(chall, prefix_size):
    line = ''
    while line != "2. Prepend something to the flag.":
        line = getline(chall)
    chall.sendline(b"2")
    chall.sendline(("a"*prefix_size).encode("utf-8"))
    
    blocks = []
    line = ''
    while len(line) < len("Choice? Data? Result:") or line[:len("Choice? Data? Result:")] != "Choice? Data? Result:":
        line = getline(chall)

    prepended_flag = line.split(": ", 1)[1]
    
    return prepended_flag


def encrypt_data(chall, data):
    line = ''
    while line != "2. Prepend something to the flag.":
        line = getline(chall)
    chall.sendline(b"1")
    chall.sendline(data.encode("utf-8"))
    while len(line) < len("Choice? Data? Result:") or line[:len("Choice? Data? Result:")] != "Choice? Data? Result:":
        line = getline(chall)

    encrypted_data  = line.split(": ", 1)[1]   
    return encrypted_data


padsize = find_padsize(chall) 
flagsize = len(to_blocks(prepend_to_flag(chall, 0)))*16 - padsize
finished = False

print(prepend_to_flag(chall, 0))
initial = prepend_to_flag(chall, flagsize+padsize)
print(initial)
flag = ''
prefix = 16*"a"
prefix_size = flagsize + padsize
known_char = ''

for i in range(len(to_blocks(prepend_to_flag(chall, 0)))):
    blocknum = 3 
    if(known_char == "}"):
        break
    for j in range(1, 17):
        prefix_size -= 1
        byte_block = to_blocks(prepend_to_flag(chall, prefix_size))[blocknum]
        prefix = prefix+known_char
        prefix = prefix[-15:]
        print(prefix)
        for char in [chr(k) for k in range(33, 128)]:
            brute = encrypt_data(chall, (prefix+char)[-16:])
            if brute == byte_block:
                flag += char
                known_char = char
                print(flag)
                break
    
