#!/bin/sh

function run_bptesting() {

  local v_major_minor=$1
  local v_micros=$2

  for v_micro in $(seq $v_micros $END)
  do
    python_version=$v_major_minor.$v_micro
    echo $python_version
    run_on_docker $python_version
  done
}

function run_on_docker() {

  local python_version=$1

  docker build -t spotflow --no-cache --build-arg VERSION=$python_version .

  docker create --name dummy spotflow
  docker cp dummy:/app/spotflow/output .

  docker rm -f dummy
  docker image rm -f spotflow

}

# python 3.7.x: 1-15 - https://peps.python.org/pep-0537/
# python 3.8.x: 1-15 - https://peps.python.org/pep-0569/
# python 3.9.x: 1-15 - https://peps.python.org/pep-0596/
# python 3.10.x: 1-8 - https://peps.python.org/pep-0619/

run_bptesting 3.7 15
#run_bptesting 3.8 15
#run_bptesting 3.9 15
#run_bptesting 3.10 8
