# LEVEL 0

In x86, arguments are passed to functions through the stack.
So, accounting for the old `ebp`, pushed by the prolog, and the return address, we can infer:   
- argc is at `[ebp + 0x8]`
- argv is at `[ebp + 0xc]`
   
$ objdump -d -Mintel level0

```asm
 8048ec9:       8b 45 0c                mov    eax,DWORD PTR [ebp+0xc]
 8048ecc:       83 c0 04                add    eax,0x4
 8048ecf:       8b 00                   mov    eax,DWORD PTR [eax]
```
Those lines are taking the argv pointer, adding 4 and then dereferencing it.   
4 bytes being the pointer size on the machine we're working on, this is argv + 1.
By dereferencing it, we obtain a pointer to the first argument of the program.   
```asm
 8048ed1:       89 04 24                mov    DWORD PTR [esp],eax
 8048ed4:       e8 37 08 00 00          call   8049710 <atoi>
 8048ed9:       3d a7 01 00 00          cmp    eax,0x1a7
 8048ede:       75 78                   jne    8048f58 <main+0x98>
```
This part is then setting the top stack value to our argv[1] pointer, and calls atoi on it.   
It then compares the result in `eax` to the value 423 and exits of the program if its not.   

Thus, by sending 423 to this program, it spawns a shell allowing us to do:   
$ cat /home/user/level1/.pass
