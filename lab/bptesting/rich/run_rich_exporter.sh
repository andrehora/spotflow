#!/bin/sh

function run_rich() {

  export PYTHONPATH='../../../../spotflow'

  local versions=$1
#  git clone https://github.com/Textualize/rich

  for version in $versions
  do
    echo $version
    run_on_tag $version
  done
}

function run_on_tag() {

  local version=$1
  cd rich
  git checkout tags/$version
  cd ..
  python3 -m spotflow -t rich -a mine -arg $version pytest -k 'not card and not markdown and not progress' rich/tests

}

# rich tags: https://github.com/Textualize/rich/tags

run_rich "v12.0.0 v12.0.1 v12.1.0 v12.2.0 v12.3.0 v12.4.0 v12.4.1 v12.4.2 v12.4.3 v12.4.4 v12.5.0 v12.5.1 v12.6.0"

