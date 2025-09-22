#!/usr/bin/env bash

#SBATCH --job-name=Array
#SBATCH --partition=batch
#SBATCH --array=1-100
#SBATCH --time=00:10:00

echo "This is task ${SLURM_ARRAY_TASK_ID}"

./monte_carlo_π 1000000000
