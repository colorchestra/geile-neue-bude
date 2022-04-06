#!/bin/bash

date
while true; do
    sleep $(( $RANDOM % 300 ))
    python ./main.py
done