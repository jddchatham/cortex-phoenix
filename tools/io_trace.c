#define _GNU_SOURCE
#include <dlfcn.h>
#include <inttypes.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

static ssize_t (*real_pread_fn)(int, void *, size_t, off_t);
static ssize_t (*real_read_fn)(int, void *, size_t);
static uint64_t pread_calls, pread_bytes, read_calls, read_bytes;
static void init_real(void) {
    if (!real_pread_fn) real_pread_fn = dlsym(RTLD_NEXT, "pread");
    if (!real_read_fn) real_read_fn = dlsym(RTLD_NEXT, "read");
}
ssize_t pread(int fd, void *buf, size_t n, off_t off) {
    init_real(); ssize_t r = real_pread_fn(fd, buf, n, off);
    if (r > 0) { ++pread_calls; pread_bytes += (uint64_t)r; }
    return r;
}
ssize_t pread64(int fd, void *buf, size_t n, off_t off) {
    return pread(fd, buf, n, off);
}
ssize_t read(int fd, void *buf, size_t n) {
    init_real(); ssize_t r = real_read_fn(fd, buf, n);
    if (r > 0) { ++read_calls; read_bytes += (uint64_t)r; }
    return r;
}
__attribute__((destructor)) static void report(void) {
    dprintf(2, "IO_TRACE pread_calls=%" PRIu64 " pread_bytes=%" PRIu64 " read_calls=%" PRIu64 " read_bytes=%" PRIu64 "\n", pread_calls, pread_bytes, read_calls, read_bytes);
}
