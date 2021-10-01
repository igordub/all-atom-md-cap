#!/bin/bash
# Strucutre minimisation

#SBATCH --job-name=min
#SBATCH --time=02:00:00
#SBATCH --mem=10gb
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --output=min.%j.log
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=username@york.ac.uk           
#SBATCH --account=account_name

module load chem/Amber/16-intel-2018b-AmberTools-17-patchlevel-10-15

SRC_DIR="src/minimisation"
TMP_DIR="tmp"
INPUT_DIR="data/structure"
OUTPUT_DIR="data/minimisation"

echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo

# Minimise the solvent
time mpirun -np $SLURM_NTASKS pmemd.MPI -O -i ${SRC_DIR}/01.min_solv.in \
        -o ${OUTPUT_DIR}/01.min_solv.out \
        -p ${INPUT_DIR}/complex.prmtop \
        -c ${INPUT_DIR}/complex.inpcrd \
        -r ${OUTPUT_DIR}/01.min_solv.ncrst \
        -x ${OUTPUT_DIR}/01.min_solv.mdcrd \
        -ref ${INPUT_DIR}/complex.inpcrd \        
        -inf ${TMP_DIR}/min_solv.mdinfo
   
# Minimise the solute
time mpirun -np $SLURM_NTASKS pmemd -O -i ${SRC_DIR}/02.min_solu.in \
        -o ${OUTPUT_DIR}/02.min_solu.out \
        -r ${OUTPUT_DIR}/02.min_solu.ncrst \
        -x ${OUTPUT_DIR}/02.min_solu.mdcrd \
        -c ${OUTPUT_DIR}/01.min_solv.ncrst \
        -ref ${OUTPUT_DIR}/01.min_solv.ncrst \
        -p ${INPUT_DIR}/complex.prmtop \
        -inf ${TMP_DIR}/min_solu.mdinfo

echo
echo Job completed at `date`
