#!/bin/bash

#SBATCH --job-name=struc_6wx4
#SBATCH --time=00:05:00
#SBATCH --mem=1gb
#SBATCH --ntasks=1
#SBATCH --output=struc_6wx4.%j.log
#SBATCH --mail-type=BEGIN,END,FAIL              
#SBATCH --mail-user=igors.dubanevics@york.ac.uk           
#SBATCH --account=phys-covid19-2020

module load chem/Amber/16-intel-2018b-AmberTools-17-patchlevel-10-15

echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo

time ./src/structure/download_pdb.sh 
time ./src/structure/prepare_pdb.sh
time tleap -f src/structure/tleap.in

echo
echo Job completed at `date`
