#!/bin/bash
# Check minimized system

STRUC_DIR="data/00-structure"
MIN_DIR="data/01-minimisation"
TMP_DIR="tmp"

ambpdb -p ${STRUC_DIR}/complex.prmtop -c ${MIN_DIR}/01.min_solv.ncrst -x ${TMP_DIR}/01.min_solv.pdb
ambpdb -p ${STRUC_DIR}/complex.prmtop -c ${MIN_DIR}/02.min_solv.ncrst -x ${TMP_DIR}/02.min_solv.pdb
