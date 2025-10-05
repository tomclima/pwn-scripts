import base64
from Crypto.Cipher import AES

key_b64 = "2zdYBNUy1wBHMZIo7n6KuqO8Vv8biVgvjxqD/+DSnhQ="
input_file = "dns_queries.txt"
output_file = "flag.docx"


# 1. Read all queries
with open(input_file, "r") as f:
    lines = f.read().splitlines()

    # 2. Remove separators and domain suffixes
    chunks = []
    for line in lines:
        clean_line = line[:-11]
        chunks.append(clean_line)
        print(line)
        print(clean_line)

# 3. Concatenate all chunks
full_base64 = ''.join(chunks)

# 4. Decode Base64 to get IV + ciphertext
full_bytes = base64.b64decode(full_base64)
iv = full_bytes[:16]
ciphertext = full_bytes[16:]


# 5. AES decrypt
key = base64.b64decode(key_b64)
aes = AES.new(key, AES.MODE_CBC, iv)
plaintext = aes.decrypt(ciphertext)

# 6. Remove trailing zeros (original zero padding)
plaintext = plaintext.rstrip(b'\x00')

# 7. Write output
with open(output_file, "wb") as f:
    f.write(plaintext)

print(f"[+] File reconstructed: {output_file}")
