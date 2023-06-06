#!/bin/sh

msg=$(python -m spotflow)
if [ "$msg" != 'Nothing to run...' ]; then
  exit 1;
else
  echo "OK";
  exit 0;
fi