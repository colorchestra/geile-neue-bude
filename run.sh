#!/bin/bash

date
while true; do
    python3 ./main.py
    sleep $(( $RANDOM % 300 ))
done