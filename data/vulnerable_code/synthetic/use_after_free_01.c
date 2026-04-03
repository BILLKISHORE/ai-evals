#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct session {
    char name[32];
    int authenticated;
    void (*handler)(struct session *);
};

void default_handler(struct session *s) {
    printf("Handling session for %s\n", s->name);
}

struct session *create_session(const char *name) {
    struct session *s = malloc(sizeof(struct session));
    if (strlen(name) > 31) {
        free(s);  /* BUG: frees s but does not return */
    }
    strncpy(s->name, name, 31);  /* BUG: use after free if name > 31 */
    s->name[31] = '\0';
    s->authenticated = 0;
    s->handler = default_handler;
    return s;  /* BUG: returns freed pointer */
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    struct session *s = create_session(argv[1]);
    s->handler(s);
    free(s);
    return 0;
}
