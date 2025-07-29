/**
 * level0.c
 */

#define _GNU_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    if (atoi(argv[1]) == 0x1a7)
    {
        const char  *shell = "/bin/sh";
		const char	*null = NULL;
        const char  *dup = strdup(shell);

        int egid = getegid();
        int euid = geteuid();

        setresgid(egid, egid, egid);
        setresuid(euid, euid, euid);

        execv(shell, (char *const *)&dup);
    }
    else
        fwrite("No !\n", 1, 5, stdout);
    return (0);
}
