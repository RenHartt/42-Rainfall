# LEVEL 4

Like in the last level, the `main` function is only used to call another function called `n`.
This function have the same `fgets` call than the last one, taking 512 bytes of user input.
It is however sending the buffer to the `p` function, that will call `printf(buffer)`, allowing us the exact
same vulnerability exploit than before.
```asm
 8048488:	e8 b7 ff ff ff       	call   8048444 <p>
 804848d:	a1 10 98 04 08       	mov    eax,ds:0x8049810
 8048492:	3d 44 55 02 01       	cmp    eax,0x1025544
 8048497:	75 0c                	jne    80484a5 <n+0x4e>
 8048499:	c7 04 24 90 85 04 08 	mov    DWORD PTR [esp],0x8048590
 80484a0:	e8 bb fe ff ff       	call   8048360 <system@plt>
 80484a5:	c9                   	leave
 80484a6:	c3                   	ret
```
After the `p` call, a global variable is checked against the value `0x01025544`, and exits of the function if not
equal. We will use the same format tricks of `level3` (TODO : insert level3.md link here), using `%hhn` to write
the magic value `0x01025544` at the right address.   
```bash
level4@RainFall:~$ echo "%8x %8x %8x %8x %8x %8x %8x %8x %8x %8x %8x %8x %8x %8x %8x %8x %8x " | ./level4
b7ff26b0 bffffcb4 b7fd0ff4        0        0 bffffc78  804848d bffffa70
200 b7fd1ac0 b7ff37d0 20783825 20783825 20783825 20783825 20783825 20783825
```
As in the last level, we dump the stack using `%8x ` formats, searching for our buffer (We could also compute the
actual offset using the stack frames but its easier like this (: ). We see that there are 11 values to use in the
format string before va_arg actually takes our buffer as data. We will then have `%8x%8x%8x%8x%8x%8x%8x%8x%8x%8x%Nx`
where `N` will be the amount of characters missing to write our first byte. So, we do something like this with G as 
the global address: `"(G)    (G + 1)    (G + 2)    (G + 3)    "` for 32 bytes, then our format chain of
80 + N characters. This sums up to 112 (or 0x70). The spaces between the adresses are 4 byte long placeholders to let
us be able to dereference a value with another curstom `%Nx` before each byte write.
```

```
