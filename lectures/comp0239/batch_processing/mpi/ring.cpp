/*
 * This program passes the rank to the process rank + 1 in a ring.

 *   mpic++ -o ring ring.cpp

 * You can then run the program with
 *   mpirun -np [procs] ring
 *
 * Dr Owain Kenway, UCL
 */
#include <iostream>
#include <cstdlib>

#include <mpi.h>

using namespace std;

int main(int argc, char **argv) {
	int last_proc, next_proc, this_proc, num_procs, remainder;

	MPI_Init(&argc,&argv);
	MPI_Comm_size(MPI_COMM_WORLD,&num_procs);
 	MPI_Comm_rank(MPI_COMM_WORLD,&this_proc);

	last_proc = (this_proc - 1);
	next_proc = this_proc + 1;

	if (last_proc < 0) {
		last_proc = num_procs - 1;
	}

	if (next_proc >= num_procs) {
		next_proc = 0;
	}

	cout << "This is process " << this_proc << " and I will send a message to " 
		<< next_proc << " and receive one from " << last_proc << "." << endl;
	
 	
	int message = this_proc;
	int rmessage;
	MPI_Request request;
	MPI_Status status;

	MPI_Isend(&message, 1, MPI_INTEGER, next_proc, 0, MPI_COMM_WORLD, &request);

	MPI_Recv(&rmessage, 1, MPI_INTEGER, last_proc, 0, MPI_COMM_WORLD, &status);
	
	cout << "This is process " << this_proc << " and I got " << rmessage 
		<< " from process " << last_proc << "." << endl;


	MPI_Finalize();

}

