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
 * Dr Owain Kenway, UCL
 */
#include <iostream>
#include <cstdlib>
#include <limits>
#include <random>
#include <chrono>

using namespace std;
using namespace std::chrono;

int main(int argc, char **argv) {
	long i, in_count, num_steps = 10000000;
	double x, y, p;
	uint32_t seed;
	random_device dev;
	mt19937 r(dev());
	uniform_real_distribution<double> dist(0.0,1.0);
	

	cout.precision(numeric_limits<double>::digits10+2);

	if (argc > 1) {
		num_steps = atol(argv[1]);
	}

	cout << "Estimating π using:" << endl << 
                "  " << num_steps << " Monte Carlo steps." << endl;

	if (argc > 2) {
		seed = atoi(argv[2]);
		r.seed(seed);
		cout << "  A fixed seed of " << seed << "." << endl;
	}

	auto start = high_resolution_clock::now();

	in_count = 0;

	for (i=0;i<num_steps; i++) {
		x = dist(r);
		y = dist(r);
		if ((y * y + x * x) < 1.0) {
			in_count++;
		}
	}

	p = 4.0 * ((double)in_count)/((double)num_steps);

	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

	cout << "Estimated value of π is " << p << "." << endl;
	cout << "This took " << duration.count() << " μs." << endl;
}

