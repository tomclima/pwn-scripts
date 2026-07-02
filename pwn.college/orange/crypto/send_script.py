#!/usr/bin/env python3
import pathlib
import subprocess

parent = pathlib.Path(__file__).resolve().parent

scriptname = "aes-cbc-poa-partial.py"
username = "hacker"
remote = "pwn.college"
filepath = pathlib.Path(f"/home/hacker/crypto/{scriptname}")
subprocess.run(f"scp {parent/scriptname} {username}@{remote}:{filepath}", shell=True)