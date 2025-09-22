#!/usr/bin/env bash

#SBATCH --job-name=mpitest
#SBATCH --partition=batch
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=1

srun ./monte_carlo_π 1000000000

