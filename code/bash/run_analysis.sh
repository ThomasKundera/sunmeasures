#!/bin/bash

# Location of this script
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Projectdir is two up
export PROJECTDIR="$( cd $SCRIPTDIR/../.. >/dev/null 2>&1 && pwd )"

export WORKDIR=$PROJECTDIR/output
mkdir -p $WORKDIR

echo "Working in $WORKDIR"

cd $WORKDIR

echo "Setting up python environment"
# Only if runenv does not exist
if [ ! -d "runenv" ]; then
    echo "Creating runenv"
    python3 -m venv runenv
fi
source runenv/bin/activate

echo "Installing requirements"
pip install -r $PROJECTDIR/requirements.txt

echo "Running analysis"
python $PROJECTDIR/code/python/image_analysis.py
