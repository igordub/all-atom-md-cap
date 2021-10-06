#!/bin/bash
# Analyze equilibration MD simulation results

STRUC_DIR="data/structure"
HEAT_DIR="data/heating"
PRES_DIR="data/pressure"
SRC_DIR="src/analysis"
TMP_DIR="tmp"

ambpdb -p ${STRUC_DIR}/protein.prmtop -c ${HEAT_DIR}/heat.ncrst > ${TMP_DIR}/heat.pdb
ambpdb -p ${STRUC_DIR}/protein.prmtop -c ${EQ_DIR}/pres.ncrst > ${TMP_DIR}/pres.pdb

process_mdout.perl ${HEAT_DIR}/heat.out ${EQ_DIR}/pres.out
pyhton ${SRC_DIR}/plot_summary_mdout.py

mv summary* -t ${TMP_DIR}
