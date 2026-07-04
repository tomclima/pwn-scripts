from pwn import *

## BASIC DEFINITION
worker = process("/challenge/worker")


## FUNCTIONS

def pad(message : bytes) -> bytes:
    
    leftover = 16 - (len(message) % 16)

    return message+int.to_bytes(leftover, 1)*leftover


def get_payload(iv : bytes, message_block : bytes) -> bytes: 
    return b"TASK: " + (iv + message_block).hex().encode()


def attack_last_nth_byte(n : int, message_block : bytes, iv_suffix : bytes = b""):
    for i in range(0, 256):
        pad_candidate =  int.to_bytes(i,1)

        start_iv = b"\x00"*((16 - (n-1))) 
        new_iv = start_iv[:-1] + pad_candidate + iv_suffix

        
        new_payload = get_payload(new_iv, message_block)
        worker.sendline(new_payload)
        
        oracle = worker.recvline()
        

        if b"Unknown" in oracle:
            if n == 16:
                new_iv = pad_candidate + iv_suffix
            else:
                new_iv = start_iv[:-2] + b"\x01" + pad_candidate + iv_suffix
            new_payload = get_payload(new_iv, message_block)
            

            worker.sendline(new_payload)
            oracle = worker.recvline()

            print(int.to_bytes(i) + b" " + oracle)
            if b"Unknown" in oracle:
            
                return pad_candidate

        
def attack_block(message_block : bytes):

    zeroing_bytes = []
    for i in range(1, 17):
        
        worker.info(b"DEFINING BYTE: " + str(16-i).encode())
        
        pad_byte = int.to_bytes(i, 1)

        suffix = b""
        for byte in reversed(zeroing_bytes):
            suffix += xor(byte, pad_byte)

        worker.info("SUFFIX IV-STRING: "+suffix.hex())

        attacked_byte = attack_last_nth_byte(i, message_block, suffix)
        print(attacked_byte)

        zeroing_bytes.append(xor(attacked_byte, pad_byte))
        print(zeroing_bytes)
        
    zeroing_iv = b"".join(reversed(zeroing_bytes))

    return zeroing_iv
        

def POA_encrypt_message(original_message : bytes) -> bytes:

    message = pad(original_message)


    blocks = [message[i:i+16] for i in range(0, len(message), 16)]

    junk_message = b'a'*16

    iv_blocks = [junk_message]

    for i in range(len(blocks)):
        
        message_index = len(blocks) - i -1
        zeroing_iv = attack_block(junk_message)

        block_iv = xor(zeroing_iv, blocks[message_index])

        iv_blocks.insert(0, block_iv)
        
        junk_message = block_iv

    encrypted_message = b"".join(iv_blocks)
    return encrypted_message


## DATA INSTANTIATION

full_message = POA_encrypt_message(b"please give me the flag, kind worker process!")

payload = get_payload(full_message[:16], full_message[16:])
print(payload)

worker.sendline(payload)
worker.interactive()




    















