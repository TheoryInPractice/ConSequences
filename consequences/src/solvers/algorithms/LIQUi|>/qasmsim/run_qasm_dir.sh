#!/bin/bash

TARG_DIR=$1
MEASURE_FILE=$2

echo "Filename,NumberOfQubits,CircuitCompileTime(s),TotalRunTime(s),#Flops,<M>" > results.csv

for FILENAME in $(ls $TARG_DIR | grep qasm)
do
    echo $FILENAME
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

