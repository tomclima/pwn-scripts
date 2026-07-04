from pwn import *


## BASIC DEFINITION
worker = process("/challenge/worker")


## FUNCTIONS

def get_message_block(message : bytes, block_index: int) -> bytes:
    
    blocks = [message[i:i+16] for i in range(0, len(message), 16)]
    
    if block_index >= len(blocks):
        worker.error(f"Block index {block_index} out of message range")
    
    return blocks[block_index]


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



## DATA INSTANTIATION

dispatcher = process(["/challenge/dispatcher", "flag"])
original_text = dispatcher.recvline()[:-1]
print(original_text)
input()

#original_text = b"TASK: 594f186047a33eb6c4e5a385925980d463c2589e846e16f0fa7be77f318b76791cf32d3899ff6aade19baa32f97bdbdb6660b64c5ba04e8c008eadf2b76fecfb544010f488c517b7d50d82c48650333e"

pw_data =original_text[6:].decode()
hex_data = bytes.fromhex(pw_data)
message_body = hex_data




piecewise_flag = []
for i in range(0, len(message_body)//16 -1):
    
    print(len(message_body)/16)

    
    iv_block = get_message_block(message_body, i)
    print(iv_block)

    message_block = get_message_block(message_body, i+1)
    print(message_block)

    attack_block(message_block)
        
    zeroing_iv = attack_block(message_block)
    flag_piece = xor(zeroing_iv, iv_block)
    print(flag_piece)
    piecewise_flag.append(flag_piece)

print(b"".join(piecewise_flag))






