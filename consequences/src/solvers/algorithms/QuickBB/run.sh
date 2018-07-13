#!bin/bash

TIMEOUT=$2

function timeout_monitor(){
  sleep "$TIMEOUT"
  if ps -p $1 >/dev/null ; then
    kill $(ps -o pid= --ppid $1)
  fi
}

CID=$(awk -F/ '{ print $NF }' /proc/1/cpuset)

IN="/data/$1"
OUT="/data/output:$CID.td"

cp $IN input.line

# Renamed convert.py to graph-to-cnf.py
./graph-to-cnf.py input.line

{ time ./quickbb_64 --min-fill-ordering --time $TIMEOUT --cnffile input.cnf > \
output.peo 2>/dev/null ; } 2> time.log & pid=$!

( timeout_monitor $pid ) &

wait $pid

# Calling the new .peo to .td script
./peo-to-td.py output.peo input.cnf

RUNTIME=$(awk '/^user/{print $2}' time.log)

echo "c user runtime $RUNTIME" | cat - output.td > temp && mv temp output.td

chmod 777 output.td

cp output.td $OUT
