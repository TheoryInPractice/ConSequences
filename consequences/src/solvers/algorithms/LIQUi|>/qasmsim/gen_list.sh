#!/bin/bash

NNODES=(10 12 14 16 18 20 22 24 26 28 30)

rm filelist

for n in "${NNODES[@]}"
do
   echo $n
   ls qcitcoin-tn-files/maxcut-circ-bat-1 | grep `printf "%dNode" $n` >> filelist
done
