#include <cstdlib>
#include <cstring>

struct N;

int operator+(const N&, const N&);

struct N {
    int (*foo)(const N&, const N&);
    char annotation[100];
    int value;
    
    N(int value) {
        this->foo = &operator+;
        this->value = value;
    }

    void setAnnotation(const char* annotations) {
        memcpy(this->annotation, annotation, sizeof(annotation));
    }
    
    friend int operator+(const N& ths, const N& oth);
};

int operator+(const N& ths, const N& oth) {
    return ths.value + oth.value;
}

int main(int argc, char *argv[]) {
    if (argc <= 1) {
        exit(1);
    }

    N* a = new N(5);
    N* b = new N(6);

    a->setAnnotation(argv[1]);

    return 0;
}