#!/bin/bash
for i in `seq 1 100`;
do
    python generate_data.py -n 3000 -dt $(( ( RANDOM % 2 )  + 2 ))
done