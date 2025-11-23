#!/bin/bash

# robust bash scripting
set -o errexit
set -o nounset

# get absolute path of this script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

source "$SCRIPT_DIR"/setenv.sh

# get dito version
DITO_VERSION="$(cd "$PACKAGE_DIR" && uv version --short)"
echo "Using dito version number $DITO_VERSION"

# build docs
cd "$PACKAGE_DIR" && uv run pdoc dito --output-directory=docs --docformat=numpy --footer-text="dito v$DITO_VERSION"

