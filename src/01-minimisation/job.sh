#!/bin/bash
# Strucutre minimisation

#SBATCH --job-name=min_6wx4
#SBATCH --time=02:00:00
#SBATCH --mem=10gb
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --output=min_6wx4.%j.log
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=username@york.ac.uk           
#SBATCH --account=account_name

module load chem/Amber/16-intel-2018b-AmberTools-17-patchlevel-10-15

SRC_MIN="src/minimisation"
TMP_DIR="tmp"
INPUT_DIR="data/structure"
OUTPUT_DIR="data/minimisation"

echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo

# Minimise the solvent
time mpirun -np $SLURM_NTASKS pmemd.MPI -O -i ${SRC_MIN}/min_solv.in \
        -c ${INPUT_DIR}/protein.inpcrd -p ${INPUT_DIR}/protein.prmtop \
        -ref ${INPUT_DIR}/protein.inpcrd -o ${OUTPUT_DIR}/min_solv.out \
        -r ${OUTPUT_DIR}/min_solv.ncrst -inf ${TMP_DIR}/min_solv.mdinfo
   
# Minimise the solute
time mpirun -np $SLURM_NTASKS pmemd -O -i ${SRC_MIN}/min_solu.in \
        -c ${OUTPUT_DIR}/min_solv.ncrst -p ${INPUT_DIR}/protein.prmtop \
        -o ${OUTPUT_DIR}/min_solu.out -r ${OUTPUT_DIR}/min_solu.ncrst \
        -inf ${TMP_DIR}/min_solu.mdinfo

echo
echo Job completed at `date`
