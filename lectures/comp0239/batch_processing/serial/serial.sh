#!/usr/bin/env bash

#SBATCH --job-name=Serial
#SBATCH --partition=batch

#SBATCH --time=00:10:00

./monte_carlo_π 1000000000
