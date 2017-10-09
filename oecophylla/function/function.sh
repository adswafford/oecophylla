#!/bin/bash
set -e

conda env create --name oecophylla-humann2 -f oecophylla-humann2.yaml --quiet > /dev/null

if [[ conda env list | grep '^oecophylla-shogun\s' ]]
then
  conda env create --name oecophylla-humann2 -f ../taxonomy/oecophylla-shogun.yaml --quiet > /dev/null
fi
