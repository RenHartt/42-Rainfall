#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'end'
password = open("../bonus3/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    p = s.process(["cat", "end"])

    def ssh_send(line):
        if type(line) == str:
            line = line.encode("utf-8")
        elif type(line) != bytes:
            print("[x] Wrong data format !")
            raise ValueError
        print(f"[x] Sending: {line!r}")
        p.sendline(line)

    def ssh_recv(timeout = 1.0) -> str:
        data = p.recv(timeout=timeout)
        text = data.decode(errors='ignore')
        print(f"[x] Received: {text!r}")
        return text

    def wait_for_shell():
        while True:
            output = ssh_recv()
            if output == "$ ":
                break
   
    data = ssh_recv()

    print(f"\n{data}")

    s.close()

