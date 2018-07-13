#!/bin/bash

TARG_DIR=$1
TARG_LIST=$2
MEASURE_FILE=$3 
echo "Filename,NumberOfQubits,CircuitCompileTime(s),TotalRunTime(s)" > results.csv

for FILENAME in $(cat $TARG_LIST)
do
    echo $TARG_DIR/$FILENAME
    fsharpi qasm2fsx.fsx $TARG_DIR/$FILENAME circfunc.fsx $MEASURE_FILE
    mono ../bin/Liquid.exe /s circfunc.fsx runqasmcirc
    let LINE_CTR=1
    OUT_STR="$TARG_DIR/$FILENAME"
    while read LINE
    do
        OUT_STR="$OUT_STR,$LINE"
    done < out_time 
    echo "$OUT_STR" >> results.csv
done

