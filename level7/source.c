#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct s_data {
    int             data;
    struct s_data*  next;
} t_data;

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

    FILE *f = fopen("output.txt", "w");
    fgets((char *)0x8049960, 0x44, f);
    puts("Done");

    return 0;
}