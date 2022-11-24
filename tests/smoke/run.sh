#!/bin/sh

msg=$(python -m spotflow)
if [ "$msg" != 'Nothing to run...' ]; then
  exit 1;
fi