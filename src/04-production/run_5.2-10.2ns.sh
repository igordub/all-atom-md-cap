#!/bin/bash
# Splits 45 ns production MD into nine 5 ns runs
# Times can be changed by varying nstlim in prod.in
# and changing MD_END_JOB
# Good practice is to start with MD_END_JOB=MD_START_JOB

MD_START_JOB=2
MD_END_JOB=2
# set MD_CURRENT_JOB=$MD_START_JOB
# set MD_INPUT=0

SRC_DIR="src/production"
TMP_DIR="tmp"
INPUT_DIR="data/pressure"
OUTPUT_DIR="data/production"

PRMTOP_PATH="data/structure/protein.prmtop"

# Copy coordinate file from pressure equilibration
# as the first input coordiante file for production
printf -v INPUT_FILENAME "prod.%02d" "1"
cp ${INPUT_DIR}/pres.ncrst ${OUTPUT_DIR}/${INPUT_FILENAME}.ncrst

echo -n "Starting script at: "
date
echo ""

for MD_CURRENT_JOB in $(seq $MD_START_JOB $MD_END_JOB)
do
   echo -n "Job $MD_CURRENT_JOB started at: "
   date
   MD_INPUT=$((${MD_CURRENT_JOB} - 1))
   printf -v INPUT_FILENAME "prod.%02d" ${MD_INPUT}
   printf -v OUTPUT_FILENAME "prod.%02d" ${MD_CURRENT_JOB}
   pmemd.cuda -O -i ${SRC_DIR}/prod.in \
                           -o ${OUTPUT_DIR}/${OUTPUT_FILENAME}.out \
                           -p ${PRMTOP_PATH} \
                           -c ${OUTPUT_DIR}/${INPUT_FILENAME}.ncrst \
                           -r ${OUTPUT_DIR}/${OUTPUT_FILENAME}.ncrst \
                           -x ${OUTPUT_DIR}/${OUTPUT_FILENAME}.mdcrd \
                           -inf ${TMP_DIR}/${OUTPUT_FILENAME}.mdinfo

   gzip -9 -v ${OUTPUT_DIR}/${OUTPUT_FILENAME}.mdcrd
   mv ${OUTPUT_FILENAME}.mdcrd.gz ${OUTPUT_DIR}

   echo -n "Job $MD_CURRENT_JOB finished at: "
   date
   # MD_CURRENT_JOB=$((${MD_CURRENT_JOB} + 1))
done
echo "ALL DONE"
