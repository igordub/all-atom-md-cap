#!/bin/bash

# Creates force field modification for ligand

PDB_RAW_DIR="pdb/00-raw"
PDB_INT_DIR="pdb/01-interim"
PDB_PRO_DIR="pdb/02-processed"
TMP_DIR="tmp"

# Ligand name: cAMP
# Ligand charge: -1
antechamber -i ${PDB_PRO_DIR}/ligand.pdb -fi pdb -o ${PDB_INT_DIR}/ligand.mol2 -fo mol2 \
    -s 2 -c bcc -at gaff2 -nc -1 -m 2

rm ANTECHAMBER_*.AC ANTECHAMBER_*.AC0 ATOMTYPE.INF sqm.*

parmchk2 -i ${PDB_INT_DIR}/ligand.mol2 -f mol2 -o ${TMP_DIR}/ligand.frcmod
