/*
 * This program is a simple pthreads "hello, world" program.
 *
 * Compile the program with:
 *   g++ -o hello -O3 hello.cpp

 * You can then run the program with
 *   ./hello
 *
 * You can control the number of threads by setting NUM_THREADS.
 *
 * Dr Owain Kenway, UCL
 */

#include <iostream>
#include <cstdlib>

#include <thread>

using namespace std;

// Struct to communicate with each thread.
typedef struct thread_data {
    int num_threads;
    int thread_num;
} thread_data;

void* worker(void *arg) {
    thread_data *mydata = (thread_data *)arg;
    cout << "Hello from thread " << mydata->thread_num << " of " << mydata->num_threads << "." << endl;
    pthread_exit(NULL);
}

int main(int argc, char **argv) {
    int num_threads = 1;
    int i;

    const char* NUM_THREADS = getenv("NUM_THREADS");

    if (NUM_THREADS!=NULL) {
        num_threads = atoi(NUM_THREADS);
    }

    thread_data td[num_threads];
    pthread_t threads[num_threads]; 

    for (i=0; i<num_threads;i++) {
        td[i].num_threads=num_threads;
        td[i].thread_num=i;
        pthread_create(&threads[i], NULL, worker, (void *)&td[i]);
    }

    for (i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    } 
}