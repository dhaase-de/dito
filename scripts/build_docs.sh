#!/bin/bash

# robust bash scripting
set -o errexit
set -o nounset

# get absolute path of this script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

DITO_VERSION="$(echo "import dito; print(dito.__version__)" | /usr/bin/env python3)"

source "$SCRIPT_DIR"/setenv.sh
cd "$PACKAGE_DIR" && pdoc dito --output-directory=docs --docformat=numpy --footer-text="dito v$DITO_VERSION"

