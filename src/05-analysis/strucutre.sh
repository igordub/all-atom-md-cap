#!/bin/bash
# Creates PDB files for the initial and minimized strucutures

STRUC_DIR="data/structure"
MIN_DIR="data/minimisation"

ambpdb -p ${STRUC_DIR}/protein.prmtop -c ${STRUC_DIR}/protein.incrd > ${STRUC_DIR}/protein.pdb
ambpdb -p ${STRUC_DIR}/protein.prmtop -c ${MIN_DIR}/min_solu.ncrst > ${MIN_DIR}/min_solu.pdb
