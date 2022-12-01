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
  python3 -m spotflow -t rich -a mine pytest -k 'not card and not markdown and not progress' rich/tests

}

# rich tags: https://github.com/Textualize/rich/tags

run_rich "v12.4.0"

