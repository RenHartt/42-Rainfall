#include <cstdlib>
#include <cstring>

struct N {
    char* annotations;
    int (*foo)(int, int);
    int value;
    
    N(int value) {
        this->value = value;
        this->foo = [](int a, int b) -> int { return a + b; };
    }
    void setAnnotations(const char* annotations) {
        memcpy(this->annotations, annotations, sizeof(annotations));
    }

    int operator+(const N& other) const {
        return this->foo(this->value, other.value);
    }
};

int main(int argc, char *argv[]) {
    if (argc <= 1) {
        exit(1);
    }

    N* a = new N(5);
    N* b = new N(6);

    a->setAnnotations(argv[1]);

    return 0;
}