#!/bin/bash

TARG_DIR=$1
MEASURE_FILE=$2

echo "Filename,NumberOfQubits,CircuitCompileTime(s),TotalRunTime(s),#Flops,<M>" > results.csv

for SUBDIR in $(find $TARG_DIR -type d -print)
do
    for FILENAME in $(ls $SUBDIR | grep qasm)
    do
        echo $FILENAME
        fsharpi qasm2fsx.fsx $SUBDIR/$FILENAME circfunc.fsx $MEASURE_FILE
        mono ../bin/Liquid.exe /s circfunc.fsx runqasmcirc
        let LINE_CTR=1
        OUT_STR="$SUBDIR/$FILENAME"
        while read LINE
        do
            OUT_STR="$OUT_STR,$LINE"
        done < out_time 
        echo "$OUT_STR" >> results.csv
    done
done
