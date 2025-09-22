/*
 * This program is a simple pthreads "hello, world" program.
 *
 * Compile the program with:
 *   mpic++ -o hello hello.cpp

 * You can then run the program with
 *   mpirun -np 2 ./hello
 *
 * Dr Owain Kenway, UCL
 */

#include <iostream>
#include <cstdlib>

#include <mpi.h>

using namespace std;

int main(int argc, char **argv) {
    int this_proc, num_procs;

	MPI_Init(&argc,&argv);
	MPI_Comm_size(MPI_COMM_WORLD,&num_procs);
 	MPI_Comm_rank(MPI_COMM_WORLD,&this_proc);

    cout << "Hello world, from process " << this_proc << " of " << num_procs << endl;

    MPI_Finalize();
}