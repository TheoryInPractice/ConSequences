#!bin/bash

validator/td-validate /data/$1 /data/$2

if [[ $? == 0 ]]; then
  echo 'c valid' | cat - /data/$2 > temp && mv temp /data/$2
else
  echo 'c invalid' | cat - /data/$2 > temp && mv temp /data/$2
fi








