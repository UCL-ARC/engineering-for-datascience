#!/usr/bin/env bash

#SBATCH --job-name=test_openmp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:10:00

export NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

./monte_carlo_π 1000000000

