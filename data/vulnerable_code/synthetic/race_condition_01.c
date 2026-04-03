#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

int safe_write(const char *filepath, const char *data) {
    struct stat st;

    /* BUG: TOCTOU race condition between stat() check and fopen() */
    /* An attacker can replace the file with a symlink between these calls */
    if (stat(filepath, &st) == 0) {
        if (st.st_mode & S_IWOTH) {
            printf("Error: file is world-writable, refusing to write\n");
            return -1;
        }
    }

    /* Race window: file can be replaced with symlink here */
    FILE *f = fopen(filepath, "w");
    if (!f) return -1;
    fprintf(f, "%s", data);
    fclose(f);
    return 0;
}
