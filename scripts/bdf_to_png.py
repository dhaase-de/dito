#!/usr/bin/env python3

import argparse
import glob
import os.path
import sys

import bdfparser
import numpy as np

import dito


def get_args():
    parser = argparse.ArgumentParser(description="Convert font given in the Glyph Bitmap Distribution Format (BDF) into a PNG image.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--debug", action="store_true", help="If set, show full stack trace for errors.")
    parser.add_argument("-f", "--font-filenames", type=str, nargs="+", required=True, help="Filenames of the font (should end on '.bdf').")
    parser.add_argument("-o", "--output-dirname", type=str, required=True, help="Directory in which to save the output file(s).")
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    filenames = []
    for font_filename in args.font_filenames:
        filenames += glob.glob(os.path.expanduser(font_filename))
    filenames = sorted(filenames)
    file_count = len(filenames)
    if file_count == 0:
        raise FileNotFoundError("Found no fonts with the filenames(s) {}".format(args.input_filenames))
    print("Found {} font file(s)".format(file_count))

    print("Saving PNGs to '{}'...".format(args.output_dirname))
    for (n_file, filename) in enumerate(filenames):
        out_filename = os.path.join(args.output_dirname, "{}.png".format(os.path.splitext(os.path.basename(filename))[0]))
        print("[{}/{}]  {}  ->  {}".format(n_file + 1, file_count, filename, out_filename))

        font = bdfparser.Font(filename)
        default_glyph = font.glyph(chr(0))
        bitmap = font.draw(string="".join(chr(n_char) for n_char in range(256)), linelimit=font.headers["fbbx"], mode=0, missing=default_glyph)
        image = np.array(bitmap.todata(datatype=2), dtype=np.uint8) * 255
        dito.save(filename=out_filename, image=image)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        args = get_args()
        if args.debug:
            raise
        else:
            print("ERROR: {} ({})".format(e, type(e).__name__))
            sys.exit(1)
