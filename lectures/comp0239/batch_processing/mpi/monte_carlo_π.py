#!/usr/bin/env python3

import time
import sys
import random
from openmpi.mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
random.seed()
manual_seed = False

num_steps = 1000*1000*10

if len(sys.argv) > 1:
  num_steps = int(sys.argv[1])

if len(sys.argv) > 2:
  random.seed(int(sys.argv[2]))
  manual_seed = True

seeds = []

if (rank == 0):
  print("Calculating PI with:\n  %d slices" % num_steps)
  print("  %d process(s)" % size)
  if manual_seed:
    print("  Manual seed %d" % int(sys.argv[2]))

  for a in range(size):
    seeds.append(random.randint(-sys.maxsize, sys.maxsize))

seeds = comm.bcast(seeds, root=0)

seed = seeds[rank]
random.seed(seed)

total_sum = 0
step = 1.0 / num_steps

if (rank == 0):
  start = time.time()

chunkstart = int(rank * num_steps / size)
chunkend = int((rank + 1) * num_steps / size) 

for i in range(chunkstart, chunkend):
  x = random.random()
  y = random.random()
  if ((x*x) + (y*y)) < 1.0:
    total_sum += 1

# This puts a list on rank 0 of the values gathered.
total_sum = comm.gather(total_sum, root=0)

if (rank == 0):
  total_sum = sum(total_sum) 
  pi = 4.0 * total_sum / num_steps
  stop = time.time()

  print("Obtained value of PI: %.32g\n"
        "Time taken: %g seconds"
        % (pi, stop - start) )




