/*
 * This program estimates π by Monte Carlo methods.
 * It generates num_steps pounts in the (0.0 <= x <= 1.0, 0.0 <= y <= 1.0)
 * quadrant and then calulates the ratio of points inside a circle of radius
 * 1.0 to estimate π.
 *
 * Compile the program with:
 *   mpic++ -o monte_carlo_π -O3 monte_carlo_π.cpp

 * You can then run the program with
 *   mpirun -np [procs] ./monte_carlo_π [num_steps] [seed]
 *
 * Dr Owain Kenway, UCL
 */
#include <iostream>
#include <cstdlib>
#include <limits>
#include <climits>
#include <random>
#include <chrono>

#include <mpi.h>

using namespace std;
using namespace std::chrono;

int main(int argc, char **argv) {
	long i, in_count, local_in_count, per_proc, num_steps = 10000000;
	double x, y, p;
	uint32_t seed;
	random_device dev;
	uniform_real_distribution<double> dist(0.0,1.0);
	uniform_int_distribution<uint32_t> seed_dist(0,UINT_MAX);


	int this_proc, num_procs, remainder;

	MPI_Init(&argc,&argv);
	MPI_Comm_size(MPI_COMM_WORLD,&num_procs);
 	MPI_Comm_rank(MPI_COMM_WORLD,&this_proc);

	// Shuffle the seed by rank
	mt19937 r(dev());


	cout.precision(numeric_limits<double>::digits10+2);

	if (argc > 1) {
		num_steps = atol(argv[1]);
	}

	if (this_proc == 0) {
		cout << "Estimating π using:" << endl << 
                	"  " << num_steps << " Monte Carlo steps." << endl <<
                        "  " << num_procs << " MPI processes." << endl;
	}

	if (argc > 2) {
		seed = atoi(argv[2]);
		r.seed(seed);
		if (this_proc == 0) {
			cout << "  A fixed seed of " << seed << "." << endl;
		}
	}

	uint32_t seeds[num_procs];

	if (this_proc == 0) {
		// Generate different seeds for each thread from initial seed.
		for (i=0; i<num_procs; i++) {
			seeds[i] = seed_dist(r);
		}
	}

	MPI_Bcast(seeds, num_procs, MPI_UINT32_T, 0, MPI_COMM_WORLD);
	r.seed(seeds[this_proc]);

	auto start = high_resolution_clock::now();

	MPI_Barrier(MPI_COMM_WORLD);

	per_proc = num_steps/num_procs;
	remainder = num_steps - (per_proc * num_procs);
	
	if (this_proc < remainder) {
		per_proc++;
	}

	local_in_count = 0;
	for (i=0;i<per_proc; i++) {
		x = dist(r);
		y = dist(r);
		if ((y * y + x * x) < 1.0) {
			local_in_count++;
		}
	}

	in_count = 0;

	MPI_Reduce(&local_in_count, &in_count, 1, MPI_LONG, MPI_SUM, 0, MPI_COMM_WORLD);

	p = 4.0 * ((double)in_count)/((double)num_steps);

	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

	if (this_proc == 0) {
		cout << "Estimated value of π is " << p << "." << endl;
		cout << "This took " << duration.count() << " μs." << endl;
	}

	MPI_Finalize();

}

