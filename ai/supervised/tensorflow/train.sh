#!/bin/bash
cd "$(dirname "$0")"
for f in `find ../data/*.h5 | shuf` 
do
    echo $f
    python train.py -f $f
done 