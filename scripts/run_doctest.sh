#!/bin/bash

# robust bash scripting
set -o errexit
set -o nounset

# get absolute path of this script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

source "$SCRIPT_DIR"/setenv.sh
cd "$PACKAGE_DIR" && uv run --dev python -m doctest -v "$SOURCE_DIR"/*.py --option REPORT_NDIFF
