#!/usr/bin/env python3

from openmpi.mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"Hello from node {rank} of {size}")
