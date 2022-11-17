#!/bin/sh

run_bptesting(){
  for v_micro in $(seq $2 $END)
  do
    echo "$1.$v_micro"
  done
}

run_bptesting 3.7 15
# run_bptesting 3.8 15
# run_bptesting 3.9 15
# run_bptesting 3.10 8
