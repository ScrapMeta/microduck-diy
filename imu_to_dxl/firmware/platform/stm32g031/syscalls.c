/* Newlib stubs for bare-metal */
#include <sys/stat.h>
#include <errno.h>

extern char _end;

void *_sbrk(int incr)
{
    static char *heap;
    char *prev;
    if (!heap) {
        heap = &_end;
    }
    prev = heap;
    heap += incr;
    return prev;
}

int _write(int fd, char *ptr, int len)
{
    (void)fd;
    (void)ptr;
    return len;
}

int _close(int fd)
{
    (void)fd;
    return -1;
}
int _fstat(int fd, struct stat *st)
{
    (void)fd;
    st->st_mode = S_IFCHR;
    return 0;
}
int _isatty(int fd)
{
    (void)fd;
    return 1;
}
int _lseek(int fd, int ptr, int dir)
{
    (void)fd;
    (void)ptr;
    (void)dir;
    return 0;
}
int _read(int fd, char *ptr, int len)
{
    (void)fd;
    (void)ptr;
    (void)len;
    return 0;
}
void _exit(int code)
{
    (void)code;
    for (;;) {
    }
}
int _kill(int pid, int sig)
{
    (void)pid;
    (void)sig;
    errno = EINVAL;
    return -1;
}
int _getpid(void)
{
    return 1;
}
