/*
 * This program does a basic mathematical kernel calculating R^2 for a point
 * to an array of points. It does the loop twice - once without vectorisation
 * and once with OpenMP SIMD instructions to compare times.
 *
 * Compile it with: 
 *   g++ -O1 -fopenmp -fopt-info-vec vector_demo.cpp -o vector_demo
 *
 * Dr Owain Kenway, UCL
 */

#include <iostream>
#include <cstdlib>
#include <cmath>
#include <limits>
#include <random>
#include <chrono>

using namespace std;
using namespace std::chrono;

int main(int argc, char **argv) {
	int i, j, repeat = 100000, num_elements = 100000;
	double x, y, z;

	uint32_t seed;
	random_device dev;
	mt19937 r(dev());
	uniform_real_distribution<double> dist(0.0,10.0); // 10x10x10 unit cell

	if (argc > 1) {
		num_elements = atoi(argv[1]);
	}

	cout << "Intialising X,Y,Z,R arrays with " << num_elements << " elements." << endl;

	if (argc > 2) {
		seed = atoi(argv[2]);
		r.seed(seed);
		cout << "  A fixed seed of " << seed << "." << endl;
	}

	double X[num_elements];
	double Y[num_elements];
	double Z[num_elements];
	double R[num_elements];

	x = dist(r);
	y = dist(r);
	z = dist(r);

	for (i = 0; i < num_elements; i++) {
		X[i] = dist(r);
		Y[i] = dist(r);
		Z[i] = dist(r);
		R[i] = 0.0d;
	}

	cout << "Running radius kernel " << repeat << " times."  << endl;

	auto start = high_resolution_clock::now();

	for (j = 0; j < repeat; j++) {
		for (i = 0; i < num_elements; i++) {
			R[i] = ((x - X[i])*(x - X[i])) 
			     + ((y - Y[i])*(y - Y[i]))
        	             + ((z - Z[i])*(z - Z[i]));
		}
	}

	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

	cout << "This took " << duration.count() << " μs." << endl;
	cout << "Running vectorized radius kernel " << repeat << " times."  << endl;

	start = high_resolution_clock::now();

	for (j = 0; j < repeat; j++) {
		#pragma omp simd
		for (i = 0; i < num_elements; i++) {
			R[i] = ((x - X[i])*(x - X[i])) 
			     + ((y - Y[i])*(y - Y[i]))
        	             + ((z - Z[i])*(z - Z[i]));
		}
	}

	stop = high_resolution_clock::now();
	duration = duration_cast<microseconds>(stop - start);

	cout << "This took " << duration.count() << " μs." << endl;

}
