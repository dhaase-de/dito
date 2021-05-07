#!/bin/bash

# robust bash scripting
set -o errexit
set -o nounset

# get absolute path of this script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

cd "$SCRIPT_DIR"
./bdf_to_df2.py -r $HOME/git/bitmap-fonts/bitmap/terminus-font-4.39/ter-u*n.bdf -b $HOME/git/bitmap-fonts/bitmap/terminus-font-4.39/ter-u*b.bdf -o ../dito/resources/fonts/terminus
./bdf_to_df2.py -r $HOME/git/bitmap-fonts/bitmap/scientifica/scientifica-11.bdf -b $HOME/git/bitmap-fonts/bitmap/scientifica/scientificaBold-11.bdf -o ../dito/resources/fonts/scientifica
./ttf_to_df2.py -r $HOME/git/source-code-pro/TTF/SourceCodePro-Regular.ttf -b $HOME/git/source-code-pro/TTF/SourceCodePro-Black.ttf -o ../dito/resources/fonts/source_code_pro

cd "$SCRIPT_DIR"/../dito/resources/fonts
optipng -o9 */*df2.png
