#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

char* flag;

typedef struct s_data {
    int             data;
    struct s_data*  next;
} t_data;

void m() {
    printf("%s - %d", flag, (int)time(NULL));
}

int main(int argc, char *argv[]) {
    t_data *A = malloc(sizeof(t_data));
    t_data *B = malloc(sizeof(t_data));
    t_data *C = malloc(sizeof(t_data));
    t_data *D = malloc(sizeof(t_data));

    A->data = 1;
    A->next = B;
    C->data = 2;
    C->next = D;

    strcpy((char *)A->next, argv[1]);
    strcpy((char *)C->next, argv[2]);

    FILE *f = fopen("/home/user/level8/.pass", "r");
    fgets(flag, 68, f);
    puts("~~");

    return 0;
}