#!bin/bash
set -x
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

{ time /p17/tw-exact  < $IN > output.tmp 2>/dev/null ; } 2> time.log  & pid=$!

( timeout_monitor $pid ) &

wait $pid

RUNTIME=$(awk '/^user/{print $2}' time.log)

echo "c user runtime $RUNTIME" | cat - output.tmp > temp && mv temp output.tmp

cp output.tmp $OUT

chmod 777 $OUT

