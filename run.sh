#!/bin/bash

while true; do
    date
    python3 ./main.py
    sleep $(( $RANDOM % 120 ))
done