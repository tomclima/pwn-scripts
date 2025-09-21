import sys
import subprocess
import codecs
if len(sys.argv) < 2:
    raise(Exception("Too few arguments"))


subprocess.run(["touch", sys.argv[1]])
magic = (codecs.decode(input("magic number: "), "unicode-escape")).encode("utf-8")
version = int(input("version number: "))
width = int(input("width: "))
height = int(input("height: "))
data = ("\n"+"a"*width*height).encode("utf-8")
with open(f"{sys.argv[1]}", "wb") as payload:
    payload.write(magic)
    payload.write(version.to_bytes(2, "little"))
    payload.write(width.to_bytes(1, "little"))
    payload.write(height.to_bytes(8, "little"))
    payload.write(data)


subprocess.run(["/challenge/cimg", sys.argv[1]])