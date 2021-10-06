#!/bin/bash
# Check heating MD simulation results

STRUC_DIR="data/00-structure"
HEAT_DIR="data/02-heating"
TMP_DIR="tmp"

ambpdb -p ${STRUC_DIR}/complex.prmtop -c ${HEAT_DIR}/heat.ncrst > ${TMP_DIR}/heat.pdb

process_mdout.perl ${HEAT_DIR}/heat.out
mv summary* -t ${TMP_DIR}
