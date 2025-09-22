import subprocess
import time
command = ["nc", "10.0.0.2", "31337"]
procs = [subprocess.Popen(command) for i in range(0, 10000000)]
time.sleep(10)
for proc in procs:
    proc.kill()
    proc.wait()

