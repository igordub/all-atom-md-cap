#!/bin/bash
# Production MD
#SBATCH --job-name=prod_6wx4
#SBATCH --time=12:00:00
#SBATCH --mem=32gb
#SBATCH --ntasks=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --output=prod_%j.log
#SBATCH --mail-type=BEGIN,END,FAIL              
#SBATCH --mail-user=username@york.ac.uk           
#SBATCH --account=account_name

module load chem/Amber/16-foss-2018a-AmberTools-17-CUDA

# Run Full MD Simulation for 5 ns

echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo

./src/production/run_5.2-10.2ns.sh

echo
echo Job completed at `date`