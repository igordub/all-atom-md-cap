#!/bin/bash

# Prepares PDB file for AMBER
# AmebrTtools must be loaded and/or added to PATH

PDB_RAW_DIR="pdb/00-raw"
PDB_INT_DIR="pdb/01-interim"
PDB_PRO_DIR="pdb/02-processed"


pdb4amber -i ${PDB_RAW_DIR}/complex.pdb -o ${PDB_INT_DIR}/complex.pdb --dry --reduce

# Exctract protein and ligand coordinates
grep -e '^ATOM\|^TER\|^END' ${PDB_INT_DIR}/complex.pdb > ${PDB_INT_DIR}/protein.pdb
grep -e '^HETATM' ${PDB_INT_DIR}/complex.pdb > ${PDB_INT_DIR}/ligand.pdb


cp ${PDB_INT_DIR}/complex.pdb ${PDB_PRO_DIR}/complex.pdb
cp ${PDB_INT_DIR}/protein.pdb ${PDB_PRO_DIR}/protein.pdb
# Extract only one ligand from chain A
grep -e '^HETATM.\{14\} A ' ${PDB_INT_DIR}/ligand.pdb > ${PDB_PRO_DIR}/ligand.pdb
