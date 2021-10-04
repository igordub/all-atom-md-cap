#!/bin/bash
# Extact non-trivial eigenvalues (Units: cm^{-1}) from 
# diagonalized mass-weighted covariance matrix

grep '\*\*\*\*' data/05-analysis/eigmodes.dat -A 1 | grep -v '\*\*\*\*' | \
    grep -v '\-\-' > data/05-analysis/eigvals.dat