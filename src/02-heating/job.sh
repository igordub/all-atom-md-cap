#!/bin/bash
# Heating srtructure

#SBATCH --job-name=heat_6wx4
#SBATCH --time=00:20:00
#SBATCH --mem=5gb
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --output=heat_6wx4.%j.log
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=username@york.ac.uk           
#SBATCH --account=account_name

module load chem/Amber/16-intel-2018b-AmberTools-17-patchlevel-10-15

SRC_MIN="src/heat"
TMP_DIR="tmp"
STRUC_DIR="data/structure"
INPUT_DIR="data/minimisation"
OUTPUT_DIR="data/heating"

echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo

#Run annealing equilibration
time mpirun -np $SLURM_NTASKS pmemd.MPI -O -i ${SRC_MIN}/heat.in \
        -c ${INPUT_DIR}/min_solu.ncrst -p ${STRUC_DIR}/protein.prmtop \
        -ref ${INPUT_DIR}/min_solu.ncrst -o ${OUTPUT_DIR}/heat.out \
        -r ${OUTPUT_DIR}/heat.ncrst -inf ${TMP_DIR}/heat.mdinfo

echo
echo Job completed at `date`
