#!/usr/bin/env bash

set -e
set -x

mypy src/ec_maze
ruff src/ec_maze tests scripts
black src/ec_maze tests --check