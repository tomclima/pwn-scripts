from pwn import *
import sys

a = sys.stdout.__class__.__mro__
print(a)

chall = remote("challs1.pyjail.club", 19992)
b = "a"
line = "flag".__class__.__mro__[1].__subclasses__()
print(len(line))
IObase = line[129]
a = line[0](b, a)
print(a)


chall.interactive()


