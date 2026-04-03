#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 64

struct request {
    char *data;
    size_t length;
};

void process_request(struct request *req) {
    char *buf = malloc(BUFFER_SIZE);
    memcpy(buf, req->data, req->length);  /* BUG: req->length can exceed BUFFER_SIZE */
    printf("Processed %zu bytes\n", req->length);
    free(buf);
}

int main(int argc, char **argv) {
    struct request req;
    req.data = argv[1];
    req.length = strlen(argv[1]);
    process_request(&req);
    return 0;
}
