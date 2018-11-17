#!bin/bash

# First arg is input file (.gr)
IN="/data/$1"
# Second arg is the timeout (seconds)
TIMEOUT=$2
# Third arg is the output file (.td)
# If none is provided then write the containerID.td
if [ -z "$3" ]; then
    CID=$(awk -F/ '{ print $NF }' /proc/1/cpuset)
    OUT="/data/output:$CID.td"
else
    OUT="/data/$3"
fi

# Our timeout function
function timeout_monitor(){
    sleep "$TIMEOUT"
    if ps -p $1 >/dev/null ;
    then
        kill $(ps -o pid= --ppid $1)
    fi
}


# Convert the line from PACE to CNF format per
# http://www.hlt.utdallas.edu/~vgogate/quickbb.html
cp $IN input.cnf
./graph-to-cnf.py input.cnf

# Run the treewidth solver
{ time ./quickbb_64 --min-fill-ordering --time $TIMEOUT --cnffile input.cnf > \
output.eo 2> error.log; } 2> time.log & pid=$!

( timeout_monitor $pid ) &

# Wait for the solver to finish
wait $pid

# If there's been an error, echo to stderr
if [ -s error.log ]
then
    cat error.log >&2
fi

# Convert the elimination ordering (.eo) output to a tree decomposition (.td)
./peo-to-td.py output.eo input.cnf

# Save the solver's run time to the output
RUNTIME=$(awk '/^user/{print $2}' time.log)
echo "c user runtime $RUNTIME" | cat - output.td > temp && mv temp output.td

# Copy the output file to the mounted dir, give permissions to everyone
chmod 777 output.td
cp output.td $OUT
