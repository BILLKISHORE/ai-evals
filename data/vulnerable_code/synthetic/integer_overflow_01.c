#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

struct image_header {
    uint16_t width;
    uint16_t height;
    uint8_t channels;
};

void *allocate_image(struct image_header *hdr) {
    /* BUG: width * height * channels can overflow uint32_t
       e.g., width=65535, height=65535, channels=4 = 17,179,607,040
       which wraps around to a small number, causing undersized allocation */
    uint32_t size = hdr->width * hdr->height * hdr->channels;
    void *buffer = malloc(size);
    if (!buffer) return NULL;

    /* This memset writes the actual intended amount of data
       into the undersized buffer, causing heap overflow */
    memset(buffer, 0, (size_t)hdr->width * hdr->height * hdr->channels);
    return buffer;
}
