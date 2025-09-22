#!/usr/bin/env python3

import time
import sys
import random
from multiprocessing import Process, Queue, cpu_count
import os

def pi_chunk(q, seed, num_steps):
  random.seed(seed)
  total_sum = 0
  for i in range(0, num_steps):
    x = random.random()
    y = random.random()
    if ((x*x) + (y*y)) < 1.0:
      total_sum += 1
  q.put(total_sum)

if __name__ == "__main__":
  q = Queue()
  processes = []
  num_procs = 1

  try: 
    num_procs = int(os.environ["NUM_PROCS"])
  except:
    num_procs = cpu_count()

  random.seed()
  manual_seed = False

  num_steps = 1000*1000*10

  if len(sys.argv) > 1:
    num_steps = int(sys.argv[1])

  if len(sys.argv) > 2:
    random.seed(int(sys.argv[2]))
    manual_seed = True

  print("Calculating PI with:\n  %d slices" % num_steps)
  print(f"  {num_procs} process")

  if manual_seed:
      print("  Manual seed %d" % int(sys.argv[2]))

  seeds = []
  for a in range(num_procs):
    seeds.append(random.randint(-sys.maxsize, sys.maxsize))

  total_sum = 0
  step = 1.0 / num_steps

  start = time.time()
  
  chunks = []
  for a in range(num_procs):
    chunks.append(int(num_steps/num_procs))
    if a < num_steps%num_procs:
      chunks[a] += 1

    processes.append(Process(target=pi_chunk, args=(q, seeds[a], chunks[a] )))
    processes[a].start()

  #print(chunks) # Uncomment to print out decomposition

  for a in range(num_procs):
    total_sum += q.get()

  for a in range(num_procs):
    processes[a].join()
  

  pi = 4.0 * total_sum / num_steps
  stop = time.time()

  print("Obtained value of PI: %.32g\n"
      "Time taken: %g seconds"
      % (pi, stop - start) )




