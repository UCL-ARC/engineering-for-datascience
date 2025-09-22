#!/usr/bin/env python3

from openmpi.mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

next_proc = rank + 1
last_proc = rank - 1

if last_proc < 0:
  last_proc = size - 1

if next_proc >= size:
  next_proc = 0

print(f"I am process {rank} and I will send a message to {next_proc} and receive one from {last_proc}")

comm.isend(rank, dest=next_proc)
rmessage = comm.recv(source=last_proc)

print(f"This is process {rank} and I got {rmessage} from {last_proc}.")
