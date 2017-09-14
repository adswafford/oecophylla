[![Build Status](https://travis-ci.org/biocore/oecophylla.svg?branch=master)](https://travis-ci.org/biocore/oecophylla)

# oecophylla

Canonically pronounced *eco-fill-uh*

Snakemake testbed for shotgun sequence analysis

## Installation

To install the workflow environment, run `bash install.sh` from the `oecophylla` directory.

## Test data execution

To run on a simple set of test data, run:

```bash
source activate oecophylla

snakemake all --cores 2 --configfile config.yaml
```
