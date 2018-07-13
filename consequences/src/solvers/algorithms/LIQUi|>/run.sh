#!/bin/bash

 echo "Y" | mono /root/Liquid/bin/Liquid.exe
 echo $?

./run2.sh $1 $2

exit 0
