#!/bin/bash

# Prepares PDB file for AMBER
# AmebrTtools must be loaded and/or added to PATH

PDB_RAW_DIR="pdb/00-raw"
PDB_INT_DIR="pdb/01-interim"
PDB_PRO_DIR="pdb/02-processed"

# Add hydrogens
# reduce $PDB_RAW_DIR/6wx4.pdb > $PDB_INT_DIR/6wx4.reduced.pdb
# pymol -qrc ./src/structure/add_hydrogens.py $PDB_RAW_DIR/6wx4.pdb $PDB_INT_DIR/6wx4.reduced.pdb

grep '^ATOM\|^HETATM' $PDB_RAW_DIR/complex.pdb | # Extract ATOM and HETATM record types
    grep -Ev '^.{16} HOH' | grep -Ev '^HETATM.{5} ZN' | # Remove water and zinc
    sed -E 's/ATOM  (.{14} I )/HETATM\1/' | # Change ligand ATOM record types to HETATM
    sed -E 's/(.{16}) ... I /\1 LIG I /' | # Rename ligand chain ID
    sed -E 's/(.{20}) I..../\1 I   1/' > $PDB_INT_DIR/complex.pdb # Set residue number to 1 for ligand and save

# grep '^ATOM\|^HETATM' $PDB_INT_DIR/6wx4.reduced.pdb | # Extract ATOM and HETATM record types
#     grep -Ev '^.{16} HOH' | grep -Ev '^HETATM.{5} ZN' > $PDB_INT_DIR/complex.pdb

# Format PDB file for AMBER
pdb4amber -i $PDB_INT_DIR/complex.pdb -o $PDB_PRO_DIR/complex.pdb
rm $PDB_PRO_DIR/*_nonprot.pdb $PDB_PRO_DIR/*_renum.txt $PDB_PRO_DIR/*_sslink

# Extract protein and ligand form complex
grep '^ATOM' $PDB_PRO_DIR/complex.pdb > $PDB_PRO_DIR/protein.pdb
grep '^HETATM' $PDB_PRO_DIR/complex.pdb > $PDB_PRO_DIR/ligand.pdb
