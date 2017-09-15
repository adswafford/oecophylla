![oecophylla](https://raw.githubusercontent.com/wasade/oecophylla/assets/assets/oecophylla.png | width=100)
[![Build Status](https://travis-ci.org/biocore/oecophylla.svg?branch=master)](https://travis-ci.org/biocore/oecophylla)

# Oecophylla

Canonically pronounced *eco-fill-uh*

Snakemake testbed for shotgun sequence analysis

## Installation

To install the workflow environment, run `bash install.sh` from the `oecophylla` directory.

## Test data execution

To speed development, Travis is currently only testing the validity
of the module installs and checking the snakefiles syntax, by using the `--dryrun` option in snakemake:

```
snakemake all --cores 2 --configfile config.yaml --dryrun
```

To run actual tools on a simple set of test data, run:

```bash
source activate oecophylla

snakemake all --cores 2 --configfile config.yaml
```
