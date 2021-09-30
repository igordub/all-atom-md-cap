#!/bin/bash
# Analyze production MD simulations results

PROD_DIR="data/production"
SRC_DIR="src/analysis"
TMP_DIR="tmp"

process_mdout.perl ${PROD_DIR}/prod.*.out
# pyhton -m src.analysis.plot_summary_mdout
# pyhton ${SRC_DIR}/plot_summary_mdout.py

mv summary* -t ${TMP_DIR}
