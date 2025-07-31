#include <stdio.h>
#include <string.h>
#include <unistd.h>

char* p(char* pp_buffer, const char* prompt) {
    char    padding2[8];
    char    buffer[4096];
    char    padding1[16];
    
    puts(prompt);
    read(0, buffer, 4096);
    *(strchr(buffer, '\n')) = 0;
    return strncpy(pp_buffer, buffer, 20);
}

char* pp(char* main_buffer) {
    char padding2[8];
    char buffer2[20];
    char buffer1[20];
    char padding1[32];

    p(buffer1, " - ");
    p(buffer2, " - ");
    strcpy(main_buffer, buffer1);
    
    main_buffer[strlen(main_buffer)] = *" ";
    main_buffer[strlen(main_buffer) + 1] = 0;
    main_buffer[strlen(main_buffer) + 2] = 0;
    main_buffer[strlen(main_buffer) + 3] = 0;

    strcat(main_buffer, buffer2);
}

int main(void) {
    char buffer[42];
    char padding[6];
   
    pp(buffer);
    puts(buffer);
    
    return 0;
}