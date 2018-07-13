#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
for D in $DIR/algorithms/*; do [ -d "${D}" ] & $D/build.sh; done
docker system prune

