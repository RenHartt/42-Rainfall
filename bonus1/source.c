#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define CHECK   1464814662

int main(int argc, char **argv)
{
    unsigned int    size = atoi(argv[1]);
    char            buffer[36];
    char            padding[24];

    if (size > 9)
        return (1);

    memcpy(argv[2], buffer, size * 4);
    if (size == CHECK)
        execl("/bin/sh", NULL);
    
    return (0);
}