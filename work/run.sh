#!/bin/bash
# usage: run.sh <file with python code>
n=$(date +%s%N); cp "$1" work/q/$n.tmp; mv work/q/$n.tmp work/q/$n.py
for i in $(seq 1 120); do [ -f work/q/$n.out ] && { cat work/q/$n.out; rm work/q/$n.out; exit 0; }; sleep 1; done; echo TIMEOUT
