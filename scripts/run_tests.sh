#!/bin/bash

# robust bash scripting
set -o errexit
set -o nounset

# get absolute path of this script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
source "$SCRIPT_DIR"/setenv.sh

/usr/bin/env python3 "$SOURCE_DIR"/tests.py --verbose
