#!/usr/bin/env python3

import time
import sys
import random

random.seed()
manual_seed = False

num_steps = 1000*1000*10

if len(sys.argv) > 1:
  num_steps = int(sys.argv[1])

if len(sys.argv) > 2:
  random.seed(int(sys.argv[2]))
  manual_seed = True

print("Calculating PI with:\n  %d slices" % num_steps)
print("  1 process")

if manual_seed:
    print("  Manual seed %d" % int(sys.argv[2]))
    random.seed(seed)

total_sum = 0
step = 1.0 / num_steps

start = time.time()
 
for i in range(0, num_steps):
  x = random.random()
  y = random.random()
  if ((x*x) + (y*y)) < 1.0:
    total_sum += 1

pi = 4.0 * total_sum / num_steps
stop = time.time()

print("Obtained value of PI: %.32g\n"
    "Time taken: %g seconds"
    % (pi, stop - start) )




