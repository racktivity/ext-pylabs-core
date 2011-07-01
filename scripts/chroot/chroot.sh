#!/bin/bash
SCRIPTDIR=$(readlink -f $(dirname $0))
command=$1
shift
pushd $SCRIPTDIR
./${command}.sh $*
popd
