/*
 * This program estimates π by Monte Carlo methods.
 * It generates num_steps pounts in the (0.0 <= x <= 1.0, 0.0 <= y <= 1.0)
 * quadrant and then calulates the ratio of points inside a circle of radius
 * 1.0 to estimate π.
 *
 * Compile the program with:
 *   g++ -o monte_carlo_π -O3 monte_carlo_π.cpp

 * You can then run the program with
 *   ./monte_carlo_π [num_steps] [seed]
 *
 * You can control the number of threads by setting NUM_THREADS.
 *
 * Dr Owain Kenway, UCL
 */
#include <iostream>
#include <cstdlib>
#include <limits>
#include <climits>
#include <random>
#include <chrono>

#include <thread>

using namespace std;
using namespace std::chrono;

// Struct to communicate with each thread.
typedef struct chunk {
        long num_samples;
        int num_threads;
        int thread_num;
        long value;
	uint32_t seed;
} chunk;

// This is the actual function that executes in the thread.
void* worker(void *arg) {
	chunk *mydata = (chunk *)arg;
	uniform_real_distribution<double> dist(0.0,1.0);
        long num_samples = mydata->num_samples;
        int num_threads = mydata->num_threads;
        int thread_num = mydata->thread_num;
	uint32_t seed = mydata->seed;
	mt19937 r(seed);

	double x, y;
	long i;

	long local_in_count = 0;
	for (i=0;i<num_samples; i++) {
		x = dist(r);
		y = dist(r);
		if ((y * y + x * x) < 1.0) {
			local_in_count++;
		}
	}

        mydata->value=local_in_count;
        pthread_exit(NULL);
}

int main(int argc, char **argv) {
	long i, in_count, per_thread, num_steps = 10000000;
	double x, y, p;
	uint32_t seed;
	random_device dev;
	uniform_int_distribution<uint32_t> seed_dist(0,UINT_MAX);


	int num_threads, remainder;
	num_threads = 1;

	mt19937 r(dev());

        const char* NUM_THREADS = getenv("NUM_THREADS");

        if (NUM_THREADS!=NULL) {
                num_threads = atoi(NUM_THREADS);
        }

	cout.precision(numeric_limits<double>::digits10+2);

	if (argc > 1) {
		num_steps = atol(argv[1]);
	}

	cout << "Estimating π using:" << endl << 
               	"  " << num_steps << " Monte Carlo steps." << endl <<
                "  " << num_threads << " thread(s)." << endl;


	if (argc > 2) {
		seed = atoi(argv[2]);
		r.seed(seed);
		cout << "  A fixed seed of " << seed << "." << endl;
	}

	uint32_t seeds[num_threads];

	// Generate different seeds for each thread from initial seed.
	for (i=0; i<num_threads; i++) {
		seeds[i] = seed_dist(r);
	}

	auto start = high_resolution_clock::now();

	per_thread = num_steps/num_threads;
	remainder = num_steps - (per_thread * num_threads);
	
        pthread_t threads[num_threads]; 
        chunk chunks[num_threads];

	// Loop over the threads, creating each thread.
        for (i = 0; i < num_threads; i++) {
		per_thread = num_steps/num_threads;
		if (i < remainder) {
			per_thread++;
		}
                chunks[i].num_samples = per_thread;
                chunks[i].num_threads = num_threads;
		chunks[i].seed = seeds[i];
                chunks[i].thread_num = i;
                pthread_create(&threads[i], NULL, worker, (void *)&chunks[i]);
        } 
	
	in_count = 0;

	// Join each thread in turn.
        for (i = 0; i < num_threads; i++) {
                pthread_join(threads[i], NULL);
                in_count += chunks[i].value;
        } 


	p = 4.0 * ((double)in_count)/((double)num_steps);

	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

	cout << "Estimated value of π is " << p << "." << endl;
	cout << "This took " << duration.count() << " μs." << endl;

}

