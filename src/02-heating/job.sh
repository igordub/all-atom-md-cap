#!/bin/bash
# All-atom MD simulation: heating

#SBATCH --job-name=heat
#SBATCH --time=01:00:00
#SBATCH --mem=5gb
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --output=heat.%j.log
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=username@york.ac.uk           
#SBATCH --account=account_name

module load chem/Amber/16-intel-2018b-AmberTools-17-patchlevel-10-15

SRC_MIN="src/02-heating"
TMP_DIR="tmp"
STRUC_DIR="data/00-structure"
INPUT_DIR="data/01-minimisation"
OUTPUT_DIR="data/02-heating"

echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo

time mpirun -np $SLURM_NTASKS pmemd.MPI -O -i ${SRC_MIN}/heat.in -c ${INPUT_DIR}/02.min_solu.ncrst -p ${STRUC_DIR}/complex.prmtop -ref ${INPUT_DIR}/02.min_solu.ncrst -o ${OUTPUT_DIR}/heat.out -r ${OUTPUT_DIR}/heat.ncrst -inf ${TMP_DIR}/heat.mdinfo

echo
echo Job completed at `date`
