#!/usr/bin/env python3

import argparse
import collections
import glob
import os.path
import sys

import bdfparser
import numpy as np

import dito


def get_args():
    parser = argparse.ArgumentParser(description="Convert font(s) given in the Glyph Bitmap Distribution Format (BDF) into dito's internal monospace bitmap font format ('lh4rb').", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--debug", action="store_true", help="If set, show full stack trace for errors.")
    parser.add_argument("-r", "--font-filenames-regular", type=str, nargs="+", required=True, help="Filenames of the regular font (should end on '.bdf').")
    parser.add_argument("-b", "--font-filenames-bold", type=str, nargs="+", required=True, help="Filenames of the bold font (should end on '.bdf'). Must match the corresponsing regular fonts.")
    parser.add_argument("-o", "--output-dirname", type=str, required=True, help="Directory in which to save the output file(s).")
    args = parser.parse_args()
    return args


def collect_filenames(filename_args):
    filenames = []
    for filename_arg in filename_args:
        filenames += glob.glob(os.path.expanduser(filename_arg))
    filenames = sorted(filenames)
    if len(filenames) == 0:
        raise FileNotFoundError("Found no fonts with the filenames(s) {}".format(filename_args))
    return filenames


def get_out_filename(output_dirname, filename_regular, filename_bold):
    assert os.path.dirname(filename_regular) == os.path.dirname(filename_bold)
    basename_regular = os.path.basename(filename_regular)
    basename_bold = os.path.basename(filename_bold)
    out_basename = "".join(item_regular for (item_regular, item_bold) in zip(basename_regular, basename_bold) if item_regular == item_bold)
    out_basename = os.path.splitext(out_basename)[0] + "_lh4rb.png"
    out_filename = os.path.join(output_dirname, out_basename)
    return out_filename


def font_to_char_images(filename):
    font = bdfparser.Font(filename)
    default_glyph = font.glyph("?")
    chars = dito.MonospaceBitmapFont.get_iso_8859_1_chars()
    char_images = collections.OrderedDict()
    for char in chars:
        bitmap = font.draw(string=char, linelimit=font.headers["fbbx"], mode=0, missing=default_glyph)
        char_image = np.array(bitmap.todata(datatype=2), dtype=np.uint8) * 255
        char_images[char] = char_image
    return char_images


def main():
    args = get_args()

    filenames_regular = collect_filenames(args.font_filenames_regular)
    filenames_bold = collect_filenames(args.font_filenames_bold)
    count_regular = len(filenames_regular)
    count_bold = len(filenames_bold)

    if count_regular != count_bold:
        raise RuntimeError("Filename counts for regular and bold font files differ ({} vs. {})".format(count_regular, count_bold))
    print("Found {} font file(s)".format(count_regular))

    #print("Saving PNGs to '{}'...".format(args.output_dirname))
    for (n_file, (filename_regular, filename_bold)) in enumerate(zip(filenames_regular, filenames_bold)):
        out_filename = get_out_filename(output_dirname=args.output_dirname, filename_regular=filename_regular, filename_bold=filename_bold)
        print("[{}/{}]  {}  ->  {}".format(n_file + 1, count_regular, filename_regular, out_filename))

        char_images_regular = font_to_char_images(filename=filename_regular)
        char_images_bold = font_to_char_images(filename=filename_bold)
        dito.MonospaceBitmapFont.save_lh4rb(filename=out_filename, char_images_regular=char_images_regular, char_images_bold=char_images_bold)


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
