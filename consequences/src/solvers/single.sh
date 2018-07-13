#!/bin/sh

FILENAME=""
OUTPUT=""
ALGORITHM=""
TIMEOUT="30"
VALIDATE=false

while [ ! $# -eq 0 ]
do
  case "$1" in
    -f|--filename)
      FILENAME=$2
      shift
    ;;
    -s|--seed)
      SEED=$2
      shift
    ;;
    -t|--timeout)
      TIMEOUT=$2
      shift
    ;;
    -v|--verbose)
      set -x
    ;;
    -o|--output)
      OUTPUT=$2
      shift
    ;;
    -a|--algorithm)
      ALGO=$2
      shift
    ;;
    --validate)
      VALIDATE=true
    ;;
  esac
  shift
done


if [[ ! -e $FILENAME ]]
  then
  echo "Input file does not exist"
  exit 1
fi

if [[ -z $OUTPUT ]]
  then
  echo "No output file specified"
  exit 1
fi

if [[ -z $ALGO ]]
  then
  echo "No algorithm specified"
  exit 1
fi

GRAPH=$(basename $FILENAME)


CID=$(docker run -d -v=$(dirname $FILENAME):/data/ \
  $ALGO /run.sh $GRAPH $TIMEOUT $SEED)

docker wait $CID

if $VALIDATE; then
  docker run -v=$(dirname $FILENAME):/data/ \
    td-validate /run.sh $GRAPH output:$CID.td
else
  echo 'c unvalidated' | cat - $(dirname $FILENAME)/output:$CID.td > temp && \
      mv temp $(dirname $FILENAME)/output:$CID.td
fi

cp $(dirname $FILENAME)/output:$CID.td $OUTPUT

rm -f $(dirname $FILENAME)/output:$CID.td
