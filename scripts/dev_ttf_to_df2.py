#!/usr/bin/env python3

import argparse
import collections
import os.path
import sys

import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import dito


def get_args():
    parser = argparse.ArgumentParser(description="Convert TrueType font (TTF) into dito's internal monospace bitmap font format ('df2').", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--debug", action="store_true", help="If set, show full stack trace for errors.")
    parser.add_argument("-r", "--font-filename-regular", type=str, required=True, help="Filename of the regular font (should end on '.ttf').")
    parser.add_argument("-b", "--font-filename-bold", type=str, required=True, help="Filename of the bold font (should end on '.ttf'). Must match the corresponsing regular font.")
    parser.add_argument("-s", "--sizes", type=int, nargs="+", default=[7, 12, 15, 19, 24, 28, 32, 40, 56], help="Font sizes to render.")
    parser.add_argument("-o", "--output-dirname", type=str, required=True, help="Directory in which to save the output file(s).")
    args = parser.parse_args()
    return args


def get_size(font):
    chars = dito.MonospaceBitmapFont.get_supported_chars()[:191]
    (width_0, max_height) = font.getsize("".join(chars))

    max_width = 0
    for char in chars:
        (width, _) = font.getsize("".join(chars + (char,)))
        max_width = max(max_width, width - width_0)

    return (width_0, max_width, max_height)


def font_to_char_images(font, width_0, max_width, max_height):
    chars = dito.MonospaceBitmapFont.get_supported_chars()
    char_images = collections.OrderedDict()
    for char in chars:
        canvas = PIL.Image.new('RGB', (width_0 + max_width, max_height), (0, 0, 0))
        draw = PIL.ImageDraw.Draw(canvas)
        offset = (0, 0)
        draw.text(offset, "".join(chars[:191] + (char,)), font=font, fill="#FFFFFF")
        char_image = np.array(canvas)
        char_image = char_image[:, width_0:, :]
        char_image = dito.as_gray(char_image)
        char_images[char] = char_image.copy()
    return char_images


def main():
    args = get_args()

    for size in args.sizes:
        font_regular = PIL.ImageFont.truetype(font=args.font_filename_regular, size=size, encoding="unic")
        font_bold = PIL.ImageFont.truetype(font=args.font_filename_bold, size=size, encoding="unic")

        (width_0_regular, max_width_regular, max_height_regular) = get_size(font=font_regular)
        (width_0_bold, max_width_bold, max_height_bold) = get_size(font=font_bold)
        max_width = max(max_width_regular, max_width_bold)
        max_height = max(max_height_regular, max_height_bold)

        out_filename = os.path.join(args.output_dirname, "{}_df2.png".format(max_height))
        print("Size {} ({}x{})  ->  {}".format(size, max_width, max_height, out_filename))

        char_images_regular = font_to_char_images(font=font_regular, width_0=width_0_regular, max_width=max_width, max_height=max_height)
        char_images_bold = font_to_char_images(font=font_bold, width_0=width_0_bold, max_width=max_width, max_height=max_height)
        dito.MonospaceBitmapFont.save_df2(filename=out_filename, char_images_regular=char_images_regular, char_images_bold=char_images_bold)


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
