#!/bin/bash

# Creates force field modification for ligand

PDB_RAW_DIR="pdb/00-raw"
PDB_INT_DIR="pdb/02-interim"
PDB_PRO_DIR="pdb/03-processed"

# Ligand name: VIR251
# Ligand charge: 0
antechamber -i ${PDB_PRO_DIR}/ligand.pdb -fi pdb -o ${PDB_INT_DIR}/ligand.mol2 -fo mol2 \
    -s 2 -c bcc -at gaff2 -nc 0 -m 1 -eq 2
parmchk2 -i ${PDB_INT_DIR}/ligand.mol2 -f mol2 -o ${PDB_PRO_DIR}/ligand.frcmod
