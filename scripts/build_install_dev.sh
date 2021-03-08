#!/bin/bash

# robust bash scripting
set -o errexit
set -o nounset

# get important dirs of this Python package (absolute paths)
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# run local installation
cd "$SCRIPT_DIR/.." && /usr/bin/env python3 setup.py develop --user
