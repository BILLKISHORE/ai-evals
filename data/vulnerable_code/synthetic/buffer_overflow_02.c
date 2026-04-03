#include <stdio.h>
#include <string.h>

void greet_user(const char *name) {
    char greeting[32];
    /* BUG: strcpy has no bounds checking, name can overflow greeting */
    strcpy(greeting, "Hello, ");
    strcat(greeting, name);  /* BUG: strcat can overflow if name > 24 chars */
    printf("%s\n", greeting);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <name>\n", argv[0]);
        return 1;
    }
    greet_user(argv[1]);
    return 0;
}
