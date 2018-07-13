#!/bin/bash

TARGNAME=$1
MEASURE_FILE=$2

echo "Filename,NumberOfQubits,CircuitCompileTime(s),TotalRunTime(s),FlopCount,MeasureTime(s),Expectation" > results.csv

fsharpi qasm2fsx.fsx $TARGNAME circfunc.fsx $MEASURE_FILE
mono ../bin/Liquid.exe /s circfunc.fsx runqasmcirc
let LINE_CTR=1
OUT_STR="$TARGNAME"
while read LINE
do
    OUT_STR="$OUT_STR,$LINE"
done < out_time 
echo "$OUT_STR" >> results.csv

