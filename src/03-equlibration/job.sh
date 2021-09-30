#!/bin/bash
# Pressure equilibration

#SBATCH --job-name=pres_6wx4
#SBATCH --time=02:00:00
#SBATCH --mem=20gb
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --output=pres_6wx4.%j.log
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=username@york.ac.uk           
#SBATCH --account=account_name

module load chem/Amber/16-intel-2018b-AmberTools-17-patchlevel-10-15

SRC_DIR="src/pressure"
TMP_DIR="tmp"
STRUC_DIR="data/structure"
INPUT_DIR="data/heating"
OUTPUT_DIR="data/pressure"

echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo

time mpirun -np $SLURM_NTASKS pmemd.MPI -O -i ${SRC_DIR}/pres.in \
        -c ${INPUT_DIR}/heat.ncrst -p ${STRUC_DIR}/protein.prmtop \
        -ref ${INPUT_DIR}/heat.ncrst -o ${OUTPUT_DIR}/pres.out \
        -r ${OUTPUT_DIR}/pres.ncrst -inf ${TMP_DIR}/pres.mdinfo

echo
echo Job completed at `date`