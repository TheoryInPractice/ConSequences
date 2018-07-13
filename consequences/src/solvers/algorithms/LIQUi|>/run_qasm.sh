#!/bin/bash

TARGNAME=$1
MEASURE_FILE=$2

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Filename,NumberOfQubits,CircuitCompileTime(s),TotalRunTime(s),FlopCount,MeasureTime(s),Expectation" > results.csv

fsharpi $DIR/qasm2fsx.fsx $TARGNAME $DIR/circfunc.fsx $DIR/$MEASURE_FILE
mono $DIR/../bin/Liquid.exe /s $DIR/circfunc.fsx runqasmcirc
let LINE_CTR=1
OUT_STR="$TARGNAME"
while read LINE
do
    OUT_STR="$OUT_STR,$LINE"
done < $DIR/out_time
echo "$OUT_STR" >> $DIR/results.csv

