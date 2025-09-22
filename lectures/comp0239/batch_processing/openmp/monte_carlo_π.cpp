/*
 * This program estimates π by Monte Carlo methods.
 * It generates num_steps pounts in the (0.0 <= x <= 1.0, 0.0 <= y <= 1.0)
 * quadrant and then calulates the ratio of points inside a circle of radius
 * 1.0 to estimate π.
 *
 * Compile the program with:
 *   g++ -o monte_carlo_π -O3 -fopenmp monte_carlo_π.cpp

 * You can then run the program with
 *   ./monte_carlo_π [num_steps] [seed]
 *
 * Dr Owain Kenway, UCL
 */
#include <iostream>
#include <cstdlib>
#include <limits>
#include <climits>
#include <random>
#include <chrono>

#include <omp.h>

using namespace std;
using namespace std::chrono;

int main(int argc, char **argv) {
	long i, in_count, num_steps = 10000000;
	double x, y, p;
	uint32_t seed;
	random_device dev;
	mt19937 r(dev());
	uniform_int_distribution<uint32_t> seed_dist(0,UINT_MAX);

	int num_threads = omp_get_max_threads();

	cout.precision(numeric_limits<double>::digits10+2);

	if (argc > 1) {
		num_steps = atol(argv[1]);
	}

	cout << "Estimating π using:" << endl << 
                "  " << num_steps << " Monte Carlo steps." << endl <<
                "  " << num_threads << " OpenMP threads." << endl;

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

	in_count = 0;

#pragma omp parallel private(x,y) reduction(+:in_count)
	{  // This block is all in parallel.
		mt19937 r_t(seeds[omp_get_thread_num()]);
		uniform_real_distribution<double> dist(0.0,1.0);
		
#pragma omp for 
		for (i=0; i<num_steps; i++) {
			x = dist(r_t);
			y = dist(r_t);
			if ((y * y + x * x) < 1.0) {
				in_count++;
			}
		}
	}
	p = 4.0 * ((double)in_count)/((double)num_steps);

	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

	cout << "Estimated value of π is " << p << "." << endl;
	cout << "This took " << duration.count() << " μs." << endl;
}

