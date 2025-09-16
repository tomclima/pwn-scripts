import subprocess

file = "version" + "python" + ".cimg"

subprocess.run(f"touch /home/hacker/reverse-engineer/payloads/{file}")
with open("~/reverse-engineering/payloads/filename", "wb") as payload:
    payload.write(b",<mgE")
    a = 134
    payload.write(a.to_bytes(2, "little"))